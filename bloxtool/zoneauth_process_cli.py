from zoneauth import ZoneAuth
import sys


def zoneauth_process_cli(config, auth, opt):
    if opt['--delimeter'] is None:
        delimeter = " "
    else:
        delimeter = opt['--delimeter']

    if opt['-6'] is None:
        ipv6 = False
    elif opt['-6'] is False:
        ipv6 = False
    else:
        ipv6 = True

    if opt['--format'] is None:
        o_format = "text"
    else:
        o_format = opt['--format']

    z = ZoneAuth(
        hostname=config.host,
        auth=auth,
        o_format=o_format,
        delimeter=delimeter,
        ipv6=ipv6
    )


    if opt['create'] is True:
        zone = opt['<zone>']
        view = opt['<view>']
        grid_primary = opt['--grid-primary']
        ns_group = opt['--ns-group']
        if grid_primary is None and ns_group is None:
            print "--ns-group or --grid-primary is required"
            sys.exit(2)
        z.create_zoneauth(
            zone,
            view,
            ns_group = ns_group,
            grid_primary = grid_primary
        )

    if opt['delete'] is True:
        zone = opt['<zone>']
        view = opt['<view>']
        z.delete_zoneauth(
            zone,
            view
        )
