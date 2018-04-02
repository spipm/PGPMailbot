MAILBOT_BASICMAIL = '''Hi,

I'm an email bot to help you set up PGP public key encryption for your email. 

[EMAIL_IS_ENCRYPTED]

[BOT_HAS_PUBCERT]


With kind regards,

Mailbot
graa.nl
'''

MAILBOT_STARTMESSAGE = '''
So you want to be able to send encrypted email? Try the following software:

Linux/Windows/Mac OS: Thunderbird with Enigmail, Mailvelope, Mailpile
Android: OpenKeychain, APG
iOS: oPenGP

Please look up a tutorial online on how to install the software (I don't like sending links).
Once you've generated a public key for your email address, send it to me so we can continue.
I'll always send you my public key. Please import it so you can also send me encrypted mail.
'''

MAILBOT_PUBKEYIMPORTSUCCESS = '''
I managed to import your public key! I will now try to send you an encrypted email.
'''

