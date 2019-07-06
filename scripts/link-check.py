import sys
import re
import json
import click

from requests_html import HTMLSession
from typing import Dict

session = HTMLSession()


def is_outbound_link(link: str) -> bool:
    return re.fullmatch("^https?://(.+)$", link) is not None


def check_link_health(link: str) -> Dict:
    response = session.head(link, allow_redirects=True)

    return {"url": link, "status": response.status_code}


@click.command()
@click.argument("url", type=str)
def main(url):
    response = session.get(url)

    outbound_links = filter(is_outbound_link, response.html.links)
    sanitized_links = map(check_link_health, outbound_links)

    sys.stdout.write(json.dumps(list(sanitized_links)))


if __name__ == "__main__":
    sys.exit(main())
