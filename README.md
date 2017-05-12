# bloxtool
Command Line tools for interfacing with InfoBlox appliances

## Configuration File
~/.bloxtool.cfg

[InfoBlox]
host = https://localhost  
username = user@domain.com  
password = foo bar baz  
ssl_verify = true  

## Example Usage
### Host
bloxtool host get hostname *foo.domain.com*  
bloxtool host get hostname foo.domain.com --options --extattrs  # Returns the host's ipv4 DHCP options and InfoBlox extattrs  
bloxtool host create mac "" ipv4addrs 10.48.75.6 name foo.domain.com  
bloxtool host create mac "00:00:00:00:00:00" ipv4addrs nextavailableip name foo.domain.com  
### Host dhcp option
bloxtool host dhcpoption set host-name value different-foo.domain.com hostname foo.domain.com  
bloxtool host dhcpoption delete host-name hostname foo.domain.com  
