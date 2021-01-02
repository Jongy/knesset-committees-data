import sys
import re
from typing import List

import requests


def crawl(knesset: int) -> List[str]:
    """
    Returns the list of URLs to all available committee protocol files for the 'knesset'th Knesset, for example
    23 for the 23rd Knesset..
    Their API at https://oknesset.org/api/v2/ seems to be off, hence this stupid crawler
    """
    BASE_URL = "https://oknesset.org"
    COMMITTEES_RE = re.compile(r'href="(committees/\d+\.html)"')
    MEETINGS_RE = re.compile(r'href="(meetings/\d/\d/\d+\.html)"')

    committees = requests.get(f"{BASE_URL}/committees/knesset-{knesset}.html")
    assert committees.status_code == 200
    all_meetings = []
    for committee in COMMITTEES_RE.findall(committees.text):
        committee_url = f"{BASE_URL}/{committee}"
        print("querying committee", committee_url, file=sys.stderr)
        meetings = requests.get(committee_url)
        assert meetings.status_code == 200
        all_meetings.extend(MEETINGS_RE.findall(meetings.text))

    return all_meetings


if __name__ == "__main__":
    for url in crawl(int(sys.argv[1])):
        print(url)
