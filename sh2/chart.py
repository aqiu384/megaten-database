#!/usr/bin/python3
import json

RACES = []
TABLE = []
ELEMS = ['Melon', 'B-Hawaii', 'Lemon', 'Strawberry', 'Milky']

with open('sh2-data - chart.tsv') as tsvfile:
    for i, line in enumerate(tsvfile):
        parts = line.split('\t')[1:]
        parts[-1] = parts[-1].strip()
        parts = [x for x in parts]

        if i == 0:
            RACES = parts
            continue

        TABLE.append(parts)

for r in range(len(TABLE)):
    for c in range(len(TABLE)):
        if TABLE[r][c] != TABLE[c][r]:
            print(RACES[r], RACES[c], TABLE[r][c])
        if TABLE[r][c] == '' or TABLE[r][c] == 'XXXX':
            TABLE[r][c] = '-'
            TABLE[c][r] = '-'

NRACES = [''.join(('|' + x + '|,        ')[:10] for x in RACES[:-5]).strip()[1:-2]]
NTABLE = []
ETABLE = []

for r in range(len(TABLE) - 5):
    row = TABLE[r][:r + 1]
    row = '[' + ''.join(('|' + x + '|,        ')[:10] for x in row).strip()[:-1] + ']'
    NTABLE.append(row)

    row = TABLE[r][-5:]
    row = '[' + ''.join((' ' + str(int(x)) + ', ')[-4:] for x in row)[:-2] + ']'
    ETABLE.append(row)

OTEXT = json.dumps({ 'races': NRACES, 'table': NTABLE }, indent=2, sort_keys=True)
OTEXT = 'const SH2_FUSION_CHART = ' + OTEXT.replace('"[', '[').replace(']"', ']').replace('|', '"').replace('0', '-')

with open('../docs/sh2/fusion-chart.js', 'w+') as jsonfile:
    for elem in ELEMS:
        OTEXT = OTEXT.replace(elem, elem + ' Frost')
    jsonfile.write(OTEXT)

OTEXT = json.dumps({ 'elems': RACES[-5:], 'races': RACES[:-5], 'table': ETABLE }, indent=2, sort_keys=True)
OTEXT = 'const SH2_ELEMENT_CHART = ' + OTEXT.replace('"[', '[').replace(']"', ']')

with open('../docs/sh2/element-chart.js', 'w+') as jsonfile:
    for elem in ELEMS:
        OTEXT = OTEXT.replace(elem, elem + ' Frost')
    jsonfile.write(OTEXT)
