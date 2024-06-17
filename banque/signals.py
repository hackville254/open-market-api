""" import smtplib
from email.message import EmailMessage

email = 'openmarket@op-markets.com'
password = 'jWph78#84'

msg = EmailMessage()
msg.set_content('Test email content')

msg['Subject'] = 'Test Email'
msg['From'] = email
msg['To'] = 'fdelbo47@gmail.com'

with smtplib.SMTP_SSL('op-markets.com', 465) as smtp:
    smtp.login(email, password)
    smtp.send_message(msg)
 """