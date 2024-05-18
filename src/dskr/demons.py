#!/usr/bin/python3
import struct
import json
from shared import load_id_file, save_ordered_demons

GAME = 'krao'

RES_LVLS = {
    0: '-',
    16: 'n',
    32: 'd',
    64: 'w'
}

with open(f"configs/{GAME}-comp-config.json") as jsonfile:
    COMP_CONFIG = json.load(jsonfile)

DEMON_IDS = load_id_file(COMP_CONFIG['demonIds'])
SKILL_IDS = [x.split('\t')[0] for x in load_id_file(COMP_CONFIG['skillIds'])]
SKILL_LVLS = [0.1, 0.2, 1, 2, 3, 4, 5, 6]
OLD_DEMONS = {}

with open(COMP_CONFIG['demonSkillDump']['file'], 'rb') as binfile:
    NEW_DEMONS = binfile.read()

LINE_LEN = COMP_CONFIG['demonSkillDump']['length']
START_OFFSET = COMP_CONFIG['demonSkillDump']['start']
END_OFFSET = START_OFFSET + len(DEMON_IDS) * LINE_LEN

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, included = DEMON_IDS[d_id].split('\t')

    lvl, new_d_id = struct.unpack('<2H', line[0x04:0x08])
    hps = struct.unpack('<4L', line[0x18:0x28])
    stats = struct.unpack('<4H', line[0x28:0x30])
    skills = struct.unpack('<8H', line[0x30:0x40])

    stats = [hps[0], hps[2]] + [stats[i] for i in (0, 2, 1, 3)]
    skills = { SKILL_IDS[x]: SKILL_LVLS[i] for i, x in enumerate(skills) if x != 0 }
    for sname, slvl in skills.items():
        if 1 <= slvl:
            skills[sname] = lvl + slvl

    if int(included) != 1:
        continue

    entry = {
        'lvl': lvl,
        'stats': stats,
        'skills': skills
    }

    OLD_DEMONS[dname] = entry

LINE_LEN = COMP_CONFIG['demonResistDump']['length']
START_OFFSET = COMP_CONFIG['demonResistDump']['start']
END_OFFSET = START_OFFSET + len(DEMON_IDS) * LINE_LEN

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, included = DEMON_IDS[d_id].split('\t')

    resists = struct.unpack('<10L', line[0x00:0x28])

    if int(included) != 1:
        continue

    resmods = [x & 0xFF for x in resists]
    resists = ''.join(RES_LVLS.get(x >> 8, '?') for x in resists)

    entry = OLD_DEMONS[dname]
    entry.update({
        'resists': resists,
        'resmods': resmods
    })

save_ordered_demons(OLD_DEMONS, 'new-demon-data.json')
