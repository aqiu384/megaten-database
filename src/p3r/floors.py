#!/usr/bin/python3
from shared import iterate_int_tsvfile, load_item_codes, load_item_descs, save_ordered_demons

GAME = 'Astrea'
ATTKS = ['Slash Attack', 'Strike Attack', 'Pierce Attack'] + ['Phys Attack'] * 5
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

FNAME = 'Content/{}/Activity/{}.tsv'
FLOORS = []
APPEARS = []
for floor_set in ['EndFloors', 'SpecialFloors', 'BossEnemies']:
    with open(FNAME.format(GAME, floor_set)) as tsvfile:
        FLOORS.append({ x.split('\t')[0]: x.split('\t')[1].strip() for x in tsvfile })
END_FLOORS, SPECIAL_FLOORS, BOSSES = FLOORS
END_FLOORS = { int(x): y for x, y in END_FLOORS.items() }
SPECIAL_FLOORS = { int(x): y for x, y in SPECIAL_FLOORS.items() }

FNAME = 'Content/{}/Blueprints/common/Names/Dat{}DataAsset.tsv'
with open(FNAME.format(GAME, 'EnemyName'), encoding='utf8') as tsvfile:
    next(tsvfile)
    ENEMIES = [x.split('\t')[1] for x in tsvfile]

FNAME = 'Content/{}/Battle/Tables/Dat{}DataAsset.tsv'
ENCOUNTERS = []
for line in iterate_int_tsvfile(FNAME.format(GAME, 'EncountTable'), skip_first=False):
    encounters = [line[f"id{i + 1}"] for i in range(5)]
    ENCOUNTERS.append([ENEMIES[x] for x in encounters if x != 0])
    print(ENCOUNTERS[-1])

FNAME = 'Content/{}/Field/Data/DataTable/DT_FldDungeon{}.tsv'
PACKS = []
for line in iterate_int_tsvfile(FNAME.format(GAME, 'EncountPac'), skip_first=False):
    packs = [line[f"encNo{i + 1}"] for i in range(8)]
    PACKS.append([ENCOUNTERS[x] for x in packs if x != 0])

APPEARS = {}

for floor, line in enumerate(iterate_int_tsvfile(FNAME.format(GAME, 'Floor'))):
    if floor > 152:
        break
    if floor in END_FLOORS or floor in SPECIAL_FLOORS:
        continue
    for pack_type in ['encountPack', 'strongEncountPack', 'rareEncountPack']:
        for encounter in PACKS[line[pack_type]]:
            for enemy in encounter:
                if enemy not in APPEARS:
                    APPEARS[enemy] = {}
                APPEARS[enemy][floor] = 0

def find_area(floor):
    min_floor = 0
    for max_floor, area in END_FLOORS.items():
        if floor <= max_floor:
            return area, min_floor
        min_floor = max_floor
    return '???', min_floor

for enemy, appears in APPEARS.items():
    floors = sorted(appears.keys()) + [999]
    assert(find_area(floors[0] == find_area(floors[-2])))
    area, zero_floor = find_area(floors[0])
    floors = [x - zero_floor for x in floors]

    start_floor = floors[0]
    curr_floor = start_floor
    abbrs = []
    for next_floor in floors[1:]:
        if next_floor - curr_floor > 1:
            if curr_floor == start_floor:
                abbrs.append(str(start_floor))
            else:
                abbrs.append(f"{start_floor}-{curr_floor}")
            start_floor = next_floor
        curr_floor = next_floor

    APPEARS[enemy] = f"{area[:3]} {' '.join(abbrs)}"

FNAME = 'Content/{}/Blueprints/common/Names/Dat{}DataAsset.tsv'
ITEMS = load_item_codes('en')
DEMONS = { x: { 'name': y } for x, y in load_item_descs(FNAME.format(GAME, 'EnemyName'), 'en', max_flag=6).items() }
RACES = load_item_descs(FNAME.format(GAME, 'Race'), 'en')
SKILLS = load_item_descs(FNAME.format(GAME, 'SkillName'), 'en')
ITEMS[16764] = 'Custom Parts'

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
        'skills': skills,
        'eskills': [skills[0]]
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

FNAME = 'Content/{}/Battle/Tables/Dat{}DataAsset.tsv'

for fname, updater in UPDATERS:
    for i, line in enumerate(iterate_int_tsvfile(FNAME.format(GAME, fname), skip_first=False)):
        if i in DEMONS:
            updater(DEMONS[i], line)

DEMONS = { x['name']: x for x in DEMONS.values() }
for dname, demon in DEMONS.items():
    del demon['eskills']
    del demon['name']
    demon['area'] = APPEARS.get(dname, 'Unknown')
    if dname in BOSSES:
        if demon['race'] != 'Fool':
            demon['race'] += ' P'
        parts = BOSSES[dname].split(' ')
        demon['area'] = f"{parts[0][:3]} {' '.join(parts[1:])}"

save_ordered_demons(DEMONS, 'enemy-data.json')
