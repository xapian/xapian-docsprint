import re
import BeautifulSoup
import time
import eventlet
from eventlet.green import urllib2
import csv
import sys

def pull(title):
    """pull all the infobox goodies from wikipedia"""
    url = "http://en.wikipedia.org/w/index.php?action=render&title=%s" % title
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (user-agent-restrictions-are-silly)')]
    try:
        html = opener.open(url.encode("utf-8")).read()
    except:
        print (u"  Could not fetch %s" % url).encode('utf-8')
        return None
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
    except:
        print (u"  Could not parse %s" % url).encode('utf-8')
        return None
    # Extract information
    infobox = soup.find("table", { 'class': re.compile(r'\binfobox\b') })
    if not infobox:
        print (u"  No infobox found in %s" % url).encode('utf-8')
        return None

    information = {}
    name = infobox.find("th", { 'class': 'fn org' })
    if name:
        information['name'] = extract_text(name)

    def grab(info, name=None):
        if name is None:
            name = info
        text = infobox.find("text", text=info)
        if text:
            information[name] = extract_text(text.parent.findNext("td"))

    grab("Capital")
    grab("Admission to Union", "Admitted")
    pop = infobox.find("text", text="Population")
    if pop:
        text = pop.findNext("text", text=re.compile("Total$"))
        if text:
            information['Population'] = extract_text(text.parent.findNext("td"))
    grab(re.compile("Latitude$"), "Latitude")
    grab(re.compile("Longitude$"), "Longitude")
    text = infobox.find("text", text=re.compile("Motto"))
    if text:
        information["Motto"] = extract_text(text.findNext("i"))
    information["Description"] = extract_text(infobox.findNext("p"))

    return information

def extract_text(tag):
    if isinstance(tag, BeautifulSoup.NavigableString):
        return tag.string
    elif tag is None:
        return ""
    else:
        return " ".join(" ".join([extract_text(item) for item in tag.contents]).split()).replace("( ", "(").replace(" )", ")").replace(" :", ":")


pool = eventlet.GreenPool(size=10)
results = pool.imap(
    pull,
    sys.stdin.readlines(),
    )
with open("data/states.csv", "w") as fh:
    w = csv.writer(fh, dialect='excel')
    w.writerow(
        [
            'name',
            'capital',
            'admitted',
            'population',
            'latitude',
            'longitude',
            'motto',
            'description',
            ]
        )
    for result in results:
        if result is None:
            continue
        w.writerow(
            map(
                lambda x: x.encode('utf-8'),
                [
                    result.get("Name", u""),
                    result.get("Capital", u""),
                    result.get("Admitted", u""),
                    result.get("Population", u""),
                    result.get("Latitude", u""),
                    result.get("Longitude", u""),
                    result.get("Motto", u""),
                    result.get("Description", u""),
                    ]
                )
            )
