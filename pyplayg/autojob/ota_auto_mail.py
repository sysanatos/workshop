import pandas as pd
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import cx_Oracle as ora
import os

def __main__():
    print(out_log('info')+'OTA auto data job is starting')
    
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
    print(out_log('info')+'today is '+str(datetime.date.today())+' and generate files name '+str(yesterday1))
    
    if not df.empty:
        print(out_log('info')+'it has selected data, generating excel file '+ filename)
        df.to_excel(filename)
        print(out_log('success')+'excel file '+ filename +' generated')
        auto_mail(yesterday, 1)
        #os.remove(filename)
    else:
        print(out_log('info')+'it has not selected data, no need to generate file, go to the next step')
        auto_mail(yesterday, 0)
    print(out_log('success')+'OTA_'+yesterday1+' auto_mail job finished')
    return 0

def out_log(flag):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    stamp = datetime.datetime.now().timestamp()
    if flag == 'info':
        flag = ' [INFO] '
    elif flag == 'error':
        flag = ' [ERROR] '
    elif flag == 'success':
        flag = ' [SUCCESS] '
    else:
        print(str(time)+' '+str(stamp)+' [ERROR] '+flag+' is not a available flag, plz choose on of "info", "error", "success"')
        return 1
    log_head = str(time)+' '+str(stamp)+flag
    return log_head

def oracle_select(sql):
    tns = '10.66.5.27:1521/hnacard_standby1'
    uname = 'card_read'
    upwd = 't0Wz3pKBxl$A'
    try:
        print(out_log('info')+'connecting to oracle')
        db = ora.connect(uname, upwd, tns)
        print(out_log('success')+'connected to oracle')
        print(out_log('info')+'database version: '+db.version)
    except ora.Error as error:
        print(out_log('error')+'connection error: '+str(error))
        return 1
    df = pd.read_sql(sql, db)
    db.close()
    return df

def auto_mail(yesterday, file):
    print(out_log('info')+'start to send email process')
    yesterday1 = yesterday.replace('-', '')
    sender_address = 'hnapay11@new.hnapay.com'
    sender_pass = '411TES@LRB8vi29O'
    receiver_address = ['xiaoch.chen@hnagroup.com', 'manyi@hnagroup.com', 'yish.he@hnagroup.com', 'yu_sun@hnagroup.com']
    #receiver_address = ['yu_sun@hnagroup.com']

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = ", ".join(receiver_address)
    message['Subject'] = yesterday1+"_OTA失败通知"

    if file == 0:
        text = """
        您好，\n    """+"      "+yesterday+"""的OTA没有失败的通知结果，请知悉\n\n\n\n\n
            ------This is a test message from pyautomail.fkbjob, don't reply to this email-----
        """
    elif file == 1:
        text = """
        您好，\n    """+"      "+yesterday+"""的OTA失败通知结果请详见见附件\n\n\n\n\n
            ------This is a test message from pyautomail.fkbjob, don't reply to this email-----
        """
        filename = "OTA" + str(yesterday1) + ".xlsx"
        if filename in os.listdir(os.getcwd()):
            print(out_log('info')+'excel file '+ filename + ' exists, attaching it to mail')
        else: 
            print(out_log('error')+'excel file '+ filename + 'does not exist, please check the file path')
            return 1
        with open(filename, 'rb') as f:
            attach = MIMEApplication(f.read(),_subtype='xlsx')
            attach.add_header('Content-Disposition','attachment',filename=str(filename))
            message.attach(attach)
    else:
        print(out_log('error')+"Bad entre, please check parameter.")
        return 1
    message.attach(MIMEText(text, 'plain'))
    session = smtplib.SMTP('smtp.qiye.163.com', 587)  
    session.starttls()  # enable security
    session.login(sender_address, sender_pass) 
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print(out_log('success')+'email process finished')
      
__main__()
