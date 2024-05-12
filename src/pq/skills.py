#!/usr/bin/python3
import struct
import json
from shared import load_id_file, printif_notequal, save_ordered_demons

SKILL_IDS = load_id_file('skillnametable.tsv')

with open('../../../megaten-fusion-tool/src/app/pq/data/skill-data.json') as jsonfile:
    OLD_SKILLS = json.load(jsonfile)

LINE_LEN = 0x188
START_OFFSET = 0x00
END_OFFSET = START_OFFSET + 1376 * LINE_LEN

TEMP_KEYS = {}
EXAMPLE_SKILL = {}

with open('pq1-data/battle/table/skilltable.bin', 'rb') as binfile:
    NEW_SKILLS = binfile.read()

for s_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_SKILLS[line_start:line_start + LINE_LEN]
    sname, included = SKILL_IDS[s_id].split('\t')

    header = struct.unpack('<10L', line[0x00:0x28])
    parts = struct.unpack('<88l', line[0x28:0x188])

    if int(included) < 1:
        continue

    for i in range(0, 88, 11):
        key, val = parts[i:i + 2]
        # print(s_id, sname, key, val)

        if key == 0:
            continue

        if key not in TEMP_KEYS:
            TEMP_KEYS[key] = []
            EXAMPLE_SKILL[key] = f"{s_id}-{sname}"
        TEMP_KEYS[key].append(f"{s_id} {sname} {val}")

for key, vals in TEMP_KEYS.items():
    print(str(key).zfill(3), EXAMPLE_SKILL[key], ', '.join(vals), sep='\t')
