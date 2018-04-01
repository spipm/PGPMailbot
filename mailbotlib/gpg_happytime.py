import gnupg

gpg = gnupg.GPG(gnupghome='.')


def has_pubkey_for(address):
	keyID = False

	for pub in gpg.list_keys():
		for uid in pub['uids']:
			if address in uid:
				keyID = pub['keyid']

	if keyID == False:
		return False

	return True


def get_pubkey_for(address):
	keyID = False
	for pub in gpg.list_keys():
		for uid in pub['uids']:
			if address in uid:
				keyID = pub['keyid']
	if keyID == False:
		return False, ""

	pubkey = gpg.export_keys(keyID)
	return keyID, pubkey


def get_signer_fingerprint_for(fromAddress):
	for pub in gpg.list_keys():
		for uid in pub['uids']:
			if fromAddress in uid:
				return pub['fingerprint']
	return False
	

def check_bot_keys(botAddress):
	if has_pubkey_for(botAddress) == False:
		print "Could not find key ID for %s, generating key.." % botAddress
		gen_data = gpg.gen_key_input(key_type="RSA", key_length=2048, name_real="Graa mailbot", name_comment="Generated for your pleasure", name_email=botAddress)
		input_data = gpg.gen_key(gen_data)


def has_pubkey_attached(mailObject):
	for part in mailObject.walk():
		if part.get_content_type() == 'application/pgp-keys':
			return True

	return False


def try_import(pubkey):
	import_result = gpg.import_keys(pubkey)
	return import_result.imported == 1


def encrypt(msg, to, fromAddress, _always_trust, _sign):
	if _sign:
		sign_fingerprint = get_signer_fingerprint_for(fromAddress)
		return gpg.encrypt(msg, to, always_trust=_always_trust, sign=sign_fingerprint)
	else:
		return gpg.encrypt(msg, to, always_trust=_always_trust)


def can_import_pubkey(mailObject):

	for part in mailObject.walk():

		if part.get_content_type() == 'application/pgp-keys':
			
			if try_import(part.get_payload(decode=True)):
				return True
			else:
				return False

	return False


def decrypt_mail(mailObject):
	'''
		Check if mail contains encrypted content 
		returns wasEncrypted, couldDecrypt, wasSigned, decryptedContent
		'''
	wasEncrypted = False
	couldDecrypt = False
	wasSigned = False
	decryptedContent = ""

	for part in mailObject.walk():
		attachmentContentType = part.get_content_type()
		if attachmentContentType == 'application/octet-stream':
			if 'encrypted' in part.get("Content-Description"):
				if part.get_filename() == 'encrypted.asc':
					wasEncrypted = True
					encrypted_message = part.get_payload()#decode=True
					#print "Decrypted message:"
					#print encrypted_message
					decryptedMessage = gpg.decrypt(encrypted_message)
					if decryptedMessage.ok:
						couldDecrypt = True
						if decryptedMessage.signature_id != None:
							wasSigned = True
						#print decryptedMessage.__dict__
						decryptedContent = decryptedMessage.data
						break

	return wasEncrypted, couldDecrypt, wasSigned, decryptedContent