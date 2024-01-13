#!/usr/bin/python3
import json
from math import floor

with open('comp-config.json') as jsonfile:
    compConfig = json.load(jsonfile)

RACES = compConfig['races']

RESIST_LVLS = {
    'w': 'Weak',
    's': 'Resist',
    'n': 'Null',
    'r': 'Repel',
    'd': 'Drain'
}

def parseDemons(demons, skillData):
    with open('sh2-data - demons.tsv') as tsvfile:
        for line in tsvfile:
            parts = line.split('\t')
            parts[-1] = parts[-1].strip()
            race, dname, lvl = parts[1:4]
            lvl = int(lvl)
            stats = [int(x or '0') for x in parts[5:10]]
            resists = ['-'] * 7
            skills = []

            for i, rlvl in enumerate(parts[10:17]):
                if rlvl in RESIST_LVLS:
                    resists[i] = rlvl

            if race not in RACES:
                print(race)

            price = int(parts[17])

            for i, sname in enumerate(parts[18:]):
                if sname:
                    if sname not in skillData:
                        print(sname)
                        continue

                    slvl = 0 if i < 2 else int(floor(lvl)) + i - 2
                    skills.append('|' + sname + '|: ' + str(slvl) + '|')

            demons[dname] = {
                'race': race,
                'lvl': lvl,
                'price': price,
                'stats': stats,
                'resists': ''.join(resists),
                'skills': skills
            }

    return demons

def parseInherits(demons):
    with open('sh2-data - inherits.tsv') as tsvfile:
        for line in tsvfile:
            parts = line.split('\t')
            parts[-1] = parts[-1].strip()
            race, dname, lvl = parts[:3]
            inherits = ''.join(parts[3:]).replace('O', 'o')
            demons[dname]['inherits'] = inherits

    return demons

def parseSkills(skills):
    with open('sh2-data - skills.tsv') as tsvfile:
        for line in tsvfile:
            parts = line.split('\t')
            parts[-1] = parts[-1].strip()
            elem, sname, cost, target, effect, unique = parts
            cost = int(cost or '0')

            entry = {
                'element': elem,
                'effect': effect
            }

            if target != '':
                entry['target'] = target
            if cost != 0:
                entry['cost'] = 1000 + cost
            if unique.strip():
                entry['rank'] = 99

            skills[sname] = entry

    return skills

skillData = {}
skillData = parseSkills(skillData)

demonData = {}
demonData = parseDemons(demonData, skillData)
demonData = parseInherits(demonData)

print(len(demonData))

for entry in demonData.values():
    entry['stats'] = '[' + ', '.join(str(x) for x in entry['stats']) + ']'
with open('../docs/sh2/demon-data.js', 'w+') as jsonfile:
    demonData = json.dumps(demonData, indent=2, sort_keys=True)
    demonData = 'const SH2_DEMON_DATA = ' + demonData.replace('"[', '[').replace(']"', ']').replace('[]', '{}').replace('"skills": [', '"skills": {').replace('    ],', '    },').replace('"|', '"').replace('|:', '":').replace('|"', '')
    jsonfile.write(demonData)
with open('../docs/sh2/skill-data.js', 'w+') as jsonfile:
    skillData = 'const SH2_SKILL_DATA = ' + json.dumps(skillData, indent=2, sort_keys=True)
    jsonfile.write(skillData)
