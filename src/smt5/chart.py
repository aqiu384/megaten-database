#!/usr/bin/python3
import struct
import json

ELEMS = [
    'Erthys',
    'Aeros',
    'Aquans',
    'Flaemis'
]

RACES = [
    'Herald',
    'Megami',
    'Avian',
    'Divine',
    'Yoma',
    'Vile',
    'Raptor',
    'Deity',
    'Wargod',
    'Avatar',
    'Holy',
    'Genma',
    'Fairy',
    'Beast',
    'Jirae',
    'Fiend',
    'Jaki',
    'Wilder',
    'Fury',
    'Lady',
    'Dragon',
    'Kishin',
    'Kunitsu',
    'Femme',
    'Brute',
    'Fallen',
    'Night',
    'Snake',
    'Tyrant',
    'Drake',
    'Haunt',
    'Foul'
]

def load_id_file(fname):
    with open('Content/Blueprints/Gamedata/BinTable/' + fname) as tsvfile:
        next(tsvfile)
        return [x.split('\t')[0].strip() for x in tsvfile]

RACE_IDS = load_id_file('Common/DevilRace.tsv')
DEMON_IDS = load_id_file('Common/CharacterName.tsv')
DIFF_RACE_START = 0x85
SAME_RACE_START = 0x805
ELEMENT_START = 0x895
SPECIAL_START = 0xA95
UNKNOWN_START = 0xCD5

with open('Content/Blueprints/Gamedata/BinTable/Unite/UniteTable.bin', 'rb') as binfile:
    NEW_FUSIONS = binfile.read()

fusion_lookup = { x: {} for x in RACE_IDS }
elem_lookup = { x: {} for x in RACE_IDS }
special_lookup = {}

for i in range(DIFF_RACE_START + 0x10, SAME_RACE_START, 4):
    race1, race2, raceR = struct.unpack('<BBH', NEW_FUSIONS[i:i + 4])
    race1 = RACE_IDS[race1]
    race2 = RACE_IDS[race2]
    raceR = RACE_IDS[raceR]
    fusion_lookup[race1][race2] = raceR
    fusion_lookup[race2][race1] = raceR

for i in range(SAME_RACE_START + 0x10, ELEMENT_START, 4):
    race1, race2, elem = struct.unpack('<BBH', NEW_FUSIONS[i:i + 4])
    race1 = RACE_IDS[race1]
    race2 = RACE_IDS[race2]
    elem = DEMON_IDS[elem]
    fusion_lookup[race1][race2] = elem

for i in range(ELEMENT_START + 0x10, SPECIAL_START, 4):
    race1, elem, rank = struct.unpack('<BHB', NEW_FUSIONS[i:i + 4])
    race1 = RACE_IDS[race1]
    elem = DEMON_IDS[elem]
    elem_lookup[race1][elem] = 1 if rank == 1 else -1

for i in range(SPECIAL_START + 0x10, UNKNOWN_START - 12, 12):
    ingreds = struct.unpack('<6H', NEW_FUSIONS[i:i + 12])
    ingreds = [DEMON_IDS[x] for x in ingreds[1:] if x > 0]
    special_lookup[ingreds[-1]] = ingreds[:-1]

NRACES = [''.join(('|' + x + '|,        ')[:10] for x in RACES).strip()[1:-2]]
ERACES = []
NTABLE = []
ETABLE = []

for i, race1 in enumerate(RACES):
    row = [fusion_lookup[race1].get(race2, '-') for race2 in RACES[:i + 1]]
    row = '[' + ''.join(('|' + x + '|,        ')[:10] for x in row).strip()[:-1] + ']'
    NTABLE.append(row)

for race1 in RACES:
    row = [elem_lookup[race1].get(elem, 0) for elem in ELEMS]

    if row[0] != 0:
        row = '[' + ''.join((' ' + str(int(x)) + ', ')[-4:] for x in row)[:-2] + ']'
        ERACES.append(race1)
        ETABLE.append(row)

with open('fusion-chart.json', 'w+') as jsonfile:
    OTEXT = json.dumps({ 'races': NRACES, 'table': NTABLE }, indent=2, sort_keys=True)
    OTEXT = OTEXT.replace('"[', '[').replace(']"', ']').replace('|', '"')
    jsonfile.write(OTEXT)

with open('element-chart.json', 'w+') as jsonfile:
    OTEXT = json.dumps({ 'elems': ELEMS, 'races': ERACES, 'table': ETABLE }, indent=2, sort_keys=True)
    OTEXT = OTEXT.replace('"[', '[').replace(']"', ']')
    jsonfile.write(OTEXT)

for result, recipe in special_lookup.items():
    special_lookup[result] = '[|' + '|, |'.join(recipe) + '|]'

with open('new-special-recipes.json', 'w+') as jsonfile:
    OTEXT = json.dumps(special_lookup, indent=2, sort_keys=True)
    OTEXT = OTEXT.replace('"[', '[').replace(']"', ']').replace('|', '"')
    jsonfile.write(OTEXT)
