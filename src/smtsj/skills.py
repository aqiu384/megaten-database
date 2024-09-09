#!/usr/bin/python3
import struct

AILMENTS = ['-', 'instakill', 'Sleep', 'Poison', 'Paralyze', 'Charm', 'Mute', 'Stone', 'Fear', 'Strain', 'Bomb', 'Freeze', 'Rage', '???', '???', 'Random']
LINE_LEN = 0x40
START_OFFSET = 0x30
END_OFFSET = START_OFFSET + 350 * LINE_LEN

LINE_LEN = 0x4C
START_OFFSET = 0x30
END_OFFSET = START_OFFSET + 350 * LINE_LEN

with open('smtdsj-data/Skill/SkillData.bin', 'rb') as binfile:
    NEW_SKILLS = binfile.read()
with open('smtsj-data/skill-ids.tsv') as tsvfile:
    next(tsvfile)
    SKILL_IDS = [x.strip() for x in tsvfile]

def printif_notequal(dname, field, lhs, rhs):
    if str(lhs) != str(rhs):
        print(dname, field, lhs, rhs)

for s_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    s_id += 1
    line = NEW_SKILLS[line_start:line_start + LINE_LEN]
    sname = SKILL_IDS[s_id]

    new_sname = line[0x00:0x20].decode('utf8').rstrip('\x00')

    new_s_id, cost, hits, crit, power, acc, ailment, ail_acc = struct.unpack('<HBx2xBBHBBB3x', line[0x20:0x30])
    min_hits = (hits & 0x0F) >> 1
    max_hits = hits >> 5
    print(sname, new_sname, new_s_id, cost, power, min_hits, max_hits, acc, 0, ail_acc, AILMENTS[ailment], sep='\t')
