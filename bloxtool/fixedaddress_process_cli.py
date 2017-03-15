import json
import sys
from fixedaddress import FixedAddress

def fixedaddress_process_cli(config, auth, opt):
    if opt['--delimeter'] is None:
        delimeter = " "
    else:
        delimeter = opt['--delimeter']

    if opt['--format'] is None:
        o_format = "text"
    else:
        o_format = opt['--format']

    fa = FixedAddress(
        hostname=config.host,
        auth=auth,
        o_format=o_format,
        delimeter=delimeter
    )
    if opt['search'] is True:
        mac_address = opt['<mac_address>']
        if mac_address:
            fa.search_by_mac(mac_address)
        elif opt['<ipv4addr>']:
            fa.search_by_ipv4addr(
                opt['<ipv4addr>'],
            )
    elif opt['create'] is True:
        ipv4addr = opt['<ipv4addr>']
        mac = opt['<mac_address>']
        ipv4addr = opt['<ipv4addr>']
        name = opt['<name>']
        fa.create_fixed_address(
            name=name,
            ipv4addr=ipv4addr,
            mac=mac,
            should_print=True
        )
    elif opt['option'] is True:
        ipv4addr = opt['<ipv4addr>']
        option = opt['<option>']
        value = opt['<value>']
        if opt['--delete']:
            fa.delete_option(
                ipv4addr=ipv4addr,
                dhcp_option=option,
                dhcp_value='',
            )

        else:
            fa.create_option(
                ipv4addr=ipv4addr,
                dhcp_option=option,
                dhcp_value=value,
            )
    elif opt['delete'] is True:
        ipv4addr = opt['<ipv4addr>']
        mac = opt['<mac_address>']
        fa.delete_fixed_address(
            ipv4addr=ipv4addr,
            mac=mac,
            should_print=True
        )
