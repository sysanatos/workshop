import pandas as pd
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import cx_Oracle as ora
import os

def __main__():
    sql="""
    select  ta.http_record_id,
    ta.async_msg_id,
    ta.status_code,
    ta.response_content,
    ta.request_content,
    ta.request_time,
    ta.response_time,
    ta.url_method,
    ta.url,
    ta.merchant_code,ta.ranks rn,to_char(ta.request_time,'yyyy-MM-dd HH24:mi:ss' ) request_time,ta.retry_count from (
    select row_number() over(partition by ts.async_msg_id order by ts.request_time desc ) ranks,ts.*,t.retry_count from card_business.T_HTTP_RECORD_INFO ts,card_business.T_FAILED_REQUEST_INFO t  
    where  ts.request_time >= trunc(sysdate - 2) 
    and ts.request_time < trunc(sysdate - 1) and ts.merchant_code='114400001011124' 
    and   t.retry_count>=5 and t.queue_name='hnacard.notification.http' and t.async_msg_id = ts.async_msg_id
    and  t.create_date >= trunc(sysdate - 2) 
    and t.create_date < trunc(sysdate - 1)
    ) ta where ta.ranks =1  order by ta.request_time desc
    """
    df = oracle_select(sql)

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = str(yesterday)
    yesterday1 = yesterday.replace('-', '')
    filename = "OTA" + str(yesterday1) + ".xlsx"
    
    #if df is not empty, write df into a excel file
    if not df.empty:
        df.to_excel(filename)
        auto_mail(yesterday, 1)
        #os.remove(filename)
    else:
        auto_mail(yesterday, 0)
    print("OTA "+yesterday+" auto_mail job finished")
    return 0

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
    receiver_address = ['xiaoch.chen@hnagroup.com', 'manyi@hnagroup.com', 'yish.he@hnagroup.com', 'yu_sun@hnagroup.com']
    #receiver_address = ['yu_sun@hnagroup.com']

    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = ", ".join(receiver_address)
    #message['Subject'] = yesterday1+" ota test"
    message['Subject'] = yesterday1+"_OTA失败通知"

    # if has no file to send, 
    if file == 0:
    # Create the body of the message (a plain-text and an HTML version)
        text = """
        您好，\n    """+"      "+yesterday+"""的OTA没有失败的通知结果，请知悉\n\n\n\n\n
            ------This is a test message from pyautomail.fkbjob, don't reply to this email-----
        """
    elif file == 1:
        text = """
        您好，\n    """+"      "+yesterday+"""的OTA失败通知结果请详见见附件\n\n\n\n\n
            ------This is a test message from pyautomail.fkbjob, don't reply to this email-----
        """

        # filename
        filename = "OTA" + str(yesterday1) + ".xlsx"
        #if filename.xlsx exists: continue, if not exists: return 1
        if filename in os.listdir(os.getcwd()):
            print("file exists")
        else: 
            print(filename + " not exists")
            return 1
        
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
      
__main__()
