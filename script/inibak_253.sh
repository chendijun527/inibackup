#!/bin/bash
name=`hostname`'_'`date +%Y%m%d`.tar.gz
tar czvpPf $name {/etc/sysconfig/network-scripts,/etc/sysconfig/network,/etc/modprobe.conf,/etc/hosts,/home/moniotor,/opt/rma_p_unix,/root/.bash_profile} --exclude={log,flow,*_Info.txt,*.log,*20[0-1][0-9]*,*.tar.gz}
