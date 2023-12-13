#!/usr/local/bin/python3

# basic info
import docker
import os.path
from os import path
from functools import partial
from harbor.harbor18 import Harbor18
from multiprocessing.pool import ThreadPool
from harbor.utils import get_filtered_images

DOMAIN = "https://armharbor.alauda.cn"
REGISTRY = "armharbor.alauda.cn"
REGISTRY_NEW = "harbor-b.alauda.cn"
HTTP_PROXY = "http://alauda:Tnriw2z267geivn5aLvk@139.186.17.154:52975"
HTTPS_PROXY = HTTP_PROXY
AUTH = ('admin', 't4YSpvPrrFOsjAapawc5')
PROXIES = {
    "http": HTTP_PROXY,
    "https": HTTPS_PROXY
}


# 0.clean images with pr
# 1.pull arm image, tag and push
# 2.pull amd image, tag and push
# 3.create manifest


def write_to_file(filename, images):
    with open(filename, "w") as f:
        f.writelines("%s\n" % image for image in images)


def read_from_file(filename):
    with open(filename, "r") as f:
        return f.readlines()


def get_images(harbor_client, expression, filename):
    images = get_filtered_images(harbor_client, expression)
    write_to_file(filename, images)


def pull_images(image_name, docker_client):
    repo = image_name.split(':')[0]
    tag = image_name.replace('\n', '').split(':')[1]
    arm_tag = tag + '-arm64'
    if docker_client.images.pull(REGISTRY + "/" + repo, tag) \
            .tag(REGISTRY_NEW + "/" + repo, arm_tag):
        docker_client.images.push(REGISTRY_NEW + "/" + repo, arm_tag,
                                  auth_config={"username": "admin", "password": "raOYiOXaDyGMlLhi"})
    # print(REGISTRY_NEW + "/" + repo + "/" + arm_tag)


if __name__ == '__main__':
    harbor_client = Harbor18(DOMAIN, AUTH, PROXIES)
    docker_client = docker.from_env()
    docker_client.login("admin", password="t4YSpvPrrFOsjAapawc5", registry=DOMAIN, reauth=True)
    release_expression = 'v\d{1,3}\.\d{1,4}\.\d{1,5}'
    filename = "images.txt"

    if not path.exists(filename) or os.stat(filename).st_size == 0:
        get_images(harbor_client, release_expression, filename)
    images = read_from_file(filename)

    pull_images_async = partial(pull_images, docker_client=docker_client)
    pool = ThreadPool(64)
    pool.map(pull_images_async, images)
    pool.close()
    pool.join()
