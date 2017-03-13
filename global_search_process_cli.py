from global_search import GlobalSearch
def global_search_process_cli(config, auth, opt):
    if opt['--delimeter'] is None:
        delimeter = " "
    else:
        delimeter = opt['--delimeter']

    if opt['--format'] is None:
        o_format = "text"
    else:
        o_format = opt['--format']

    n = GlobalSearch(
        hostname=config.host,
        auth=auth,
        o_format=o_format,
        delimeter=delimeter
    )
    n.search(
        opt['<search_string>'],
        opt['--exact'],
        opt['--objtype'],
    )
