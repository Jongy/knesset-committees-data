import sys
import re
from typing import List
from datetime import date

import requests


def crawl(from_: date, to_: date) -> List[str]:
    """
    Returns the list of URLs to all available committee protocol files between the given 2 dates.
    """
    BASE_URL = "https://main.knesset.gov.il/Activity/committees/Pages/AllCommitteeProtocols.aspx?fDate={from_}&tDate={to_}"
    DATE_FMT = "%d/%m/%y"
    DOC_URL_RE = re.compile(r'<a href="([^"]+\.doc)"')

    while True:
        url = BASE_URL.format(from_=from_.strftime(DATE_FMT), to_=to_.strftime(DATE_FMT))
        r = requests.get(url)
        matches = DOC_URL_RE.findall(r.text)
        # TODO doesn't really work because the main response doesn't contain the data... the returned page runs
        # a few other requests later, and they do.
        print(matches)
        # TODO find last date, then query again with to_=that date.
        break


def parse_date(d: str) -> date:
    return date(*reversed(list(map(int, d.split('.')))))


if __name__ == "__main__":
    for url in crawl(parse_date(sys.argv[1]), parse_date(sys.argv[2])):
        print(url)
