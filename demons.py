#!/usr/bin/python3
import json

with open('comp-config.json') as jsonfile:
    compConfig = json.load(jsonfile)

RACES = compConfig['races']
AILMENTS = compConfig['ailments']

RESIST_LVLS = {
    'Weak': 'w',
    'Resist': 's',
    'Null': 'n',
    'Repel': 'r',
    'Drain': 'd'
}

def parseEnemies(demons):
    with open('smtv-data - raw-enemies.tsv') as tsvfile:
        for line in tsvfile:
            parts = line.split('\t')
            parts[-1] = parts[-1].strip()
            race, lvl, dname = parts[1:4]

            if lvl == '':
                continue

            lvl = int(lvl)
            resists = ''.join(x or '-' for x in parts[5:12])

            if dname not in demons:
                demons[dname] = {}

            entry = {
                'race': race,
                'lvl': lvl,
                'stats': [0] * 7,
                'resists': resists,
                'affinities': [0] * 11,
                'skills': {}
            }

            demons[dname].update(entry)

    return demons

def parseDemons(demons):
    with open('smtv-data - raw-demons.tsv') as tsvfile:
        for line in tsvfile:
            parts = line.split('\t')
            parts[-1] = parts[-1].strip()
            race, lvl, dname = parts[1:4]
            lvl = int(lvl)
            stats = [int(x or '0') for x in parts[4:6]] + [0] * 5
            affins = [int(x or '0') for x in parts[6:17]]
            skills = {}

            for i in range(17, len(parts), 2):
                sname = parts[i]
                if sname == '':
                    continue
                slvl = parts[i + 1]
                skills[sname] = int(slvl)

            if dname not in demons:
                demons[dname] = {
                    'race': race,
                    'lvl': lvl,
                    'stats': stats,
                    'resists': '-' * 7,
                    'affinities': affins,
                    'skills': skills
                }

            if sum(affins) != 0:
                demons[dname].update({
                    'affinities': affins,
                    'skills': skills
                })

            if demons[dname]['lvl'] >= lvl:
                demons[dname].update({
                    'lvl': lvl,
                    'stats': stats,
                })

    return demons

def parseStats(demons):
    with open('smtv-data - raw-stats.tsv') as tsvfile:
        for line in tsvfile:
            parts = line.split('\t')
            parts[-1] = parts[-1].strip()
            race, lvl, dname = parts[1:4]
            lvl = int(lvl)
            stats = [int(x) for x in parts[4:11]]
            resists = ''.join(x or '-' for x in parts[11:18])

            aresists = ['-'] * len(AILMENTS)
            hasails = False

            for apair in parts[18].split(', '):
                if apair == '':
                    continue
                atype, alvl = apair.split(': ')
                aresists[AILMENTS.index(atype)] = RESIST_LVLS[alvl]
                hasails = True

            aresists = ''.join(aresists)

            affins = [int(x or '0') for x in parts[19:30]]
            skills = {}

            for i in range(30, len(parts), 2):
                sname = parts[i]
                if sname == '':
                    continue
                slvl = parts[i + 1]
                skills[sname] = int(slvl)

            if dname not in demons:
                demons[dname] = {
                    'race': race,
                    'lvl': lvl
                }

            demons[dname].update({
                'resists': resists,
                'affinities': affins,
                'skills': skills
            })

            if hasails:
                demons[dname]['ailments'] = aresists

            if demons[dname]['lvl'] >= lvl:
                demons[dname].update({
                    'lvl': lvl,
                    'stats': stats
                })

    return demons

def parseSkills(skills):
    with open('smtv-data - skills.tsv') as tsvfile:
        for line in tsvfile:
            parts = line.split('\t')
            parts[-1] = parts[-1].strip()
            elem, sname, cost, target, effect, unique = parts
            cost = int(cost or '0')

            entry = {
                'element': elem,
                'effect': effect
            }

            if elem != 'pas':
                entry['target'] = target
            if cost != 0:
                entry['cost'] = 1000 + cost
            if unique.strip():
                entry['rank'] = 99

            skills[sname] = entry

    return skills

demonData = {}
demonData = parseEnemies(demonData)
demonData = parseDemons(demonData)
demonData = parseStats(demonData)

skillData = {}
skillData = parseSkills(skillData)

for entry in demonData.values():
    entry['stats'] = '[' + ', '.join(str(x) for x in entry['stats']) + ']'
    entry['affinities'] = '[' + ', '.join(str(x) for x in entry['affinities']) + ']'
with open('demon-data.json', 'w+') as jsonfile:
    demonData = json.dumps(demonData, indent=2, sort_keys=True)
    demonData = demonData.replace('"[', '[').replace(']"', ']')
    jsonfile.write(demonData)
with open('skill-data.json', 'w+') as jsonfile:
    json.dump(skillData, jsonfile, indent=2, sort_keys=True)