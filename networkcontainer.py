from common import make_request
from basemixin import BaseMixin
import sys


class NetworkContainer(BaseMixin):

    def get_networkcontainer(self, network):
        return self.search_by_ipv4addr(network)

    def search_by_ipv4addr(self, ipv4addr, should_return=False, attrs=None, network_url=False):
        if network_url is False:
            url_prefix = 'networkcontainer'
        else:
            url_prefix = 'network'
        if attrs is None:
            url = '%s?network=%s' % (url_prefix, ipv4addr)
        else:
            url = '%s?network=%s&_return_fields=%s' %\
                (url_prefix, ipv4addr, attrs)
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

    def create_option(self, network, option_name, option_value):
        net_obj = self.search_by_ipv4addr(network, should_return=True, network_url=True)
        import pdb; pdb.set_trace()
        try:
            url = net_obj.json()[0]['_ref']
        except (IndexError, KeyError):
            print "Unable to find fixed address by ip"
            sys.exit(2)
        data = {}
        existing_options = self.make_request(
            url + "?_return_fields=network",
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        import pdb; pdb.set_trace()
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
        except Exception, e:
            pass
        try:
            if ret_obj.status_code == 200:
                print "Successfully created network container option"
            else:
                import pdb; pdb.set_trace()
                print "Unable to create network container option"
                print ret_obj.json()['text']
        except Exception, e:
            print "Unable to create network container option"
            sys.exit(2)

    def list_networkcontainers(self):
        url = 'networkcontainer'
        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        print self.get_output(ret, self.o_format, self.delimeter)

    def search(self, name=None, site=None):
        if name is not None:
            self.search_by_name(name=name)
        elif site is not None:
            self.search_by_site(site=site)

    def delete_networkcontainer(self, network):
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
            print "Unable to delete network container: %s" % network
            return False

        if status_code == 200:
            print "Network Container Successfully Deleted: %s" % network
            return True
        else:
            print "Unable to delete network container: %s" % network
            return False

    def search_by_network_cidr(self, network):
        url = 'networkcontainer?network~=%s' % network
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

    def get(self, network):
        ret = self.search_by_network_cidr(
            network=network,
        )
        if ret is None:
            print "Unable to get NeworkContainer: {network}".format(
                network=network
            )
        else:
            print self.get_output(ret, self.o_format, self.delimeter)

    def delete_networkcontainer(self, network):
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
            print "Unable to delete network container: %s" % network
            return False

        if status_code == 200:
            print "Network Container Successfully Deleted: %s" % network
            return True
        else:
            print "Unable to delete network container: %s" % network
            return False

    def create_networkcontainer(
            self,
            network,
            comment="",
            should_print=False):
        url = "networkcontainer"
        data = {}
        data['network'] = network
        data['comment'] = comment
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
