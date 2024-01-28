#!/usr/bin/python3
import struct
import json
from shared import printif_notequal, save_ordered_demons, load_comp_config, check_resists

GAME_PREFIX = 'p3p'
COMP_CONFIG = load_comp_config(f"configs/{GAME_PREFIX}-comp-config.json")
TOOL_DEMONS = {}

for fname in COMP_CONFIG['enemyData']:
    with open(f"configs/{fname}") as jsonfile:
        TOOL_DEMONS.update(json.load(jsonfile))
with open(f"dumps/{GAME_PREFIX}-enemy-data.bin", 'rb') as binfile:
    GAME_ENEMIES = binfile.read()

with open(f"data/p3-enemy-ids.tsv") as tsvfile:
    DEMON_IDS = ['BLANK\t0'] + [x.strip() for x in tsvfile]
with open('data/skill-effects.tsv') as tsvfile:
    SKILL_IDS = ['BLANK'] + [x.split('\t')[0] for x in tsvfile]
with open('data/race-ids.tsv') as tsvfile:
    RACE_IDS = ['BLANK'] + [x.strip() for x in tsvfile]
with open('data/item-effects.tsv') as tsvfile:
    ITEM_IDS = ['BLANK'] + [x.split('\t')[0] for x in tsvfile]

SEEN_DEMONS = { x: False for x in TOOL_DEMONS }

stat_config = COMP_CONFIG['enemyStats']
for d_id, line_start in enumerate(range(stat_config['begin'], stat_config['end'], stat_config['length'])):
    line = GAME_ENEMIES[line_start:line_start + stat_config['length']]
    dname, in_comp = DEMON_IDS[d_id].split('\t')

    if int(in_comp) < 1:
        continue

    demon = TOOL_DEMONS[dname]
    SEEN_DEMONS[dname] = True

    race_id = struct.unpack('<1B', line[0x02:0x03])[0]
    dlvl = struct.unpack('<1B', line[0x03:0x04])[0]
    stats = struct.unpack('<2H5B', line[0x04:0x0D])
    innate = struct.unpack('<8H', line[0x0E:0x1E])
    exp = struct.unpack('<1H', line[0x20:0x22])[0]
    drops = struct.unpack('<8H', line[0x22:0x32])

    printif_notequal(dname, 'race', demon['race'].replace(' P', ''), RACE_IDS[race_id])
    printif_notequal(dname, 'lvl', demon['lvl'], dlvl)
    printif_notequal(dname, 'stats', demon['stats'], list(stats))
    printif_notequal(dname, 'exp', demon['exp'], exp)

    if ' P' in demon['race']:
        continue

    innate = [SKILL_IDS[s_id] for s_id in innate if s_id != 0]

    for i in range(0, len(drops), 2):
        i_id, i_chance = drops[i:i + 2]

        if i_id == 0:
            continue

        i_id -= COMP_CONFIG['itemsBegin']
        i_chance *= 0.5
        iname = ITEM_IDS[i_id]

        if iname != 'Malachite':
            printif_notequal(dname, 'drop', demon['gem'], iname)

check_resists(GAME_ENEMIES, TOOL_DEMONS, DEMON_IDS, COMP_CONFIG['enemyResists'], COMP_CONFIG)

for dname, seen in SEEN_DEMONS.items():
    if not seen:
        print(dname)

save_ordered_demons(TOOL_DEMONS, f"{GAME_PREFIX}-enemy-data.json")
