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

COST_MODS = {}

for elem, btype in rawBonuses['elements'].items():
    bonuses[elem] = rawBonuses['costs'][btype]

for dname, entry in demons.items():
    if entry['race'] not in RACES:
        print(dname, entry['race'])

    for sname, ncost in entry['skills'].items():
        if sname not in skills:
            print(dname, sname)

        selem = skills[sname]['element']

        if selem == 'pas':
            continue

        smod = entry['affinities'][ELEMS[selem]]
        scost = skills[sname]['cost'] - 1000

        if smod == 0:
            continue

        pcost = math.floor((100 - bonuses[selem][smod - 1]) / 100 * scost)

        if pcost != ncost:
            print(sname, scost, smod, pcost, ncost)

        if selem in ['rec', 'sup'] or 'cost' not in skills[sname]:
            continue

        if scost not in COST_MODS:
            COST_MODS[scost] = [0] * 8
        if COST_MODS[scost][smod - 1] == 0:
            COST_MODS[scost][smod - 1] = ncost
        if COST_MODS[scost][smod - 1] != ncost:
            print(sname, scost, smod, ncost)

for bcost in sorted(COST_MODS):
    print(str(bcost) + '\t' + '\t'.join(str(x) for x in COST_MODS[bcost]))
