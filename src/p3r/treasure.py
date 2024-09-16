#!/usr/bin/python3
from shared import iterate_int_tsvfile, load_item_codes, load_item_descs, save_ordered_demons

GAME = 'Astrea'
ITEMS = load_item_codes('en')

FNAME = 'Content/{}/Activity/{}.tsv'
FLOORS = []
for floor_set in ['EndFloors', 'SpecialFloors']:
    with open(FNAME.format(GAME, floor_set)) as tsvfile:
        FLOORS.append({ x.split('\t')[0]: x.split('\t')[1].strip() for x in tsvfile })
END_FLOORS, SPECIAL_FLOORS = FLOORS
END_FLOORS = { int(x): y for x, y in END_FLOORS.items() }
SPECIAL_FLOORS = { int(x): y for x, y in SPECIAL_FLOORS.items() }

FNAME = 'Content/{}/Field/Data/DataTable/DT_FldDungeon{}.tsv'
DROPS = []
for line in iterate_int_tsvfile(FNAME.format(GAME, 'TBoxItem'), skip_first=False):
    item_name = ITEMS.get(line['itemID'], f"item{line['itemID']}")
    item_count = f" x{line['itemNum']}" if line['itemNum'] != 1 else ''
    DROPS.append(item_name + item_count)

CHESTS = {}
MAX_CHEST = 0
for line in iterate_int_tsvfile(FNAME.format(GAME, 'TBoxPac'), skip_first=False):
    MAX_CHEST = max(MAX_CHEST, line['pacID'])
    if line['pacID'] not in CHESTS:
        CHESTS[line['pacID']] = []
    drop_chance = f"{DROPS[line['tboxID']]} ({line['probability']}%)"
    if line['probability'] > 0:
        chests = CHESTS[line['pacID']].append(drop_chance)
CHESTS = [CHESTS.get(x, []) for x in range(MAX_CHEST + 1)]

FLOORS = []
for floor, line in enumerate(iterate_int_tsvfile(FNAME.format(GAME, 'Floor'))):
    if floor > 152:
        break
    if floor in END_FLOORS or floor in SPECIAL_FLOORS:
        FLOORS.append([])
        continue
    # 'tboxPack', 'rareTboxPack', 'jewelryTboxPack', 'primFieldTboxPack', 'medal2TboxPack',
    FLOORS.append(CHESTS[line['tboxPack']])

def find_area(floor):
    min_floor = 0
    for max_floor, area in END_FLOORS.items():
        if floor <= max_floor:
            return area, min_floor
        min_floor = max_floor
    return '???', min_floor

for floor, chest in enumerate(FLOORS):
    area, min_floor = find_area(floor)
    print(f"{area} {floor - min_floor}", ', '.join(chest))
