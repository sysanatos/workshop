#This is a test python file on laptop with vscode

import sys

print("Python version")
print(sys.version)
print("Version info.")
print(sys.version_info)
print("Python executable path")
print(sys.executable)


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def auto_mail(): 
    #send mail to myself
    sender = 'XXXXXXXXXXXXXXXXXXXXX'
    receivers = ['XXXXXXXXXXXXXXXXXXXXX']
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receivers[0]
    message['Subject'] = 'Python test'
    message.attach(MIMEText('Python test', 'plain'))
    #attach file
    with open('XXXXXXXXXXXXXXXXXXXXX', 'rb') as f:
        part = MIMEApplication(f.read())
        part.add_header('Content-Disposition', 'attachment', filename='XXXXXXXXXXXXXXXXXXXXX')
        message.attach(part)
        f.close()
    #send mail
    try:     
        smtpObj = smtplib.SMTP('XXXXXXXXXXXXXXXXXXXXX')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("Successfully sent email")
        smtpObj.quit()
        return 1
    except smtplib.SMTPException:
        print("Error: unable to send email")
        return 0
    
if auto_mail() == 1:
    print("Mail sent successfully")
    sys.exit(0)
    
else:
    print("Mail sent failed")
    sys.exit(1)
    
def oracle_select(sql):
    '''connect to oracle,and execute the query sql,if the query is successful,return the result and export into a csv file,otherwise return None
    '''
    import cx_Oracle
    import pandas as pd
    try:
        conn = cx_Oracle.connect('XXXXXXXXXXXXXXXXXXXXX')
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        df.to_csv('XXXXXXXXXXXXXXXXXXXXX',index=False)
        cursor.close()
        conn.close()
        return result
    except:
        print("Error: unable to fetch data")
        return None

def today():
    '''return the date of today
    '''
    import datetime
    return datetime.date.today()

def yesterday():
    '''return the date of yesterday
    '''
    import datetime
    return datetime.date.today() - datetime.timedelta(days=1)

def oracle_null():
    '''if oracle query is empty,return None,else export the result into a csv file
    '''
    import pandas as pd
    result = oracle_select('XXXXXXXXXXXXXXXXXXXXX')
    if result == None:
        return None
    else:
        df = pd.DataFrame(result)
        df.to_csv('XXXXXXXXXXXXXXXXXXXXX',index=False)
        return result
