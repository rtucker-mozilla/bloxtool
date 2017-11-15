from common import make_request
import json
import yaml
import sys
from apioutput import APIOutput
from basemixin import BaseMixin


class ZoneAuth(BaseMixin):

    def create_zoneauth(
            self,
            zone,
            view,
            ns_group = None,
            grid_primary = None,
            disable=False,
            members=[],
            should_print=False):
        url = "zone_auth"
        data = {}
        data['fqdn'] = zone
        data['view'] = view
        if grid_primary:
            data['grid_primary'] = [
                {
                    'name': grid_primary
                }
            ]
        if ns_group:
            data['ns_group'] = ns_group
        ret_obj = make_request(
            url,
            'create',
            data=data,
            hostname=self.hostname,
            auth=self.auth
        )
        try:
            if ret_obj.status_code == 201:
                print "Successfully created zone_auth"
            else:
                print "Unable to create zone_auth"
                print ret_obj.json()['text']
        except Exception, e:
            print "Unable to create zone_auth"
            sys.exit(2)
