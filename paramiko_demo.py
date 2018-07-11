import paramiko
import time


class SshClient(object):
    def __init__(self, host="10.10.57.1", username="chenguang", password="112992", port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ssh = None

    def connect(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        ssh_client.connect(hostname=self.host, username=self.username, password=self.password, port=self.port)
        self.ssh = ssh_client

    # 每次执行都会打开一个新的channel
    def exec_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)

        return stdout.read()

    def close(self):
        self.ssh.close()


class InteractiveSsh(object):
    def __init__(self, host="10.10.57.1", username="chenguang", password="112992", port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.shell = None
        self.transport = None

    def connect(self):
        trans = paramiko.Transport((self.host, self.port))
        trans.connect(username=self.username, password=self.password)
        self.transport = trans
        chan = trans.open_channel()
        chan.get_pty()
        chan.invoke_shell()

        self.shell = chan

    def exec_cmd(self, cmd):
        self.shell.send(cmd)
        result = self.shell.recv(1024).decode()
        return result

    def exec_cmds(self, cmds):
        result = list()
        for cmd in cmds:
            self.shell.send(cmd)
            time.sleep(1)
            result.append(self.shell.recv(1024).decode())

        return result

    def close(self):
        if  self.shell:
            self.shell.close()
        if  self.transport:
            self.transport.close()


