from common import make_request
import json
import yaml
import sys
from apioutput import APIOutput
from basemixin import BaseMixin


class Network(BaseMixin):

    def get_network(self, network):
        return self.search_by_ipv4addr(network)

    def search_by_ipv4addr(self, ipv4addr, should_return=False, attrs=None):
        if attrs is None:
            url = 'network?network=%s' % ipv4addr
        else:
            url = 'network?network=%s&_return_fields=%s' % (ipv4addr, attrs)
        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        if should_return:
            return ret
        else:
            print(self.get_output(ret, self.o_format, self.delimeter))


    def list_networks(self, include_extattrs=False, ipv6=False):
        url = 'network'
        if include_extattrs:
            url = 'network' + '?_return_fields=extattrs'
        if ipv6:
            url = "ipv6" + url
        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        print(self.get_output(ret, self.o_format, self.delimeter))

    def create_zoneassociation(self, zone, view, network):
        net_obj = self.search_by_ipv4addr(network, should_return=True)
        try:
            url = net_obj.json()[0]['_ref']
        except (IndexError, KeyError):
            print("Unable to find fixed address by ip")
            sys.exit(2)
        zone_associations = self.make_request(
            url + "?_return_fields=zone_associations",
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        try:
            l_zone_associations = zone_associations.json()['zone_associations']
        except (IndexError, KeyError):
            l_zone_associations = []

        l_zone_associations.append({
            'fqdn': zone,
            'view': view,
        })

        data = {}
        data['zone_associations'] = l_zone_associations

        try:
            ret_obj = self.make_request(
                url,
                'update',
                data=data,
                hostname=self.hostname,
                auth=self.auth
            )
        except Exception as e:
            pass

        try:
            if ret_obj.status_code == 200:
                print("Successfully created zone association")
            else:
                print("Unable to create zone association")
                print(ret_obj.json()['text'])
        except Exception as e:
            print("Unable to create zone association")
            sys.exit(2)
        pass

    def create_option(self, network, option_name, option_value):
        net_obj = self.search_by_ipv4addr(network, should_return=True)
        try:
            url = net_obj.json()[0]['_ref']
        except (IndexError, KeyError):
            print("Unable to find fixed address by ip")
            sys.exit(2)
        data = {}
        existing_options = self.make_request(
            url + "?_return_fields=options",
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        try:
            options = existing_options.json()['options']
        except (AttributeError, KeyError):
            options = []
        options.append({
                'name': option_name,
                'value': option_value
            })
        data['options'] = options
        try:
            ret_obj = self.make_request(
                url,
                'update',
                data=data,
                hostname=self.hostname,
                auth=self.auth
            )
        except Exception as e:
            pass
        try:
            if ret_obj.status_code == 200:
                print("Successfully created network option")
            else:
                print("Unable to create network option")
                print(ret_obj.json()['text'])
        except Exception as e:
            print("Unable to create network option")
            sys.exit(2)

    def create_attr(self, network, attr_name, attr_value):
        net_obj = self.search_by_ipv4addr(
            network,
            should_return=True,
            attrs="extattrs"
        )
        try:
            url = net_obj.json()[0]['_ref']
        except (IndexError, KeyError):
            print("Unable to find fixed address by ip")
            sys.exit(2)
        extattrs = {}
        try:
            extattrs['extattrs'] = net_obj.json()[0]['extattrs']
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
                print("Successfully created network extattr")
            else:
                print("Unable to create network extattr")
                print(ret_obj.json()['text'])
        except Exception as e:
            print("Unable to create network extattr")
            sys.exit(2)
    def add_option(self, network, option_name, option_value):
        url = 'network?comment~:=%s' % name
        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        print(self.get_output(ret, self.o_format, self.delimeter))

    def search_by_name(self, name, ipv6=False):
        url = 'network?comment~:=%s' % name
        if ipv6 is True:
            url = 'ipv6network?comment~:=%s' % name

        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        print(self.get_output(ret, self.o_format, self.delimeter))

    def search_by_attribute_value(self, attribute, value, network=None, ipv6=False):
        network_string = ""
        if network:
            network_string = "network=%s&" % network

        url = 'network?%s*%s~:=%s' % (network_string, attribute, value)
        if ipv6 is True:
            url = "ipv6%s" % url
        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        print(self.get_output(ret, self.o_format, self.delimeter))

    def search_by_site(self, site, ipv6=False):
        url = 'network?*Site~:=%s' % site
        if ipv6 is True:
            url = 'ipv6network?*Site~:=%s' % site
        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        print(self.get_output(ret, self.o_format, self.delimeter))

    def search(self, name=None, site=None, attribute=None, value=None, network=None, ipv6=False):
        if name is not None:
            self.search_by_name(name=name, ipv6=ipv6)
        elif site is not None:
            self.search_by_site(site=site, ipv6=ipv6)
        elif attribute and value:
            self.search_by_attribute_value(attribute, value, network, ipv6=ipv6)

    def search_by_network_cidr(self, network, ipv6=False):
        url = 'network?network~=%s' % network
        if ipv6 is True:
            url = 'ipv6network?network~=%s' % network
        network_obj = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        try:
            ref = network_obj.json()[0]['_ref']
        except (IndexError, KeyError):
            return None
        return self.make_request(
            ref,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )

    def get(self, network, ipv6=False):
        ret = self.search_by_network_cidr(
            network=network,
            ipv6=ipv6
        )
        if ret is None:
            print("Unable to get Nework: {network}".format(
                network=network
            ))
        else:
            print(self.get_output(ret, self.o_format, self.delimeter))

    def fixedaddresses(self, network):
        url = 'fixedaddress?network~=%s' % network
        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        try:
            found_records_len = len(ret.json())
        except:
            found_records_len = 0
        if len(ret.json()) == 0:
            print('No Networks Found')
        print(self.get_output(ret, self.o_format, self.delimeter))

    def delete_network(self, network, ipv6=False):
        try:
            network_req = self.search_by_network_cidr(
                network=network,
            )
            network_ref = network_req.json()['_ref']
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
            print("Unable to delete network: %s" % network)
            return False

        if status_code == 200:
            print("Network Successfully Deleted: %s" % network)
            return True
        else:
            print("Unable to delete network: %s" % network)
            return False
    def create_range(
            self,
            name,
            start,
            end,
            disable=True,
            should_print=True):
        url = "range"
        data = {}
        data['name'] = name
        data['start_addr'] = start
        data['end_addr'] = end
        data['disable'] = disable
        ret = make_request(
            url,
            'create',
            data=data,
            hostname=self.hostname,
            auth=self.auth
        )
        output = self.get_output(ret, self.o_format, self.delimeter)
        # TODO: Print the object after a get range
        # Really should refactor this into it's own module
        if should_print is True:
            print(output)

    def create_network(
            self,
            network,
            comment="",
            disable=False,
            members=[],
            should_print=False):
        url = "network"
        data = {}
        data['network'] = network
        data['comment'] = comment
        data['disable'] = disable
        data['members'] = members
        ret = make_request(
            url,
            'create',
            data=data,
            hostname=self.hostname,
            auth=self.auth
        )
        output = self.get_output(ret, self.o_format, self.delimeter)
        if should_print is True:
            print(output)
