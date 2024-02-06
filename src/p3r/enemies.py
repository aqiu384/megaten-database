#!/usr/bin/python3
from shared import save_ordered_demons

ATTKS = ['Slash Attack', 'Strike Attack', 'Pierce Attack', '', '', '', '', 'Phys Attack']
SUFFIXES = ['', ' B', ' C', ' D', ' E']
MATERIAL_OFFSET = 0x6000
NAMES = []
RESISTS = {
    10: '1',    # 50050 00000000 10
    20: '-',    # 50100 00000000 20
    40: '4',    # 50200 00000000 40
    256: 'n',   # 30100 00000001 0
    512: 'r',   # 20100 00000010 0
    1024: 'd',  # 10100 00000100 0
    2048: 'w',  # 60125 00001000 0
    4096: 's',  # 40050 00010000 0
    4101: 't',  # 40025 00010000 5
    8192: 'N',  # 30100 00100000 0
    12288: 'S', # 40050 00110000 0
    12293: 'T', # 40025 00110000 5
    34816: 'Z', # 61275 10001000 255
}

for fname in ['race', 'skill', 'material']:
    with open(f"en-names/{fname}-names.tsv") as tsvfile:
        next(tsvfile)
        NAMES.append([x.split('\t')[0].strip() for x in tsvfile])

RACES, SKILLS, MATERIALS = NAMES
INCLUDED = []
DEMONS = {}
SEEN = {}

with open('en-names/enemy-names.tsv') as tsvfile:
    next(tsvfile)
    for line in tsvfile:
        dname, included = line.split('\t')
        INCLUDED.append(dname if 0 < int(included) and int(included) < 3 else '')

def load_stats(dname, parts):
    _, race, lvl = parts[:3]
    stats = parts[3:10]
    skills = [SKILLS[x] for x in parts[10:18] if x != 0]
    exp, _ = parts[18:20]
    drop1, _, drop2, _, drop3, _, drop4, _, _, dropE, _ = parts[20:31]
    drops = [x - MATERIAL_OFFSET for x in [drop1, drop2, drop3, drop4, dropE] if x != 0]
    drops = [MATERIALS[x] for x in drops if x > 0]
    atkElem, _, _ = parts[31:]
    skills.insert(0, ATTKS[atkElem])

    suffix = SEEN.get(dname, 0)
    SEEN[dname] = suffix + 1
    dname += SUFFIXES[suffix]

    race = RACES[race]
    if suffix > 0:
        race += ' P'

    DEMONS[dname] = {
        'race': race,
        'lvl': lvl,
        'exp': exp,
        'skills': skills,
        'stats': stats,
    }

    if 0 < len(drops):
        DEMONS[dname]['drops'] = drops

def load_resists(dname, parts):
    resists = [RESISTS[x] for x in parts]
    ailments = ''.join(resists[10:-3])
    resists = ''.join(resists[:7] + resists[8:10] + resists[7:8])

    suffix = SEEN.get(dname, 0)
    SEEN[dname] = suffix + 1
    dname += SUFFIXES[suffix]

    DEMONS[dname]['resists'] = resists
    if ailments != '------':
        DEMONS[dname]['ailments'] = ailments

PARSERS = [
    ('stats', load_stats),
    ('resists', load_resists)
]

for fname, parser in PARSERS:
    with open(f"battle/enemy-{fname}.tsv") as tsvfile:
        next(tsvfile)
        SEEN = {}
        for i, line in enumerate(tsvfile):
            parts = [int(x) for x in line.split()]
            dname = INCLUDED[i]
            if dname != '':
                parser(dname, parts)

for dname, entry in list(DEMONS.items()):
    if entry['stats'][1] == 0:
        del DEMONS[dname]

save_ordered_demons(DEMONS, 'enemy-data.json')
