#!/usr/bin/python3
import struct
import json
from shared import load_id_file

GAME = 'pq'

with open(f"configs/{GAME}-comp-config.json") as jsonfile:
    COMP_CONFIG = json.load(jsonfile)

SKILL_IDS = load_id_file(COMP_CONFIG['skillIds'])
OLD_SKILLS = {}
TEMP_KEYS = {}
EXAMPLE_SKILL = {}

for fname in COMP_CONFIG['skillData']:
    with open(f"../../../megaten-fusion-tool/src/app/{fname}") as jsonfile:
        OLD_SKILLS.update(json.load(jsonfile))
with open(COMP_CONFIG['skillDump']['file'], 'rb') as binfile:
    NEW_SKILLS = binfile.read()

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

    for i in range(0, TRAIT_LEN << 3, TRAIT_LEN):
        key, val = parts[i:i + 2]
        if key == 0:
            continue
        if key not in TEMP_KEYS:
            TEMP_KEYS[key] = []
            EXAMPLE_SKILL[key] = f"{s_id}-{sname}"
        TEMP_KEYS[key].append(f"{s_id} {sname} {val}")

for key, vals in TEMP_KEYS.items():
    print(str(key).zfill(3), EXAMPLE_SKILL[key], ', '.join(vals), sep='\t')
