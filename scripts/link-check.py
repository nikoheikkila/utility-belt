import sys
import re
import json
import click
import meta

from requests import Response
from requests.exceptions import ConnectionError
from requests_html import HTMLSession
from typing import Tuple

LinkStatus = Tuple[str, int]

headers = {"User-Agent": meta.get_repo(), "X-Version": meta.get_version()}


def is_valid_url(link: str, pattern: str = "^https?://(.+)$") -> bool:
    """
    Checks whether a link is valid URL against regex.
    Returns 'True' if the link is valid, otherwise 'False'.

    :param link:    Link to validate
    :param pattern: Pattern to check URLs against (optional)
    :return bool:
    """
    return re.fullmatch(pattern, link) is not None


def check_link_health(link: str) -> LinkStatus:
    """
    Maps the given link to a tuple containing the link and its 'health'.
    This is executed using a HTTP/HEAD request following redirects.

    :param link:
    :return LinkStatus:
    """
    response = session.head(link, allow_redirects=True, headers=headers)

    return (link, response.status_code)


@click.command()
@click.argument("url", type=str)
@click.option("--limit", type=int, default=50, help="Maximum amount of links to check (default: 50)")
def main(url: str, limit: int) -> int:
    """
    Checks a given URL for outbound links and their status.
    Good for detecting and fixing broken links on a web page.

    May return false-positives since some websites may block incoming
    HEAD requests.
    """
    if not is_valid_url(url):
        print(f"{url} is not a valid URL")
        return 1

    try:
        response = session.get(url, headers=headers)
    except ConnectionError:
        print(f"Unable to GET {url}")
        return 1

    links = response.html.links

    if not links:
        print(f"Source of {url} does not contain any links")
        return 1

    outbound_links = [l for l in links if is_valid_url(l)]

    if len(outbound_links) > limit:
        outbound_links = outbound_links[:limit]

    accepted = lambda status: status in range(200, 299)

    for l in outbound_links:
        link, status = check_link_health(l)
        mark = "✔️" if accepted(status) else "❌"
        print(f"{link} {mark}  (status: {status})")

    return 0


if __name__ == "__main__":
    session = HTMLSession()
    sys.exit(main())
