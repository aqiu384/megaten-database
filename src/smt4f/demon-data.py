#!/usr/bin/python3
import struct
import json

LINE_LEN = 0xB4
START_OFFSET = 0x96 + 3*LINE_LEN
END_OFFSET = 5*LINE_LEN
OLD_AILMENTS = ['Bind', 'Charm', 'Daze', 'Mute', 'Panic', 'Poison', 'Sick', 'Sleep']

RESIST_LVLS = {
    20: 's',
    16: 'd',
    12: 'r',
    9: 'w',
    8: 'w',
    4: 'n',
    1: '-',
    0: '-'
}

AILMENTS = [
    'ELEM_009',
    'ELEM_010',
    'ELEM_011',
    'Poison',
    'Panic',
    'Sleep',
    'Bind',
    'Sick',
    'ELEM_017',
    'Charm',
    'Daze',
    'Mute',
    'ELEM_021'
]

AILMENT_ORDER = [1 + 2*AILMENTS.index(x) for x in OLD_AILMENTS]

with open('data/demon-data.json') as jsonfile:
    OLD_DEMONS = json.load(jsonfile)
with open('data/demon-data.bin', 'rb') as binfile:
    NEW_DEMONS = binfile.read()
with open('data/demon-ids.tsv') as tsvfile:
    DEMON_IDS = ['BLANK\t0'] + [x.strip() for x in tsvfile]
with open('data/skill-ids.tsv') as tsvfile:
    SKILL_IDS = ['BLANK'] + [x.strip() for x in tsvfile]
with open('data/race-ids.tsv') as tsvfile:
    RACE_IDS = ['BLANK'] + [x.strip() for x in tsvfile]

def printif_notequal(dname, field, lhs, rhs):
    if str(lhs) != str(rhs):
        print(dname, field, lhs, rhs)

def save_ordered_demons(demons, fname):
    for entry in demons.values():
        entry['stats'] = '[' + ', '.join(str(x) for x in entry['stats']) + ']'
        entry['affinities'] = '[' + ', '.join(str(x) for x in entry['affinities']) + ']'
        nskills = sorted(entry['skills'].items(), key=lambda x: x[1])
        nskills = '{||      ' + ',||      '.join(f'|{x[0]}|: {x[1]}' for x in nskills) + '||    }'
        entry['skills'] = nskills

    jstring = json.dumps(demons, indent=2, sort_keys=True)
    jstring = jstring.replace('||', '\n').replace('|', '"')
    jstring = jstring.replace('"[', '[').replace(']"', ']').replace('"{', '{').replace('}"', '}')

    with open(fname, 'w+') as jsonfile:
        jsonfile.write(jstring)

for d_id, line_start in enumerate(range(START_OFFSET, len(NEW_DEMONS) - END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, in_comp = DEMON_IDS[d_id].split('\t')

    if int(in_comp) != 1:
        continue

    demon = OLD_DEMONS[dname]

    new_d_id = struct.unpack('<1H', line[0x00:0x02])[0]
    race_id = struct.unpack('<1L', line[0x02:0x06])[0]
    dlvl = struct.unpack('<1H', line[0x06:0x08])[0]
    stats = struct.unpack('<5H', line[0x1E:0x28])
    innate = struct.unpack('<8H', line[0x40:0x50])
    learned = struct.unpack('<16H', line[0x50:0x70])
    full_resists = struct.unpack('<16B', line[0x70:0x80])
    full_ailments = struct.unpack('<26B', line[0x80:0x9A])
    full_affinities = struct.unpack('<16b', line[0xA2:0xB2])

    printif_notequal(dname, 'd_id', d_id, new_d_id)
    printif_notequal(dname, 'race', demon['race'], RACE_IDS[race_id])
    printif_notequal(dname, 'lvl', demon['lvl'], dlvl)
    printif_notequal(dname, 'stats', demon['stats'][2:], list(stats))

    resists = ''.join(RESIST_LVLS[x] for x in full_resists[1::2])
    ailments = ''.join(RESIST_LVLS[full_ailments[x]] for x in AILMENT_ORDER)
    affinities = list(full_affinities[:8]) + [full_affinities[x] for x in (8, 12, 10, 14)]

    printif_notequal(dname, 'resists', demon['resists'], resists)
    printif_notequal(dname, 'ailments', demon.get('ailments', '--------'), ailments)
    printif_notequal(dname, 'affinities', demon['affinities'], affinities)

    skills = demon['skills']

    for i, s_id in enumerate(innate):
        sname = SKILL_IDS[s_id]
        if s_id == 0:
            continue
        if sname not in skills or skills[sname] > 1:
            print(dname, sname, 0, skills)
        else:
            skills[sname] = (i + 1) / 10

    for i in range(0, 16, 2):
        slvl, s_id = learned[i:i + 2]
        sname = SKILL_IDS[s_id]
        if s_id == 0:
            continue
        if sname not in skills or skills[sname] != slvl:
            print(dname, sname, slvl, skills)
        else:
            skills[sname] = slvl

save_ordered_demons(OLD_DEMONS, 'new-demon-data.json')
