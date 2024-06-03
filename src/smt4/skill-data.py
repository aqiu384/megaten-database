#!/usr/bin/python3
import struct
import json
import os

LINE_LEN = 0x68
START_OFFSET = 0x30
END_OFFSET = START_OFFSET + 400 * LINE_LEN

WHISPERS = ['None', 'Dmg +', 'Heal +', 'Ail +', 'Cost -']
ELEMS = [
    'fir', 'ice', 'ele', 'for',
    'alm', 'lig', 'dar', 'phy',
    'gun', 'ail', 'rec', 'sup',
    'spe', '???', '???'
]

with open('../../../megaten-fusion-tool/src/app/smt4/data/skill-data.json') as jsonfile:
    OLD_SKILLS = { x['name']: x for x in json.load(jsonfile) }
with open('data/skill-ids.tsv') as tsvfile:
    SKILL_IDS = ['BLANK'] + [x.strip() for x in tsvfile]

SEEN_SKILLS = { x: False for x in OLD_SKILLS }
NEW_SKILLS = {}

def printif_notequal(name, field, lhs, rhs):
    if str(lhs) != str(rhs):
        print(name, field, lhs, rhs)

def parse_active_skills(fname, start_offset, end_offset, line_len):
    with open(fname, 'rb') as binfile:
        new_skills = binfile.read()
    is_dlc = end_offset < 10 * line_len

    for s_id, line_start in enumerate(range(start_offset, end_offset, line_len)):
        s_id += 1
        line = new_skills[line_start:line_start + LINE_LEN]
        new_sname = line[0x00:0x20].decode('utf8')
        new_s_id, cost, whisper_type, alpha_order = struct.unpack('<H2BL', line[0x20:0x28])
        target, unk_elem, max_hit, crit = struct.unpack('<4B', line[0x28:0x2C])
        pwr, acc, ailment, ail_acc, mostly_zero = struct.unpack('<H4B', line[0x2C:0x32])
        buffs = struct.unpack('<4b', line[0x32:0x36])
        heal_pwr, heal_flag, align_flag = struct.unpack('<H2B', line[0x36:0x3A])
        charge_flags, drain_hp, drain_mp = struct.unpack('<L2B', line[0x3A:0x40])
        unk_multiply = struct.unpack('<24B', line[0x40:0x58])
        whispers = struct.unpack('<16B', line[0x58:0x68])

        if is_dlc:
            s_id = new_s_id
        sname = SKILL_IDS[s_id]
        if sname not in SEEN_SKILLS:
            continue

        SEEN_SKILLS[sname] = True
        elem_hit = target & 0x0F
        target = target >> 4
        min_hit = max_hit >> 1 & 0x7
        max_hit = max_hit >> 5
        elem = ELEMS[elem_hit]
        cost += 1000

        entry = OLD_SKILLS[sname]
        printif_notequal(sname, 'cost', cost, entry.get('cost', 0))
        stats = [entry['rank'], cost, pwr, min_hit, max_hit, acc, crit, ail_acc]
        prefix = [sname, elem, entry.get('target', '-')]
        suffix = [str(ailment), '-', '-', entry.get('effect', '-')]
        NEW_SKILLS[f"{s_id:03}"] = prefix + [str(x) for x in stats] + suffix
        print(heal_pwr, s_id, sname)

def parse_passive_skills(fname, start_offset, end_offset, line_len):
    with open(fname, 'rb') as binfile:
        new_skills = binfile.read()
    is_dlc = end_offset == -1

    for s_id, line_start in enumerate(range(start_offset, len(new_skills) if is_dlc else end_offset, line_len)):
        s_id += 401
        line = new_skills[line_start:line_start + LINE_LEN]
        new_sname = line[0x00:0x20].decode('utf8')
        new_s_id, alpha_order = struct.unpack('<2H', line[0x20:0x24])
        unk_parts = struct.unpack('<24B', line[0x24:0x3C])
        sname = SKILL_IDS[s_id]

        if is_dlc:
            s_id = new_s_id
        if sname not in SEEN_SKILLS:
            continue

        entry = OLD_SKILLS[sname]
        SEEN_SKILLS[sname] = True
        stats = [entry['rank']] + [0] * 7
        prefix = [sname, 'pas', '-']
        suffix = ['-', '-', '-', entry.get('effect', '-')]
        NEW_SKILLS[f"{s_id:03}"] = prefix + [str(x) for x in stats] + suffix
        print(unk_parts, s_id, sname)

parse_active_skills('data/battle/SkillData.bin', START_OFFSET, END_OFFSET, LINE_LEN)

DLC_DIR = 'data/addon/testdata/'
DLC_LENS = [(3, 6), (6, 6), (8, 2), (12, 3), (14, 3), (15, 6)]

for dlc_num, active_num in DLC_LENS:
    fname = f"content{dlc_num:02}-tbl-SkillData.bin"
    end_offset = START_OFFSET + active_num * LINE_LEN
    parse_active_skills(DLC_DIR + fname, START_OFFSET, end_offset, LINE_LEN)

LINE_LEN = 0x3C
START_OFFSET = END_OFFSET + 0x10
END_OFFSET = START_OFFSET + 100 * LINE_LEN

parse_passive_skills('data/battle/SkillData.bin', START_OFFSET, END_OFFSET, LINE_LEN)

for s_id, entry in NEW_SKILLS.items():
    pass
    # print(s_id, '\t'.join(entry), sep='\t')

for sname, seen in SEEN_SKILLS.items():
    if not seen:
        print(sname)

# save_ordered_skills(OLD_SKILLS, 'new-demon-data.json')
