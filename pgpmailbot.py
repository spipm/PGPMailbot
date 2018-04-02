from mailbotlib.input_functions import *
from mailbotlib.parse_config import *
from mailbotlib.mailbot_core import *


# init
config = parse_config_file(filename="/home/postfix-scripts/pgpmailbot/config/pgpmailbot.conf")
init_gpg(config['bot_address'], config['gpg_dir'])

# get mail text
#mail_text = get_mail_from_imap(config['imap_username'], config['imap_password'], config['imap_server'], removeMsg=False)
mail_text = get_mail_from_stdin()

if mail_text == False:
	if config['debug']:
		log_message(config, "No email text")
	exit(0)

if config['debug']:
	log_message(config, mail_text)

# check if mail is meant for the bot
is_meant_for_me(mail_text, config)

# process the email message
process_message(mail_text, config)
