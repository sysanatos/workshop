import paramiko
import pandas as pd
import io
from abc import ABC, abstractmethod

class HostConnection(ABC):
    def __init__(self, hostname, username, password):
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
    print(f"Storage info for {host.hostname}:")
    print(df)
    # 这里可以添加更多的处理逻辑

# 使用示例
host_201 = HostTypeA('10.66.5.201', '3paradm', '3pardata')
host_209 = HostTypeA('10.66.5.209', '3paradm', '3pardata')
host_210 = HostTypeA('10.66.5.210', '3paradm', '3pardata')
host_211 = HostTypeC('10.66.5.211', 'superuser', 'hnair123')
host_212 = HostTypeB('10.66.5.212', 'superuser', '1qaz@WSX')

process_host(host_201)
process_host(host_209)
process_host(host_210)
process_host(host_211)
process_host(host_212)