#!/usr/bin/python3
import struct
import json
from shared import load_id_file

GAME = 'dds2'

RES_ELEMS = [
    'phy',
    'gun',
    'fir',
    'ice',
    'ele',
    'for',
    'ear',
    'alm',
    'lig',
    'dar',
    'charm',
    'poison',
    'seal',
    'panic',
    'nerve',
    'hunt'
]

RES_LVLS = {
    32768: 'w',
    32784: 'W',
    0: '-',
    16: '_',
    1: 'n',
    2: 'r',
    4: 'd',
    5: '0',
    25: 'q',
    50: 's',
    75: 't',
}

RES_MODS = {
    80: 75,
    70: 75,
    60: 50,
    51: 50,
    30: 25,
    20: 25,
    1: 5
}

GAINS = ['Macca', '???', 'Karma', 'AP Normal', 'AP Hunt', '???']

with open(f"configs/{GAME}-comp-config.json") as jsonfile:
    COMP_CONFIG = json.load(jsonfile)

DEMON_IDS = load_id_file(COMP_CONFIG['demonIds'])
SKILL_IDS = [x.split('\t')[0] for x in load_id_file(COMP_CONFIG['skillIds'])]
ITEM_IDS = [x.split('\t')[0] for x in load_id_file(COMP_CONFIG['itemIds'])]
RACE_IDS = load_id_file(COMP_CONFIG['raceIds'])
OLD_DEMONS = {}

with open(COMP_CONFIG['demonDump']['file'], 'rb') as binfile:
    NEW_DEMONS = binfile.read()

LINE_LEN = COMP_CONFIG['demonDump']['length']
START_OFFSET = COMP_CONFIG['demonDump']['start']
END_OFFSET = START_OFFSET + len(DEMON_IDS) * LINE_LEN

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, in_comp = DEMON_IDS[d_id].split('\t')

    zero, race, lvl = struct.unpack('<L2B', line[0x00:0x06])
    hps = struct.unpack('<5H', line[0x06:0x10])
    stats = struct.unpack('<8B', line[0x10:0x18])
    skills = struct.unpack('<8H', line[0x18:0x28])
    gains = struct.unpack('6H', line[0x28:0x34])
    drop_items = struct.unpack('2B', line[0x3E:0x40])
    drop_odds = struct.unpack('2B', line[0x40:0x42])

    race = RACE_IDS[race]
    skills = [SKILL_IDS[x] for x in skills if x != 0]
    drops = {}
    for i in range(2):
        if drop_odds[i] == 0:
            continue
        drops[ITEM_IDS[drop_items[i]]] = drop_odds[i]

    if int(in_comp) != 1:
        continue

    entry = {
        'race': race,
        'lvl': lvl,
        'stats': [hps[0], hps[2]] + list(stats[6:]),
        'gains': gains,
        'drops': drops
    }

    OLD_DEMONS[dname] = entry

START_OFFSET = END_OFFSET
END_OFFSET = START_OFFSET + len(DEMON_IDS) * LINE_LEN

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, in_comp = DEMON_IDS[d_id].split('\t')

    full_resists = struct.unpack('<16L', line[0x00:0x40])

    if int(in_comp) != 1:
        continue

    resists = [RES_LVLS[x >> 16] for x in full_resists]
    resmods = [RES_MODS.get(x & 0xFFFF, x & 0xFFFF) for x in full_resists]

    for i, mod in enumerate(resmods):
        res = resists[i]
        if res != 'w' and mod == 100:
            resmods[i] = 0
        elif res == 'w' and mod == 150:
            resmods[i] = 0
        elif res == '-' and mod in RES_LVLS:
            resists[i] = RES_LVLS[mod]
            resmods[i] = 0
        elif res == 'w' and mod == 200:
            resists[i] = 'x'
            resmods[i] = 0

    resists = ''.join(resists)

    if sum(resmods) != 0:
        print(dname, resists, resmods)
