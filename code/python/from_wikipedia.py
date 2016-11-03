import re
import BeautifulSoup
from datetime import date, datetime
import time
import eventlet
from eventlet.green import urllib2
import csv
import sys

def middle_coord(text):
    """Get the middle coordinate from a coordinate range.

    The input is in the form <start> to <end> with both extents being in
    degrees and minutes as N/S/W/E. S and W thus need to be negated as we only
    care about N/E.

    """
    def numbers_from_string(s):
        """Find all numbers in a string."""
        return [float(n) for n in re.findall(r'[\d.]*\d[\d.]*', s)]


    def tuple_to_float(numbers):
        divisor = 1
        result = 0
        for num in numbers:
            result += float(num) / divisor
            divisor = divisor * 60
        return result

    if text is None:
        return None
    pieces = text.split(' to ', 1)
    start, end = map(numbers_from_string, pieces)
    start = tuple_to_float(start)
    end = tuple_to_float(end)
    if pieces[0][-1] in ('S', 'W'):
        start = -start
    if pieces[1][-1] in ('S', 'W'):
        end = -end
    return (start + end) / 2


def pull(title):
    """pull all the infobox goodies from wikipedia"""
    # Use cached copy if there is one, otherwise fetch and then cache.
    try:
        cache = open("data/%s.html" % title, "r")
        html = cache.read()
    except:
        url = "http://en.wikipedia.org/w/index.php?action=render&title=%s" % title
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (user-agent-restrictions-are-silly)')]
        try:
            html = opener.open(url.encode("utf-8")).read()
        except:
            print((u"  Could not fetch %s" % url).encode('utf-8'))
            return None
        cache = open("data/%s.html" % title, "w")
        cache.write(html)
        cache.close()

    try:
        soup = BeautifulSoup.BeautifulSoup(html)
    except:
        print((u"  Could not parse %s" % title).encode('utf-8'))
        return None

    # Extract information
    infobox = soup.find("table", { 'class': re.compile(r'\binfobox\b') })
    if not infobox:
        print((u"  No infobox found in %s" % title).encode('utf-8'))
        return None

    information = {}
    name = infobox.find("th", { 'class': 'fn org' })
    if name:
        information['name'] = extract_text(name)

    def grab(info, name=None):
        if name is None:
            name = info.lower()
        text = infobox.find("text", text=info)
        if text:
            information[name] = extract_text(text.parent.findNext("td"))

    grab("Capital")
    text = infobox.find("text", text="Admission to Union")
    if text:
        admitted = extract_text(text.parent.findNext("td"))
        # Split "Date (order)" into two fields.
        pieces = admitted.split(' (', 1)
        # Remove any citation like ' [9]'.
        admitted = re.sub(r'\s*\[\d+\]$', '', pieces[0])
        try:
            admitted = datetime.strptime(admitted, "%B %d, %Y")
            information['admitted'] = \
                "%04d%02d%02d" % (admitted.year, admitted.month, admitted.day)
        except ValueError:
            print("couldn't parse admitted '%s'" % admitted)
        order = pieces[1][:-1]
        if any(x in order for x in ('st', 'nd', 'rd', 'th')):
            order = order[:-2]
        information['order'] = order

    pop = infobox.find("text", text="Population")
    if pop:
        text = pop.findNext("text", text=re.compile("Total$"))
        if text:
            population = extract_text(text.parent.findNext("td"))
            # Population-comma-formatted (comment) extra
            pieces = population.split('(', 1)
            population = pieces[0].replace(',', '').strip()
            try:
                information['population'] = population
            except ValueError:
                pass

    grab(re.compile("Latitude$"), "latitude")
    grab(re.compile("Longitude$"), "longitude")
    text = infobox.find("text", text=re.compile("Motto"))
    if text:
        information["motto"] = extract_text(text.findNext("i"))
    information["description"] = extract_text(infobox.findNext("p"))

    information["midlat"] = str(middle_coord(information.get("latitude", None)))
    information["midlon"] = str(middle_coord(information.get("longitude", None)))

    return information

def extract_text(tag):
    if isinstance(tag, BeautifulSoup.NavigableString):
        return tag.string
    elif tag is None:
        return ""
    else:
        return " ".join(" ".join([extract_text(item) for item in tag.contents]).split()).replace("( ", "(").replace(" )", ")").replace(" :", ":")


columns = [
    'name',
    'capital',
    'admitted',
    'order',
    'population',
    'latitude',
    'longitude',
    'motto',
    'description',
    'midlat',
    'midlon',
    ]
pool = eventlet.GreenPool(size=10)
results = pool.imap(
    pull,
    [line.rstrip() for line in sys.stdin.readlines()],
    )
with open("data/states.csv", "w") as fh:
    w = csv.writer(fh, dialect='excel')
    w.writerow(columns)
    for result in results:
        if result is None:
            continue
        w.writerow([ result.get(col, u"").encode('utf-8') for col in columns ])
