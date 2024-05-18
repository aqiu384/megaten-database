#!/usr/bin/python3
import struct
import json
from shared import load_id_file

GAME = 'pq2'

with open(f"configs/{GAME}-comp-config.json") as jsonfile:
    COMP_CONFIG = json.load(jsonfile)

DEMON_IDS = load_id_file(COMP_CONFIG['partyIds'])
SKILL_IDS = [x.split('\t')[0] for x in load_id_file(COMP_CONFIG['skillIds'])]
OLD_DEMONS = {}

DUMP_CONFIG = COMP_CONFIG['partyDump']
LINE_LEN = DUMP_CONFIG['length']
SKILL_COUNT = 32

with open(DUMP_CONFIG['file'], 'rb') as binfile:
    NEW_DEMONS = binfile.read()

for d_id, line_start in enumerate(range(DUMP_CONFIG['start'], len(DEMON_IDS) * LINE_LEN, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, included = DEMON_IDS[d_id].split('\t')

    if int(included) != 1:
        continue

    new_d_id, nines = struct.unpack('<2H', line[0x00:0x04])
    stats = [0] * 7
    skills = {}

    for i, skill_start in enumerate(range(0x04, DUMP_CONFIG['statStart'], DUMP_CONFIG['skillLength'])):
        slvl, sflag, sname = struct.unpack('<BBH', line[skill_start:skill_start + 0x04])
        slvl = (i + 1) / 10 if slvl == 0 else slvl
        sname = SKILL_IDS[sname & 0x0FFF]

        if sflag != 0:
            skills[sname] = slvl if sflag == 1 else (slvl * 10 - 1) / 10
            print(dname, sname, skills[sname])

    for dlvl, grow_start in enumerate(range(DUMP_CONFIG['statStart'], LINE_LEN, 28)):
        growths = struct.unpack('<7L', line[grow_start:grow_start + 0x1C])
        for i in range(len(stats)):
            stats[i] += growths[i]
        # print(dname, dlvl + 2, stats)
