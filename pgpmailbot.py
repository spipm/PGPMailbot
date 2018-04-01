from mailbotlib.input_functions import *
from mailbotlib.parse_config import *
from mailbotlib.mailbot_core import *


# init
config = parse_config_file()
init_gpg(config['bot_address'])

# get mail text
mail_text = get_mail_from_imap(config['imap_username'], config['imap_password'], config['imap_server'], removeMsg=False)

# print mail_text
if mail_text == False:
	print "No email text"
	exit(0)

is_meant_for_me(mail_text, config)

process_message(mail_text, config)


