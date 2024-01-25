#!/usr/bin/python3
import struct
import json

OLD_RESISTS = ['phy', 'fir', 'ice', 'ele', 'win', 'lig', 'dar', 'alm']
RESISTS = OLD_RESISTS[:-3] + ['alm', 'lig', 'dar']
OLD_AILMENTS = ['Panic', 'Poison', 'Fear', 'Rage', 'Dizzy', 'Exhaustion', 'Enervation', 'Mute']
AILMENTS = OLD_AILMENTS[:]
RESIST_ORDER = [RESISTS.index(x) for x in OLD_RESISTS]
AILMENT_ORDER = [AILMENTS.index(x) for x in OLD_AILMENTS]

RESIST_LVLS = {
    0: '-',
    1: 'n',
    2: 'r',
    4: 'd',
    8: 'w',
    16: 's',
    32: 'N'
}

TREASURE_DEMONS = ['Wealth', 'Treasure', 'Supreme', 'Opulent', 'Luxury', 'Glorious', 'Happiness', 'Isolated']
TREASURE_DEMONS = [x + ' Hand' for x in TREASURE_DEMONS]

RESIST_MODS = {
    'd': 0,
    'r': 0,
    'n': 0,
    's': 0,
    '-': 100,
    'w': 0,
    'Z': 1275,
    'N': 0
}

with open('data/golden-enemy-data.json') as jsonfile:
    OLD_DEMONS = json.load(jsonfile)
with open('data/enemy-data.bin', 'rb') as binfile:
    NEW_DEMONS = binfile.read()
with open('data/enemy-ids.tsv') as tsvfile:
    DEMON_IDS = ['BLANK\t0'] + [x.strip() for x in tsvfile]
with open('data/skill-ids.tsv') as tsvfile:
    SKILL_IDS = ['BLANK'] + [x.strip() for x in tsvfile]
with open('data/race-ids.tsv') as tsvfile:
    RACE_IDS = ['BLANK'] + [x.strip() for x in tsvfile]
with open('data/item-ids.tsv') as tsvfile:
    ITEM_IDS = ['BLANK'] + [x.strip() for x in tsvfile]

SEEN_DEMONS = { x: False for x in OLD_DEMONS }

def printif_notequal(dname, field, lhs, rhs):
    if str(lhs) != str(rhs):
        print(dname, field, lhs, rhs)

def save_ordered_demons(demons, fname):
    for entry in demons.values():
        for stat_set in ['resmods', 'ailmods', 'stats']:
            if stat_set in entry:
                entry[stat_set] = '[' + ', '.join(str(x) for x in entry[stat_set]) + ']'
        for stat_set in ['skills', 'drops']:
            if stat_set in entry:
                if len(entry[stat_set]) == 0:
                    entry[stat_set] = '[]'
                else:
                    entry[stat_set] = '[|' + '|, |'.join(x for x in entry[stat_set]) + '|]'

    jstring = json.dumps(demons, indent=2, sort_keys=True)
    jstring = jstring.replace('||', '\n').replace('|', '"')
    jstring = jstring.replace('"[', '[').replace(']"', ']').replace('"{', '{').replace('}"', '}')

    with open(fname, 'w+') as jsonfile:
        jsonfile.write(jstring)

LINE_LEN = 0x3C

for d_id, line_start in enumerate(range(0x00, LINE_LEN * len(DEMON_IDS), LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, in_comp = DEMON_IDS[d_id].split('\t')

    if int(in_comp) != 1:
        continue

    demon = OLD_DEMONS[dname]
    SEEN_DEMONS[dname] = True

    race_id = struct.unpack('<1B', line[0x00:0x01])[0]
    dlvl = struct.unpack('<1B', line[0x01:0x02])[0]
    stats = struct.unpack('<2H5B', line[0x02:0x0B])
    innate = struct.unpack('<8H', line[0x0C:0x1C])
    exp, price = struct.unpack('<2H', line[0x1C:0x20])
    drops = struct.unpack('<8H', line[0x20:0x30])

    printif_notequal(dname, 'race', demon['race'].replace(' P', ''), RACE_IDS[race_id])
    printif_notequal(dname, 'lvl', demon['lvl'], dlvl)
    printif_notequal(dname, 'stats', demon['stats'], list(stats))
    printif_notequal(dname, 'stats', demon['price'], price)
    printif_notequal(dname, 'exp', demon['exp'], exp)

    innate = [SKILL_IDS[s_id] for s_id in innate if s_id != 0]

    if dname not in TREASURE_DEMONS:
        printif_notequal(dname, 'innate', sorted(demon['skills']), sorted(innate))
        demon['skills'] = innate

    for i in range(0, 8, 2):
        i_id, i_chance = drops[i:i + 2]

        if i_id == 0:
            continue

        i_chance *= 0.5
        iname = ITEM_IDS[i_id]

        if i == 0:
            printif_notequal(dname, 'drop', demon['material'], iname)
        if i == 0:
            printif_notequal(dname, 'drop', demon['material'], iname)

for d_id, line_start in enumerate(range(LINE_LEN * len(DEMON_IDS) - 2, len(NEW_DEMONS), 0x20)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, in_comp = DEMON_IDS[d_id].split('\t')

    if int(in_comp) != 1:
        continue

    demon = OLD_DEMONS[dname]
    full_resists = struct.unpack('<8H', line[0x00:0x10])
    full_ailments = struct.unpack('<8H', line[0x10:0x20])

    resists = [full_resists[x] >> 8 for x in RESIST_ORDER]
    ailments = [full_ailments[x] >> 8 for x in AILMENT_ORDER]

    resists = ''.join(RESIST_LVLS[full_resists[x] >> 8] for x in RESIST_ORDER)
    ailments = ''.join(RESIST_LVLS[full_ailments[x] >> 8] for x in AILMENT_ORDER)
    res_mods = [5 * (full_resists[x] & 0xFF) for x in RESIST_ORDER]
    ail_mods = [5 * (full_ailments[x] & 0xFF) for x in AILMENT_ORDER]

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

    old_resists = old_resists.replace('Z', 'w')

    printif_notequal(dname, 'resists', old_resists, resists)
    printif_notequal(dname, 'ailments', old_ailments, ailments)
    printif_notequal(dname, 'res_mods', old_res_mods, res_mods)
    printif_notequal(dname, 'ail_mods', old_ail_mods, ail_mods)

for dname, seen in SEEN_DEMONS.items():
    if not seen:
        print(dname)

save_ordered_demons(OLD_DEMONS, 'golden-enemy-data.json')
