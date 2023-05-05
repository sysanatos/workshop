import pandas as pd
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import cx_Oracle as ora

#def __main__():



def oracle_select(sql):
    tns = '10.66.5.27:1521/hnacard_standby1'
    uname = 'card_read'
    upwd = 't0Wz3pKBxl$A'
    '''try a oracle connection, if success, print the version and return success, else print connection error and return fail
    '''
    try:
        db = ora.connect(uname, upwd, tns)
        print(db.version)
        print('connected')
    except ora.Error as error:
        print(error)
        return 1
    df = pd.read_sql(sql, db)
    db.close()
    return df
    
    '''
    sql0 = 'select 1 from dual'
    df0 = pd.read_sql(sql0, db)
    print(df0)
   
    conn = cx_Oracle.connect('scott/tiger@localhost:1521/xe')
    df = pd.read_sql(sql, conn)
    return df
    '''

def auto_mail(yesterday, file):
    '''date generated'''
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    '''delete - in yesterday 
    '''
    yesterday = str(yesterday)
    yesterday1 = yesterday.replace('-', '')
    # automail test
    # Set up email addresses and password
    sender_address = 'hnapay11@new.hnapay.com'
    sender_pass = '411TES@LRB8vi29O'
    #receiver_address = ['xiaoch.chen@hnagroup.com', 'manyi@hnagroup.com', 'yish.he@hnagroup.com']
    receiver_address = ['yu_sun@hnagroup.com']

    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = ", ".join(receiver_address)
    message['Subject'] = yesterday1+" ota test"

    # if has no file to send, 
    if file == 0:
    # Create the body of the message (a plain-text and an HTML version)
        text = """
        您好，\n    """+yesterday+"""的OTA没有失败的通知结果，请知悉\n\n\n
            ------This is a test message from pyautomail.fkbjob, don't reply to this email-----
        """
    elif file == 1:
        text = """
        您好，\n    """+yesterday+"""的OTA失败通知结果请详见见附件\n\n\n
            ------This is a test message from pyautomail.fkbjob, don't reply to this email-----
        """
        # filename
        filename = "OTA" + str(yesterday1) + ".xlsx"
        # Open the file and attach it to the mail
        with open(filename, 'rb') as f:
            attach = MIMEApplication(f.read(),_subtype='xlsx')
            attach.add_header('Content-Disposition','attachment',filename=str(filename))
            message.attach(attach)
    else:
        print("Bad entre, please check parameter.")
        return 1
    # Add HTML/plain-text parts to MIMEMultipart message
    message.attach(MIMEText(text, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.qiye.163.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
      
