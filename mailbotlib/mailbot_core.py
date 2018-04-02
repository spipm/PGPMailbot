import email
import mailbotlib.mailbot_spamcheck as spamcheck
import mailbotlib.gpg_happytime as gpgfun
from mailbotlib.mailbot_messages import *
import mailbotlib.mailbot_sendmail as mailbotreply


def log_message(config, message):
	with open(config['log_file'],'a') as fout:
		fout.write(message+"\n")


def init_gpg(botAddress, gpgHomeDir):
	gpgfun.init_gpgfun(gpgHomeDir)	
	gpgfun.check_bot_keys(botAddress)


def is_meant_for_me(mail_text, config):
	mailObject = email.message_from_string(mail_text)
	toAddress = mailObject.get("To")
	if config['bot_address'] in toAddress:
		return True
	#if parsedMessage.get("Subject") == "Start PGP mail":

	return False


def could_be_spam(mailObject):
	'''
		Do some basic checks to block obvious spam messages
		'''
	# Dont' allow different return path and from address
	if not spamcheck.return_path_match_from(mailObject):
		return True


def process_message(mail_text, config):
	'''
		Process email for pgp mail bot
		'''
	#print mail_text
	tryEncryptResponse = False
	
	# first convert mail string to mail object
	mailObject = email.message_from_string(mail_text)

	# don't handle possible spam messages
	if could_be_spam(mailObject) == True:
		return

	# get from address
	fromAddress = mailObject.get("From")

	# 'load' mail template
	emailResponseTemplate = MAILBOT_BASICMAIL

	# template status placeholders
	EMAIL_ENCRYPTED_MESSAGE = "Encryption status unknown"
	
	# is mail encrypted for me?
	wasEncrypted, couldDecrypt, wasSigned, decryptedContent = gpgfun.decrypt_mail(mailObject)
	encryptedFailed = True
	
	if not wasEncrypted:
		EMAIL_ENCRYPTED_MESSAGE = "Mail was not encrypted :(\nTry to import my public key and try again."
	
	elif wasEncrypted:
		EMAIL_ENCRYPTED_MESSAGE = "Mail was encrypted. "
		if not couldDecrypt:
			EMAIL_ENCRYPTED_MESSAGE += "But could not decrypt :("
		elif couldDecrypt:
			EMAIL_ENCRYPTED_MESSAGE += "And decryption worked! :)\n"
			encryptedFailed = False
			if wasSigned:
				EMAIL_ENCRYPTED_MESSAGE += "And the mail was signed! Yeah! :)"	
			elif not wasSigned:
				EMAIL_ENCRYPTED_MESSAGE += "But the mail was not yet signed :(\nLet's continue with your public key."
	
	if encryptedFailed:
		emailResponseTemplate = emailResponseTemplate.replace("[BOT_HAS_PUBCERT]", "")
		emailResponseTemplate = emailResponseTemplate.replace("[EMAIL_IS_ENCRYPTED]", EMAIL_ENCRYPTED_MESSAGE)

		mailbotreply.send_email(fromAddress, config, emailResponseTemplate, True, tryEncryptResponse)
		return


	EMAIL_EXTERNAL_PUBKEY_MESSAGE = "Your public key status is unknown"
	# do I haz the public key?
	if not gpgfun.has_pubkey_for(fromAddress):
		EMAIL_EXTERNAL_PUBKEY_MESSAGE = "Could not find your public key in my keystore :(\n"
		
		if wasEncrypted and couldDecrypt:
			mailObject = email.message_from_string(decryptedContent)

		if gpgfun.has_pubkey_attached(mailObject):
			EMAIL_EXTERNAL_PUBKEY_MESSAGE += "But I found it attached! "
		
			if gpgfun.can_import_pubkey(mailObject):
				EMAIL_EXTERNAL_PUBKEY_MESSAGE += "And I was able to import it! :)"
				tryEncryptResponse = True
		
			else:
				EMAIL_EXTERNAL_PUBKEY_MESSAGE += "Aarg, error importing the key :("
		else:
			EMAIL_EXTERNAL_PUBKEY_MESSAGE += "And I could not find it attached :(\nPlease attach your public key to your message."
	else:
		EMAIL_EXTERNAL_PUBKEY_MESSAGE = "I have your public key, so I'll try to encrypt and sign my response. :)"
		tryEncryptResponse = True

	emailResponseTemplate = emailResponseTemplate.replace("[BOT_HAS_PUBCERT]", EMAIL_EXTERNAL_PUBKEY_MESSAGE)
	emailResponseTemplate = emailResponseTemplate.replace("[EMAIL_IS_ENCRYPTED]", EMAIL_ENCRYPTED_MESSAGE)

	mailbotreply.send_email(fromAddress, config, emailResponseTemplate, False, tryEncryptResponse)
