import lxml.html
import json
import os
import html
import sys
import re

def main():
    out = []
    dumpdir = sys.argv[1]
    genreMap = dict()
    for _, _, files in os.walk(dumpdir):
        for name in files:
            tree = lxml.html.parse(f"{dumpdir}/{name}")
            # this is terribly fragile but it works and it only has to run once
            jsonText = tree.getroot().xpath("//script[contains(text(),'__APOLLO_STATE__')]")[0].text_content()
            jsonObj = json.loads(jsonText.split("__APOLLO_STATE__=")[1])
            defaultClient = jsonObj["defaultClient"]

            keys = list(filter(lambda k: re.search(r"Movie.*content.*\)$", k), defaultClient.keys()))
            movieKey = max(keys, key=lambda k: len(defaultClient[k].keys()))
            movie = defaultClient[movieKey]

            externelIds = list(filter(lambda k: re.search(r"Movie.*content.*\).externalIds$", k), defaultClient.keys()))
            if externelIds:
                imdbExternalId = list(filter(lambda k: "imdbId" in defaultClient[k], externelIds))[0]
                imdbid = defaultClient[imdbExternalId]["imdbId"]
            else:
                imdbid = ""

            genreKeys = list(filter(lambda k: re.search(r"Genre:", k), defaultClient.keys()))

            for genreKey in genreKeys:
                genreObj = defaultClient[genreKey]
                genreMap[genreObj["shortName"]] = genreObj["slug({\"language\":\"en\"})"]

            creditKeys = list(map(lambda k: k["id"], movie["credits"]))
            directors = []
            for k in creditKeys:
                credit = defaultClient[k]
                if "role" in credit and credit["role"] == "DIRECTOR":
                    directors.append(credit["name"])
            directors.sort()

            title = html.unescape(movie["title"])
            ogtitle = html.unescape(movie["originalTitle"])

            genres = list(map(lambda g: genreMap[defaultClient[g["id"]]["shortName"]], movie["genres"]))

            duration = movie["runtime"]
            out.append({
                "englishTitle": title,
                "originalTitle": ogtitle,
                "director": directors,
                "imdbID": imdbid,
                "releaseYear": movie["originalReleaseYear"],
                "releaseDate": movie["originalReleaseDate"] if movie["originalReleaseDate"] else "",
                "runtime": duration,
                "ageCertification": movie["ageCertification"],
                "genres": sorted(genres)
            })

    out.sort(key=lambda m: m["releaseDate"], reverse=True)

    with open('data.json', 'w') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

main()
