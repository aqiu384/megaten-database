#!/usr/bin/python3
import json
import re
from shared import table_header, table_row
from shopper import load_shops_to_items

def format_lvl(lvl):
    return ' (Theurgy)' if lvl > 1000 else f" ({lvl})" if lvl >= 2 else ''
def format_skills(skills):
    return ', '.join(f"{x}{format_lvl(y)}" for x, y in skills.items())

shops = load_shops_to_items()

with open('../../../megaten-fusion-tool/src/app/p3r/data/comp-config.json') as jsonfile:
    CONFIG = json.load(jsonfile)
with open('../../../megaten-fusion-tool/src/app/p3r/data/demon-unlocks.json') as jsonfile:
    UNLOCKS  = json.load(jsonfile)

def all_personas(flag):
    unlocks = {
        'Io': "Yukari's initial persona",
        'Hermes': "Junpei's initial persona",
        'Polydeuces': "Akihiko's initial persona",
        'Penthesilea': "Mitsuru's initial persona",
        'Lucia': "Fuuka's initial persona",
        'Palladion': "Aigis's initial persona",
        'Cerberus': "Koromaru's initial persona",
        'Nemesis': "Ken's initial persona",
        'Castor': "Shinjiro's initial persona"
    }

    for unlock_set in UNLOCKS:
        for name, condition in unlock_set['conditions'].items():
            unlock = condition.replace("Clear Elizabeth's ", '')
            unlock = 'DLC' if unlock_set['category'] == 'Downloadable Content' else unlock
            unlocks[name] = unlock

    RESIST_ELEMS = [x.title()[:2] for x in CONFIG['resistElems']]
    stat_headers = ['Lv.', 'Name', 'Inherits', 'Unlock', 'Skills']
    resist_headers = ['Lv.', 'Name'] +  CONFIG['baseStats'] +  RESIST_ELEMS[:-1]

    stats = { x: [] for x in CONFIG['races'] }
    resists = { x: [] for x in CONFIG['races'] }
    data_file = '../../../megaten-fusion-tool/src/app/p3r/data/demon-data.json'
    with open(data_file) as jsonfile:
        demons = json.load(jsonfile)
    data_file = '../../../megaten-fusion-tool/src/app/p3r/data/party-data.json'
    with open(data_file) as jsonfile:
        demons.update(json.load(jsonfile))
    for name, entry in demons.items():
        lvl = entry['lvl']
        race = entry['race'].replace(' P', '')
        inherits = ' '.join(re.findall('[a-zA-Z][^A-Z]*', entry['inherits'])).title()
        stats[race].append([lvl, name, inherits, unlocks.get(name, '-'), format_skills(entry['skills'])])
        resists[race].append([lvl, name] +  entry['stats'] + [x for x in entry['resists'][:-1]])
    for race in stats:
        stats[race].sort(key=lambda x: x[0])
        resists[race].sort(key=lambda x: x[0])

    for race in stats:
        print(f"#### {race}")
        print(f"##### Stats")
        print(table_header(stat_headers))
        for line in stats[race]:
            print(table_row(str(x) for x in line))
        print(f"##### Resists")
        print(table_header(resist_headers))
        for line in resists[race]:
            print(table_row(str(x) for x in line))

def count_costs(entry):
    if 'cost' not in entry:
        return '-'
    cost = entry['cost']
    return 'Therugy' if cost > 2000 else f"{cost - 1000} SP" if cost > 1000 else f"{cost}% HP"
def count_hits(entry):
    min = entry.get('min', 1)
    max = entry.get('max', 1)
    return str(min) if min == max else f"{min}-{max}"
def count_mods(entry):
    mod = entry.get('mod', 0)
    return '-' if mod == 0 else f"{mod}% {entry['add']}"

def all_skills(flag):
    skill_parsers = {
        'cost': count_costs,
        'target': lambda x: x.get('target', 'Self'),
        'power': lambda x: str(x.get('power', '-')),
        'hits': count_hits,
        'acc': lambda x: str(x.get('hit', '-')),
        'crit': lambda x: str(x.get('crit', '-')),
        'mod': count_mods
    }
    skills_sets = [
        (['sla', 'str', 'pie'], ['cost', 'target', 'power', 'hits', 'acc', 'crit', 'mod']),
        (['fir', 'ice', 'ele', 'win', 'lig', 'dar', 'alm'], ['cost', 'target', 'power', 'hits', 'acc', 'mod']),
        (['ail'], ['cost', 'target', 'mod']),
        (['rec', 'sup', 'spe'], ['cost', 'target']),
        (['pas'], [])
    ]
    elem_parsers = {}
    for elems, parsers in skills_sets:
        for elem in elems:
            elem_parsers[elem] = parsers

    stats = { x: [] for x in elem_parsers }
    data_file = '../../../megaten-fusion-tool/src/app/p3r/data/skill-data.json'
    with open(data_file) as jsonfile:
        for name, entry in json.load(jsonfile).items():
            rank = entry['rank'] if 'unique' not in entry else 99
            elem = entry['elem']
            line = [rank, name] + [skill_parsers[x](entry) for x in elem_parsers[elem]] + [entry['effect']]
            stats[elem].append(line)
    for elem in stats:
        stats[elem].sort(key=lambda x: x[0])

    for elem in stats:
        print(f"#### {elem.title()} Skills")
        print(table_header(['Rank', 'Name'] + [x.title() for x in elem_parsers[elem]] + ['Description']))
        for line in stats[elem]:
            print(table_row(str(x) for x in line))

def shuffle_time(arcana):
    print(table_header(['Rank', 'Drops']))
    for shop in shops:
        prefix = f"{arcana} "
        if shop.startswith(prefix):
            print(table_row([shop.replace(prefix, ''), shops[shop]]))

FILLERS = {
    'all_personas': all_personas,
    'all_skills': all_skills,
    'shuffle_time': shuffle_time
}

SUBME = re.compile("\{\{ (\w+)\('(.*)'\) \}\}\n")

with open('walkthrough/combat.md') as mdfile:
    for line in mdfile:
        matching = SUBME.match(line)
        if matching:
            FILLERS[matching.group(1)](matching.group(2))
        else:
            print(line, end='')
