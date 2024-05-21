#!/usr/bin/python3
import struct
import json
from shared import load_id_file

SAME_FUN = lambda x: x
COMMON_KEYS = {
    1: ('cost', lambda x: 1000 + x),
    2: ('cost', lambda x: 2000 + x),
    4: ('acc', SAME_FUN),
    44: ('mod', lambda x: 2000 + x), # Splash damage
    63: ('mod', SAME_FUN),
    72: ('pow', SAME_FUN),
    74: ('pow', SAME_FUN), # Healing power
    83: ('min', SAME_FUN),
    84: ('max', SAME_FUN),
    164: ('none', SAME_FUN), # Ailment or cure
    206: ('none', SAME_FUN), # Magic damage
    281: ('mod', lambda x: 2000 + x),  # Boost, Amp
    501: ('none', SAME_FUN), # Ailment
    505: ('cost', SAME_FUN),
    539: ('mod', SAME_FUN)
}

GAME = 'pq'

with open(f"configs/{GAME}-comp-config.json") as jsonfile:
    COMP_CONFIG = json.load(jsonfile)

SKILL_IDS = load_id_file(COMP_CONFIG['skillIds'])
OLD_SKILLS = {}
TEMP_KEYS = {}
EXAMPLE_SKILL = {}
COMMON_SKILLS = { 'Name': {
    'id': 0,
    'elem': 'Element',
    'rank': 'Rank',
    'cost': 'Cost',
    'pow': 'Power',
    'min': 'Min Hit',
    'max': 'Max Hit',
    'acc': 'Accura',
    'crit': 'Crit',
    'mod': 'Add Amt',
    'targ': 'Target',
    'add': 'Add Eff',
    'eff': 'Effect',
    'desc': 'Description'
} }

for fname in COMP_CONFIG['skillData']:
    with open(f"../../../megaten-fusion-tool/src/app/{fname}") as jsonfile:
        OLD_SKILLS.update(json.load(jsonfile))
with open(f"../../../megaten-fusion-tool/src/app/{COMP_CONFIG['skillCodes']}") as jsonfile:
    SKILL_CODES = { y: int(x) for x, y in json.load(jsonfile).items() }
with open(COMP_CONFIG['skillDump']['file'], 'rb') as binfile:
    NEW_SKILLS = binfile.read()

SEEN = { x: False for x in OLD_SKILLS }
SEEN['Name'] = True

LINE_LEN = COMP_CONFIG['skillDump']['length']
START_OFFSET = COMP_CONFIG['skillDump']['start']
END_OFFSET = COMP_CONFIG['skillDump']['end']
if END_OFFSET == -1:
    END_OFFSET = len(NEW_SKILLS)
TRAIT_LEN = (LINE_LEN - 0x28) >> 5

for s_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_SKILLS[line_start:line_start + LINE_LEN]
    sname, included = SKILL_IDS[s_id].split('\t')
    header = struct.unpack('<10L', line[0x00:0x28])
    parts = struct.unpack(f"<{TRAIT_LEN << 3}l", line[0x28:LINE_LEN])

    if int(included) < 1:
        continue

    if sname in SEEN and sname not in COMMON_SKILLS:
        SEEN[sname] = True
        COMMON_SKILLS[sname] = {
            'id': s_id,
            'rank': (90 if sname in SKILL_CODES else 99) if 'unique' in OLD_SKILLS[sname] else 0,
            'elem': OLD_SKILLS[sname]['elem'],
            'targ': OLD_SKILLS[sname].get('target', ''),
            'desc': OLD_SKILLS[sname]['effect']
        }

    for i in range(0, TRAIT_LEN << 3, TRAIT_LEN):
        key, val = parts[i:i + 2]
        if key == 0:
            continue
        if key in COMMON_KEYS:
            COMMON_SKILLS[sname][COMMON_KEYS[key][0]] = COMMON_KEYS[key][1](val)
        else:
            if key not in TEMP_KEYS:
                TEMP_KEYS[key] = []
                EXAMPLE_SKILL[key] = f"{s_id}-{sname}"
            TEMP_KEYS[key].append(f"{s_id} {sname} {val}")

for key, vals in TEMP_KEYS.items():
    print(str(key).zfill(3), EXAMPLE_SKILL[key], ', '.join(vals), sep='\t')
for sname, seen in SEEN.items():
    if not seen:
        print('Not seen:', sname)

LINES = []
DISPLAY_KEYS = ['elem', 'rank', 'cost', 'pow', 'min', 'max', 'acc', 'crit', 'mod', 'targ', 'add', 'eff', 'desc']
for sname, entry in COMMON_SKILLS.items():
    if sname in SEEN:
        LINES.append('\t'.join([str(entry['id']), sname, '\t'.join(str(entry.get(x, 0)) for x in DISPLAY_KEYS)]))

with open('new-skill-data.json', 'w+') as jsonfile:
    jsonfile.write('\n'.join(LINES))
