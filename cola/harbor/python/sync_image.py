'''
This file sync armharbor releases to harbor-b
'''
import os
import time
import docker
from os import path
from functools import partial

from retry import retry

from harbor.harbor18 import Harbor18
from multiprocessing.dummy import Pool as ThreadPool
# basic info
from harbor.utils import get_filtered_images, write_to_file, read_from_file

DOMAIN = "https://armharbor.alauda.cn"
DOMAIN2 = "https://harbor-b.alauda.cn"
HTTP_PROXY = "http://alauda:Tnriw2z267geivn5aLvk@139.186.17.154:52975"
HTTPS_PROXY = HTTP_PROXY

AUTH = ('admin', 't4YSpvPrrFOsjAapawc5')
PROXIES = {
    "http": HTTP_PROXY,
    "https": HTTPS_PROXY
}
REGISTRY = "armharbor.alauda.cn"
REGISTRY_NEW = "harbor-b.alauda.cn"


# concurrency
@retry(docker.errors.APIError, tries=3, delay=2)
def pull_and_tag(image_name, docker_client):
    if not image_name:
        return
    if image_name:
        repo = image_name.split(":")[0]
        tag = image_name.split(":")[1]
    try:
      if docker_client.images.pull(REGISTRY + "/" + repo, tag).tag(REGISTRY_NEW + "/" + repo, tag + '-arm64'):
          docker_client.images.push(REGISTRY_NEW + "/" + repo, tag + '-arm64')
          docker_client.images.remove(REGISTRY + "/" + image_name, True, True)
          docker_client.images.remove(REGISTRY_NEW + "/" + image_name + '-arm64', True, True)
          print("parsed image %s" % REGISTRY + "/" + repo + ":" + tag)
    except docker.errors.ImageNotFound:
      return

if __name__ == '__main__':
    start_time = time.time()
    filename = "release.txt"

    harbor_client1 = Harbor18(DOMAIN, AUTH, None)
    docker_client = docker.from_env()
    docker_client.login("admin", password="t4YSpvPrrFOsjAapawc5", registry=DOMAIN)
    docker_client.login("admin", password="t4YSpvPrrFOsjAapawc5", registry=DOMAIN2)

    # get images from origin harbor
    if not path.exists(filename) or os.stat(filename).st_size == 0:
        images = get_filtered_images(harbor_client1, "v\d{1,3}\.\d{1,4}\.\d{1,5}")
        write_to_file(filename, images=images)
    images = read_from_file(filename)
    print(images)

    pool = ThreadPool(16)
    pull_and_tag_by_image = partial(pull_and_tag, docker_client=docker_client)
    pool.map(pull_and_tag_by_image, images)
    pool.close()
    pool.join()

    print("--- %s seconds ---" % (time.time() - start_time))
