import json
import yaml
import sys


class APIOutput(object):
    allowed_o_format = [
        'json',
        'text',
        'yaml',
    ]

    # List of fields to rename in output
    default_translation_map = {
        '_ref': 'ref'
    }

    def __init__(
        self,
        resp,
        o_format='text',
        delimeter=" ",
        translation_map=None,
        fields=None
    ):
        self.has_error = False
        self.error_message = ""
        if translation_map is None:
            translation_map = self.default_translation_map
        if resp is None:
            self.has_error = True
            self.error_message = "Resp is empty"
            return None
        self.resp = resp
        if resp.status_code == 401:
            print "Invalid Credentials"
            sys.exit(2)
        self.api_data = resp.json()
        self.o_format = o_format
        self.delimeter = delimeter
        self.translation_map = translation_map
        self.fields = fields
        self.formatted_text = ""
        if self.o_format is None:
            self.o_format = 'text'
        self.good_format, self.error = self._check_format(self.o_format)
        if self.good_format is False:
            return

    def format_text(self, api_data=None):
        if api_data is None:
            api_data = self.api_data
        formatted_text = self._get_formatted_text(
            self.o_format,
            api_data,
            self.delimeter
        )
        self.formatted_text = formatted_text
        return self.formatted_text

    def _translate_key(self, k):
        try:
            return self.translation_map[k]
        except KeyError:
            return k

    def process_resp(self, i_resp=None):
        has_error = False
        error_text = ""
        if i_resp is not None:
            resp = i_resp
        else:
            try:
                resp = self.resp
            except AttributeError:
                return None, None
        if resp is None:
            return None, None
        if str(resp.status_code).startswith('4'):
            error_text = resp.json()['text']
            self.error = error_text
            has_error = True
        return has_error, error_text

    def _build_string(self, entry, delimeter):
        i_str = ""
        if self.fields is not None:
            f_keys = self.fields
        else:
            try:
                f_keys = entry.keys()
            except AttributeError:
                return entry
        key_counter = 1
        for k in f_keys:
            v = entry[k]
            if k == "extattrs":
                for extattr in entry[k]:
                    i_str += "{key}: {value}{delimeter}".format(
                        key=extattr,
                        value=entry[k][extattr]['value'],
                        delimeter=delimeter
                    )
            else:
                translated_key = self._translate_key(k)
                i_str += "{key}: {value}{delimeter}".format(
                    key=translated_key,
                    value=v,
                    delimeter=delimeter
                )
        i_str = i_str.rstrip(delimeter)
        if len(i_str) > 0:
            i_str += "\n"
        return i_str

    def _format_list(self, api_data, delimeter=" "):
        i_str = ""
        for entry in api_data:
            i_str += self._build_string(entry, delimeter)
        return i_str

    def _format_string(self, api_data, delimeter):
        i_str = self._build_string(api_data, delimeter)
        return i_str

    def _get_formatted_text(self, o_format, api_data, delimeter):
        formatted_text = ""
        if o_format == 'text':
            if isinstance(api_data, list):
                formatted_text = self._format_list(api_data, delimeter)
            else:
                formatted_text = self._format_string(api_data, delimeter)
        elif o_format != 'text':
            if o_format == 'json':
                formatted_text = json.dumps(api_data, indent=4)
            elif o_format == 'yaml':
                formatted_text = yaml.safe_dump(
                    api_data,
                    default_flow_style=False
                )
        return formatted_text

    def _check_format(self, o_format):
        good_format = o_format in self.allowed_o_format
        error = None
        if good_format is False:
            error = "Unknown Output Format"
        return good_format, error
