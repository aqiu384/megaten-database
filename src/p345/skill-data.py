#!/usr/bin/python3
import struct
import json
from shared import load_comp_config

GAME_PREFIX = 'p4g'
GAME_TYPE = GAME_PREFIX[:2]
COMP_CONFIG = load_comp_config(f"configs/{GAME_PREFIX}-comp-config.json")
OLD_SKILLS = {}

with open(f"dumps/{GAME_PREFIX}-skill-data.bin", 'rb') as binfile:
    NEW_SKILLS = binfile.read()
with open(f"{GAME_TYPE}-data/{COMP_CONFIG['skillIds']}") as tsvfile:
    SKILL_IDS = ['BLANK\t0'] + [x.strip() for x in tsvfile]
ELEM_IDS = COMP_CONFIG['gameResists'] + COMP_CONFIG['gameAilments'] + COMP_CONFIG['gameElems']
ELEM_IDS = [x[:3].lower() for x in ELEM_IDS]

stat_config = COMP_CONFIG['skillElems']
for d_id, line_start in enumerate(range(stat_config['begin'], stat_config['end'], stat_config['length'])):
    line = NEW_SKILLS[line_start:line_start + stat_config['length']]
    sname, included = SKILL_IDS[d_id].split('\t')
    included = int(included)

    elem, = struct.unpack('<H', line)
    elem_flag = elem >> 8
    elem = 0xFF & elem

    if included == 0 or COMP_CONFIG['inCompMax'] < included:
        continue

    elem = 'pas' if elem_flag == 2 or elem == 255 else ELEM_IDS[elem]
    OLD_SKILLS[sname] = {
        'elem': elem
    }

stat_config = COMP_CONFIG['skillPowers']
for d_id, line_start in enumerate(range(stat_config['begin'], stat_config['end'], stat_config['length'])):
    line = NEW_SKILLS[line_start:line_start + stat_config['length']]
    sname, included = SKILL_IDS[d_id].split('\t')
    included = int(included)

    cost_type, cost = struct.unpack('<3x2B', line[0x00:0x05])
    acc, min_hit, max_hit = struct.unpack('<3Bx', line[0x0E:0x12])
    power, = struct.unpack('<H', line[0x12:0x14])
    ail_acc, = struct.unpack('<B', line[0x19:0x1A])
    ailment, = struct.unpack('<B', line[0x1C:0x1D])
    crit, = struct.unpack('<B', line[0x25:0x26])

    if included == 0 or COMP_CONFIG['inCompMax'] < included:
        continue

    OLD_SKILLS[sname].update({
        'cost': cost,
        'acc': acc,
        'min': min_hit,
        'max': max_hit,
        'pow': power,
        'mod': ail_acc,
        'effect': ailment,
        'crit': crit
    })

with open(f"dumps/{COMP_CONFIG['skillRanksFile']}", 'rb') as binfile:
    NEW_SKILLS = binfile.read()

stat_config = COMP_CONFIG['skillRanks']
for d_id, line_start in enumerate(range(stat_config['begin'], stat_config['end'], stat_config['length'])):
    line = NEW_SKILLS[line_start:line_start + stat_config['length']]
    sname, included = SKILL_IDS[d_id].split('\t')
    rank, = struct.unpack('<B', line[0x00:0x01])

    if rank != 0:
        OLD_SKILLS[sname]['rank'] = rank

with open('new-skill-data.json', 'w+') as jsonfile:
    json.dump(OLD_SKILLS, jsonfile, indent=2, sort_keys=True)
