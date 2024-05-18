#!/usr/bin/python3
import struct
from shared import load_comp_config

GAME = 'p3p'
GAME_TYPE = GAME[:2]
ENDI = '>' if GAME == 'p5' else '<'
COMP_CONFIG = load_comp_config(f"configs/{GAME}-comp-config.json")

with open(f"dumps/{GAME}-demon-data.bin", 'rb') as binfile:
    GAME_DEMONS = binfile.read()

with open(f"{GAME_TYPE}-data/party-ids.tsv") as tsvfile:
    DEMON_IDS = [x.strip() for x in tsvfile]
with open(f"{GAME_TYPE}-data/{COMP_CONFIG['skillEffects']}") as tsvfile:
    SKILL_IDS = ['BLANK'] + [x.strip().split('\t')[0] for x in tsvfile]

stat_config = COMP_CONFIG['partySkills']
for d_id, line_start in enumerate(range(stat_config['begin'], stat_config['end'], stat_config['length'])):
    line = GAME_DEMONS[line_start:line_start + stat_config['length']]
    dname, included = DEMON_IDS[d_id].split('\t')
    included = int(included)

    if included == 0 or COMP_CONFIG['includedMax'] < included:
        continue

    new_d_id, nines = struct.unpack(f"{ENDI}2H", line[0x00:0x04])
    stats = [0] * 5
    skills = {}

    innate_count = 0
    for skill_start in range(0x04, 0x04 + 0x04 * 33, 0x04):
        slvl, sflag, sname = struct.unpack(f"{ENDI}BBH", line[skill_start:skill_start + 0x04])

        if sflag != 0 and sflag < 3:
            if slvl == 0:
                innate_count += 1
                slvl = innate_count / 10
            sname = SKILL_IDS[sname & 0x0FFF]
            skills[sname] = slvl if sflag == 1 else (slvl * 10 - 1) / 10
            print(dname, sname, skills[sname])

    for dlvl, grow_start in enumerate(range(0x04 + 0x04 * 32, stat_config['length'], 0x05)):
        growths = struct.unpack('<5B', line[grow_start:grow_start + 0x05])
        for i in range(len(stats)):
            stats[i] += growths[i]
        print(dname, dlvl + 2, stats)
