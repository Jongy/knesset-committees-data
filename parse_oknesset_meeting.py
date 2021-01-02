import os
import sys
from collections import defaultdict
from typing import Dict, List

import requests
import bs4

from utils import to_words


def parse_meeting_html(meeting_url_or_file: str, words: Dict[str, List[str]] = None) -> Dict[str, List[str]]:
    """
    Parses a Knesset committee protocol meeting page and returns a dictionary mapping speaker name
    to list of words they said.
    """
    if words is None:
        words = defaultdict(list)

    if os.path.isfile(meeting_url_or_file):
        text = open(meeting_url_or_file, "r").read()
    else:
        r = requests.get(meeting_url_or_file)
        # https://stackoverflow.com/a/52615216/797390
        r.encoding = r.apparent_encoding  # let chardet choose the encoding
        text = r.text

    # meeting file with no protocol :/
    if "מצטערים! אין לנו את הפרוטוקול." in text:
        return words

    b = bs4.BeautifulSoup(text, features="lxml")
    started = False
    for d in b.body.find_all("div", attrs={"class": "speech-container"}):
        speaker = d.find("div", attrs={"class": "text-speaker"}).text
        speaker = speaker.replace('¶', '').replace('היו"ר', "").strip()  # remove crap

        # first few divs are actually "headers", like who participated in the meeting and stuff.
        # the headers end in this one
        # they're not very consistent with this field title, it seems.
        if speaker in ("רישום פרלמנטרי", "רשמת פרלמנטרית", "קצרנית פרלמנטרית", "רישום פרלמנט"):
            started = True
            continue
        if not started:
            continue

        spoken = d.find("blockquote", attrs={"class": "entry-content"}).text.strip()
        words[speaker].extend(to_words(spoken))

    assert started, f"parsing went badly, I guess - {meeting_url_or_file!r}"

    return words


if __name__ == "__main__":
    path = sys.argv[1]
    if os.path.isdir(path):
        # parse all files in the directory into one dict
        words = defaultdict(list)
        files = os.listdir(path)
        for i, f in enumerate(files):
            print(f"{i}/{len(files)}")
            parse_meeting_html(os.path.join(path, f), words)

        output = os.path.abspath(path) + "_all.json"
        print("Dumping to..", output)
        import json
        json.dump(words, open(output, "w"))
        print("Done.")
    else:
        # just print this one for debugging
        words = parse_meeting_html(path)
        for k, v in words.items():
            print("Speaker:", k)
            print("Words:", v)
