#!/usr/bin/python3
import struct
import json
from shared import printif_notequal, load_id_file

RESIST_LVLS = ['d', 'r', 'n', 's', '-', 'w']
RESMOD_LVLS = { 'n': 0, 's': 50, 'w': 150, }

with open('../../../megaten-fusion-tool/src/app/sh2/data/demon-data.json', 'rb') as jsonfile:
    OLD_DEMONS = json.load(jsonfile)
with open('dumps/demons.bin', 'rb') as binfile:
    NEW_DEMONS = binfile.read()

TALK_IDS = [
    'None',
    'Boy',
    'Youth',
    'Gentleman',
    'Eminent',
    'Elderly',
    'Girl',
    'Gyaru',
    'Lady',
    'Queen',
    'Beast',
    'Jack',
    'Gain',
    'Madness',
    'Professional',
    'Elderbeast',
    'Doppelganger',
    'Nemissa'
]

GIFT_IDS = [
    'Fire',
    'Fire Rare',
    'Ice',
    'Ice Rare',
    'Elec',
    'Elec Rare',
    'Force',
    'Force Rare',
    'Curse',
    'UNKNOWN',
    'Almighty',
    'Almighty Rare',
    'Recovery',
    'UNKNOWN',
    'Support',
    'UNKNOWN',
    'HP Item',
    'SP Item',
    'Fae King\'s Crown',
    'Fae Queen\'s Band',
    'Sandal Slippers',
    'Seraph Breastplate',
    'Glass Shitoki',
    'Caprine Pentagram',
    'Slave Anklet'
]

DEMON_IDS = load_id_file('data/demon-ids.tsv')
SKILL_IDS = load_id_file('data/skill-ids.tsv')
RACE_IDS = load_id_file('data/race-ids.tsv')
D_ID_OFFSET = 161
MAGIC_ID = (192, 2, 2, 137, 32, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
# ENEMY_MAGIC_ID = (64, 239, 1, 137, 32, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
INNATES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

START_OFFSET = 0
END_OFFSET = len(NEW_DEMONS)
LINE_LEN = 0x120

SKILL_CODES = {}

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    d_id = D_ID_OFFSET - d_id
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, included = DEMON_IDS[d_id].split('\t')

    magic_id = struct.unpack('<16B', line[0x00:0x10])
    new_d_id, unk_id, race = struct.unpack('<2LQ', line[0x10:0x20])
    name_point, info_point, unlocked, fusion_point, lvl = struct.unpack('<4QL', line[0x20:0x44])
    stats = struct.unpack('<5L', line[0x44:0x58])
    growths = struct.unpack('<5f', line[0x58:0x6C])
    full_resists = struct.unpack('<8Q', line[0x6C:0xAC])
    skill_lvls = struct.unpack('<6L', line[0xAC:0xC4])
    skill_names = struct.unpack('<6L', line[0xC4:0xDC])
    d_id_20, = struct.unpack('<L', line[0xDC:0xE0])
    full_gifts = struct.unpack('<8L', line[0xE0:0x100])
    unlock_flag, unlock_cond, price_coeff = struct.unpack('<3L', line[0x100:0x10C])
    talk, unk_talk = struct.unpack('<2L12x', line[0x10C:0x120])

    growths = [round(x * 100) for x in growths]
    full_resists = list(full_resists[:6]) + [full_resists[7], full_resists[6]]
    resists = ''.join(RESIST_LVLS[x & 0xFFFF] for x in full_resists)
    resmods = tuple(x >> 32 for x in full_resists)
    skills = {}
    gifts = {}
    talk = TALK_IDS[talk]

    for i in range(6):
        if skill_names[i] == 0:
            continue
        sname = SKILL_IDS[skill_names[i] - 1000]
        slvl = INNATES[i] if skill_lvls[i] == 0 else skill_lvls[i]
        skills[sname] = slvl
    for i in range(0, 8, 2):
        gname, glvl = full_gifts[i:i + 2]
        if glvl == 0:
            continue
        gifts[GIFT_IDS[gname]] = glvl

    if int(included) < 1:
        continue

    entry = OLD_DEMONS[dname]
    old_resists = entry['resists'] + '-'
    old_resmods = tuple(RESMOD_LVLS.get(x, 100) for x in old_resists)

    for i, sname in enumerate(entry['skills']):
        SKILL_CODES[skill_names[i]] = sname

    race = RACE_IDS[race]

    printif_notequal(dname, 'magic_id', magic_id, MAGIC_ID)
    printif_notequal(dname, 'lvl', lvl, entry['lvl'])
    printif_notequal(dname, 'race', race, entry['race'])
    printif_notequal(dname, 'resists', resists, old_resists)
    printif_notequal(dname, 'resmods', resmods, old_resmods)
    # printif_notequal(dname, 'skills', str(skills), str(entry['skills']))
    print(unk_id, dname)
    printif_notequal(dname, 'd_id_20', d_id_20, d_id + 20)
