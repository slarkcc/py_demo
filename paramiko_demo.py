import paramiko
import time


class SshClient(object):
    def __init__(self, host="10.x.x.1", username="username", password="password", port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ssh = None
        self.chan = None

    def connect(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        ssh_client.connect(hostname=self.host, username=self.username, password=self.password, port=self.port)
        trans = ssh_client.get_transport()
        chan = trans.open_session()
        chan.get_pty(width=200)
        chan.invoke_shell()

        self.chan = chan
        self.ssh = ssh_client

    # 每次执行都会打开一个新的channel
    def exec_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)

        # return stdout.read().decode()
        # if self.chan.recv_exit_status():
        ret = stdout.read()
        # else:
        #     ret = b"xxx"
        # print(ret)
        # print("\n")
        # print(ret.decode())
        return ret.decode()

    def send_cmd(self, cmd):
        self.chan.send(cmd)

    def send_cmds(self, cmds):
        for cmd in cmds:
            self.chan.send(cmd)

    # 从channel获取信息，在一条命令执行玩后
    def get_result_from_chan(self):
        self.chan.recv(4096)
        while True:
            if self.chan.recv_ready():
                time.sleep(0.1)
                ret = self.chan.recv(2048)
                break
        return ret.decode()

    def close(self):
        self.ssh.close()


if __name__ == '__main__':
    ssh = SshClient()
    ssh.connect()
    ret = ssh.exec_cmd("ls -a")
    print(ret)
    ssh.close()
