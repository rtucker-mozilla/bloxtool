import requests
import json
import sys
from apioutput import APIOutput


class BaseMixin(object):
    def __init__(self, hostname, auth, o_format="text", delimeter=" "):
        self.hostname = hostname
        self.auth = auth
        self.o_format = o_format
        self.delimeter = delimeter
        self.api_out = None

    def get_output(self, ret, o_format='text', delimeter=" ", should_return=False):
        self.api_out = APIOutput(ret, o_format=o_format, delimeter=delimeter)
        has_error, error_text = self.api_out.process_resp()
        if has_error is True:
            print error_text
            sys.exit(2)
        formatted_text = self.api_out.format_text()
        return formatted_text

    def make_request(
            self,
            url,
            request_type='get',
            data={},
            hostname='http://localhost',
            auth=None):
        url = "%s/wapi/v1.2/%s" % (hostname, url)
        headers = {}
        headers['Content-Type'] = 'application/json'
        if isinstance(data, list):
            data = json.dumps(data)
        if isinstance(data, dict) and not data == {}:
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
