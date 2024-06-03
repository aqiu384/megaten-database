#!/usr/bin/python3
import sys
import struct
import json
from shared import load_comp_config, printif_notequal

GAME = sys.argv[1]
GAME_TYPE = GAME[:2]
BIG_ENDI = GAME == 'p5'
COMP_CONFIG = load_comp_config(f"configs/{GAME}-comp-config.json")
DATA_DIR = '../../../megaten-fusion-tool/src/app/{}'
OLD_SKILLS = {}
ELEM_IDS = COMP_CONFIG['gameResists'] + ['ail'] * len(COMP_CONFIG['gameAilments']) + COMP_CONFIG['gameElems']
ELEM_IDS = [x[:3].lower() for x in ELEM_IDS]
SKILL_PWRS = {}

for fname in COMP_CONFIG['skillData']:
    with open(DATA_DIR.format(fname)) as jsonfile:
        OLD_SKILLS.update(json.load(jsonfile))
with open(f"dumps/{GAME}-skill-data.bin", 'rb') as binfile:
    NEW_SKILLS = binfile.read()
with open(f"{GAME_TYPE}-data/{COMP_CONFIG['skillIds']}") as tsvfile:
    SKILL_IDS = ['BLANK'] + [x.split('\t')[0] for x in tsvfile]
if GAME == 'p5':
    SKILL_IDS[946] = 'Pressing Stance'
    SKILL_IDS[953] = 'Snipe'
    SKILL_IDS[954] = 'Cripple'

SEEN = { x: entry['element'] in ['pas', 'tra'] for x, entry in OLD_SKILLS.items() }

stat_config = COMP_CONFIG['skillPowers']
for s_id, line_start in enumerate(range(stat_config['begin'], stat_config['end'], stat_config['length'])):
    line = NEW_SKILLS[line_start:line_start + stat_config['length']]
    sname = SKILL_IDS[s_id]

    if GAME == 'p5':
        cost_type, cost = struct.unpack('>BxH', line[0x04:0x08])
        acc, min_hit, max_hit, pwr = struct.unpack('>3BxH', line[0x14:0x1A])
        mod, ailment = struct.unpack('>2L', line[0x1C:0x24])
    else: 
        cost_type, cost = struct.unpack('<xBH', line[0x02:0x06])
        acc, min_hit, max_hit, pwr = struct.unpack('<3BxH', line[0x10:0x16])
        mod, ailment = struct.unpack('<BL', line[0x1B:0x20])
    crit, = struct.unpack('<B', line[0x29:0x2A])

    if sname not in SEEN or SEEN[sname]:
        continue

    SEEN[sname] = True
    entry = OLD_SKILLS[sname]
    cost = cost + 1000 if cost_type == 2 else cost
    mod = 0xFF & mod
    SKILL_PWRS[s_id] = [cost, pwr, min_hit, max_hit, acc, crit, mod, ailment]
    printif_notequal(sname, 'cost', cost, entry.get('cost', 0))
    printif_notequal(sname, 'pwr', pwr, entry.get('power', 0))

if GAME == 'p5':
    with open(f"dumps/{COMP_CONFIG['skillRanksFile']}", 'rb') as binfile:
        NEW_SKILLS = binfile.read()

    SEEN = { x: False for x in OLD_SKILLS }
    BLANK_PWR = [0] * 8

    stat_config = COMP_CONFIG['skillElems']
    for s_id, line_start in enumerate(range(stat_config['begin'], stat_config['end'], stat_config['length'])):
        line = NEW_SKILLS[line_start:line_start + stat_config['length']]
        sname = SKILL_IDS[s_id]

        elem, unk_elem, rank = struct.unpack('>3B', line)

        if sname not in SEEN or SEEN[sname]:
            continue

        SEEN[sname] = True
        elem = ELEM_IDS[elem] if elem != 255 else 'pas'
        entry = OLD_SKILLS[sname]
        rank = 99 if rank == 0 else rank
        pwrs = '\t'.join(str(x) for x in SKILL_PWRS.get(s_id, BLANK_PWR))
        print(s_id, sname, elem, entry.get('target', '-'), rank, pwrs, '-', entry.get('add', '-'), entry.get('mod', '-'), sep='\t')

for sname, seen in SEEN.items():
    if not seen:
        print('Not seen:', sname)
