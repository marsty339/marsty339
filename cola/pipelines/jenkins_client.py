import requests


class JenkinsClient:
    def __init__(self, url, auth):
        self.jenkins_url = url
        self.auth = auth

    def get_pipeline_log(self, pipeline):
        return requests.get(pipeline["log"], auth=self.auth).text
