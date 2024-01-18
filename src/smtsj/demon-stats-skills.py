#!/usr/bin/python3
import struct
import json
from shared import printif_notequal, save_ordered_demons

LINE_LEN = 0x28
START_OFFSET = 0x00 + 0*LINE_LEN
END_OFFSET = 0*LINE_LEN

with open('data/demon-data.json') as jsonfile:
    OLD_DEMONS = json.load(jsonfile)
with open('data/redux-demon-data.json') as jsonfile:
    OLD_DEMONS.update(json.load(jsonfile))
with open('data/demon-stats-skills.bin', 'rb') as binfile:
    NEW_DEMONS = binfile.read()
with open('data/demon-ids.tsv') as tsvfile:
    DEMON_IDS = ['BLANK\t0'] + [x.strip() for x in tsvfile]
with open('data/skill-ids.tsv') as tsvfile:
    SKILL_IDS = ['BLANK'] + [x.strip() for x in tsvfile]

for d_id, line_start in enumerate(range(START_OFFSET, LINE_LEN * len(DEMON_IDS), LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, in_comp = DEMON_IDS[d_id].split('\t')

    if int(in_comp) != 1:
        continue

    demon = OLD_DEMONS[dname]

    dlvl = struct.unpack('<1B', line[0x00:0x01])[0]
    stats = struct.unpack('<5B', line[0x01:0x06])
    innate = struct.unpack('<3H', line[0x10:0x16])

    printif_notequal(dname, 'lvl', demon['lvl'], dlvl)
    printif_notequal(dname, 'stats', demon['stats'][2:], list(stats))

    skills = demon['skills']

    for i, s_id in enumerate(innate):
        sname = SKILL_IDS[s_id]
        if s_id == 0:
            continue
        if skills[i] != sname:
            print(dname, sname, 0, skills)

save_ordered_demons(OLD_DEMONS, 'demon-data.json')
