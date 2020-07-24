import smtplib
import ssl  # so that your message and login credentials are not easily accessed by others.

smtp_server = "smtp.gmail.com"
port = 465  # For SSL
sender_email = "raspberrypi.iot.lisha@gmail.com"
sender_password = ""
receiver_email = ""
lisha_email = "https://iot.lisha.ufsc.br"

message = """\
Subject: Hi there

This message was send using Python3 from a Raspberry Pi
from the LISHA department at UFSC
""" + lisha_email + """\
 This is simply to remind you that the electromyogram has finished
and the results shows that the patient is bad.
You can go to https://iot.ufsc.br/HomePage to see the results
Cheers
"""

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message)
print(message)
