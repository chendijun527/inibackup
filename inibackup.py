#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paramiko, time, sys, os

def inibackup(ip ,user , passwd, pdir, flog):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, port = 22, username = user, password = passwd)
    except:
        print('ssh连接失败', file = flog)
        return 'ssh连接失败'
    sftp = client.open_sftp()
    stdin, stdout, stderr = client.exec_command('hostname')
    hostname = str(stdout.read())[2:-3]
    if '/' in hostname:
        hostname = hostname.split('/')[0]
    sname = 'inibak_' + ip.split('.')[-1] + '.sh'
    command = pdir + sname
    fname = hostname + '_' + time.strftime('%Y%m%d') + '.tar.gz'
    plocalPath = 'script/' + sname
    premotePath = pdir + sname
    gremotePath = pdir + fname
    glocalPath = 'bakfile/' + fname

    plocalPath = 'script/' + sname
    premotePath = pdir + sname
    try:
        sftp.put(plocalPath, premotePath)
    except:
        print('上传脚本失败', file = flog)
        return '上传脚本失败'
    try:
        sftp.chmod(command, 0o755)
    except:
        print('设置脚本权限失败', file = flog)
        return '设置脚本权限失败'
    try:
        stdin, stdout, stderr = client.exec_command('cd ' + pdir + ';' + command)
    except:
        print('运行脚本失败', file = flog)
        return '运行脚本失败'
    print(hostname, ip, file = flog)
    for line in stdout:
        print('...' + line.strip('\n'), file = flog)
    try:
        sftp.get(gremotePath, glocalPath)
    except:
        print('下载备份文件失败', file = flog)
        return '下载备份文件失败'    

    client.close()
    sftp.close()
    return 'ok'


pdir = '/tmp/'
user = input('用户名\n')
passwd = input('密码\n')
print('用户名 =', user, '密码 =', passwd,'\n')
flag = input('输入 \'y\' 继续\n')
if flag == 'y':
    if os.path.exists('log.txt'):
        os.remove('log.txt')
    flog = open('log.txt','a')
    for line in open('iplist.ini'):
        if '#' in line:
            continue
        ip = line.strip('\n')
        if ip == '':
            continue
        print('\n'+'#'*5+ip+'#'*5, file = flog)
        ret = inibackup(ip, user, passwd, pdir, flog)
        if  ret == 'ok':
            print(ip, '完成')
        else:
            print(ip, ret)
print('\n')
flog.close()
os.system('pause')