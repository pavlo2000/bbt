import smtplib

default_email = 'aslwojncj@gmail.com'
default_password = 'qwedsazxc@2000'
default_receive = 'gladiypavlo@gmail.com'

import smtplib
from email.mime.text import MIMEText

def send_email1(user, pwd, recipient, subject, body):
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    print('Авторизация:')
    MAIL_USERNAME = user
    MAIL_PASSWORD = pwd
    FROM = MAIL_USERNAME
    TO = recipient
    # теперь можно использовать кириллицу
    msg = body
    msg = MIMEText('\n {}'.format(msg).encode('utf-8'), _charset='utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
        smtpObj.ehlo()
        smtpObj.login(MAIL_USERNAME, MAIL_PASSWORD)
        smtpObj.sendmail(FROM, TO,
                         msg.as_string())
        smtpObj.quit()
        print('Success')
    except:
        print('Error sending')
    # recipient = 'gladiypavlo@gmail.com'
    # FROM = user
    # TO = recipient if isinstance(recipient, list) else [recipient]
    # SUBJECT = subject
    # TEXT = body
    #
    #
    #
    # # Prepare actual message
    # message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    # """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    # print(message)
    # try:
    #     server = smtplib.SMTP("smtp.gmail.com", 587)
    #     server.ehlo()
    #     print(1)
    #     server.starttls()
    #     print(2)
    #     server.login(user, pwd)
    #     print(3)
    #     server.sendmail(FROM, TO, message)
    #     print(4)
    #     server.close()
    #     print('successfully sent the mail')
    # except:
    #     print("failed to send mail")

