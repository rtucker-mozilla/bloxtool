from network import Network


def network_process_cli(config, auth, opt):
    if opt['--delimeter'] is None:
        delimeter = " "
    else:
        delimeter = opt['--delimeter']

    if opt['-6'] is False:
        ipv6 = None
    else:
        ipv6 = True

    if opt['--format'] is None:
        o_format = "text"
    else:
        o_format = opt['--format']

    n = Network(
        hostname=config.host,
        auth=auth,
        o_format=o_format,
        delimeter=delimeter,
        ipv6=ipv6
    )

    if opt['list'] is True:
        n.list_networks(
            include_extattrs=opt['--extattrs'],
            ipv6=ipv6
        )
    elif opt['search'] is True:
        if opt['--network']:
            opt_network = opt['--network']
        else:
            opt_network = None
        n.search(
            name=opt['<name>'],
            site=opt['<site>'],
            attribute=opt['<attribute>'],
            value=opt['<value>'],
            network=opt_network,
            ipv6=ipv6
        )
    elif opt['get'] is True:
        network = opt['<network>']
        n.get(network, ipv6=ipv6)
    elif opt['fixedaddresses'] is True:
        network = opt['<network>']
        n.fixedaddresses(network)
    elif opt['option'] is True and opt['create']:
        network_block = opt['<network_block>']
        option_name = opt['<option>']
        option_value = opt['<value>']
        if '\-' in option_value:
            option_value = option_value.replace('\-', '-')
        n.create_option(network_block, option_name, option_value)
    elif opt['attr'] is True and opt['create']:
        network_block = opt['<network_block>']
        attr_name = opt['<option>']
        attr_value = opt['<value>']
        n.create_attr(network_block, attr_name, attr_value)

    elif opt['create'] is True:
        if not opt['range']:
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
            n.create_network(
                network,
                name,
                disable=disable,
                members=members,
            )
            if n.api_out.has_error:
                print "Unable to Create Network: %s" % network
                sys.exit(2)
            else:
                print "Network Created Successfully"
                n.get(network)
        elif opt['range'] is True:
            start = opt['<start>']
            end = opt['<end>']
            name = opt['<name>']
            comment = opt['--comment']
            disable = opt['--disable']

            if disable is None:
                disable = True

            # Make a method out of this
            # def parse_disable
            if isinstance(disable, str):
                if disable.upper() == 'TRUE':
                    disable = True
                elif disable.upper() == 'FALSE':
                    disable = False
            n.create_range(
                name,
                start,
                end,
                disable=disable,
            )

    if opt['delete'] is True:
        network = opt['<network>']
        if network is not None:
            ret = n.delete_network(
                network,
            )
            if ret is False:
                print "Unable to delete network"
