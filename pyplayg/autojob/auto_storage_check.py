import paramiko
import pandas as pd
import io
import json
from abc import ABC, abstractmethod

class HostConnection(ABC):
    def __init__(self, hostname, username, password):
    def __init__(self, tag_name,hostname, username, password):
        self.tag_name = tag_name
        self.hostname = hostname
        self.username = username
        self.password = password

    def ssh_execute_command(self, command):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.hostname, username=self.username, password=self.password)
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode('utf-8')
            ssh.close()
            return output
        except Exception as e:
            return f"An error occurred: {str(e)}"

    @abstractmethod
    def get_storage_info(self):
        pass

class HostTypeA(HostConnection):
    def get_storage_info(self):
        command = 'showpd'
        result = self.ssh_execute_command(command)
        result = '\n'.join([line for line in result.split('\n') if '-' not in line])
        #result = '\n'.join([line for line in result.split('\n') if 'total' not in line.lower()])
        return pd.read_csv(io.StringIO(result), sep='\s+')
        
        

class HostTypeB(HostConnection):
    def get_storage_info(self):
        command = 'lsdrive'  # 假设这是HostTypeB需要的命令
        result = self.ssh_execute_command(command)
        # 这里可能需要对result进行一些预处理
        return pd.read_csv(io.StringIO(result), sep='\s+')

class HostTypeC(HostConnection):
    def get_storage_info(self):
        command = 'svcinfo lsdrive'  # 假设这是HostTypeC需要的命令
        result = self.ssh_execute_command(command)
        # 这里可能需要对result进行一些预处理
        return pd.read_csv(io.StringIO(result), sep='\s+')

def process_host(host):
    df = host.get_storage_info()
    #print("init df")
    #print(df)
    # Remove rows where 'cagepos' column is 'total'
    df = df[df['CagePos'] != 'total']
    #print("after df")
    #print(df)
    return df[df['State'] != 'normal']
    # 这里可以添加更多的处理逻辑

def process_host_ibm(host):
    tag_name = host.tag_name
    df = host.get_storage_info()
    df = df[df['status'] != 'online']
    if result_201.empty:
        print(tag_name, "disks all green")
    else:
        print(tag_name, "disks has some problem:")
        print(df)
    #return df[df['status'] != 'online']

'''
def process_host_210(host):
    df = host.get_storage_info()
    #df = df[df['']]
    return df
    '''

def process_host_so(host):
    df = host.get_storage_info()
    #print("init df")
    #print(df)
    # Remove rows where 'cagepos' column is 'total'
    #df = df[df['CagePos'] != 'total']
    #print("after df")
    #print(df)
    #return df[df['State'] != 'normal']
    return df

# 使用示例
host_201 = HostTypeA('host_201', '10.66.5.201', '3paradm', '3pardata')
host_209 = HostTypeA('host_209', '10.66.5.209', '3paradm', '3pardata')
host_210 = HostTypeA('host_210', '10.66.5.210', '3paradm', '3pardata')
host_211 = HostTypeC('host_211', '10.66.5.211', 'superuser', 'hnair123')
host_212 = HostTypeB('host_212', '10.66.5.212', 'superuser', '1qaz@WSX')

#print(process_host(host_201))
result_201 = process_host(host_201)
if result_201.empty:
    print("201 "+"all green")
else:
    print(result_201)

#print(process_host(host_209))
result_209 = process_host(host_209)
if result_209.empty:
    print("209 "+"all green")
else:
    print(result_209)

#print(process_host(host_210))
result_210 = process_host(host_210)
if result_210.empty:
    print("210 "+"all green")
else:
    print(result_210)
#df_201 = host_201.get_storage_info()
#print(df_201)

process_host_ibm(host_211)

process_host_ibm(host_212)


'''
# 查看df_201的基本信息
print("DataFrame Info:")
print(df_201.info())

# 显示列名
print("\nColumn Names:")
print(df_201.columns)

# 显示数据类型
print("\nData Types:")
print(df_201.dtypes)

# 显示基本统计信息
print("\nBasic Statistics:")
print(df_201.describe())

# 显示前几行数据
print("\nFirst Few Rows:")
print(df_201.head())

# 显示唯一值和计数
for column in df_201.columns:
    print(f"\nUnique values in {column}:")
    print(df_201[column].value_counts())

# 检查是否有缺失值
print("\nMissing Values:")
print(df_201.isnull().sum())

# 显示DataFrame的形状（行数和列数）
print("\nDataFrame Shape:")
print(df_201.shape)

abnormal_drives = df_201[df_201['state'] != 'normal']
if not abnormal_drives.empty:
    print(f"Abnormal drives for {host_201.hostname}:")
    print(abnormal_drives)
else:
    print(f"No abnormal drives found for {host_201.hostname}")

#process_host(host_209)
#process_host(host_210)
#process_host(host_211)
#process_host(host_212)
'''