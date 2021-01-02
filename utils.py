from typing import List


def to_words(text: str) -> List[str]:
    if text == "":
        return []
    filtered = filter(lambda w: w != "-", text.split(' '))
    return list(map(lambda w: w.strip('.'), filtered))
