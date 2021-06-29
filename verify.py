#!/usr/bin/python3
import json
import math

ELEMS = ['phy', 'fir', 'ice', 'ele', 'for', 'lig', 'dar', 'alm', 'ail', 'rec', 'sup']
ELEMS = { x: i for i, x in enumerate(ELEMS) }

with open('demon-data.json') as jsonfile:
    demons = json.load(jsonfile)
with open('skill-data.json') as jsonfile:
    skills = json.load(jsonfile)
with open('affinity-bonuses.json') as jsonfile:
    rawBonuses = json.load(jsonfile)
with open('comp-config.json') as jsonfile:
    compConfig = json.load(jsonfile)

RACES = compConfig['races']
bonuses = {}

for elem, btype in rawBonuses['elements'].items():
    bonuses[elem] = rawBonuses['costs'][btype]

for dname, entry in demons.items():
    if entry['race'] not in RACES:
        print(dname, entry['race'])

    for sname, ncost in entry['skills'].items():
        if sname not in skills:
            print(dname, sname)

        selem = skills[sname]['element']

        if selem in ['pas']:
            continue

        scost = skills[sname]['cost'] - 1000
        smod = entry['affinities'][ELEMS[selem]]

        if smod > 0:
            sbonus = scost * bonuses[selem][smod - 1] / 100
            sbonus = scost - round(sbonus + 0.01)
        else:
            sbonus = scost

        if scost <= 10 and smod > 0:
            if selem in ['rec', 'sup']:
                sbonus = scost - 2
            else:
                sbonus = scost - min(smod, 2)

        if ncost != sbonus:
            print(dname, sname, ncost, sbonus)
