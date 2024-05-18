#!/usr/bin/python3
import struct
import json
from shared import printif_notequal, save_ordered_demons, load_comp_config, check_resists

GAME_PREFIX = 'p4g'
GAME_TYPE = GAME_PREFIX[:2]
COMP_CONFIG = load_comp_config(f"configs/{GAME_PREFIX}-comp-config.json")
DATA_DIR = '../../../megaten-fusion-tool/src/app/{}'
TOOL_DEMONS = {}

for fname in COMP_CONFIG['enemyData']:
    with open(DATA_DIR.format(fname)) as jsonfile:
        TOOL_DEMONS.update(json.load(jsonfile))
with open(f"dumps/{GAME_PREFIX}-enemy-data.bin", 'rb') as binfile:
    GAME_ENEMIES = binfile.read()

datasets = []

with open(f"{GAME_TYPE}-data/{COMP_CONFIG['enemyIds']}") as tsvfile:
    DEMON_IDS = ['BLANK\t0'] + [x.strip() for x in tsvfile]
for fname in [COMP_CONFIG['skillEffects'], 'race-ids.tsv', 'item-effects.tsv']:
    with open(f"{GAME_TYPE}-data/{fname}") as tsvfile:
        datasets.append(['BLANK'] + [x.strip().split('\t')[0] for x in tsvfile])

SKILL_IDS, RACE_IDS, ITEM_IDS = datasets
SEEN_DEMONS = { x: False for x in TOOL_DEMONS }

stat_config = COMP_CONFIG['enemyStats']
for d_id, line_start in enumerate(range(stat_config['begin'], stat_config['end'], stat_config['length'])):
    line = GAME_ENEMIES[line_start:line_start + stat_config['length']]
    dname, in_comp = DEMON_IDS[d_id].split('\t')

    if int(in_comp) < 1:
        continue

    demon = TOOL_DEMONS[dname]
    SEEN_DEMONS[dname] = True

    if GAME_PREFIX == 'p5r':
        race_id = struct.unpack('<1H', line[0x04:0x06])[0]
        dlvl = struct.unpack('<1H', line[0x06:0x08])[0]
        stats = struct.unpack('<2I5B', line[0x08:0x15])
        innate = struct.unpack('<8H', line[0x16:0x26])
        exp, yen = struct.unpack('<2H', line[0x26:0x2A])
        drops = []
    else:
        race_id = struct.unpack('<1B', line[0x02:0x03])[0]
        dlvl = struct.unpack('<1B', line[0x03:0x04])[0]
        stats = struct.unpack('<2H5B', line[0x04:0x0D])
        innate = struct.unpack('<8H', line[0x0E:0x1E])
        exp, yen = struct.unpack('<2H', line[0x1E:0x22])
        drops = struct.unpack('<8H', line[0x22:0x32])

    if GAME_TYPE == 'p3':
        temp = exp
        exp = yen
        yen = temp

    printif_notequal(dname, 'race', demon['race'].replace(' P', ''), RACE_IDS[race_id])
    printif_notequal(dname, 'lvl', demon['lvl'], dlvl)
    printif_notequal(dname, 'stats', demon['stats'], list(stats))
    printif_notequal(dname, 'exp', demon['exp'], exp)
    printif_notequal(dname, 'yen', demon.get('price', 0), yen)

    if ' P' in demon['race']:
        continue

    innate = [SKILL_IDS[s_id] for s_id in innate if s_id != 0]
    old_skills = demon['skills'][1 if GAME_TYPE == 'p3' else 0:]
    printif_notequal(dname, 'skills', old_skills, innate)

    old_drops = demon.get('gem', '-').split(', ')
    if 'material' in demon:
        old_drops.append(demon['material'])
    for i in range(0, len(drops), 2):
        i_id, i_chance = drops[i:i + 2]

        if i_id == 0:
            continue

        i_id -= COMP_CONFIG['itemsBegin']
        i_chance *= 0.5
        iname = ITEM_IDS[i_id]

        if iname not in old_drops:
            print(dname, 'drop', iname, old_drops)

if GAME_PREFIX == 'p5r':
    with open(f"dumps/{GAME_PREFIX}-enemy-resists.bin", 'rb') as binfile:
        GAME_ENEMIES = binfile.read()
check_resists(GAME_ENEMIES, TOOL_DEMONS, DEMON_IDS, COMP_CONFIG['enemyResists'], COMP_CONFIG)

for dname, seen in SEEN_DEMONS.items():
    if not seen:
        print(dname)

save_ordered_demons(TOOL_DEMONS, f"{GAME_PREFIX}-enemy-data.json")
