import smtplib
from email.mime.text import MIMEText
from email.message import Message
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
import mailbotlib.gpg_happytime as gpgfun
from mailbotlib.mailbot_spamcheck import string_between_lt_gt


def new_mail_msg(fromAddress, toAddress, subject):
	msg = MIMEMultipart()
	msg['From'] = fromAddress
	msg['To'] = toAddress
	msg['Subject'] = subject
	return msg


def send_email(toAddress, config, emailResponseTemplate, attachPub, tryEncryptResponse):
	
	fromAddress = config['bot_address']

	# new email message
	msg = new_mail_msg(fromAddress, toAddress, 'PGP mail bot')

	# add normal plaintext message
	if not tryEncryptResponse:
		msg.attach(MIMEText(emailResponseTemplate, 'plain'))

	# to attach public key
	if attachPub:
		keyID, puybkey = gpgfun.get_pubkey_for(fromAddress)
		if keyID != False:
			part = MIMEBase('application', 'pgp-keys')
			part.set_payload(puybkey)

			filename = "0x%s.asc" % keyID
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % filename)
			msg.attach(part)

	# try the encryption
	if tryEncryptResponse:

		#print "Trying to encrypt for..%s" % string_between_lt_gt(toAddress)
		encrypted_text = gpgfun.encrypt(emailResponseTemplate, string_between_lt_gt(toAddress), fromAddress, _always_trust=True, _sign=True)
		
		if encrypted_text.ok:
			msg = new_mail_msg(fromAddress, toAddress, 'PGP mail bot')
			# attach encrypted message
			part = MIMEBase('application', 'octet-stream')
			part.add_header('Content-Disposition', 'attachment; filename="encrypted.asc"')
			part.set_payload(str(encrypted_text))
			msg.attach(part)

	s = smtplib.SMTP(config['imap_server'], 587)
	s.starttls()
	s.login(config['imap_username'], config['imap_password'])

	s.sendmail(fromAddress, [toAddress], msg.as_string())
	s.quit()
