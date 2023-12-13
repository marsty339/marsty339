#!/usr/local/bin/python3
from harbor.utils import get_filtered_images, delete_images, read_from_file, write_to_file
import os.path
from os import path
from harbor.harbor18 import Harbor18

# basic info
DOMAIN = "https://harbor.alauda.cn"
AUTH = ('admin', 'raOYiOXaDyGMlLhi')

DOMAIN2 = "https://armharbor.alauda.cn"
AUTH2 = ('admin', 't4YSpvPrrFOsjAapawc5')

HTTP_PROXY = "http://alauda:Tnriw2z267geivn5aLvk@139.186.17.154:52975"
HTTPS_PROXY = HTTP_PROXY

PROXIES = {
    "http": HTTP_PROXY,
    "https": HTTPS_PROXY
}

if __name__ == '__main__':
    filename = "pr_images.txt"
    harbor_client = Harbor18(DOMAIN2, AUTH2, PROXIES)
    projects = harbor_client.get_projects()

    if not path.exists(filename) or os.stat(filename).st_size == 0:
        images = get_filtered_images(harbor_client, ".*-pr-.*")
        write_to_file(filename, images)
    images = read_from_file(filename)
    print(images)
    delete_images(harbor_client, images)
