import sys
from collections import defaultdict
from typing import Dict, List, Optional

import docx

from utils import to_words


def parse_doc(filename: str) -> Dict[str, List[str]]:
    """
    Parses a Knesset committee protocol document (.doc file which is actually .docx format, it seems)
    and returns a dictionary mapping speaker name to list of words they said.
    """
    SPEAKER_MARKS = (
        ("דובר", "<< דובר >> ", ": << דובר >>"),
        ("יור", '<< יור >> היו"ר ', ": << יור >>"),
        # TODO: דובר-המשך
    )
    speaker: Optional[str] = None
    words = defaultdict(list)

    doc = docx.Document(filename)
    for p in doc.paragraphs:
        style = p.style.name
        t = p.text.strip()
        # paragraphs with style "Normal" are continuation.
        if style == "Normal":
            if speaker is not None:
                words[speaker].extend(to_words(t))
        else:
            speaker = None
            try:
                for mark in SPEAKER_MARKS:
                    if style == mark[0]:
                        assert t.startswith(mark[1]), f"unexpected start: {t!r}, expected {mark[1]!r} after it matched {mark[0]!r} style ({p.style})"
                        assert t.endswith(mark[2]), f"unexpected end: {t!r}, expected {mark[2]!r} after it matched {mark[0]!r} style ({p.style})"
                        speaker = p.text.strip()[len(mark[1]):-len(mark[2])]
                        break
            except AssertionError:
                # TODO sometimes asserts fail, fix it
                pass

    return words


if __name__ == "__main__":
    words = parse_doc(sys.argv[1])
    for k, v in words.items():
        print("Speaker:", k)
        print("Words:", v)

    import make_wordcloud
    make_wordcloud.make_wordcloud(words[sys.argv[2]], f"{sys.argv[2]}.png")
