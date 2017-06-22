import paramiko, time, sys, os

def inibackup(ip ,user , passwd, pdir):
    flog = open('./log.txt','a')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port = 22, username = user, password = passwd)
    sftp = client.open_sftp()
    stdin, stdout, stderr = client.exec_command('hostname')
    hostname = str(stdout.read())[2:-3]
    if '/' in hostname:
        hostname = hostname.split('/')[0]
    sname = 'inibak_' + ip.split('.')[-1] + '.sh'
    command = pdir + sname
    fname = hostname + '_' + time.strftime('%Y%m%d') + '.tar.gz'
    plocalPath = './script/' + sname
    premotePath = pdir + sname
    gremotePath = pdir + fname
    glocalPath = './bakfile/' + fname

    plocalPath = './script/' + sname
    premotePath = pdir + sname
    sftp.put(plocalPath, premotePath)
    sftp.chmod(command, 0o755)

    stdin, stdout, stderr = client.exec_command('cd ' + pdir + ';' + command)
    print('\n', file = flog)
    print(hostname, ip, file = flog)
    for line in stdout:
        print('...' + line.strip('\n'), file = flog)

    sftp.get(gremotePath, glocalPath)

    client.close()
    sftp.close()
    flog.close()



pdir = '/tmp/'
user = input('Please input username\n')
passwd = input('Please input password\n')
print('username =', user, 'password =', passwd,'\n')
flag = input('input \'y\' continue\n')
if flag == 'y':
    if os.path.exists('./log.txt'):
        os.remove('./log.txt')
    for line in open('./iplist.ini'):
        if '#' in line:
            continue
        ip = line[:-1]
        inibackup(ip, user, passwd, pdir)
        print(ip, 'ok')
print('\n')
os.system('pause')
