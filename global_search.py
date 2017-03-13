from common import make_request
import json
import yaml
import sys
from basemixin import BaseMixin


class GlobalSearch(BaseMixin):

    def search(
        self,
        search_string,
        exact=False,
        objtype=None,
    ):
        exact_string = ""
        objtype_string = ""
        if exact is False:
            exact_string = "~"
        if objtype is not None:
            objtype_string = "&objtype={}".format(objtype)
            # Cannot use exact matching with objtype
            exact_string = "~"
        url = 'search?search_string{}={}{}'.format(
            exact_string,
            search_string,
            objtype_string
        )
        ret = self.make_request(
            url,
            'get',
            hostname=self.hostname,
            auth=self.auth
        )
        print self.get_output(ret, self.o_format, self.delimeter)
