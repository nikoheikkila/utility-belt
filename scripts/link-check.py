"""
Checks a given URL for outbound links and their status.
Good for detecting broken links on a web page.

See link-check.py --help for usage.
"""

import sys
import re
import json
import click

from requests_html import HTMLSession
from typing import Dict

LinkStatus = Dict[str, str]


def is_outbound_link(link: str) -> bool:
    """
    Checks whether a link is outbound by checking the protocol.
    Returns 'True' if the link is outbound, otherwise 'False'.

    :param link:
    :return bool:
    """
    return re.fullmatch("^https?://(.+)$", link) is not None


def check_link_health(link: str) -> LinkStatus:
    """
    Maps the given link to a dictionary containing the link and its 'health'.
    This is executed using a HTTP/HEAD request following redirects.

    :param link:
    :return LinkStatus:
    """
    response = session.head(link, allow_redirects=True)

    return {"url": link, "status": response.status_code}


@click.command()
@click.argument("url", type=str)
def main(url: str) -> int:
    """
    Main function.

    :param url: URL as a command line argument
    :return int:
    """
    links = session.get(url).html.links

    outbound_links = filter(is_outbound_link, links)
    sanitized_links = map(check_link_health, outbound_links)

    sys.stdout.write(json.dumps(list(sanitized_links)))

    return 0


if __name__ == "__main__":
    session = HTMLSession()
    sys.exit(main())
