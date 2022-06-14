ARG KUBE_VERSION=v1.21.10
ARG SOCAT_VERSION=v1.7.3.4

FROM build-harbor.alauda.cn/ait/kubelet:${KUBE_VERSION} AS kubelet

FROM --platform=linux/amd64 build-harbor.alauda.cn/ait/socat:${SOCAT_VERSION} AS socat-amd64
FROM --platform=linux/arm64 build-harbor.alauda.cn/ait/socat:${SOCAT_VERSION} AS socat-arm64

FROM --platform=linux/amd64 build-harbor.alauda.cn/ops/centos:7.9.2009 AS centos
RUN yum install yum-utils -y -q
RUN printf "[arm]\nname=arm\nbaseurl=https://opentuna.cn/centos-altarch/7.9.2009/os/aarch64/" > /etc/yum.repos.d/arm.repo

RUN yumdownloader --resolve --destdir /tmp/yum/amd64  lvm2 mdadm open-iscsi
RUN yumdownloader --archlist=aarch64 --disablerepo=\* --enablerepo=arm --resolve --destdir /tmp/yum/arm64 lvm2 mdadm open-iscsi


FROM build-harbor.alauda.cn/ops/alpine:3.15 AS build

ARG HELM_VERSION=v3.7.1
ARG RUNC_VERSION=v1.1.1
ARG CONTAINERD_VERSION=1.6.4
ARG KUBE_VERSION=v1.21.10
ARG WITHOUT_AMD64=false
ARG WITHOUT_ARM64=false

RUN apk add --no-cache wget skopeo bash
RUN mkdir -p /tmp/amd64 /tmp/arm64

RUN [[ "${WITHOUT_AMD64}" == "true" ]] || wget https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz -O - | tar xzv --strip-components 1 -C /tmp/amd64
RUN [[ "${WITHOUT_AMD64}" == "true" ]] || wget https://storage.googleapis.com/kubernetes-release/release/${KUBE_VERSION}/bin/linux/amd64/kubectl -O /tmp/amd64/kubectl
RUN [[ "${WITHOUT_AMD64}" == "true" ]] || wget https://storage.googleapis.com/kubernetes-release/release/${KUBE_VERSION}/bin/linux/amd64/kubeadm -O /tmp/amd64/kubeadm
RUN [[ "${WITHOUT_AMD64}" == "true" ]] || wget https://github.com/opencontainers/runc/releases/download/${RUNC_VERSION}/runc.amd64 -O /tmp/amd64/runc
RUN [[ "${WITHOUT_AMD64}" == "true" ]] || (TMP=$(mktemp -d) && \
    wget https://github.com/containerd/containerd/releases/download/v${CONTAINERD_VERSION}/cri-containerd-cni-${CONTAINERD_VERSION}-linux-amd64.tar.gz -O - | tar xzv -C "${TMP}" && \
    mv "${TMP}/usr/local/bin/"* /tmp/amd64/ && \
    tar czvf /tmp/amd64/cni.tgz opt/cni/bin -C "${TMP}")

RUN [[ "${WITHOUT_ARM64}" == "true" ]] || wget https://get.helm.sh/helm-${HELM_VERSION}-linux-arm64.tar.gz -O - | tar xzv --strip-components 1 -C /tmp/arm64
RUN [[ "${WITHOUT_ARM64}" == "true" ]] || wget https://storage.googleapis.com/kubernetes-release/release/${KUBE_VERSION}/bin/linux/arm64/kubectl -O /tmp/arm64/kubectl
RUN [[ "${WITHOUT_ARM64}" == "true" ]] || wget https://storage.googleapis.com/kubernetes-release/release/${KUBE_VERSION}/bin/linux/arm64/kubeadm -O /tmp/arm64/kubeadm
RUN [[ "${WITHOUT_ARM64}" == "true" ]] || wget https://github.com/opencontainers/runc/releases/download/${RUNC_VERSION}/runc.arm64 -O /tmp/arm64/runc
RUN [[ "${WITHOUT_ARM64}" == "true" ]] || (TMP=$(mktemp -d) && \
    wget https://github.com/containerd/containerd/releases/download/v${CONTAINERD_VERSION}/cri-containerd-cni-${CONTAINERD_VERSION}-linux-arm64.tar.gz -O - | tar xzv -C "${TMP}" && \
    mv "${TMP}/usr/local/bin/"* /tmp/arm64/ && \
    tar czvf /tmp/amd64/cni.tgz opt/cni/bin -C "${TMP}")

COPY --from=socat-amd64 /socat /tmp/amd64/socat
COPY --from=socat-arm64 /socat /tmp/arm64/socat

COPY --from=kubelet /kubelet-amd64 /tmp/amd64/kubelet
COPY --from=kubelet /kubelet-arm64 /tmp/arm64/kubelet

COPY --from=centos /tmp/yum /tmp/yum/

RUN chmod +x /tmp/amd64/*
RUN chmod +x /tmp/arm64/*

COPY bins /tmp/installer/bins
COPY charts /tmp/installer/charts
COPY res /tmp/installer/res
COPY images.txt setup.sh saveimages.sh /tmp/installer/

RUN chmod +x /tmp/installer/setup.sh

RUN [[ "${WITHOUT_AMD64}" == "true" ]] || mv /tmp/amd64/* /tmp/installer/bins/x86_64/
RUN [[ "${WITHOUT_ARM64}" == "true" ]] || mv /tmp/arm64/* /tmp/installer/bins/aarch64/

RUN mkdir /tmp/installer/yum -p
RUN [[ "${WITHOUT_AMD64}" == "true" ]] || mv /tmp/yum/amd64/ /tmp/installer/yum/x86_64/
RUN [[ "${WITHOUT_ARM64}" == "true" ]] || mv /tmp/yum/arm64/ /tmp/installer/yum/aarch64/


WORKDIR /tmp/installer
RUN bash saveimages.sh
RUN  rm /tmp/installer/saveimages.sh

RUN tar czvf /opt/mini-k8s-installer.tgz installer -C /tmp


FROM build-harbor.alauda.cn/ops/alpine:3.15

COPY --from=build /opt/ /opt/

