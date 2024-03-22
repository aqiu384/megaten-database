#!/usr/bin/python3
import re
import json
from shared import table_row, table_header
from shopper import load_shops_to_items

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
stat_headers = ['Floors', 'Name', 'Lv.', 'Exp', 'HP', 'SP', 'Drops']
resist_headers = ['Floors', 'Name'] + RESIST_ELEMS[:-1] + AILMENTS
chest_headers = ['Floors', 'Chest', 'Drops']

chests = load_shops_to_items()

with open('../../../megaten-fusion-tool/src/app/p3r/data/enemy-data.json') as jsonfile:
    DEMONS = json.load(jsonfile)

def enemy_stats(area):
    prefix = f"{area} "
    rows = []
    print(f"#### Enemy Stats")
    print(table_header(stat_headers))
    for dname, entry in DEMONS.items():
        if entry['area'].startswith(prefix):
            floor = entry['area'].replace(prefix, '')
            parts = [floor, dname, entry['lvl'], entry['exp'], entry['stats'][0], entry['stats'][1], format_drops(entry.get('drops',{}))]
            rows.append((100 * index_floor(floor) + entry['lvl'], parts))
    rows.sort(key=lambda x: x[0])
    for row in rows:
        print(table_row(str(x) for x in row[1]))

def enemy_resists(area):
    prefix = f"{area} "
    rows = []
    print(f"#### Enemy Resistances")
    print(table_header(resist_headers))
    for dname, entry in DEMONS.items():
        if entry['area'].startswith(prefix):
            floor = entry['area'].replace(prefix, '')
            parts = [floor, dname] + [x for x in entry['resists'][:-1]] + [x for x in entry.get('ailments', '------')]
            rows.append((100 * index_floor(floor) + entry['lvl'], parts))
    rows.sort(key=lambda x: x[0])
    for row in rows:
        print(table_row(str(x) for x in row[1]))

def area_chests(area):
    prefix = f"{area} "
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

FILLERS = {
    'enemy_stats': enemy_stats,
    'enemy_resists': enemy_resists,
    'area_chests': area_chests
}

SUBME = re.compile("\{\{ (\w+)\('(.*)'\) \}\}\n")

with open('walkthrough/tartarus.md') as mdfile:
    for line in mdfile:
        matching = SUBME.match(line)
        if matching:
            FILLERS[matching.group(1)](matching.group(2))
        else:
            print(line.strip())
