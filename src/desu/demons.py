#!/usr/bin/python3
import math
import struct
import json
from shared import printif_notequal, load_id_file

INNATES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
DATA_DIR = '../../../megaten-fusion-tool/src/app/desu1/data/{}.json'
OLD_DEMONS = {}
RESIST_IDS = []
RESIST_LVLS = {
    0: 'n',
    1: 'r',
    2: 'd',
    3: 's',
    4: 's',
    5: 's',
    70: 's',
    6: '-',
    7: 'w',
}

RACES = load_id_file('dso-data/dso-races.tsv')
DEMON_IDS = load_id_file('dso-data/dso-demons.tsv')
SKILL_IDS = load_id_file('dso-data/dso-skills.tsv')

for fname in ['van-demon-data', 'ove-demon-data']:
    with open(DATA_DIR.format(fname)) as jsonfile:
        OLD_DEMONS.update(json.load(jsonfile))

SEEN = { x: False for x in OLD_DEMONS }
REV_LOOK = { x: {} for x in RACES }

for dname, entry in OLD_DEMONS.items():
    REV_LOOK[entry['race']][entry['lvl']] = f"{dname}\t1"

with open('dumps/dso-demons.bin', 'rb') as binfile:
    NEW_DEMONS = binfile.read()

LINE_LEN = 0x06
START_OFFSET = 0x14 + 233* 0x3C
END_OFFSET = len(NEW_DEMONS)

for r_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    resists = ''.join(RESIST_LVLS[0x7F & x] for x in line)
    RESIST_IDS.append(resists)

LINE_LEN = 0x3C
START_OFFSET = 0x14
END_OFFSET = START_OFFSET + 233 * LINE_LEN

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, included = DEMON_IDS[d_id].split('\t')

    new_id, comp_id = struct.unpack('<2h', line[0x00:0x04])
    # unk1
    hp_mod, mp_mod = struct.unpack('<2H', line[0x0C:0x10])
    race, race_ind = struct.unpack('<2B', line[0x10:0x12])
    unk_neg, zero, lvl, unk3, resists = struct.unpack('<h4B', line[0x12:0x18])
    stats = struct.unpack('<4B', line[0x18:0x1C])
    stat_grows = struct.unpack('<4B', line[0x1C:0x20])
    skills = struct.unpack('<12B', line[0x20:0x2C])
    unk2 = struct.unpack('<16B', line[0x2C:0x3C])

    # print(unk2, dname)

    race = RACES[race]
    resists = RESIST_IDS[resists]
    stat_mods = [round(hp_mod / 25.6) / 10, round(mp_mod / 25.6) / 10]
    # dis_name = REV_LOOK[race].get(lvl, f"{race}_{lvl}\t0")
    printif_notequal(d_id, 'd_id', d_id, new_id)

    if int(included) < 1:
        continue

    entry = OLD_DEMONS[dname]
    SEEN[dname] = True
    printif_notequal(dname, 'stat_mods', str(list(stat_mods)), str(entry['growths'][:2]))
    printif_notequal(dname, 'resists', resists, entry['resists'])
    printif_notequal(dname, 'stats', str(list(stats)), str(entry['stats'][3:]))

    old_skills = entry['skills']
    invert_skills = { y: x for x, y in old_skills.items() }
    innate_ind = 0
    for i in range(0, 12, 2):
        sname, slvl = skills[i:i + 2]
        if sname == 0:
            continue
        if i >= 6:
            sname += 82
        if slvl == 0 or slvl <= lvl:
            slvl = INNATES[innate_ind]
            innate_ind += 1
        sname = SKILL_IDS[sname]
        if old_skills[sname] != slvl:
            print(dname, sname, slvl, old_skills[sname])
        # print(str(sname).zfill(4), invert_skills[slvl], dname, sep='\t')

    # print(d_id, dname)

for dname, seen in SEEN.items():
    if not seen:
        print('Not seen:', dname)
