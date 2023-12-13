#!/usr/bin/env python3
import concurrent.futures
from acp_client import AcpClient
from jenkins_client import JenkinsClient
from utils import failed_filter, aborted_filter, time_filter, notify_to_wework, failed_catalog_filter, \
    send_to_prometheus


def new_jenkins_client():
    jenkins_auth = ('pipeline', '1163b42738f293cad5a76adb5e0bbfdbb7')
    jenkins_url = "https://jenkins-new.alauda.cn"
    return JenkinsClient(jenkins_url, jenkins_auth)


def new_acp_client():
    acp_url = 'https://build.alauda.cn'
    jenkins_domain = 'jenkins-new.alauda.cn'
    acp_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ilp1eU9WMS16WTRtRnpMYk1Cbl9Ua3drWjZMZmRyNjI4aVZTbTZGaW4xZDgifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi10b2tlbi02OW43cyIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImJlNmYzODg4LWIyYjktNDhmOC05ZjVhLTEwZTM2ZjBmMjZjNSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTphZG1pbiJ9.J-OhTXnRb-8nVUKxxjpUaFPxoRItHhEbCBwAiOWu_DZTlyLT7hZHNqrG8TwJujQzStNgD6zZZsgeuF-cO2Bcgg_QuSWC9Hd0KYdxXe2QsxEzQkzYfOkz6dLLJHCciRyGQk78CU-2ekWTC-Bc-M2elItJCf1N7WznPQ_BOhLscsZ7CItuqu79ozw4AhAa_fwrNb8rdjjpg4NEFFIT2snSzMKvzcaM6cVVTlg5-AMsOwQCpGtXiqmD3C8PpsvWbb0heejO18LrFxrS_MISxBQcsGuJt9HG_hmIxf-rtfyI9Y5UtQF4AJQzC604OlU5NM7m_tiWx-f1plsAzIZAaQNKRg'
    return AcpClient(acp_url, acp_token, jenkins_domain)


def get_failed_pipelines(pipelines):
    results = []
    for pipeline in pipelines:
        if failed_filter(pipeline):
            results.append(pipeline)
    return results


def get_aborted_pipelines(pipelines):
    results = []
    for pipeline in pipelines:
        if aborted_filter(pipeline):
            results.append(pipeline)
    return results


def get_specific_pipelines(pipelines, jenkins_client, key_word):
    results = []
    for pipeline in pipelines:
        log_text = jenkins_client.get_pipeline_log(pipeline)
        if failed_catalog_filter(log_text, key_word): results.append(pipeline)
    return results


if __name__ == '__main__':
    jenkins_domain = 'jenkins-new.alauda.cn'
    jenkins_client = new_jenkins_client()
    acp_client = new_acp_client()
    we_work = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c9863e53-e58c-4e18-a059-b8a24135cb3d'
    days_offset = 1  # days before today,this value should >= 0

    key_words = ['Automatic merge failed',
                 'plugin "devops" exited with error',
                 'Couldn\'t find any revision to build',
                 'failed commit on ref "layer-sha256',
                 'script returned exit code 1']

    # 1. get all pipelines
    all_pipelines = []
    for pipeline in acp_client.get_all_pipelines():
        if time_filter(pipeline, days_offset): all_pipelines.append(pipeline)
    # 2. get failed and aborted pipelines
    failed_pipelines = get_failed_pipelines(all_pipelines)
    aborted_pipelines = get_aborted_pipelines(all_pipelines)
    # 3. concurrently to filter failed log
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(key_words)) as executor:
        future_to_keyword = {
            executor.submit(get_specific_pipelines, failed_pipelines, jenkins_client, key_word): key_word for key_word
            in key_words}
        results = {}
        for future in concurrent.futures.as_completed(future_to_keyword):
            results[future_to_keyword[future]] = future.result()

    aborted_rate = len(aborted_pipelines) / len(all_pipelines)
    failed_rate = (len(failed_pipelines) + len(aborted_pipelines)) / len(all_pipelines)
    conflict_rate = len(results[key_words[0]]) / len(failed_pipelines)
    notify_to_wework(we_work, days_offset, len(all_pipelines), failed_rate, conflict_rate)

    conflict_pipelines = set()
    for pipeline in results[key_words[0]]:
        conflict_pipelines.add(pipeline["pipe_name"])

    # send_to_prometheus(results)
    print("\n")
    print("合并冲突的流水线： ", conflict_pipelines)
    print('\n')
    print("Total    Num: " + '\t', len(all_pipelines))
    print("Aborted  Num: " + '\t', len(aborted_pipelines))
    print("Failed   Num: " + '\t', len(failed_pipelines))
    print("Conflict Rate: " + '\t', "{:.0%}".format(conflict_rate))
