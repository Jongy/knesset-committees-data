import sys
from collections import defaultdict
from typing import Dict, List

import requests
import bs4

from utils import to_words


def parse_meeting_html(meeting_url: str) -> Dict[str, List[str]]:
    """
    Parses a Knesset committee protocol meeting page and returns a dictionary mapping speaker name
    to list of words they said.
    """
    words = defaultdict(list)

    r = requests.get(meeting_url)
    # https://stackoverflow.com/a/52615216/797390
    r.encoding = r.apparent_encoding  # let chardet choose the encoding
    b = bs4.BeautifulSoup(r.text, features="lxml")
    started = False
    for d in b.body.find_all("div", attrs={"class": "speech-container"}):
        speaker = d.find("div", attrs={"class": "text-speaker"}).text
        speaker = speaker.replace('¶', '').strip()  # remove crap

        # first few divs are actually "headers", like who participated in the meeting and stuff.
        # the headers end in this one
        if speaker == "רישום פרלמנטרי":
            started = True
            continue
        if not started:
            continue

        spoken = d.find("blockquote", attrs={"class": "entry-content"}).text.strip()
        words[speaker].extend(to_words(spoken))

    assert started, "parsing went badly, I guess"

    return words


if __name__ == "__main__":
    words = parse_meeting_html(sys.argv[1])
    for k, v in words.items():
        print("Speaker:", k)
        print("Words:", v)

    # import make_wordcloud
    # make_wordcloud.make_wordcloud(words[sys.argv[2]], f"{sys.argv[2]}.png")
