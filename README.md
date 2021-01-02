Crawl, parse and (possibly) extract interesting information from the Knesset committees protocols.

*Note: this is the result of just a couple of hours of work, I **know** it has some errors in parsing, do not take
it too seriously until parsing is proven fully correct.*

This is currently an attempt to produce a "word cloud" from all words said by a given speaker.

Usage (tested with `python:3.8` Docker):
```sh
$ python crawler_openknesset.py 23 > 23.txt  # URLs for all committee meeting protocols of the 23rd Knesset
$ mkdir 23
$ # downloads all URLs, synchronously & with some cooldown between wgets, so we don't kill their server...
$ cd mkdir && for x in $(cat ../23.txt); do if ! ls | grep $(basename $x) > /dev/null ; then wget https://oknesset.org/$x; sleep 0.5; fi; done; cd ..
$ # now we have all meetings htmls in 23/
$ # aggregate them all into a single json
$ python parse_oknesset_meeting.py 23
$ # output is at 23_all.json
$ # now, we can investigate the result in IPython, or make a wordcloud from it
$ python make_wordcloud.py 23_all.json "ראש הממשלה בנימין נתניהו"
$ # now you got a "ראש הממשלה בנימין נתניהו.png" file
```

### Crawlers
```sh
$ python crawler_openknesset.py <Knesset ordinal>
```

### Parsers
```sh
$ python parse_oknesset_meeting.py <dir with htmls, single html file or single URL>
```

### TODOs
* After I downloaded some files and merged them into a JSON, I looked at the list of keys, and while most are indeed
names, some are just broken parts of sentences, which indicate the parsing is wrong. Need to figure that out. For example,
the sentence "אני מעמיד זאת להצבעה" was parsed as a speaker name somehow.
* Some names appear with multiple titles; for example, ministers are sometimes without their "שר ה ..." title, and sometimes
with it. Need to merge those multiple different "speakers" into one.
