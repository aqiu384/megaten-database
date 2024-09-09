#!/usr/bin/python3
import struct
from shared import load_id_file

ELEMS = ['???', 'phy', 'gun', 'fir', 'ice', 'ele', 'for', 'dar', 'alm', 'rec', 'sup', 'spe', 'pas', '???', '???', '???', 'sab']
SKILL_IDS = load_id_file('data/skill-ids.tsv')

with open('dumps/skills.bin', 'rb') as binfile:
    NEW_SKILLS = binfile.read()

LINE_LEN = 0xD8
START_OFFSET = 0x00
END_OFFSET = len(NEW_SKILLS)

for line_start in range(START_OFFSET, END_OFFSET, LINE_LEN):
    line = NEW_SKILLS[line_start:line_start + LINE_LEN]
    s_id, = struct.unpack('<L', line[0x00:0x04])
    sname = SKILL_IDS[s_id - 1000]

    parts = struct.unpack('<54l', line)
    id = parts[0]
    elem = parts[7]
    acc, one, min_hits, max_hits = parts[14:18]
    _, cost, _, power = parts[22:26]

    if sname == '???':
        continue

    print(sname, id, ELEMS[elem], cost, power, min_hits, max_hits, acc, sep='\t')
