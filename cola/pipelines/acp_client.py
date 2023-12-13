import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AcpClient:
    def __init__(self, acp_url, token, jenkins_domain):
        self.token = token
        self.acp_url = acp_url
        self.headers = {"Authorization": "Bearer " + self.token}
        self.jenkins_domain = jenkins_domain

    def get_all_projects(self):
        pro_names = []
        pro_url = '{}/apis/auth.alauda.io/v1/projects'.format(self.acp_url)
        res_pro = requests.get(pro_url, headers=self.headers, verify=False).json()
        for item in res_pro['items']:
            if item['kind'] == 'Project':
                pro_names.append(item['metadata']['name'])
        return pro_names

    def get_project_pipelines(self, pro_name):
        pipelines = []
        url = '{}/devops/api/v1/pipeline/{}'.format(self.acp_url, pro_name)
        resp = requests.get(url, headers=self.headers, verify=False).json()
        for pipeline in resp['pipelines']:
            if pipeline['status']['phase'] not in ('Queued', 'Error'):
                if 'jenkins' in pipeline['status']:
                    print(pipeline['status']['jenkins'])
                    pipelines.append({'ns': pipeline['metadata']['namespace'], 'pipe_name': pipeline['metadata']['name'],
                                      'status': pipeline['status']['jenkins']['status'],
                                      'ctime': pipeline['metadata']['creationTimestamp'],
                                      'ftime': pipeline['status']['finishedAt'],
                                      'log': "https://" + self.jenkins_domain + '/' + pipeline['metadata']['annotations'][
                                          'cpaas.io/jenkins-log-url']})
        return pipelines

    def get_all_pipelines(self):
        pipelines = []
        for project in self.get_all_projects():
            for pipeline in self.get_project_pipelines(project):
                pipelines.append(pipeline)
        return pipelines
