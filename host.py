from common import make_request
import json
import yaml
import sys
from apioutput import APIOutput
from basemixin import BaseMixin


class Host(BaseMixin):

    def search(
        self,
        attribute=None,
        value=None,
        network=None,
        stype=None,
        status=None
    ):
        if status:
            status = status.upper()
        if stype:
            stype = stype.upper()
        if attribute and value:
            return self.search_by_attribute_value(
                attribute,
                value,
                network,
                stype,
                status
            )
        else:
            return self.search_by_network(network, stype, status)

    def search_by_network(self, network=None, stype=None, status=None):
        network_string = "network=%s" % network

        url = 'ipv4address?{}'.format(network_string)

        if stype:
            url = "{}&types={}".format(url, stype)

        if status:
            url = "{}&status={}".format(url, status)

        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        print self.get_output(ret, self.o_format, self.delimeter)

    def search_by_attribute_value(
        self,
        attribute,
        value,
        network=None,
        stype=None,
        status=None
    ):
        network_string = ""
        if network:
            network_string = "network=%s&" % network

        url = 'ipv4address?%s*%s~:=%s' % (network_string, attribute, value)
        if stype:
            url = "{}&types={}".format(url, stype)
        if status:
            url = "{}&status={}".format(url, status)
        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        print self.get_output(ret, self.o_format, self.delimeter)

    def create_host(
            self,
            name,
            ipv4addrs,
            mac,
            should_print=False):
        url = "record:host"
        data = {}
        addrobj = {}
        addrobj['ipv4addr'] = "10.48.8.43"
        if mac:
            addrobj['mac'] = mac
        data['ipv4addrs'] = [addrobj]
        data['name'] = name
        addrobj['ipv4addr'] = ipv4addrs
        data['view'] = "MDC1 Private"
        ret = make_request(
            url,
            'create',
            data=data,
            hostname=self.hostname,
            auth=self.auth
        )
        output = self.get_output(ret, self.o_format, self.delimeter)
        if should_print is True:
            print output

    def search_by_record_name(self, name, should_return=False):
        url = 'record:host?name=%s' % name
        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        if should_return:
            return ret
        else:
            print self.get_output(ret, self.o_format, self.delimeter)

    def list_hosts(self, should_return=False):
        url = 'record:host'
        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        if should_return:
            return ret
        else:
            print self.get_output(ret, self.o_format, self.delimeter)

    def get(self, address=None, name=None, n_type="host:record", ipv6=False):
        ret = False
        if name and n_type == "host:record":
            print 'here'
            ret = self.search_by_record_name(
                name,
            )
        """
        if ret is None:
            print "Unable to get Nework: {network}".format(
                network=network
            )
        else:
            print self.get_output(ret, self.o_format, self.delimeter)
        """
