#!/usr/bin/python3
import struct
import json
from shared import load_demons, load_skills

INNATES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
ALIGNS1 = ['???', 'Neutral', 'Light', 'Dark']
ALIGNS2 = ['???', 'Neutral', '???', '???', 'Law', 'Chaos']

RESIST_LVLS = {
    0: 'n',
    10: '1',
    20: '2',
    40: '4',
    50: 's',
    100: '-',
    125: 'w',
    300: 'x',
    900: '?',
    999: 'r',
    1000: 'd'
}

AILMENTS = {
    11: 'cha',
    13: 'sea',
    10: 'pan',
    8: 'poi',
    12: 'sle',
    20: 'mir'
}

GIFT_TYPES = [
    'NONE',
    'fir',
    'ice',
    'ele',
    'for',
    'lig',
    'dar',
    'rec',
    'sup',
    'ail',
    'phy',
    'alm'
]

SPEECHES = {
    1: 'Boy',
    2: 'Youth',
    3: 'Warrior',
    5: 'Gentleman',
    6: 'Eminent',
    7: 'Elderly',
    8: 'Girl',
    9: 'Gyaru',
    10: 'Lady',
    11: 'Witch',
    12: 'Animal',
    13: 'Jack',
    14: 'Eerie',
    36: 'Nuwa',
    83: 'Nushi',
    84: 'Hime'
}

AREAS = {
    6: 'Temple of Eternity',
    19: 'Demon King Castle',
    31: 'Minato',
    51: 'Shinagawa',
    67: 'Chiyoda',
    88: 'Taito',
    120: 'Nowhere'
}

def load_id_file(fname):
    with open('Content/Blueprints/Gamedata/BinTable/' + fname) as tsvfile:
        next(tsvfile)
        return [x.split('\t')[0].strip() for x in tsvfile]

with open('../../../megaten-fusion-tool/src/app/smt5/data/demon-data.json') as jsonfile:
    VAN_DEMONS = json.load(jsonfile)
with open('../../../megaten-fusion-tool/src/app/smt5v/data/demon-data.json') as jsonfile:
    OLD_DEMONS = json.load(jsonfile)
with open('../../../megaten-fusion-tool/src/app/smt5v/data/innate-skills.json') as jsonfile:
    OLD_INNATES = json.load(jsonfile)

RACE_IDS = load_id_file('Common/DevilRace.tsv')
DEMON_IDS = [x.split('\t')[0] for x in load_demons()]
SKILL_IDS = [x.split('\t')[0] for x in load_skills()]
LINE_LEN = 0x1C4
LINE_LEN = 0x1D0
START_OFFSET = 0x55
END_OFFSET = START_OFFSET + 1201 * LINE_LEN
MAGIC_COMP = (0, 1, 1, 0, 98, 0, 5, 100, 70, 100, 0)

with open('Content/Blueprints/Gamedata/BinTable/Devil/NKMBaseTable.bin', 'rb') as binfile:
    NEW_DEMONS = binfile.read()
with open('../../../megaten-fusion-tool/src/app/smt5/data/alignments.json') as jsonfile:
    RACE_ALIGNS = json.load(jsonfile)

def save_ordered_demons(demons, fname):
    for entry in demons.values():
        for stat_set in ['affinities', 'stats']:
            if stat_set in entry:
                entry[stat_set] = '[' + ', '.join(str(x) for x in entry[stat_set]) + ']'
        if 'skills' in entry:
            nskills = sorted(entry['skills'].items(), key=lambda x: x[1])
            nskills = '{||      ' + ',||      '.join(f'|{x[0]}|: {x[1]}' for x in nskills) + '||    }'
            entry['skills'] = nskills

    jstring = json.dumps(demons, indent=2, sort_keys=True)
    jstring = jstring.replace('||', '\n').replace('|', '"')
    jstring = jstring.replace('"[', '[').replace(']"', ']').replace('"{', '{').replace('}"', '}')

    with open(fname, 'w+') as jsonfile:
        jsonfile.write(jstring)

def printif_notequal(dname, field, lhs, rhs):
    if str(lhs) != str(rhs):
        print(dname, field, lhs, rhs)

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname = DEMON_IDS[d_id]

    d_id2, order_comp, race = struct.unpack('<LLB', line[0x00:0x09])
    unk_race = struct.unpack('<6B', line[0x09:0x0F])
    align1, align2 = struct.unpack('<BL', line[0x0F:0x14])
    lvl, in_comp = struct.unpack('<LB', line[0x14:0x19])
    magic_comp = struct.unpack('<7B4L', line[0x19:0x30])
    race = RACE_IDS[race]

    if in_comp == 0:
        continue

    stats = list(struct.unpack('<14L', line[0x30:0x68]))
    ten, gift, fuse_special, speech = struct.unpack('<2BHL', line[0x68:0x70])
    zero, fuse_unlock, price_coeff, four, zero = struct.unpack('<5L', line[0x70:0x84])
    stats_base = stats[:2] + stats[4:9]
    stats_growth = [10 * stats[2], 10 * stats[3]] + stats[9:]
    gift = GIFT_TYPES[gift]
    fuse_special = 1 if fuse_special == 257 else fuse_special
    speech = SPEECHES.get(speech, dname)

    innate = struct.unpack('<12L', line[0x84:0xB4])
    learned = struct.unpack('<24L', line[0xB4:0x114])
    trait, = struct.unpack('<L', line[0x114:0x118])

    resists = struct.unpack('<28L', line[0x118:0x188])
    affinities = struct.unpack('<12l', line[0x188:0x1B8])
    # zero, zero, area, subarea = struct.unpack('<4L', line[0x1B4:0x1C4])

    ailments = ''.join(RESIST_LVLS[resists[i]] for i in AILMENTS)
    resists = ''.join(RESIST_LVLS[x] for x in resists[:7])
    affinities = list(affinities[:-3]) + [affinities[-2], affinities[-3]]
    skills = { SKILL_IDS[x]: INNATES[i] for i, x in enumerate(innate) if x != 0 }
    # area = AREAS[area]

    for i in range(0, 24, 2):
        if learned[i + 1] > 0:
            skills[SKILL_IDS[learned[i + 1]]] = learned[i]

    align = f"{ALIGNS1[align1]}-{ALIGNS2[align2]}"

    printif_notequal(dname, 'align', RACE_ALIGNS.get(dname, RACE_ALIGNS[race]), align)
    printif_notequal(dname, 'd_id2', d_id, d_id2)
    # printif_notequal(dname, 'magic_comp', MAGIC_COMP, magic_comp)

    entry = {
        'race': race,
        'lvl': lvl,
        'stats': stats_base,
        'resists': resists,
        'skills': skills,
        'affinities': affinities
    }

    if ailments != '------':
        entry['ailments'] = ailments

    van_entry = VAN_DEMONS.get(dname, { 'price': 0 })
    entry['price'] = van_entry['price']
    if json.dumps(van_entry, sort_keys=True) != json.dumps(entry, sort_keys=True):
        entry['price'] = OLD_DEMONS[dname]['price']
        OLD_DEMONS[dname] = entry

    OLD_INNATES[dname] = SKILL_IDS[trait]

save_ordered_demons(OLD_DEMONS, 'new-demon-data.json')

with open('innate-skills.json', 'w+') as jsonfile:
    json.dump(OLD_INNATES, jsonfile, indent=2, sort_keys=True)
