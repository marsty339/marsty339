#关闭swap
swapoff -a
sed  -i -r '/swap/s/^/#/' /etc/fstab
free -m
#关闭防火墙
systemctl stop firewalld.service
systemctl disable firewalld.service
#关闭selinux
setenforce 0
sed -ri 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
cat /etc/selinux/config  | grep -w "SELINUX"
#时间同步
systemctl enable chronyd.service
systemctl start chronyd.service
sed -i -e '/^server/s/^/#/' -e '1a server ntp.aliyun.com iburst' /etc/chrony.conf
systemctl restart chronyd.service
#设置时区
timedatectl set-timezone Asia/Shanghai
#修改内核参数
echo 'vm.max_map_count = 262144' >> /etc/sysctl.conf
echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.conf
echo 'vm.drop_caches = 3' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_tw_recycle = 0' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_mtu_probing = 1' >> /etc/sysctl.conf
sysctl -p
ulimit -c 0 && echo 'ulimit -S -c 0' >>/etc/profile
modprobe iptable_nat && echo iptable_nat >> /etc/modules-load.d/cpaas.conf
sed -i -e 's/^UseDNS/#UseDNS/g' -e '$a UseDNS no' /etc/ssh/sshd_config
systemctl restart sshd
yum install -y lvm2