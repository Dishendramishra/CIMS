import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def send_email(receivers, attach_file_name, sender):
    CIMS_EMAIL_SERVER = os.environ["CIMS_EMAIL_SERVER"]
    CIMS_EMAIL_PORT   = os.environ["CIMS_EMAIL_PORT"]
    CIMS_EMAIL        = os.environ["CIMS_EMAIL"]
    CIMS_EMAIL_PASSWD = os.environ["CIMS_EMAIL_PASSWD"]
    CIMS_EMAIL_CC     = os.environ["CIMS_EMAIL_CC"]

    mail_content  = f"""
Dear Madam/Sir,

Seasons Greetings…!

We are happy to inform you that PC-DT Team has assembled your Desktop PC
and handed over to Stores Section for further process and delivery. Please
find below some key points for your new Desktop:

1. The Machines are pre-installed with Latest Open-Source Operating system
   Ubuntu 20.04.3 LTS with following soft-wares;
    * Firefox Browser
    * Google chrome Browser
    * LibreOffice (Similar to Microsoft Office software)
    * Thunderbird
    * BlueJeans
    * Citrix Receiver (for using Microsoft Office through Application
    Virtualization)

2. Your machine has 250 GB SSD drive which has been used for Ubuntu
    20.04.3 LTS OS installation and 1 TB Hard Disk for user data purpose.
    Please use this 1 TB disk for your own data Storage purpose.

3. The Credentials for your system are as follows:
        Username : pcdt
        Password : pcdt

4. Please find attached herewith your individual Computer parts Serial
    Numbers which can be used for your future warranty Claim purpose.

5. If you want to use Microsoft office through Application virtualization,
    please obtain its credential from Computer Centre.


Thanks & Regards,
{sender}
(for PC-DT Team)
"""

    #Setup the MIME
    message = MIMEMultipart()
    message['From']     = CIMS_EMAIL
    message['To']       = ", ".join(receivers)
    message['Cc']       = CIMS_EMAIL_CC
    message['Subject']  = 'CIMS Report'
    
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file = open(attach_file_name, 'rb')
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)
    payload.add_header('Content-Disposition', 'attachment', filename=attach_file_name)
    
    message.attach(payload)
    message = message.as_string()
    

    try:
        smtpObj = smtplib.SMTP(CIMS_EMAIL_SERVER, CIMS_EMAIL_PORT)
        smtpObj.starttls()
        smtpObj.login( CIMS_EMAIL , CIMS_EMAIL_PASSWD)
        smtpObj.sendmail(CIMS_EMAIL, receivers, message)
        smtpObj.quit() 
    except Exception as e:
        print(e)