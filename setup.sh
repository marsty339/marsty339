#! /usr/bin/env bash


# 命令行示例
# bash setup.sh --vip 192.168.36.170 --interface eth0 --role master --srcip 192.168.36.168 --peerip 192.168.36.169
while [[ $# -gt 0 ]]
do 
key="$1"
case $key in 
--vip)
vip=$2
shift
shift
;;
--interface)
iface=$2
shift
shift
;;
--role)
role=$2
shift
shift
;;
--srcip)
srcip=$2
shift
shift
;;
--peerip)
peerip=$2
shift
shift
;;
esac
done


function set_check_script(){
cat <<EOF > check.sh
#!/bin/sh
num=\`ps -ef |grep haproxy | grep -v grep | wc -l\`
if [ \$num -lt 1 ];then
   ps -ef|grep keepalived | grep -v grep |awk '{print "kill -15 "\$1}'|sh
fi
EOF
chmod +x check.sh
}

function setup_keepalived(){
cat <<EOF > keepalived.conf
! Configuration File for keepalived

global_defs {
   router_id $role
}

vrrp_script check_haproxy {
        script "/etc/keepalived/check.sh"
        interval 3
}

vrrp_instance VI_1 {
    state MASTER
    interface $iface
    virtual_router_id 51
    priority 100
    advert_int 1
    unicast_src_ip $srcip
    unicast_peer {
    $peerip
   }
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
       $vip/24
    }
track_script {
        check_haproxy
    }
}
EOF
}

function setup_haproxy() {
 cat <<EOF > haproxy.cfg
global
    log     127.0.0.1 local0
    nbproc 1           # 1 is recommended
    maxconn  51200     # maximum per-process number of concurrent connections
    pidfile /etc/haproxy/haproxy.pid
    tune.ssl.default-dh-param 2048

defaults
        mode http      # { tcp|http|health }
        #retries 2
        #option httplog
        #option tcplog
        maxconn  51200
        option redispatch
        option abortonclose
        timeout connect 5000ms
        timeout client 2m
        timeout server 2m
        log global
        balance roundrobin

listen stats
        bind 0.0.0.0:2936
        mode http
        stats enable
        stats refresh 10s
        stats hide-version
        stats uri  /admin
        stats realm LB2\ Statistics
        stats auth mathilde:Mathilde1861

listen web-service
    bind 127.0.0.1:9

frontend cpaas_frontend_80
  bind *:80
  mode tcp
  default_backend cpaas_80

frontend cpaas_frontend_443
  bind *:443
  mode tcp
  default_backend cpaas_443

backend cpaas_80
  mode tcp
  balance roundrobin
  default-server on-marked-down shutdown-sessions
server s0 192.168.36.160:30666 check port 30666 inter 1000 maxconn 51200

backend cpaas_443
  mode tcp
  balance roundrobin
  default-server on-marked-down shutdown-sessions
server s0 192.168.36.160:30665 check port 30665 inter 1000 maxconn 51200
EOF
}

function load_image() {
  echo " load images [doing]"

  docker load -i ha.tar

  echo " load images [ok]"
}
function start_docker(){
docker run -d --restart=always -ti --name haproxy-keepalived -v $(pwd)/keepalived.conf:/etc/keepalived/keepalived.conf -v $(pwd)/haproxy.cfg:/etc/haproxy/haproxy.cfg -v $(pwd)/check.sh:/etc/keepalived/check.sh  --privileged=true --net=host build-harbor.alauda.cn/ops/alpine:ha-ke
docker exec -ti haproxy-keepalived haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -Ds
docker exec -ti haproxy-keepalived keepalived -D
}
load_image
setup_haproxy
setup_keepalived
set_check_script
start_docker
