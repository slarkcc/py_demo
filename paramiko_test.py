import paramiko

trans = paramiko.Transport(("10.10.57.1", 22))
trans.auth_password(username="chenguang", password="112992")

chan = trans.open_session(window_size=200)

chan.exec_command("ls chen/\t\t")

