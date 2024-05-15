#!/usr/bin/python3
import struct
import json
from shared import load_id_file, printif_notequal, save_ordered_demons

GAME = 'smtdsj'

with open(f"configs/{GAME}-comp-config.json") as jsonfile:
    COMP_CONFIG = json.load(jsonfile)

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
DEMON_IDS = load_id_file(COMP_CONFIG['demonIds'])
SKILL_IDS = load_id_file(COMP_CONFIG['skillIds'])
RACE_IDS = load_id_file(COMP_CONFIG['raceIds'])
OLD_DEMONS = {}

for fname in COMP_CONFIG['demonData']:
    with open(f"../../../megaten-fusion-tool/src/app/{fname}") as jsonfile:
        OLD_DEMONS.update(json.load(jsonfile))
with open(COMP_CONFIG['demonDump']['file'], 'rb') as binfile:
    NEW_DEMONS = binfile.read()

SEEN = { x: False for x in OLD_DEMONS }
LINE_LEN = COMP_CONFIG['demonDump']['length']
START_OFFSET = COMP_CONFIG['demonDump']['start']
END_OFFSET = START_OFFSET + len(DEMON_IDS) * LINE_LEN

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, in_comp = DEMON_IDS[d_id].split('\t')

    if int(in_comp) == 0 or COMP_CONFIG['inCompMax'] < int(in_comp):
        continue

    SEEN[dname] = True
    entry = OLD_DEMONS[dname]

    new_d_id, race, lvl =  struct.unpack('<H2B', line[0x00:0x04])
    stats = struct.unpack('<7B', line[0x18:0x1F])
    growths = struct.unpack('<5B', line[0x1F:0x24])
    pcoeff, = struct.unpack('<1H', line[0x2C:0x2E])
    skills = struct.unpack('<6H', line[0x2E:0x3A])
    full_resists = struct.unpack('<8H', line[0x3A:0x4A])
    full_ailments = struct.unpack('<11H', line[0x4A:0x60])

    race = RACE_IDS[race]
    stats = list(stats[:3] + stats[6:] + stats[3:6])
    skills = [SKILL_IDS[x] for x in skills if x != 0]
    resists = ''.join(RESIST_LVLS[x >> 10] for x in full_resists)
    ailments = ''.join(RESIST_LVLS[full_ailments[x] >> 10] for x in AILMENT_ORDER)
    res_mods = [x & 0x3FF for x in full_resists]
    ail_mods = [full_ailments[x] & 0x3FF for x in AILMENT_ORDER]

    old_resists = entry['resists']
    old_ailments = entry.get('ailments', '-'*len(OLD_AILMENTS))
    old_res_mods = entry.get('resmods', [0]*len(OLD_RESISTS)).copy()
    old_ail_mods = entry.get('ailmods', [0]*len(OLD_AILMENTS)).copy()

    for i, res_mod in enumerate(old_res_mods):
        if res_mod == 0:
            old_res_mods[i] = RESIST_MODS[old_resists[i]]
    for i, ail_mod in enumerate(old_ail_mods):
        if ail_mod == 0:
            old_ail_mods[i] = RESIST_MODS[old_ailments[i]]

    old_resists = old_resists.lower().replace('x', 'w').replace('5', '-')
    old_ailments = old_ailments.lower().replace('x', 'w').replace('5', '-')

    printif_notequal(dname, 'd_id', new_d_id, d_id)
    printif_notequal(dname, 'race', race, entry['race'])
    printif_notequal(dname, 'lvl', lvl, round(entry['lvl']))
    printif_notequal(dname, 'stats', stats[2:], entry['stats'][2:])
    printif_notequal(dname, 'pcoeff', pcoeff, entry['pcoeff'])
    printif_notequal(dname, 'skills', sorted(skills), sorted(entry['skills']))
    printif_notequal(dname, 'resists', resists, old_resists)
    printif_notequal(dname, 'ailments', ailments, old_ailments)
    printif_notequal(dname, 'res_mods', res_mods, old_res_mods)
    printif_notequal(dname, 'ail_mods', ail_mods, old_ail_mods)

    entry['ailments'] = ailments

with open(COMP_CONFIG['sourceDump']['file'], 'rb') as binfile:
    NEW_DEMONS = binfile.read()

LINE_LEN = COMP_CONFIG['sourceDump']['length']
START_OFFSET = COMP_CONFIG['sourceDump']['start']
END_OFFSET = START_OFFSET + len(DEMON_IDS) * LINE_LEN

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, in_comp = DEMON_IDS[d_id].split('\t')

    if int(in_comp) == 0 or COMP_CONFIG['inCompMax'] < int(in_comp):
        continue

    entry = OLD_DEMONS[dname]
    source = struct.unpack('<3H', line[0x02:0x08])
    source = [SKILL_IDS[x] for x in source if x != 0]
    printif_notequal(dname, 'source', sorted(source), sorted(entry['source']))

for dname, seen in SEEN.items():
    if not seen:
        print('Not seen:', dname)

save_ordered_demons(OLD_DEMONS, 'new-demon-data.json')
