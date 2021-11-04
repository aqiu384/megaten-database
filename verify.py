#!/usr/bin/python3
import json
import math

ELEMS = ['phy', 'fir', 'ice', 'ele', 'for', 'lig', 'dar', 'alm', 'ail', 'rec', 'sup']
ELEMS = { x: i for i, x in enumerate(ELEMS) }

with open('data/demon-data.json') as jsonfile:
    demons = jsonfile.read()
    demons = json.loads(demons)
with open('data/skill-data.json') as jsonfile:
    skills = jsonfile.read()
    skills = json.loads(skills)
with open('data/affinity-bonuses.json') as jsonfile:
    rawBonuses = jsonfile.read()
    rawBonuses = json.loads(rawBonuses)
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

        if 'cost' not in skills[sname] or selem == 'oth':
            continue

        smod = entry['affinities'][ELEMS[selem]]
        scost = skills[sname]['cost'] - 1000

        if scost == 1001:
            continue

        pbonus = bonuses[selem][smod - 1] if smod > 0 else 0
        pcost = math.floor((100 - pbonus) / 100 * scost + 0.00001)

        if pcost != ncost:
            print(dname, sname, scost, smod, pcost, ncost)

        if smod > 0 and selem not in ['rec', 'sup']:
            if scost not in COST_MODS:
                COST_MODS[scost] = [0] * 8
            if COST_MODS[scost][smod - 1] == 0:
                COST_MODS[scost][smod - 1] = ncost
            if COST_MODS[scost][smod - 1] != ncost:
                print(sname, scost, smod, ncost)

for bcost in sorted(COST_MODS):
    print(str(bcost) + '\t' + '\t'.join(str(x) for x in COST_MODS[bcost]))
