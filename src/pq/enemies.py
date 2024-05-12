#!/usr/bin/python3
import struct
import json
from shared import load_id_file, printif_notequal, save_ordered_demons

ATTACK_ELEMS = [
    'BLANK',
    'Cut',
    'Bash',
    'UNKNOWN',
    'Stab'
]

RESIST_LVLS = {
    0: 'n',
    1: '0',
    10: '1',
    20: '2',
    25: 'q',
    30: '3',
    40: '4',
    50: 's',
    60: '6',
    70: '7',
    75: 't',
    80: '8',
    90: '9',
    100: '-',
    110: 'u',
    120: 'v',
    125: 'w',
    149: 'x',
    150: 'x',
    200: 'y',
    300: 'z'
}

ELEMENTS = {
    0: 'Cut',
    2: 'Bash',
    1: 'Stab',
    3: 'Fire',
    4: 'Ice',
    5: 'Elec',
    6: 'Wind',
    7: 'Light',
    8: 'Dark',
    # 9: 'UNUSED',
    24: 'Almighty'
}

AILMENTS = {
    11: 'Sleep',
    12: 'Panic',
    # 13: 'Stone',
    14: 'Poison',
    # 15: 'Clock',
    16: 'Curse',
    17: 'Para',
    22: 'Sbind',
    21: 'Mbind',
    23: 'Abind',
    18: 'Down',
    # 19: '???',
    # 20: '???',
    10: 'Insta',
}

RACE_IDS = load_id_file('races.tsv')
DROP_IDS = load_id_file('drops.tsv')
DEMON_IDS = load_id_file('enemynametable.tsv')
SKILL_IDS = load_id_file('skillnametable.tsv')
LINE_LEN = 0x88
START_OFFSET = 0x00
END_OFFSET = START_OFFSET + 368 * LINE_LEN

with open('../../../megaten-fusion-tool/src/app/pq/data/enemy-data.json') as jsonfile:
    OLD_DEMONS = json.load(jsonfile)
with open('pq1-data/battle/table/enemydata.bin', 'rb') as binfile:
    NEW_DEMONS = binfile.read()

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, included = DEMON_IDS[d_id].split('\t')

    zero, race, lvl, hp, mostly_one = struct.unpack('<5L', line[0x00:0x14])
    stats = struct.unpack('<5H', line[0x14:0x1E])
    zero, atk_elem, atk_acc = struct.unpack('<3H', line[0x1E:0x24])
    resists = struct.unpack('<25H', line[0x24:0x56])
    innate = struct.unpack('<8H', line[0x56:0x66])
    zero, exp = struct.unpack('<HL', line[0x66:0x6C])
    drops = list(struct.unpack('<HLHLHHBB', line[0x6C:0x7E]))
    zeroes = struct.unpack('<6B', line[0x7E:0x84])
    index, = struct.unpack('<L', line[0x84:0x88])

    race = RACE_IDS[race]
    atk_elem = ATTACK_ELEMS[atk_elem]
    skills = [SKILL_IDS[x - 0x1000].split('\t')[0] for x in innate if x != 0]
    ailments = ''.join(RESIST_LVLS[resists[i]] for i in AILMENTS)
    resists = ''.join(RESIST_LVLS[resists[i]] for i in ELEMENTS)

    if int(included) < 1:
        continue

    entry = OLD_DEMONS[dname]
    drops[5] += drops[7]
    drop_odds = {}

    for i in range(0, 6, 2):
        if drops[i] == 0:
            continue
        drop = DROP_IDS[drops[i] - 0x700]
        drop_odds[drop] = drops[i + 1]

    printif_notequal(dname, 'exp', exp, entry['exp'])
    printif_notequal(dname, 'lvl', lvl, entry['lvl'])
    printif_notequal(dname, 'race', race, entry['race'])

    entry.update({
        'area': entry['area'].replace(',', ', ').replace('  ', ' '),
        'drops': drop_odds,
        'ailments': ailments,
        'drops': drop_odds,
        'exp': exp,
        'lvl': lvl,
        'race': race,
        'resists': resists,
        'skills': [x for x in skills if x != 'BLANK'],
        'stats': [hp] + list(stats)
    })

save_ordered_demons(OLD_DEMONS, 'new-enemy-data.json')
