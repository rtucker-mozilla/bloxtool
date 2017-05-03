import ConfigParser
import os


class ConfigObject(object):
    host = None
    username = None
    password = None
    ssl_verify = True

    def __init__(self, config_object, ini_section):
        try:
            self.host = config_object.get(ini_section, 'host')
        except:
            print 'host not in ini file'

        try:
            self.username = config_object.get(ini_section, 'username')
        except:
            print 'username not in ini file'

        try:
            self.password = config_object.get(ini_section, 'password')
        except:
            print 'password not in ini file'

        try:
            self.ssl_verify = config_object.get(ini_section, 'ssl_verify')
            if self.ssl_verify.upper() == 'FALSE':
                self.ssl_verify = False
        except:
            self.ssl_verify = True


def read_config_object(filepath):
    read_config = ConfigParser.RawConfigParser()
    read_config.read(filepath)
    return read_config


def get_config(filepath=None, ini_section='InfoBlox'):
    if not os.path.exists(filepath):
        return None

    if filepath is None:
        return None

    read_config = read_config_object(filepath)
    ret_object = ConfigObject(read_config, ini_section)
    return ret_object
