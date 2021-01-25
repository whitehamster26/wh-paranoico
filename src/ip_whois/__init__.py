from ipwhois import IPWhois

from collections import namedtuple

from src.logger import logger

Net = namedtuple('Net', ['name',
                         'description',
                         'country',
                         'state',
                         'city',
                         'address',
                         'emails',
                         'created',
                         'updated',
                         'range'])


def _collect_info(ip_address: str) -> dict:
    try:
        ipwhois_object = IPWhois(ip_address)
        ip_info = ipwhois_object.lookup_whois()
        return ip_info
    except ValueError as e:
        logger.error(e)
        raise ValueError(f"Can't get info about given IP: {ip_address}.\n{e}")


def _get_nets(ip_address: str) -> list:
    ip_info = _collect_info(ip_address)
    nets = ip_info['nets']
    return nets


def net_info(net: dict) -> Net:
    # Perhaps it will be used if I make an interactive mode or analytics
    return Net(
               name=net['name'],
               description=net['description'],
               country=net['country'],
               state=net['state'],
               city=net['city'],
               address=net['address'],
               emails=net['emails'],
               created=net['created'],
               updated=net['updated'],
               range=net['range']
        )


def _parse_whois(nets: list) -> dict:
    """
    This method prepares the information for output to the report.
    It removes line breaks and duplicated data
    """
    parsed_info = {}
    for net in nets:
        for key, value in net.items():
            if value and '\n' in value:
                value = value.replace('\n', ' ')
            if key not in parsed_info.keys() and value:
                parsed_info[key] = [value]
            elif value:
                parsed_info[key].append(value)
    for key, value in parsed_info.items():
        # All values were stored as lists.
        # If there's only one value in list it stores it directly.
        if len(value) == 1:
            parsed_info[key] = value[0]
        else:
            # Removing duplicated data
            parsed_info[key] = list(set(value))
    return parsed_info


def show_whois(ip_address: str) -> dict:
    nets = _get_nets(ip_address)
    return _parse_whois(nets)
