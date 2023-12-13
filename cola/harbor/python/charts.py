# -*- coding: utf-8 -*-
# 下面的列表，分别是 acp、asm、aml、amp 这四个产品里的 chart list，这个 chart list 只包括 chart 内定义有镜像，需要在打包的时候，将这项镜像打到安装包里的 chart
ACPLIST = [
    'alauda-aiops',
    'alauda-alb2',
    'alauda-base',
    'alauda-cluster-base',
    'alauda-container-platform',
    'alauda-log-agent',
    'ares',
    'artemis-e2e',
    'base-init',
    'captain',
    'cephfs-provisioner',
    'cert-manager',
    'cpaas-calico',
    'cpaas-kube-ovn',
    'cpaas-fit',
    'cpaas-lander',
    'cpaas-monitor',
    'csp-provisioner',
    'dashboard',
    'dex',
    'elasticsearch',
    'helloworld',
    'kafka-zookeeper',
    'kube-prometheus',
    'kubevirt',
    'kubefed',
    'nfs-client-provisioner',
    'nfs-server-provisioner',
    'nginx-ingress',
    'olm',
    'prometheus-operator',
    'public-chart-repo',
    'reloader',
    'rook-ceph',
    'rook-operator',
    'sentry',
    'stability',
    'virtualization'
]
DEVOPSLIST = [
    'alauda-devops',
    'gitlab-ce',
    'harbor',
    'jenkins',
    'mariadb',
    'nexus',
    'sonarqube',
    'testlink'
]
AMLLIST = [
    'aml-ambassador',
    'aml-core',
    'global-aml',
    'volcano'
]
AMPLIST = [
    'amp',
    'amp-kong'
]
ASMLIST = [
    'asm-init',
    'cluster-asm',
    'flagger',
    'global-asm',
    'istio-install',
    'jaeger-operator'
]
CMQLIST = [
    'cmq-installer'
]
TDSQLLIST = [
    'middleware-product-list',
    'tdsql'
]
REDISLIST = [
    'redis-installer'
]
CSPLIST = [
    'csp'
]
TILIST = [
    'ti-matrix-installer'
]
TSFLIST = [
    'harbor',
    'tsf-operator'
]
CODINGLIST = [
    'coding-artifacts',
    'coding-base',
    'coding-cd',
    'coding-ci',
    'coding-operator',
    'coding-testing'
]
OLMLIST = [
    'operator-manifests-images'
]

CHARTS = [
    ACPLIST,
    DEVOPSLIST,
    AMLLIST,
    AMPLIST,
    ASMLIST,
    CMQLIST,
    TDSQLLIST,
    REDISLIST,
    CSPLIST,
    TILIST,
    TSFLIST,
    CODINGLIST,
    OLMLIST
]
