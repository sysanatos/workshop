#connect to oracle database, get awr report for last week and download to local file
import cx_Oracle 
import os
import sys

'''
def main():
    #connect to database
    con = cx_Oracle.connect('system/password@localhost/xe')
    cur = con.cursor()
    #get report
    cur.execute("select * from dba_hist_snapshot")
    rows = cur.fetchall()
    #write report to file
    with open('awr.txt', 'w') as f:
        for row in rows:
            f.write(str(row))
    #close connection
    con.close()
    #download report to local file
    os.system('scp -i ~/.ssh/id_rsa -P 2222 awr.txt root@localhost:/tmp')
    #remove local file
    os.remove('awr.txt')
    #print success message
    print('awr report downloaded to local file')
    return
'''


username = 'username'
password = 'password'
hostname = 'hostname'
port = 'port'
servicename = 'servicname'

tns = username + '/' + password + '@' + hostname + ':' + port + '/' + servicename


def try_database(tns):
    #connect to database
    try:
        con = cx_Oracle.connect(tns)
        print(con.version)
        print('success to connect to database')
    except cx_Oracle.Error as error:
        print(error)
        print('failed to connect to database')
        return error
    con.close()
    return 0

def get_last_week_snap_id(start_time, end_time):
    #connect to database
    con = cx_Oracle.connect(tns)
    cur = con.cursor()
    #get snap_id
    snap_id_first = cur.execute("select min(snap_id) from dba_hist_snapshot where begin_interval_time between to_date('" + start_time + "','yyyy-mm-dd hh24:mi:ss') and to_date('" + end_time + "','yyyy-mm-dd hh24:mi:ss')")
    snap_id_second = cur.execute("select max(snap_id) from dba_hist_snapshot where begin_interval_time between to_date('" + start_time + "','yyyy-mm-dd hh24:mi:ss') and to_date('" + end_time + "','yyyy-mm-dd hh24:mi:ss')")
    #close connection
    con.close()
    #print success message
    print('snap_id retrieved')
    return snap_id_first, snap_id_second

'''
def generate_oracle_awr(snap_id_first, snap_id_second, awr_output_path):
    #get database dbid and instance_number
    
    '''