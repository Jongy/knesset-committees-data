from typing import List

from wordcloud import WordCloud


def make_wordcloud(words: List[str], filename: str) -> None:
    # reverse all words, because wordcloud doesn't handle rtl
    words = list(map(lambda w: w[::-1], words))
    font_path = "NotoSansHebrew-Regular.ttf"  # copied from /usr/share/fonts
    wordcloud = WordCloud(font_path=font_path, width=2000, height=2000, background_color='white',
                          collocations=False).generate(' '.join(words))
    wordcloud.to_file(filename)
