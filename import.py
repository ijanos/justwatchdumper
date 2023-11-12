import lxml.html
import json
import os
import html
import sys
import datetime


def get_isosplit(s, split):
    if split in s:
        n, s = s.split(split)
    else:
        n = 0
    return n, s


def parse_isoduration(s):
    # Remove prefix
    s = s.split('P')[-1]

    # Step through letter dividers
    days, s = get_isosplit(s, 'D')
    _, s = get_isosplit(s, 'T')
    hours, s = get_isosplit(s, 'H')
    minutes, s = get_isosplit(s, 'M')
    seconds, s = get_isosplit(s, 'S')

    # Convert all to seconds
    dt = datetime.timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    return int(dt.total_seconds() / 60)

def main():
    out = []
    dumpdir = sys.argv[1]
    for _, _, files in os.walk(dumpdir):
        for name in files:
            tree = lxml.html.parse(f"{dumpdir}/{name}")
            jsonText = tree.getroot().xpath('//script[@type="application/ld+json"]')[0].text_content()
            movie = json.loads(jsonText)
            genres = list(map(html.unescape, movie["genre"]))
            dirtectors = list(map(lambda d: d["name"], movie["director"]))
            title = html.unescape(movie["name"])
            duration = parse_isoduration(movie["duration"])
            out.append({
                "title": title,
                "director": dirtectors,
                "release": movie["dateCreated"],
                "duration": duration,
                "genres": genres
            })

    with open('data.json', 'w') as f:
        json.dump(out, f, indent=2)

main()
