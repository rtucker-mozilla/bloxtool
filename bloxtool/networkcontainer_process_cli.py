from networkcontainer import NetworkContainer
import sys


def networkcontainer_process_cli(config, auth, opt):
    if opt['--delimeter'] is None:
        delimeter = " "
    else:
        delimeter = opt['--delimeter']

    if opt['--format'] is None:
        o_format = "text"
    else:
        o_format = opt['--format']

    n = NetworkContainer(
        hostname=config.host,
        auth=auth,
        o_format=o_format,
        delimeter=delimeter
    )

    if opt['create'] is True and not opt['option']:
        network = opt['<network>']
        name = opt['<name>']
        disable = opt['--disable']

        if disable is None:
            disable = True

        if isinstance(disable, str):
            if disable.upper() == 'TRUE':
                disable = True
            elif disable.upper() == 'FALSE':
                disable = False
        try:
            members = opt['--members'].split(',')
        except AttributeError:
            members = []
        n.create_networkcontainer(
            network,
            name
        )
        if n.api_out.has_error:
            print("Unable to Create Network Container: %s" % network)
            sys.exit(2)
        else:
            print("Network Container Created Successfully")
            n.get(network)
    elif opt['option'] is True and opt['create']:
        print('in option')
        network_block = opt['<network_block>']
        option_name = opt['<option>']
        option_value = opt['<value>']
        if '\-' in option_value:
            option_value = option_value.replace('\-', '-')
        n.create_option(network_block, option_name, option_value)

    elif opt['delete'] is True:
        network = opt['<network>']
        if network is not None:
            ret = n.delete_networkcontainer(
                network,
            )
            if ret is False:
                print("Unable to delete network container")
