import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def send_email(receivers, attach_file_name):
    CIMS_EMAIL_SERVER = os.environ["CIMS_EMAIL_SERVER"]
    CIMS_EMAIL_PORT   = os.environ["CIMS_EMAIL_PORT"]
    CIMS_EMAIL        = os.environ["CIMS_EMAIL"]
    CIMS_EMAIL_PASSWD = os.environ["CIMS_EMAIL_PASSWD"]
    CIMS_EMAIL_CC     = os.environ["CIMS_EMAIL_CC"]

    mail_content  = """
    This is a test e-mail message.
    """

    #Setup the MIME
    message = MIMEMultipart()
    message['From']     = CIMS_EMAIL+"@prl.res.in"
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
        smtpObj = smtplib.SMTP(CIMS_EMAIL_SERVER)
        smtpObj.starttls()
        smtpObj.login( CIMS_EMAIL , CIMS_EMAIL_PASSWD)
        smtpObj.sendmail(CIMS_EMAIL, receivers, message)
        smtpObj.quit() 
    except Exception as e:
        print(e)

if __name__ == "__main__":
    send_email(["dishendra@prl.res.in"], "20220114340103.pdf")