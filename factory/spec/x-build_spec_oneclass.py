#!/usr/bin/env python3

# http://www.vacances-scolaires.education/annee-2017-2018.php
# http://www.vacances-scolaires.education/jours-feries-2017.php
# http://www.vacances-scolaires.education/jours-feries-2018.php
# http://vacances-scolaires.education/zone-a/
#
# Liste lycée france ?
# Liste ville avec un lycée france ?








exit()


from collections import defaultdict
from urllib.request import urlopen

from bs4 import BeautifulSoup
import lxml.html

print("\n"*100)
print("# ----- HOLIDAYS ----- #")


# ZONES !!!
zone_names = list("ABC")

url = r"file:///Users/projetmbc/Google%20Drive/git/writings/private/program%5Bmation%5D/_python3/_python3_in_practice/source/fr/content/medium/web/scrapping/Le%20calendrier%20scolaire%20-%20Ministe%CC%80re%20de%20l'E%CC%81ducation%20nationale.html"


html = urlopen(url).read()

soup = BeautifulSoup(html, 'html.parser')
# td = soup.find_all('td', attrs={'class': 'zone-td-common'})
td = soup.find_all('tr')
infos = td.pop(0)
infos = infos.find_all('th')
infos = td.pop(0)
infos = infos.find_all('td')

zones = defaultdict(dict)

for oneinfo in infos:
    academies = []

    for oneline in oneinfo.text.split():
        oneline = oneline.strip()

        if oneline and oneline not in [
            "Académies",
            ":"
        ]:
            for city in oneline.split(","):
                city = city.strip()

                if city:
                    academies.append(city)


    for oneclss in oneinfo["class"]:
        if oneclss[:-1] == "zone-td-bg-":
            namezone = zone_names[int(oneclss[-1])]
            break

    zones[namezone]["academies"] = academies
    zones[namezone]["holidays"]  = []


# Vacances (plus simples mais pas les infos sur les acdémies)


url = r"file:///Users/projetmbc/Google%20Drive/git/writings/private/program[mation]/_python3/_python3_in_practice/source/fr/content/medium/web/scrapping/Vacances%20scolaires%202018%20-%20Calendrier%20officiel%202017-2018.html"

html = urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

css_zones = set("tzone{0}".format(letter) for letter in zone_names + ["Z"])

def namesfromcss(css_classes):
    namesfound = [
        x[-1]
        for x in css_zones & css_classes
        if x.startswith("tzone")
    ]

    if namesfound == ['Z']:
        namesfound = zone_names

    return namesfound

def datesfromtxts(txts):
    start, end = None, None

    nbtxts = len(txts)

    if nbtxts == 2:
        start = txts[1]

    elif nbtxts == 4:
        start, end = txts[1], txts[3]

    return start, end


infos  = soup.find_all('td')

for oneinfo in infos:
    css_classes = set(oneinfo["class"])

    if "menu" in css_classes:
        keepit = True
        holidayname = oneinfo.find("a").text

    else:
        znames_found = namesfromcss(css_classes)

        if znames_found:
            datesfound = datesfromtxts(
                [x.text for x in oneinfo.find_all("span")]
            )

            if datesfound != (None, None):
                for namezone in znames_found:
                    zones[namezone]["holidays"].append(
                        (holidayname, datesfound)
                    )

        else:
            keepit = False


import pprint; pprint.pprint(zones)


# on s'arrêt là, pour le reste on le donne en exercice !!!!!
