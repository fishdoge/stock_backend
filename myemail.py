# https://mailtrap.io/blog/python-send-email-gmail/


import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

subject = "Email Subject"
body = "This is the body of the text message"

sender = "wesley@hongwangtec.com"
password = "tpgvzwefzlctvjas"
receiver = ["wesliutw@gmail.com"]
send_email(subject, body, sender, receiver, password)