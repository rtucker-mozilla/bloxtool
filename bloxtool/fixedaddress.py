from basemixin import BaseMixin
import json
import sys


class FixedAddress(BaseMixin):

    def search_by_mac(self, mac_address, o_format=None, should_return=False):
        if o_format is None:
            o_format = self.o_format
        url = 'fixedaddress?mac=%s&_return_fields=mac,ipv4addr' % mac_address
        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        if should_return is True:
            return ret
        print(self.get_output(
            ret,
            o_format,
            self.delimeter,
            should_return=False
        ))

    def search_by_ipv4addr(self, ipv4addr, should_return=False, fields=[]):
        default_fields = "mac,ipv4addr"
        final_fields = ""
        if len(fields) > 0:
            tmp = ",".join(fields)
            final_fields="{default_fields},{tmp}".format(
                default_fields=default_fields,
                tmp=tmp
            )

        else:
            final_fields = default_fields

        url = 'fixedaddress?ipv4addr={ipv4addr}&_return_fields={fields}'.format(
            ipv4addr=ipv4addr,
            fields=final_fields
        )
        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        if should_return is True:
            return ret
        print(self.get_output(ret, self.o_format, self.delimeter))

    def create_option(
        self,
        ipv4addr=None,
        dhcp_option=None,
        dhcp_value=None
    ):
        net_obj = self.search_by_ipv4addr(ipv4addr, should_return=True)
        try:
            url = net_obj.json()[0]['_ref']
        except (IndexError, KeyError):
            print("Unable to find fixed address by ip")
            sys.exit(2)
        data = {}
        options = []
        options = [{
                'name': dhcp_option,
                'value': dhcp_value
            }]
        data['options'] = options
        ret_obj = self.make_request(
            url,
            'update',
            data=data,
            hostname=self.hostname,
            auth=self.auth
        )
        try:
            if ret_obj.status_code == 200:
                print("Successfully created dhcp option")
            else:
                print("Unable to create dhcp option")
                print(ret_obj.json()['text'])
        except Exception as e:
            print("Unable to create dhcp option")
            sys.exit(2)

    def delete_option(
        self,
        ipv4addr=None,
        dhcp_option=None,
        dhcp_value=None
    ):
        net_obj = self.search_by_ipv4addr(ipv4addr, should_return=True, fields=['options'])
        try:
            url = net_obj.json()[0]['_ref']
        except (IndexError, KeyError):
            print("Unable to find fixed address by ip")
            sys.exit(2)
        try:
            net_obj_options = net_obj.json()[0]['options']
        except (IndexError, KeyError):
            net_obj_options = []

        options = []
        for obj in net_obj_options:
            if not obj['name'] == dhcp_option\
                    and not obj['value'] == dhcp_value:
                options.append(obj)
        data = {}
        data['options'] = options
        ret_obj = self.make_request(
            url,
            'update',
            data=data,
            hostname=self.hostname,
            auth=self.auth
        )
        try:
            if ret_obj.status_code == 200:
                print("Successfully deleted dhcp option")
            else:
                print("Unable to delete dhcp option")
                print(ret_obj.json()['text'])
        except Exception as e:
            print("Unable to delete dhcp option")
            sys.exit(2)

    def create_fixed_address(
        self,
        name=None,
        ipv4addr=None,
        mac=None,
        should_print=False
    ):
        url = 'fixedaddress'
        data = {
            'ipv4addr': ipv4addr,
            'mac': mac,
            'name': name,
        }
        ret = self.make_request(
            url,
            'create',
            hostname=self.hostname,
            auth=self.auth,
            data=data
        )
        output = self.get_output(ret, self.o_format, self.delimeter)
        if should_print is True:
            print("Fixed Address Successfully Created")
            print("name: {name} mac: {mac} ipv4addr: {ipv4addr}".format(
                name=name,
                mac=mac,
                ipv4addr=ipv4addr
            ))

    def delete_fixed_address(
        self,
        ipv4addr,
        mac,
        should_print=True
    ):
        url = 'fixedaddress'
        ref = None
        del_obj = None
        if ipv4addr is not None:
            del_obj = self.search_by_ipv4addr(ipv4addr, should_return=True)
        elif mac is not None:
            del_obj = self.search_by_mac(
                mac,
                o_format="json",
                should_return=True
            )
        try:
            ref = del_obj.json()[0]['_ref']
        except (IndexError, KeyError):
            return None
        if ref is not None:
            output = self.make_request(
                url,
                'delete',
                hostname=self.hostname,
                auth=self.auth
            )
            if should_print is True:
                print("Fixed Address Successfully Deleted")
