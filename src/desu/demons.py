#!/usr/bin/python3
import struct
import json
from shared import printif_notequal, load_id_file

GAME = 'dso'

INNATES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
DATA_DIR = '../../../megaten-fusion-tool/src/app/{}'
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

with open(f"configs/{GAME}-comp-config.json") as jsonfile:
    COMP_CONFIG = json.load(jsonfile)

RACES = load_id_file(COMP_CONFIG['raceIds'])
DEMON_IDS = load_id_file(COMP_CONFIG['demonIds'])
SKILL_IDS = load_id_file(COMP_CONFIG['skillIds']['file'])

for fname in COMP_CONFIG['demonData']:
    with open(DATA_DIR.format(fname)) as jsonfile:
        OLD_DEMONS.update(json.load(jsonfile))

SEEN = { x: False for x in OLD_DEMONS }
REV_LOOK = { x: {} for x in RACES }

for dname, entry in OLD_DEMONS.items():
    REV_LOOK[entry['race']][entry['lvl']] = f"{dname}\t1"

with open(COMP_CONFIG['resistDump']['file'], 'rb') as binfile:
    NEW_DEMONS = binfile.read()

LINE_LEN = COMP_CONFIG['resistDump']['length']
START_OFFSET = COMP_CONFIG['resistDump']['start']
END_OFFSET = COMP_CONFIG['resistDump']['end']
if END_OFFSET == 0:
    END_OFFSET = len(NEW_DEMONS)

for r_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    resists = ''.join(RESIST_LVLS[0x7F & x] for x in line)
    RESIST_IDS.append(resists)

with open(COMP_CONFIG['demonDump']['file'], 'rb') as binfile:
    NEW_DEMONS = binfile.read()

LINE_LEN = COMP_CONFIG['demonDump']['length']
START_OFFSET = COMP_CONFIG['demonDump']['start']
END_OFFSET = COMP_CONFIG['demonDump']['end']
if END_OFFSET == 0:
    END_OFFSET = len(NEW_DEMONS)

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, included = DEMON_IDS[d_id].split('\t')

    new_id, comp_id = struct.unpack('<2h', line[0x00:0x04])
    unk_comp = struct.unpack('<8B', line[0x04:0x0C])
    hp_mod, mp_mod = struct.unpack('<2H', line[0x0C:0x10])
    race, race_ind = struct.unpack('<2B', line[0x10:0x12])
    unk_neg, zero, lvl, unk_lvl, resists = struct.unpack('<h4B', line[0x12:0x18])
    stats = struct.unpack('<4B', line[0x18:0x1C])
    stat_grows = struct.unpack('<4B', line[0x1C:0x20])
    skills = struct.unpack('<12B', line[0x20:0x2C])
    unk_skills = struct.unpack('<16B', line[0x2C:0x3C])

    race = RACES[race]
    resists = RESIST_IDS[resists] if resists < len(RESIST_IDS) else '------'
    stat_mods = [round(hp_mod / 25.6) / 10, round(mp_mod / 25.6) / 10]
    # dis_name = REV_LOOK[race].get(lvl, f"{race}_{lvl}\t0")
    # print(d_id, dis_name, sep='\t')
    printif_notequal(d_id, 'd_id', d_id, new_id)

    if int(included) < 1:
        continue

    entry = OLD_DEMONS[dname]
    SEEN[dname] = True
    printif_notequal(dname, 'stat_mods', str(list(stat_mods)), str(entry['growths'][:2]))
    printif_notequal(dname, 'resists', resists, entry['resists'])
    printif_notequal(dname, 'stats', str(list(stats)), str(entry['stats'][3:]))

    old_skills = entry['skills']
    act_start = COMP_CONFIG['skillIds']['activeStart']
    pass_start = COMP_CONFIG['skillIds']['passiveStart']
    invert_skills = { y: x for x, y in old_skills.items() }
    innate_ind = 0
    for i in range(0, 12, 2):
        sname, slvl = skills[i:i + 2]
        if sname == 0:
            continue
        if slvl == 0 or slvl <= lvl:
            slvl = INNATES[innate_ind]
            innate_ind += 1
        sname += (act_start if i < 6 else pass_start)
        sname = SKILL_IDS[sname]
        if old_skills[sname] != slvl:
            print(dname, sname, slvl, old_skills[sname])
        # print(str(sname).zfill(4), invert_skills[slvl], dname, sep='\t')

    # print(d_id, dname)

for dname, seen in SEEN.items():
    if not seen:
        print('Not seen:', dname)
