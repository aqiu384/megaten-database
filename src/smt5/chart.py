#!/usr/bin/python3
import json

RACES = []
TABLE = []

with open('smtv-data - chart.tsv') as tsvfile:
    for i, line in enumerate(tsvfile):
        parts = line.split('\t')[1:]
        parts[-1] = parts[-1].strip()
        parts = [x for x in parts]

        if i == 0:
            RACES = parts
            continue

        TABLE.append(parts)

with open('smtv-data - combos.tsv') as tsvfile:
    for line in tsvfile:
        race1, race2, raceR = line.split('\t')
        raceR = raceR.strip()

        r = RACES.index(race1)
        c = RACES.index(race2)
        res = RACES.index(raceR)

        rcrace = TABLE[r][c]
        crrace = TABLE[c][r]

        if rcrace == '' and crrace == '':
            TABLE[r][c] = raceR
            TABLE[c][r] = raceR
        elif rcrace != raceR or crrace != raceR:
            print(race1, race2, raceR, rcrace, crrace)

for r in range(len(TABLE)):
    for c in range(len(TABLE)):
        if TABLE[r][c] != TABLE[c][r]:
            print(RACES[r], RACES[c], TABLE[r][c])
        if TABLE[r][c] == '' or TABLE[r][c] == 'XXXX':
            TABLE[r][c] = '-'
            TABLE[c][r] = '-'

NRACES = [''.join(('|' + x + '|,        ')[:10] for x in RACES[:-4]).strip()[1:-2]]
NTABLE = []
ETABLE = []

for r in range(len(TABLE) - 4):
    row = TABLE[r][:r + 1]
    row = '[' + ''.join(('|' + x + '|,        ')[:10] for x in row).strip()[:-1] + ']'
    NTABLE.append(row)

    row = TABLE[r][-4:]
    row = '[' + ''.join((' ' + str(int(x)) + ', ')[-4:] for x in row)[:-2] + ']'
    ETABLE.append(row)

OTEXT = json.dumps({ 'races': NRACES, 'table': NTABLE }, indent=2, sort_keys=True)
OTEXT = 'const SMT5_FUSION_CHART = ' + OTEXT.replace('"[', '[').replace(']"', ']').replace('|', '"').replace('0', '-')

with open('../docs/smt5/fusion-chart.js', 'w+') as jsonfile:
    jsonfile.write(OTEXT)

OTEXT = json.dumps({ 'elems': RACES[-4:], 'races': RACES[:-4], 'table': ETABLE }, indent=2, sort_keys=True)
OTEXT = 'const SMT5_ELEMENT_CHART = ' + OTEXT.replace('"[', '[').replace(']"', ']')

with open('../docs/smt5/element-chart.js', 'w+') as jsonfile:
    jsonfile.write(OTEXT)
