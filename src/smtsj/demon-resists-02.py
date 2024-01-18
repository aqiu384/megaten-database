#!/usr/bin/python3
import struct
import json
from shared import printif_notequal, save_ordered_demons

LINE_LEN = 0x88 # 0x68
START_OFFSET = 0x00 + 0*LINE_LEN
END_OFFSET = 0*LINE_LEN
OLD_RESISTS = ['phy', 'gun', 'fir', 'ice', 'ele', 'for', 'lig', 'dar']
OLD_AILMENTS = ['Poison', 'Paralyze', 'Stone', 'Strain', 'Sleep', 'Charm', 'Mute', 'Fear', 'Bomb', 'Rage']

RESIST_LVLS = {
    0: '-',
    1: 'n',
    2: 'w',
    3: 'r',
    4: 'd',
    5: 's'
}

RESIST_MODS = {
    'X': 300,
    'W': 200,
    'w': 125,
    '5': 50,
    '-': 100,
    's': 50,
    'n': 100,
    'N': 0,
    'r': 100,
    'd': 100,
    'D': 200
}

AILMENTS = [
    'Sleep',
    'Poison',
    'Paralyze',
    'Charm',
    'Mute',
    'Stone',
    'Fear',
    'Strain',
    'Bomb',
    'Rage'
]

AILMENT_ORDER = [AILMENTS.index(x) for x in OLD_AILMENTS]

with open('data/demon-data.json') as jsonfile:
    OLD_DEMONS = json.load(jsonfile)
with open('data/redux-demon-data.json') as jsonfile:
    OLD_DEMONS.update(json.load(jsonfile))
with open('data/demon-resists-02.bin', 'rb') as binfile:
    NEW_DEMONS = binfile.read()
with open('data/demon-ids.tsv') as tsvfile:
    DEMON_IDS = ['BLANK\t0'] + [x.strip() for x in tsvfile]

for d_id, line_start in enumerate(range(START_OFFSET, LINE_LEN * len(DEMON_IDS), LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, in_comp = DEMON_IDS[d_id].split('\t')

    if int(in_comp) != 1:
        continue

    demon = OLD_DEMONS[dname]

    full_resists = struct.unpack('<8H', line[0x00:0x10])
    full_ailments = struct.unpack('<11H', line[0x10:0x26])

    resists = ''.join(RESIST_LVLS[x >> 10] for x in full_resists)
    ailments = ''.join(RESIST_LVLS[full_ailments[x] >> 10] for x in AILMENT_ORDER)
    res_mods = [x & 0x3FF for x in full_resists]
    ail_mods = [full_ailments[x] & 0x3FF for x in AILMENT_ORDER]

    old_resists = demon['resists']
    old_ailments = demon.get('ailments', '-'*len(OLD_AILMENTS))
    old_res_mods = demon.get('resmods', [0]*len(OLD_RESISTS)).copy()
    old_ail_mods = demon.get('ailmods', [0]*len(OLD_AILMENTS)).copy()

    for i, res_mod in enumerate(old_res_mods):
        if res_mod == 0:
            old_res_mods[i] = RESIST_MODS[old_resists[i]]
    for i, ail_mod in enumerate(old_ail_mods):
        if ail_mod == 0:
            old_ail_mods[i] = RESIST_MODS[old_ailments[i]]

    old_resists = old_resists.lower().replace('x', 'w').replace('5', '-')
    old_ailments = old_ailments.lower().replace('x', 'w').replace('5', '-')

    printif_notequal(dname, 'resists', old_resists, resists)
    printif_notequal(dname, 'ailments', old_ailments, ailments)
    printif_notequal(dname, 'res_mods', old_res_mods, res_mods)
    printif_notequal(dname, 'ail_mods', old_ail_mods, ail_mods)

save_ordered_demons(OLD_DEMONS, 'demon-data.json')
