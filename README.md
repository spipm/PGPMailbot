#### PGP Mail Bot ####

This is a mail bot to learn about:
* Setting up Postfix to automatically handle email.
* Using PGP in email (MIME) with Python.
* Sending and receiving email with Python.

##### Set-up #####

The file *pgpmailbot.py* receives the mail and processes it. This can be done in two ways:
* To automate email:
    * Install postfix;
    * Add an alias to /etc/aliases like `mailbot: "| python /path/to/pgpmailbot.py"`;
    * Run `newaliases`;
    * Restart postfix (`service postfix restart`);
    * Modify script to use *get_mail_from_stdin* to retrieve the mail.
* Use *get_mail_from_imap* to retrieve email from outside of the mailserver.

Note that you have to create a config file and point to it in *pgpmailbot.py*. Also you need to edit the config file and file permissions to get it to work, but you'll find that out when you run it.

##### Things #####

* Currently anyone can send a random public certificate and it will be imported.
* Directory permissions are kind of hassle. (Postfix seems to invoke the user *nobody* to run the script. This user will create gpg key store and log file).
