#!/usr/bin/python3
from shared import save_ordered_demons, load_item_descs, load_item_codes, iterate_int_tsvfile

ATTKS = ['Slash Attack', 'Strike Attack', 'Pierce Attack'] + ['Phys Attack'] * 5
SUFFIXES = ['', ' B', ' C', ' D', ' E']
MATERIAL_OFFSET = 0x6000
NAMES = []
RESISTS = {
    10: 's',    # 50050 00000000 10
    20: '-',    # 50100 00000000 20
    40: 'v',    # 50200 00000000 40
    45: 'u',    # 50250 00000000 50
    256: 'n',   # 30100 00000001 0
    512: 'r',   # 20100 00000010 0
    1024: 'd',  # 10100 00000100 0
    2048: 'w',  # 60125 00001000 0
    4101: 't',  # 40025 00010000 5
    4096: 's',  # 40050 00010000 0
    8192: '_',  # 50100 00100000 0
    8232: 'V',  # 50200 00100000 40
    12293: 'T', # 40025 00110000 5
    12288: 'S', # 40050 00110000 0
    34816: 'z', # 61275 10001000 255
}

FNAME = 'Content/Xrd777/Blueprints/common/Names/Dat{}DataAsset.tsv'

ITEMS = load_item_codes('en')
DEMONS = { x: { 'name': y } for x, y in load_item_descs(FNAME.format('EnemyName'), 'en', max_flag=3).items() }
RACES = load_item_descs(FNAME.format('Race'), 'en')
SKILLS = load_item_descs(FNAME.format('SkillName'), 'en')

def update_stats(entry, line):
    skills = [line[f"skill{x}"] for x in range(1, 9)]
    skills = [SKILLS[x] for x in skills if x != 0]
    skills.insert(0, ATTKS[line['attackAttr']])
    drops = { ITEMS[line[f"itemId{x}"]]: line[f"itemProb{x}"] for x in range(1, 5) if line[f"itemProb{x}"] != 0 }

    entry.update({
        'race': RACES[line['race']],
        'lvl': line['level'],
        'exp': line['exp'],
        'stats': [line['maxhp'], line['maxsp']] + [line[f"params{x}"] for x in range(1, 6)],
        'skills': skills
    })

    if 0 < len(drops):
        entry['drops'] = drops

    return entry

def update_resists(entry, line):
    resists = [RESISTS[line[f"attr{x}"]] for x in range(1, 11)]
    resists = ''.join(resists[:7] + resists[8:] + resists[7:8])
    ailments = ''.join([RESISTS[line[f"attr{x}"]] for x in range(11, 17)])
    entry['resists'] = resists
    if ailments != '------':
        entry['ailments'] = ailments.replace('_', 'n')
    return entry

UPDATERS = [
    ('Enemy', update_stats),
    ('EnemyAffinity', update_resists)
]

FNAME = 'Content/Xrd777/Battle/Tables/Dat{}DataAsset.tsv'

for fname, updater in UPDATERS:
    for i, line in enumerate(iterate_int_tsvfile(FNAME.format(fname), skip_first=False)):
        if i in DEMONS:
            updater(DEMONS[i], line)

DEMONS = { x['name']: x for x in DEMONS.values() }
for demon in DEMONS.values():
    del demon['name']

with open('walkthrough/enemy-floors.tsv') as tsvfile:
    next(tsvfile)
    for line in tsvfile:
        name, race, floor = line.split('\t')
        if race.endswith(' C'):
            race = race.replace(' C', ' B')
            DEMONS[name]['boss'] = True
        DEMONS[name]['race'] = race
        DEMONS[name]['area'] = floor.strip()

save_ordered_demons(DEMONS, 'enemy-data.json')
