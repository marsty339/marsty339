#!/usr/bin/bash
for i in $(kubectl get pv | awk '{print $1}' | grep -v NAME)
do
   kubectl patch pv $i -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
done

mkdir -p /backup_$(date +%Y%m%d%H) && cp -r /etc/kubernetes/ /backup_$(date +%Y%m%d%H)/ && cp -r /var/lib/etcd/ /backup_$(date +%Y%m%d%H)/

docker cp $(docker ps | grep -v etcd-mirror | grep -w etcd | awk '{print $1}'):/usr/local/bin/etcdctl /usr/bin/
ETCDCTL_API=3 etcdctl --endpoints 127.0.0.1:2379 --cert="/etc/kubernetes/pki/etcd/server.crt" --key="/etc/kubernetes/pki/etcd/server.key" --cacert="/etc/kubernetes/pki/etcd/ca.crt" snapshot save /backup_$(date +%Y%m%d%H)/snap-$(date +%Y%m%d%H%M).db

ETCDCTL_API=3 etcdctl --endpoints 127.0.0.1:2379 --cert="/etc/kubernetes/pki/etcd/server.crt" --key="/etc/kubernetes/pki/etcd/server.key" --cacert="/etc/kubernetes/pki/etcd/ca.crt" snapshot save /backup_$(date +%Y%m%d%H)/snap.db

##确保大小超过几M
du -sh /backup_$(date +%Y%m%d%H)/snap.db