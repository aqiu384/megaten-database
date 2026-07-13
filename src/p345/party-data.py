#!/usr/bin/python3
import json
import struct
from shared import printif_notequal, load_comp_config

GAME = 'p5r'
GAME_TYPE = GAME[:2]
ENDI = '>' if GAME == 'p5' else '<'
COMP_CONFIG = load_comp_config(f"configs/{GAME}-comp-config.json")
DATA_DIR = '../../../megaten-fusion-tool/src/app/{}'
PARTY_DATA = {}

for fname in COMP_CONFIG['partyData']:
    with open(DATA_DIR.format(fname)) as jsonfile:
        PARTY_DATA.update(json.load(jsonfile))

with open(f"dumps/{GAME}-demon-data.bin", 'rb') as binfile:
    GAME_DEMONS = binfile.read()

with open(f"{GAME_TYPE}-data/{GAME + '-' if GAME == 'p3a' else ''}party-ids.tsv") as tsvfile:
    DEMON_IDS = [x.strip() for x in tsvfile]
with open(f"{GAME_TYPE}-data/{COMP_CONFIG['skillEffects']}") as tsvfile:
    SKILL_IDS = ['BLANK'] + [x.strip().split('\t')[0] for x in tsvfile]

if GAME == 'p5':
    SKILL_IDS[946] = 'Pressing Stance'
    SKILL_IDS[953] = 'Snipe'
    SKILL_IDS[954] = 'Cripple'

stat_config = COMP_CONFIG['partySkills']
for d_id, line_start in enumerate(range(stat_config['begin'], stat_config['end'], stat_config['length'])):
    line = GAME_DEMONS[line_start:line_start + stat_config['length']]
    dname, included = DEMON_IDS[d_id].split('\t')
    included = int(included)

    if included == 0 or COMP_CONFIG['includedMax'] < included:
        continue

    new_d_id, nines = struct.unpack(f"{ENDI}2H", line[0x00:0x04])
    old_demon = PARTY_DATA[dname]
    stats = old_demon['stats']
    base_lvl = old_demon['lvl']
    skills = {}

    prev_slvl = 0
    innate_count = 0
    for skill_start in range(0x04, 0x04 + 0x04 * 33, 0x04):
        slvl, sflag, sname = struct.unpack(f"{ENDI}BBH", line[skill_start:skill_start + 0x04])

        if sflag != 0 and sflag < 3:
            if slvl == 0:
                innate_count += 1
                slvl = innate_count / 10
            sname = SKILL_IDS[sname & 0x0FFF]
            slvl = slvl if sflag == 1 else (slvl * 10 - 1) / 10
            if prev_slvl < slvl and slvl % 1 < 0.85:
                prev_slvl = slvl
                skills[sname] = slvl
                printif_notequal(dname, sname, slvl, old_demon['skills'].get(sname, 0))

    for sname, slvl in old_demon['skills'].items():
        if slvl < 1000:
            printif_notequal(dname, sname, slvl, skills.get(sname, 0))

    for dlvl, grow_start in enumerate(range(0x04 + 0x04 * 32, stat_config['length'], 0x05)):
        growths = struct.unpack('<5B', line[grow_start:grow_start + 0x05])
        dlvl += 2
        if dlvl <= base_lvl:
            continue
        for i in range(len(stats)):
            stats[i] += growths[i]
        if dlvl == 99:
            printif_notequal(dname, 'statsm', stats, old_demon['statsm'])
