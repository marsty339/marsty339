#!/bin/sh

# create docker context
docker context create amd64-runner2 --description "Tencent amd64 runner 02" --docker "host=tcp://10.0.99.3:2375";
docker context create arm64-runner2 --description "Tencent arm64 runner 02" --docker "host=tcp://10.0.99.9:2375";

# download buildx docker-cotainer driver builder metadata
mkdir -p /root/.docker/buildx/instances
curl -sSL --retry 3 https://build-nexus.alauda.cn/repository/alauda/buildx/builder-docker.json -o /root/.docker/buildx/instances/builder

# inspect and bootstrap buildx instance
docker buildx inspect builder;
