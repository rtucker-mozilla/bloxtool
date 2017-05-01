from host import Host

def host_process_cli(config, auth, opt):
    if opt['--delimeter'] is None:
        delimeter = " "
    else:
        delimeter = opt['--delimeter']

    if opt['--format'] is None:
        o_format = "text"
    else:
        o_format = opt['--format']

    n = Host(
        hostname=config.host,
        auth=auth,
        o_format=o_format,
        delimeter=delimeter
    )

    if opt['list'] is True:
        n.list_hosts()
    elif opt['search'] is True:
        n.search(
            attribute=opt['<attribute>'],
            value=opt['<value>'],
            network=opt['<network>'],
            stype=opt['--type'],
            status=opt['--status'],
        )
    elif opt['get'] is True:
        try:
            name = opt['<name>']
        except KeyError:
            name = None

        try:
            address = opt['<address>']
        except KeyError:
            address = None

        try:
            extattrs = opt['--extattrs']
        except KeyError:
            extattrs = None

        n.get(
            address=address,
            name=name,
            extattrs=extattrs
        )
    elif opt['attr'] is True and opt['set']:
        hostname = opt['<hostname>']
        attr_name = opt['<option>']
        attr_value = opt['<value>']
        n.create_attr(hostname, attr_name, attr_value)

    elif opt['create'] is True:
        name = opt['<name>']
        ipv4addrs = opt['<ipv4addrs>']
        try:
            mac = opt['<mac_address>']
        except KeyError:
            mac=None
        try:
            network_block = opt['--network-block']
        except KeyError:
            network_block = False

        n.create_host(
            name,
            ipv4addrs,
            mac,
            network_block = network_block
        )
        if n.api_out.has_error:
            print "Unable to Create Host: %s" % network
            sys.exit(2)
        else:
            print "Host Created Successfully"
            n.get(name=name, n_type="record:host")
    if opt['delete'] is True:
        network = opt['<network>']
        if network is not None:
            ret = n.delete_network(
                network,
            )
            if ret is False:
                print "Unable to delete network"
