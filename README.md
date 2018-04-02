#### PGP Mail Bot ####

This is a mail bot to learn about:
* Setting up Postfix to automatically handle email.
* Using PGP in email (MIME) with Python.
* Sending and receiving email with Python.

##### Set-up #####

The file *pgpmailbot.py* receives the mail and processes it. This can be done in two ways:

* Install postfix and add an alias like **mailbot: "| python /path/to/pgpmailbot.py"**. Then use *get_mail_from_stdin* to retrieve the mail.
* Use *get_mail_from_imap* to retrieve email from outside of the mailserver.

Note that you have to create a config file and point to it in *pgpmailbot.py*.

##### Things #####

* Currently anyone can send a random public certificate and it will be imported.
* Directory permissions suck because postfix uses different users to invoke handle the script.
