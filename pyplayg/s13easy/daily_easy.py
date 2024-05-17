import pandas as pd
import datetime
import cx_Oracle as ora
import psycopg2
import mysql.connector
import pymysql
import openpyxl
import zipfile
import os

generated_files = []
today = datetime.datetime.today().strftime('%Y%m%d')
now = datetime.datetime.now().strftime('%H%M%S')
start_date = '20240101'
end_date = '20240515'
# channel_code = ''
# mysql_query = ''
# mysql_query_week =''
# pg_query =''
# ora_query =''
# check_24_ex = ''

def __init__():
    #channel_code = 'QRA103159773UW1'
    test_query = 'select * from busi_merchant limit 5'

    #ora_query ="select t.bus_mer_id 商户号,c.mer_name 商户名称,t.MER_DATE 交易日,t.CLS_DATE 结算日,t.BANK_NAME 开户行,aes128_decry_by_factor(t.BANK_ACCT_NO_CIPHER, t.diversify_factor) 账号,aes128_decry_by_factor(t.bank_acct_name_cipher, t.diversify_factor) 账户名,t.trade_num 交易笔数,t.trade_amt 交易金额,t.trade_fee_amt 交易手续费,t.acc_amt 入帐金额 from clear_org_set_detail t left join crm_barcode_cust_info c on c.bus_mer_id = t.bus_mer_id where t.bus_mer_id ='"+channel_code+"' and t.MER_DATE>='20210101'  order by t.MER_DATE;"
    #generated_files = []
    
def mysql_select(mysql_query):
# connect to mysql database
    connection = mysql.connector.connect(
        host = "10.66.5.105",
        port = "3305",
        user = "tmp_ops",
        password = "tmp_ops",
        database = "upunion_barcode"
    )
    cursor = connection.cursor()

    my_df = pd.read_sql(mysql_query, connection)
#    df.to_excel("output.xlsx", index=False)
    connection.close()
    return my_df

"""
def mysql_select(mysql_query):
# connect to mysql database
    connection = pymysql.connect(
        host = "10.66.5.105",
        user = "tmp_ops",
        password = "tmp_ops",
        database = "upunion_barcode"
    )
    #cursor = connection.cursor()
    my_df = pd.read_sql(mysql_query, con=connection)
#    df.to_excel("output.xlsx", index=False)
    connection.close()
    return my_df
    """

def postgresql_select(pg_query):
# Connect to PostgreSQL database
    pg_conn = psycopg2.connect(
        host = "10.66.5.91",
        database = "barcode_db",
        user = "barcode",
        password = "qgHnw8mZFMju"
    )
    pg_df = pd.read_sql(pg_query, pg_conn)
    pg_df.head()
    return pg_df

def oracle_select_test(ora_query):
    tns = '10.66.5.11:1521/pay_standby3'
    uname = 'pay'
    upwd = 'oy5hTI5hEHi$ub0q'
    try:
        print(out_log('info')+'connecting to oracle')
        db = ora.connect(uname, upwd, tns)
        print(out_log('success')+'connected to oracle')
        print(out_log('info')+'database version: '+db.version)
    except ora.Error as error:
        print(out_log('error')+'connection error: '+str(error))
        return 1
    ora_df = pd.read_sql(ora_query, db)
    db.close()
    return ora_df

def oracle_select(ora_query):
    dsn_tns = ora.makedsn('10.66.5.11', '1521', service_name='pay_standby3')
    connection = ora.connect(user='pay', password='oy5hTI5hEHi$ub0q', dsn=dsn_tns)
    ora_df = pd.read_sql(ora_query, con=connection)
    connection.close()
    return ora_df

def read_conditions_from_file(file_path):
    with open(file_path, 'r') as file:
        conditions = [line.strip() for line in file]
    return conditions

def clean_conditions_file(file_path):
    if not os.path.exists(file_path):
        print(f"conf file '{file_path}' doesn't exists!")
        return
    cleaned_conditions = []
    with open(file_path, 'r') as file:
        for line in file:
            # 去除空白字符（包括空格、制表符和换行符）
            cleaned_line = line.strip()
            # 跳过空行
            if not cleaned_line:
                continue
            # 去除重复项
            if cleaned_line not in cleaned_conditions:
                cleaned_conditions.append(cleaned_line)

    # 将清洗后的结果写回文件
    with open(file_path, 'w') as file:
        file.write('\n'.join(cleaned_conditions))


def main():
    conditions_file_path = 'D:\work\laptop_bak\py_job\conf\channos.lis' 
    clean_conditions_file(conditions_file_path)
    conditions = read_conditions_from_file(conditions_file_path)
    
    save_directory = os.path.join('D:\work\laptop_bak\py_job', today) 
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
  
    for channel_code in conditions:
        __init__()
        mysql_query ="""
           select m.merchant_nm 商户名称,
            m.channel_merchant_no 商户号,
        (select a.AREA_NAME from upunion.tbl_areacode a where a.AREA_NO=m.province) 省,
        (select a.AREA_NAME from upunion.tbl_areacode a where a.AREA_NO=m.city) 市,
        (select a.AREA_NAME from upunion.tbl_areacode a where a.AREA_NO=m.district) 地区,
        CAST(AES_DECRYPT(from_base64(replace(m.address,'new&pay&310012#','')),'1234567890123456') as char ) 地址,
        CAST(AES_DECRYPT(from_base64(replace(m.legal_person_certificate_no,'new&pay&310012#','')),'1234567890123456') as char ) 身份证,
        CAST(AES_DECRYPT(from_base64(replace(m.legal_person_name,'new&pay&310012#','')),'1234567890123456') as char ) 经营者,
        CAST(AES_DECRYPT(from_base64(replace(m.link_man_phone,'new&pay&310012#','')),'1234567890123456') as char ) 手机号码,
        m.create_dt 创建时间,
        case m.status when '1' then '正常' when '5' then '关停' when '2' then '关停' end 商户状态,
        CAST(AES_DECRYPT(from_base64(replace(s.account_no,'new&pay&310012#','')),'1234567890123456') as char ) 银行卡,
        CAST(AES_DECRYPT(from_base64(replace(s.account_nm,'new&pay&310012#','')),'1234567890123456') as char ) 卡名,
        (select  b.BankNm from upunion.tbl_bankcode b where b.branchNo= s.bank_name) 入账银行
        from busi_merchant m left join busi_settle_merchant s on s.merchant_no=m.merchant_no
        where 
        channel_merchant_no = '"""+channel_code+"""'
        """
        mysql_query_week ="""
        select final_time          交易时间,
        channel_merchant_no 商户号,
        merchant_nm         商户名称,
        third_party_uuid    平台订单号,
        third_channel_order_no        三方订单号,
        pay_type            交易类型,
        tran_sts            交易结果,
        amt / 100 交易金额,
        fee_amt / 100 手续费
        from busi_order 
        where channel_merchant_no in ('"""+channel_code+"""')
        and final_time >= '20240101' and final_time <='"""+end_date+"""' order by 2,1;
        """

        pg_query ="""
        select final_time          交易时间,
        channel_merchant_no 商户号,
        merchant_nm         商户名称,
        third_party_uuid    平台订单号,
        third_channel_order_no        三方订单号,
        pay_type            交易类型,
        tran_sts            交易结果,
        amt / 100 交易金额,
        fee_amt / 100 手续费
        from busi_order 
        where channel_merchant_no in ('"""+channel_code+"""')
        and final_time >= '20240101' and final_time <='"""+end_date+"""' order by 2,1;
        """
        
        ora_query ="""
        select t.bus_mer_id 商户号,
        c.mer_name 商户名称,
        t.MER_DATE 交易日,
        t.CLS_DATE 结算日,
        t.BANK_NAME 开户行,
        aes128_decry_by_factor(t.BANK_ACCT_NO_CIPHER, t.diversify_factor) 账号,
        aes128_decry_by_factor(t.bank_acct_name_cipher, t.diversify_factor) 账户名,
        t.trade_num 交易笔数,
        t.trade_amt 交易金额,
        t.trade_fee_amt 交易手续费,
        t.acc_amt 入帐金额
        from clear_org_set_detail t
        left join crm_barcode_cust_info c
        on c.bus_mer_id = t.bus_mer_id
        where t.bus_mer_id ='"""+channel_code+"""' and t.MER_DATE>='20210101' 
        order by t.MER_DATE
        """

        check_24_ex = "select 1 from clear_org_set_detail t left join crm_barcode_cust_info c on c.bus_mer_id = t.bus_mer_id  where t.bus_mer_id ='"+channel_code+"' and t.MER_DATE<'20240101' group by 1"
    
        xlsx_file = channel_code+'.xlsx'  
        excel_file_path = os.path.join(save_directory, xlsx_file)
        
        #print(mysql_query)
        mysql_df = mysql_select(mysql_query)
        mysql_df_week = mysql_select(mysql_query_week)
        #print(test_query)
        #mysql_df = mysql_select(test_query)
        postgresql_df = postgresql_select(pg_query)
        oracle_df = oracle_select(ora_query)
        #print(mysql_df)
        
        with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
            mysql_df.to_excel(writer, sheet_name='商户信息', index=False)
            mysql_df_week.to_excel(writer, sheet_name='交易明细(24年近期)', index=False)
            postgresql_df.to_excel(writer, sheet_name='交易明细(24年往期)', index=False)
            oracle_df.to_excel(writer, sheet_name='结算信息', index=False)
        ex_df = oracle_select(check_24_ex)
        if ex_df.values.size > 0:
            ex_print = "has data before 2024!"
        else:
            ex_print = ""
        print(f"target file {excel_file_path} complete! {ex_print}")
        generated_files.append(excel_file_path)

#    print(f"success!target file {excel_file_path}")
    # zip
    zip_file_name = os.path.join(save_directory, f'{today}_{now}.zip')
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in generated_files:
            zipf.write(file_path, os.path.basename(file_path))
    print(f"zip completed {zip_file_name}")

    # rm
    for file_path in generated_files:
        os.remove(file_path)
    print("all of files deleted")
    print("all jobs done!")

if __name__ == '__main__':
    main()