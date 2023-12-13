#!/bin/bash
yum install -y bind-utils socat
mkdir /etc/yum.repos.d/old
mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/old cat <<EOF >/etc/yum.repos.d/alauda.repo [alauda]
name=Alauda
baseurl=file:///tmp/kaldr/yum/
enabled=1
gpgcheck=0
EOF
yum clean all && yum makecache
yum install -y jq sshpass socat net-tools ntpdate
