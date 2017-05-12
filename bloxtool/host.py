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
            network_block=False,
            should_print=False):
        url = "record:host"
        data = {}
        addrobj = {}
        if ipv4addrs == 'nextavailableip' and network_block is not False:
            ipv4addrs = 'func:nextavailableip:{}'.format(
                network_block
            )
        addrobj['ipv4addr'] = ipv4addrs
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

    def delete_attr(self, name, attr_name):
        host_obj = self.search_by_record_name(
            name,
            should_return=True,
            extattrs=True
        )
        try:
            url = host_obj.json()[0]['_ref']
        except (IndexError, KeyError):
            print "Unable to find host by name"
            sys.exit(2)
        extattrs = {}
        try:
            extattrs['extattrs'] = host_obj.json()[0]['extattrs']
        except:
            extattrs['extattrs'] = {}

        if attr_name in extattrs['extattrs']:
            should_update_attrs = True
            del extattrs['extattrs']['PDU']
        else:
            should_update_attrs = False

        if should_update_attrs:
            ret_obj = self.make_request(
                url,
                'update',
                data=extattrs,
                hostname=self.hostname,
                auth=self.auth
            )
            try:
                if ret_obj.status_code == 200:
                    print "Successfully deleted host extattr"
                else:
                    print "Unable to create host extattr"
                    print ret_obj.json()['text']
            except Exception, e:
                print "Unable to create host extattr"
                sys.exit(2)
        else:
            print "attribute not found"
            sys.exit(2)

    def create_attr(self, name, attr_name, attr_value):
        host_obj = self.search_by_record_name(
            name,
            should_return=True,
            extattrs=True
        )
        try:
            url = host_obj.json()[0]['_ref']
        except (IndexError, KeyError):
            print "Unable to find host by name"
            sys.exit(2)
        extattrs = {}
        try:
            extattrs['extattrs'] = host_obj.json()[0]['extattrs']
        except:
            extattrs['extattrs'] = {}

        extattrs['extattrs'][attr_name] = {"value": attr_value}
        ret_obj = self.make_request(
            url,
            'update',
            data=extattrs,
            hostname=self.hostname,
            auth=self.auth
        )
        try:
            if ret_obj.status_code == 200:
                print "Successfully set host extattr"
            else:
                print "Unable to create network extattr"
                print ret_obj.json()['text']
        except Exception, e:
            print "Unable to create network extattr"
            sys.exit(2)

    def search_by_record_name(self, name, should_return=False, extattrs=None, options=None):
        url = 'record:host?name=%s' % name
        if extattrs:
            url = '{}&_return_fields%2B=extattrs'.format(url)
        if options:
            url = '{}&_return_fields%2B=ipv4addrs.options'.format(url)
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

    def get(self,
            address=None,
            name=None,
            n_type="host:record",
            ipv6=False,
            extattrs=None,
            options=False
            ):
        ret = False
        if name and n_type == "host:record":
            ret = self.search_by_record_name(
                name,
                extattrs=extattrs,
                options=options
            )
        else:
            print name

    def delete_host(
        self,
        name,
        should_print=True
    ):
        ref = None
        del_obj = None

        del_obj = self.search_by_record_name(
            name,
            should_return=True,
            options=True
        )
        try:
            ref = del_obj.json()[0]['_ref']
        except (IndexError, KeyError):
            print "Unable to find host"
            return None
        if ref is not None:
            output = self.make_request(
                ref,
                'delete',
                hostname=self.hostname,
                auth=self.auth
            )
            if should_print is True:
                print "Host Successfully Deleted"
        else:
                print "Unable to find host"
