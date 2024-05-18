#!/usr/bin/python3
import struct
import json
from shared import load_id_file

GAME = 'krao'

ELEM_IDS = {
    0: 'spe',
    1: 'phy',
    2: 'gun',
    4: 'fir',
    8: 'ice',
    16: 'ele',
    32: 'for',
    64: 'dar',
    128: 'min',
    256: 'alm',
    512: 'rec',
    1024: 'spe'
}

with open(f"configs/{GAME}-comp-config.json") as jsonfile:
    COMP_CONFIG = json.load(jsonfile)

SKILL_IDS = load_id_file(COMP_CONFIG['skillIds'])
OLD_SKILLS = {}

with open(COMP_CONFIG['skillDump']['file'], 'rb') as binfile:
    NEW_SKILLS = binfile.read()

LINE_LEN = COMP_CONFIG['skillDump']['length']
START_OFFSET = COMP_CONFIG['skillDump']['start']
END_OFFSET = START_OFFSET + len(SKILL_IDS) * LINE_LEN

for s_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_SKILLS[line_start:line_start + LINE_LEN]
    sname, included, desc = SKILL_IDS[s_id].split('\t')

    cost_type, cost, elem = struct.unpack('<3H', line[0x00:0x06])
    min_hit, max_hit = struct.unpack('<2B', line[0x10:0x12])
    power, = struct.unpack('<B', line[0x18:0x19])
    elem = ELEM_IDS.get(elem, 'spe')

    if int(included) != 1:
        continue

    entry = {
        'cost': cost,
        'elem': elem,
        'min': min_hit,
        'max': max_hit,
        'pow': power
    }

    OLD_SKILLS[sname] = entry

with open('new-skill-data.json', 'w+') as jsonfile:
    json.dump(OLD_SKILLS, jsonfile, indent=2, sort_keys=True)
