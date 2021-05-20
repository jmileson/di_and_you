from collections import namedtuple
from typing import List

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

Row = namedtuple("Row", ["name", "spectral_range", "bands", "cba_factor"])

URL = "https://www.indexdatabase.de/db/i-single.php?id=63"


def parse_formula(td: Tag) -> float:
    """Parse the formula to find the canopy background adjustment factor."""
    return float(td.find_all("mn")[-1].text.strip())


def parse_row(tr: Tag) -> Row:
    """Parse a table row into a Row."""
    tds = tr.find_all("td")
    cols = [td.text.strip() for td in tds]
    return Row(*cols[1:4], parse_formula(tds[4]))


def load_csv_v1() -> List[Row]:
    # TODO requests is a dependency, I should inject this
    # TODO URL is also a dependency, maybe?
    data = requests.get(URL)

    # TODO should I inject this?
    soup = BeautifulSoup(data.content, features="html.parser")

    table = soup.find("table", class_="matrix")
    if not table:
        return []

    # drop the header
    return [parse_row(tr) for tr in table.find_all("tr")[1:]]


def load_csv_v2(url: str, session: requests.Session = None) -> List[Row]:  # noqa
    # allow ourselves the option to make a session outside the functon
    # useful for testing, but maybe some loaders have specific requirements
    # e.g. for retries or auth
    if session is None:
        session = requests.Session()
    data = session.get(url)

    # I'm not injecting this, there's no good reason to at the moment
    # since it doesn't cross any boundaries in my application (network, io)
    # nor do I need to support IoC (at the moment any way)
    soup = BeautifulSoup(data.content, features="html.parser")

    table = soup.find("table", class_="matrix")

    # drop the header
    return [parse_row(tr) for tr in table.find_all("tr")[1:]]
