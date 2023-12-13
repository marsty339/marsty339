import requests
import json
import datetime
import re
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


def failed_filter(pipeline):
    return True if pipeline['status'] == "FAILED" else False


def aborted_filter(pipeline):
    return True if pipeline['status'] == "ABORTED" else False


def failed_catalog_filter(log, key_word):
    reg = re.compile(key_word)
    return True if re.search(reg, log) else False


def time_filter(pipeline, days_offset):
    current_time = datetime.datetime.utcnow()
    delta = datetime.timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second)
    time_delta = current_time - datetime.datetime.strptime(pipeline['ctime'], "%Y-%m-%dT%H:%M:%SZ")
    if days_offset == 0:
        return True if datetime.timedelta(days=0) <= time_delta <= delta else False
    if pipeline['ctime']:
        return True if delta <= time_delta <= delta + datetime.timedelta(days=days_offset) else False


def notify_to_wework(robot_url, days_offset, total, failed_rate, conflict_rate):
    content = "前%d天共运行了<font color=\"info\">%s</font>条流水线，其中失败率为<font color=\"warning\">%s</font>。" \
              (days_offset, total, "{:.0%}".format(failed_rate))

    headers = {'Content-Type': 'application/json'}
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    requests.post(robot_url, headers=headers, data=json.dumps(payload))


def send_to_prometheus(metrics):
    registry = CollectorRegistry()
    g = Gauge("build_statics", "alauda pipeline build statics yesterday", ['error_type'], registry=registry)
    for metric in metrics:
        g.labels(metric).set(len(metrics[metric]))
    push_to_gateway('https://pushgateway.alauda.cn', job='jenkins-new.alauda.cn', registry=registry)
