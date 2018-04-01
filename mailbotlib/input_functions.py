import imaplib


def get_mail_from_imap(username, password, server, port=993, secureTLS=True, removeMsg=True):
	'''
		Return first message from IMAP server
			And remove message from server
		'''
	msg = False

	# connect to IMAP server
	im = imaplib.IMAP4_SSL(server)
	im.login(username, password)

	# get email
	im.select()
	typ, data = im.search(None, 'ALL')
	for num in data[0].split():
		typ, data = im.fetch(num, '(RFC822)')
		msg = data[0][1]

		if removeMsg:
			im.store(num, '+FLAGS', '\\Deleted')
			im.expunge()

		break
	
	im.close()
	im.logout()

	return msg


def get_mail_from_stdin():
	'''
		Return content from stdin
		'''
	return sys.stdin.read()

