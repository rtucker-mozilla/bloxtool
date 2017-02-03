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
