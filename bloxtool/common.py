import requests
import json
import sys


def make_request(
        url,
        request_type='get',
        data={},
        hostname='http://localhost',
        auth=None):
    url = "%s/wapi/v2.2/%s" % (hostname, url)
    headers = {}
    headers['Content-Type'] = 'application/json'
    if data != {}:
        data = json.dumps(data)
    request_type = request_type.lower()
    if request_type == 'get':
        resp = requests.get(
            url,
            headers=headers,
            auth=auth,
            verify=False
        )
    elif request_type == 'update'\
            or request_type == 'put':
            resp = requests.put(
                url,
                headers=headers,
                auth=auth,
                data=data,
                verify=False
            )
    elif request_type == 'create'\
            or request_type == 'post':
            resp = requests.post(
                url,
                headers=headers,
                auth=auth,
                data=data,
                verify=False
            )
    elif request_type == 'delete':
        resp = requests.delete(
            url,
            headers=headers,
            auth=auth,
            verify=False
        )
    return resp
