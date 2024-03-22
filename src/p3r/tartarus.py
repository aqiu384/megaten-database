#!/usr/bin/python3
import json
from shared import table_row, table_header
from shopper import load_shops_to_items

AREAS = [
    'Thebel',
    'Arqa I',
    'Arqa II',
    'Yabbashah I',
    'Yabbashah II',
    'Tziah I',
    'Tziah II',
    'Harabah I',
    'Harabah II',
    'Adamah I',
    'Adamah II'
]

CHESTS = [
    '',
    'Breakable',
    'Common',
    'Rare',
    'Gem',
    'Material',
    '0-lock',
    '1-lock',
    '2-lock',
    '3-lock'
]

def index_floor(floor):
    if floor in CHESTS:
        return CHESTS.index(floor)
    chest = ''
    if ' ' in floor:
        floor, chest = floor.split(' ')
    start = floor.replace('D', '30').replace('P', '40')
    end = start
    if '-' in start:
        start, end = start.split('-')
    return 10000 * int(start) + 10 * int(end) + int(CHESTS.index(chest))

def format_drops(drops):
    return ', '.join(f"{x} ({y}%)" for x, y in drops.items()) if len(drops) > 0 else '-'

with open('../../../megaten-fusion-tool/src/app/p3r/data/comp-config.json') as jsonfile:
    CONFIG = json.load(jsonfile)

RESIST_ELEMS = [x.title()[:2] for x in CONFIG['resistElems']]
AILMENTS = [x.title()[:2] for x in CONFIG['ailments']]
enemy_headers = ['Floors', 'Name', 'Lv.', 'Exp', 'HP', 'SP'] + RESIST_ELEMS[:-1] + AILMENTS + ['Drops']
chest_headers = ['Floors', 'Chest', 'Drops']

chests = load_shops_to_items()

print(f"# Persona 3 Reload")
print(f"## Tartarus")
print('''* For each section of Tartarus
  * Encounterable enemies
  * Treasure chests
  * Suggested strategies''')

with open('../../../megaten-fusion-tool/src/app/p3r/data/enemy-data.json') as jsonfile:
    DEMONS = json.load(jsonfile)
for area in AREAS:
    print(f"### {area}")
    prefix = f"{area} "

    rows = []
    print(f"#### Enemies")
    print(table_header(enemy_headers))
    for dname, entry in DEMONS.items():
        if entry['area'].startswith(prefix):
            floor = entry['area'].replace(prefix, '')
            parts = [floor, dname, entry['lvl'], entry['exp'], entry['stats'][0], entry['stats'][1]]
            parts += [x for x in entry['resists'][:-1]]
            parts += [x for x in entry.get('ailments', '------')]
            parts += [format_drops(entry.get('drops',{}))]
            rows.append((100 * index_floor(floor) + entry['lvl'], parts))
    rows.sort(key=lambda x: x[0])
    for row in rows:
        print(table_row(str(x) for x in row[1]))

    rows = []
    print(f"#### Chests")
    print(table_header(chest_headers))
    for chest in chests:
        if chest.startswith(prefix):
            floor = chest.replace(prefix, '')
            floor_num = '-'
            floor_chest = floor
            if ' ' in floor:
                floor_num, floor_chest = floor.split(' ')
            parts = [floor_num, floor_chest, chests[chest]]
            rows.append((index_floor(floor), parts))
    rows.sort(key=lambda x: x[0])
    for row in rows:
        print(table_row(str(x) for x in row[1]))