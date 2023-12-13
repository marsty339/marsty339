#!/usr/local/bin/python3
import requests
from retry import retry

DELAY = 1
TRIES = 3


def check_result(resp):
    if resp.status_code == 200:
        return resp.json()
    else:
        raise ValueError("No data")


class Harbor18:
    def __init__(self, domain, auth, proxy):
        self.domain = domain
        self.auth = auth
        self.proxy = proxy

    # return a list of projects
    @retry(ValueError, tries=TRIES, delay=DELAY)
    def get_projects(self):
        url = "%s/api/projects" % self.domain
        resp = requests.get(url, auth=self.auth, proxies=self.proxy)
        return check_result(resp)

    # retrieve a list of repositories
    @retry(ValueError, tries=TRIES, delay=DELAY)
    def get_repositories(self, project_id):
        url = "%s/api/repositories" % self.domain
        resp = requests.get(url, auth=self.auth, proxies=self.proxy, params={'project_id': project_id})
        return check_result(resp)

    # retrieve tags from a relevant repository
    # repo_name = project_name + repo_name (devops/devops-api)
    @retry(ValueError, tries=TRIES, delay=DELAY)
    def get_tags(self, repo_name):
        url = "%s/api/repositories/%s/tags" % (self.domain, repo_name)
        resp = requests.get(url, auth=self.auth, proxies=self.proxy)
        return check_result(resp)

    # delete by tag
    @retry(ValueError, tries=TRIES, delay=DELAY)
    def delete_by_tag(self, repo_name, tag):
        url = "%s/api/repositories/%s/tags/%s" % (self.domain, repo_name, tag)
        resp = requests.delete(url, auth=self.auth, proxies=self.proxy)
        if resp.status_code == 200:
            return True
        else:
            raise ValueError("Delete failed")

    # create project if not exists
    @retry(ValueError, tries=TRIES, delay=DELAY)
    def create_project(self, project_name):
        url = "%s/api/projects" % self.domain
        resp = requests.head(url, auth=self.auth, proxies=self.proxy, params={'project_name': project_name})
        project = {
            "project_name": project_name,
            "metadata": {
                "public": "true",
            }
        }
        if resp.status_code == 200:
            return True
        else:
            resp = requests.post(url, json=project, auth=self.auth, proxies=self.proxy)
            if resp.status_code == 201:
                return True
            else:
                raise ValueError("Create failed")
