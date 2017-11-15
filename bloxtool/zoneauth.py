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
                print "Successfully created zone_auth: {0}".format(zone)
            else:
                print "Unable to create zone_auth"
                print ret_obj.json()['text']
        except Exception, e:
            print "Unable to create zone_auth"
            sys.exit(2)

    def search_by_zone(self, zone, view, should_return=False):
        url = 'zone_auth?fqdn={0}&view={1}'.format(
            zone,
            view
        )
        ret_obj = make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        if should_return:
            return ret_obj
        else:
            print self.get_output(ret_obj, self.o_format, self.delimeter)
        return ret_obj

    def delete_zoneauth(
            self,
            zone,
            view,
            should_print=False):
        try:
            network_req = self.search_by_zone(
                zone=zone,
                view=view,
                should_return=True
            )
            network_ref = network_req.json()[0]['_ref']
        except IndexError:
            print "Unable to delete zone {0}".format(zone)
            sys.exit(2)
        except (AttributeError, TypeError, KeyError):
            return False
        resp = self.make_request(
            network_ref,
            'delete',
            hostname=self.hostname,
            auth=self.auth
        )
        try:
            status_code = resp.status_code
        except:
            print "Unable to delete zone_auth: {0}".format(zone)
            return False

        if status_code == 200:
            print "zone_auth Successfully Deleted: {0}".format(zone)
            return True
        else:
            print "Unable to delete zone_auth: {0}".format(zone)
            return False
