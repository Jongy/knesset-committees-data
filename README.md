Crawl, parse and (possibly) extract interesting information from the Knesset committees protocols.

This is currently an attempt to produce a "word cloud" from all words said by a given speaker.
Not crawling yet - so data is based just on one committee protocol.

Usage (tested with `python:3.8` Docker):
```sh
$ wget https://fs.knesset.gov.il/23/Committees/23_ptv_593631.doc # sample URL for a committee protocol
$ python parse_doc.py 23_ptv_593631.doc "<speaker name>"
$ # will produce a <speaker name>.png wordcloud image.
```

TODOs:
* crawler
* parser fixes - not perfect and raises errors sometimes
* intermediate storage for parsed data (like a DB or so)
