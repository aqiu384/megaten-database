#!/usr/bin/python3
import struct
import json
from shared import load_id_file, printif_notequal, save_ordered_demons

INNATES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

ELEMENTS = {
    0: 'Cut',
    2: 'Bash',
    1: 'Stab',
    3: 'Fire',
    4: 'Ice',
    5: 'Elec',
    6: 'Wind',
    7: 'Light',
    8: 'Dark',
    # 9: 'UNUSED',
    24: 'Almighty'
}

INHERIT_IDS = [
    'UNUSED',
    'almpp',
    'almpn',
    'baspp',
    'baspn',
    'icepp',
    'icepn',
    'firpp',
    'firpn',
    'winpp',
    'winpn',
    'elepp',
    'elepn',
    'darpp',
    'darpn',
    'ligpp',
    'ligpn',
    'almnp',
    'almnn',
    'icenp',
    'icenn',
    'firnp',
    'firnn',
    'winnp',
    'winnn',
    'elenp',
    'elenn',
    'darnp',
    'darnn',
    'lignp',
    'lignn'
]

RACE_IDS = load_id_file('races.tsv')
DEMON_IDS = load_id_file('personanametable.tsv')
SKILL_IDS = load_id_file('skillnametable.tsv')

with open('../../../megaten-fusion-tool/src/app/pq/data/demon-data.json') as jsonfile:
    OLD_DEMONS = json.load(jsonfile)

LINE_LEN = 0x94
START_OFFSET = 0x00
END_OFFSET = START_OFFSET + 288 * LINE_LEN

with open('pq1-data/battle/table/datpersonaformat.bin', 'rb') as binfile:
    NEW_DEMONS = binfile.read()

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, included = DEMON_IDS[d_id].split('\t')

    user, race, lvl = struct.unpack('<H2B', line[0x00:0x04])
    stats = struct.unpack('<7H', line[0x04:0x12])
    resists = struct.unpack('<25H', line[0x12:0x44])
    zero, inherit = struct.unpack('<2H', line[0x44:0x48])
    unk_inherit = struct.unpack('<5B', line[0x48:0x4D])
    zeros = struct.unpack('<71B', line[0x4D:0x94])

    # print(unk_inherit, dname)

    race = RACE_IDS[race]
    inherit = INHERIT_IDS[inherit]

    if int(included) < 1:
        continue

    entry = OLD_DEMONS[dname]

    printif_notequal(dname, 'lvl', lvl, entry['lvl'])
    printif_notequal(dname, 'race', race, entry['race'])
    printif_notequal(dname, 'inherit', inherit, entry['inherit'])

    entry.update({
        'inherit': inherit,
        'lvl': lvl,
        'race': race,
        'stats': [stats[0], stats[1]]
    })

LINE_LEN = 0x48
START_OFFSET = 0x00
END_OFFSET = START_OFFSET + 288 * LINE_LEN

with open('pq1-data/battle/table/datsubpersonagrowth.bin', 'rb') as binfile:
    NEW_DEMONS = binfile.read()

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, included = DEMON_IDS[d_id].split('\t')

    growths = struct.unpack('<8B', line[0x00:0x08])
    learned = struct.unpack('<32H', line[0x08:0x48])

    if int(included) < 1:
        continue

    entry = OLD_DEMONS[dname]
    dlvl = entry['lvl']
    skills = {}

    for i in range(16):
        slvl, sname = learned[2*i:2*i + 2]
        if sname == 0:
            continue
        slvl -= 0x100
        slvl = INNATES[i] if slvl == 0 else slvl + dlvl
        sname -= 0x1000
        sname = SKILL_IDS[sname].split('\t')[0]
        skills[sname] = slvl

    printif_notequal(dname, 'skills', str(skills), str(entry['skills']))
    entry['skills'] = skills

save_ordered_demons(OLD_DEMONS, 'new-demon-data.json')
