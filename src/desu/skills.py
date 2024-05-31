#!/usr/bin/python3
import sys
import struct
import json
from shared import load_id_file

GAME = sys.argv[1]
OLD_SKILLS = {}
ELEMS = ['phy', 'fir', 'ice', 'ele', 'for', 'mys', 'spe']
AILMENTS = {
    0: '-',
    1: 'Revive',
    4: 'Paralyze',
    8: 'Stone',
    16: 'Poison',
    32: 'Mute',
    128: 'Freeze',
    256: 'Shock',
    512: 'Brand',
    1024: 'Seal',
    2044: 'Cure',
    2045: 'Cure',
    2048: '???',
    8188: '???',
    8189: '???'
}

with open(f"configs/{GAME}-comp-config.json") as jsonfile:
    COMP_CONFIG = json.load(jsonfile)
for fname in COMP_CONFIG['skillData']:
    with open(f"../../../megaten-fusion-tool/src/app/{fname}") as jsonfile:
        OLD_SKILLS.update(json.load(jsonfile))

SKILL_IDS = load_id_file(COMP_CONFIG['skillIds']['file'])
SEEN = { x: False for x in OLD_SKILLS }

with open(COMP_CONFIG['skillDump']['file'], 'rb') as binfile:
    NEW_SKILLS = binfile.read()

LINE_LEN = COMP_CONFIG['skillDump']['length']
START_OFFSET = COMP_CONFIG['skillDump']['start']
END_OFFSET = COMP_CONFIG['skillDump']['end']
if END_OFFSET == 0:
    END_OFFSET = len(NEW_SKILLS)

def parse_cost(cost):
    suffixes = [5000, 10000, 1000, 0]
    return suffixes[cost[0]] + cost[1]

def parse_req(req):
    prefixes = ['St', 'Ma', 'Vi', 'Ag']
    return f"{prefixes[req[0]]}{req[1]}" if req[0] != 4 else ''

for s_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_SKILLS[line_start:line_start + LINE_LEN]
    sname = SKILL_IDS[s_id]

    if sname == '???' or sname == 'Attack':
        continue

    dmg_type, = struct.unpack('<H', line[0x00:0x02])
    requires = struct.unpack('<4H', line[0x02:0x0A])
    field_use, can_crit = struct.unpack('<2B', line[0x0A:0x0C])
    cost = struct.unpack('<2H', line[0x0C:0x10])
    pwr_stat, elem, acc, hit_area, hit_side = struct.unpack('<5B', line[0x10:0x15])
    unk_pwr = struct.unpack('<3B', line[0x15:0x18])
    min_hits, max_hits, pwr_formula, pwr_base, pwr_add = struct.unpack('<2BH2B', line[0x18:0x1E])
    mp_formula, mp_base, one, ail_flag, ail_hit, ail_type = struct.unpack('<3HBBH', line[0x1E:0x28])
    unk1 = struct.unpack('<20B', line[0x28:0x3C])

    SEEN[sname] = True
    entry = OLD_SKILLS[sname]
    elem = ELEMS[elem]
    parts = [
        s_id, sname, entry['element'], 'target', entry.get('rank', 99), parse_cost(cost), pwr_base, min_hits, max_hits, acc, 'crit', ail_hit,
        'add', AILMENTS[ail_type], entry['effect'], f"{parse_req(requires[:2])} {parse_req(requires[2:])}".strip()
    ]

    print('\t'.join(str(x) for x in parts))

for sname, seen in SEEN.items():
    if not seen:
        print('Not seen:', sname)
