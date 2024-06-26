#!/usr/bin/python3
import struct
import json
from shared import printif_notequal, save_ordered_demons, load_comp_config, check_resists

GAME = 'p5r'
GAME_TYPE = GAME[:2]
BIG_ENDI = GAME == 'p5'
COMP_CONFIG = load_comp_config(f"configs/{GAME}-comp-config.json")
DATA_DIR = '../../../megaten-fusion-tool/src/app/{}'
TOOL_DEMONS = {}
TRAITS = []

for fname in COMP_CONFIG['demonData']:
    with open(DATA_DIR.format(fname)) as jsonfile:
        TOOL_DEMONS.update(json.load(jsonfile))
with open(f"dumps/{GAME}-demon-data.bin", 'rb') as binfile:
    GAME_DEMONS = binfile.read()
with open(f"dumps/{GAME}-enemy-data.bin", 'rb') as binfile:
    GAME_ENEMIES = binfile.read()

datasets = []

with open(f"{GAME_TYPE}-data/{COMP_CONFIG['demonIds']}") as tsvfile:
    DEMON_IDS = ['BLANK\t0'] + [x.strip() for x in tsvfile]
for fname in [COMP_CONFIG['skillEffects'], 'race-ids.tsv', 'inherit-ids.tsv', 'skillcard-effects.tsv']:
    with open(f"{GAME_TYPE}-data/{fname}") as tsvfile:
        datasets.append(['BLANK'] + [x.strip().split('\t')[0] for x in tsvfile])

SKILL_IDS, RACE_IDS, INHERIT_IDS, SKILLCARD_IDS = datasets
SEEN_DEMONS = { x: False for x in TOOL_DEMONS }

if GAME == 'p3a':
    for dname, entry in TOOL_DEMONS.items():
        nskills = sorted(entry['skills'].items(), key=lambda x: x[1])
        for i, sname in enumerate(x for x, y in nskills if 2 <= y and y < 1000):
            entry['skills'][sname] = entry['lvl'] + i + 1

    with open(DATA_DIR.format('p3/data/ans-demon-data.json')) as jsonfile:
        TOOL_DEMONS.update(json.load(jsonfile))

if GAME == 'p5':
    SKILL_IDS[946] = 'Pressing Stance'
    SKILL_IDS[953] = 'Snipe'
    SKILL_IDS[954] = 'Cripple'
if GAME == 'p5r':
    with open(f"{GAME_TYPE}-data/trait-effects.tsv") as tsvfile:
        TRAITS = ['BLANK'] + [x.strip().split('\t')[0] for x in tsvfile]

check_resists(GAME_ENEMIES, TOOL_DEMONS, DEMON_IDS, COMP_CONFIG['demonResists'], COMP_CONFIG, big_endian=BIG_ENDI)

stat_config = COMP_CONFIG['demonStats']
for d_id, line_start in enumerate(range(stat_config['begin'], stat_config['end'], stat_config['length'])):
    line = GAME_DEMONS[line_start:line_start + stat_config['length']]
    dname, in_comp = DEMON_IDS[d_id].split('\t')

    if int(in_comp) != 1:
        continue

    demon = TOOL_DEMONS[dname]
    SEEN_DEMONS[dname] = True

    race_id, dlvl = struct.unpack('<2B', line[0x02:0x04])
    stats = struct.unpack('<5B', line[0x04:0x09])
    inherits, = struct.unpack('<1B', line[0x0B:0x0C] if GAME == 'p5' else line[0x0A:0x0B])

    printif_notequal(dname, 'race', demon['race'].replace(' P', ''), RACE_IDS[race_id])
    printif_notequal(dname, 'lvl', demon['lvl'], dlvl)
    printif_notequal(dname, 'stats', demon['stats'], list(stats))
    printif_notequal(dname, 'inherits', demon['inherits'], INHERIT_IDS[inherits])

stat_config = COMP_CONFIG['demonSkills']
for d_id, line_start in enumerate(range(stat_config['begin'], stat_config['end'], stat_config['length'])):
    line = GAME_DEMONS[line_start:line_start + stat_config['length']]
    dname, in_comp = DEMON_IDS[d_id].split('\t')

    if int(in_comp) != 1:
        continue

    demon = TOOL_DEMONS[dname]
    SEEN_DEMONS[dname] = True

    growths = struct.unpack('<5B', line[0x00:0x05])

    if GAME == 'p5r':
        trait, = struct.unpack('<1B', line[0x08:0x09])
        printif_notequal(dname, 'trait', TRAITS[trait], demon['trait'])
        learned = struct.unpack('<30H', line[0x0A:0x46])
    else:
        learned = struct.unpack(f"{'>' if BIG_ENDI else '<'}32H", line[0x06:0x46])

    skills = demon['skills']
    seen_skills = []

    for i in range(0, len(learned), 2):
        slvl, s_id = learned[i:i + 2]

        if s_id == 0:
            continue
        if s_id > 1679:
            s_id -= 1679
            sname = SKILLCARD_IDS[s_id]
            slvl -= 1280 - demon['lvl']

            if sname not in demon['skills']:
                print(dname, 'skillcard', sname, demon['skills'])
            printif_notequal(dname, 'cardlvl', demon['cardlvl'], slvl)
            
            continue
        else:
            sname = SKILL_IDS[s_id]
            slvl = slvl >> 8 if BIG_ENDI else slvl & 0xFF
            slvl = (i + 2) / 20 if slvl == 0 else slvl + demon['lvl']

        seen_skills.append(sname)

        if sname not in skills or skills[sname] != slvl:
            print(dname, sname, slvl, skills)
        else:
            skills[sname] = slvl

    printif_notequal(dname, 'skills', sorted(x for x, y in skills.items() if y < 1000), sorted(seen_skills))

for dname, seen in SEEN_DEMONS.items():
    if not seen:
        print(dname)

save_ordered_demons(TOOL_DEMONS, f"{GAME}-demon-data.json")
