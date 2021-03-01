# -*- coding: utf-8 -*-

import paramiko
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, SSHException, BadHostKeyException

host = "192.168.10.148"
user = "pranali"
psw = "123"

try:
    # Make the connection
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    # print paramiko.AutoAddPolicy()
    ssh.connect(host, username=user, password=psw)

    # Somehting like this to run the command:
    stdin, stdout, stderr = ssh.exec_command("ifconfig")
    print ''.join(stdout.readlines())
except AuthenticationException:
    print("Authentication failed, please verify your credentials: %s")
except SSHException as sshException:
    print("Unable to establish SSH connection: %s" % sshException)
except BadHostKeyException as badHostKeyException:
    print("Unable to verify server's host key: %s" % badHostKeyException)
finally:
    ssh.close() 