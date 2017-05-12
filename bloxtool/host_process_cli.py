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

        try:
            options = opt['--options']
        except KeyError:
            options = None

        n.get(
            address=address,
            name=name,
            extattrs=extattrs,
            options=options
        )
    elif opt['attr'] is True and opt['set']:
        hostname = opt['<hostname>']
        attr_name = opt['<option>']
        attr_value = opt['<value>']
        n.create_attr(hostname, attr_name, attr_value)

    elif opt['attr'] is True and opt['delete']:
        hostname = opt['<hostname>']
        attr_name = opt['<option>']
        n.delete_attr(hostname, attr_name)

    elif opt['dhcpoption'] is True and opt['set']:
        hostname = opt['<hostname>']
        option_name = opt['<option>']
        option_value = opt['<value>']
        n.set_dhcpoption(hostname, option_name, option_value)

    elif opt['dhcpoption'] is True and opt['delete']:
        hostname = opt['<hostname>']
        attr_name = opt['<option>']
        n.delete_dhcpoption(hostname, attr_name)

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
    if opt['delete'] is True and not opt['dhcpoption']:
        hostname = opt['<hostname>']
        if hostname is not None:
            ret = n.delete_host(
                hostname,
            )
            if ret is False:
                print "Unable to delete host"
