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
* Exceptions are not yet handled.
* Debug logging only logs the email message.
* Does not handle in-line PGP, trust levels, key-server validation or other types or encryption like S/MIME.

##### Working example #####

Bot currently runs on graa.nl. A normal email will trigger a response with a public key and the request to encrypt: 

<kbd>![Initial bot response](https://raw.githubusercontent.com/DutchGraa/PGPMailbot/master/docs/initial-mail.png "Initial mail")</kbd>

Once you succesfully imported the bot's public key, you can send it an encrypted email. Once you've done that, it'll continue with the next step, which is sending your public key. You can send it encrypted or unencrypted.

<kbd>![Encryption success, public key request](https://raw.githubusercontent.com/DutchGraa/PGPMailbot/master/docs/step2-encrypted.png "Encryption success, public key request")</kbd>

If the bot succesfully imported your key, it'll start encrypting and signing mails to you. Last request is to sign your email.

<kbd>![Bot imported key, request sign](https://raw.githubusercontent.com/DutchGraa/PGPMailbot/master/docs/step3-sharepubkey.png "Bot imported key, request sign")</kbd>

As a final step, you can encrypt and sign your email. The bot will reply with an encrypted and signed email. Everything works!

<kbd>![Encrypted and signed both ways](https://raw.githubusercontent.com/DutchGraa/PGPMailbot/master/docs/final-worked.png "Encrypted and signed both ways")</kbd>

