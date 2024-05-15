#!/usr/bin/python3
import struct
import json
from shared import load_id_file, printif_notequal, save_ordered_demons

GAME = 'pq'

with open(f"configs/{GAME}-comp-config.json") as jsonfile:
    COMP_CONFIG = json.load(jsonfile)

ATTACK_ELEMS = [
    'BLANK',
    'Cut',
    'Bash',
    'UNKNOWN',
    'Stab'
]

DROP_TYPES = {
    0: 0,
    20992: 1000,
    21529: 2000,
    22016: 3000
}

RESIST_LVLS = {
    0: 'n',
    1: '0',
    5: '0',
    10: '1',
    15: '1',
    20: '2',
    25: 'q',
    30: '3',
    40: '4',
    50: 's',
    60: '6',
    70: '7',
    75: 't',
    80: '8',
    81: '8',
    90: '9',
    95: '9',
    100: '-',
    110: 'u',
    115: 'u',
    119: 'v',
    120: 'v',
    125: 'w',
    130: 'W',
    135: 'W',
    149: 'x',
    150: 'x',
    180: 'X',
    200: 'y',
    240: 'Y',
    300: 'z',
    2000: 'z'
}

RESIST_ELEMS = [int(x) for x in COMP_CONFIG['resistElems']]
AILMENT_ELEMS = [int(x) for x in COMP_CONFIG['ailmentElems']]
RACE_IDS = load_id_file(COMP_CONFIG['raceIds'])
DEMON_IDS = load_id_file(COMP_CONFIG['enemyIds'])
SKILL_IDS = load_id_file(COMP_CONFIG['skillIds'])
OLD_DEMONS = {}

with open(COMP_CONFIG['itemIds']['keyItemsFile']) as jsonfile:
    DROP_IDS = { int(x): y for x, y in json.load(jsonfile).items() }
for i, dname in enumerate(load_id_file(COMP_CONFIG['itemIds']['file'])):
    if dname != 'BLANK':
        DROP_IDS[i + COMP_CONFIG['itemIds']['start']] = dname

for fname in COMP_CONFIG['enemyData']:
    with open(f"../../../megaten-fusion-tool/src/app/{fname}") as jsonfile:
        OLD_DEMONS.update(json.load(jsonfile))
with open(COMP_CONFIG['enemyDump']['file'], 'rb') as binfile:
    NEW_DEMONS = binfile.read()

SEEN = { x: False for x in OLD_DEMONS }
LINE_LEN = COMP_CONFIG['enemyDump']['length']
START_OFFSET = COMP_CONFIG['enemyDump']['start']
END_OFFSET = COMP_CONFIG['enemyDump']['end']
if END_OFFSET == -1:
    END_OFFSET = len(NEW_DEMONS)
DROP_OFFSET = LINE_LEN - 0x1C

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, included = DEMON_IDS[d_id].split('\t')

    zero, race, lvl, hp, mostly_one = struct.unpack('<5L', line[0x00:0x14])
    stats = struct.unpack('<5H', line[0x14:0x1E])
    zero, atk_elem, atk_acc = struct.unpack('<3H', line[0x1E:0x24])
    resists = struct.unpack('<25H', line[0x24:0x56])
    innate = struct.unpack('<8H', line[0x56:0x66])
    zero, exp = struct.unpack('<HL', line[0x66:0x6C])
    drops = list(struct.unpack('<9H', line[DROP_OFFSET:DROP_OFFSET + 0x12]))
    # zeroes = struct.unpack('<6B', line[0x7E:0x84])
    # index, = struct.unpack('<L', line[0x84:0x88])

    race = RACE_IDS[race]
    # atk_elem = ATTACK_ELEMS[atk_elem]
    skills = [SKILL_IDS[x & 0x0FFF].split('\t')[0] for x in innate if x != 0]

    if int(included) < 1:
        continue

    ailments = ''.join(RESIST_LVLS[resists[i]] for i in AILMENT_ELEMS)
    resists = ''.join(RESIST_LVLS[resists[i]] for i in RESIST_ELEMS)

    SEEN[dname] = True
    entry = OLD_DEMONS[dname]
    stats = [hp] + list(stats)

    drop_odds = {}
    for i in range(0, 9, 3):
        if drops[i] == 0:
            continue
        drop = DROP_IDS[drops[i]]
        drop_odds[drop] = drops[i + 1] + DROP_TYPES.get(drops[i + 2], drops[i + 2] >> 8)

    printif_notequal(dname, 'exp', exp, entry['exp'])
    printif_notequal(dname, 'lvl', lvl, entry['lvl'])
    printif_notequal(dname, 'race', race, entry['race'])
    printif_notequal(dname, 'stats', stats, entry['stats'])
    printif_notequal(dname, 'skills', skills, entry.get('skills', []))

    entry.update({
        'area': entry['area'].replace(',', ', ').replace('  ', ' '),
        'ailments': ailments,
        'drops': drop_odds,
        'exp': exp,
        'lvl': lvl,
        # 'race': race,
        'resists': resists,
        'skills': skills,
        'stats': stats
    })

for dname, seen in SEEN.items():
    if not seen:
        print('Not seen:', dname)

save_ordered_demons(OLD_DEMONS, 'new-enemy-data.json')
