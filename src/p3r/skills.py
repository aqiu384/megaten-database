#!/usr/bin/python3
import json
from shared import load_item_descs, iterate_int_tsvfile

ELEMS = [
    'sla', 'str', 'pie', 'fir',
    'ice', 'ele', 'win', 'alm',
    'lig', 'dar', 'ail', 'ail',
    'ail', 'ail', 'ail', 'ail',
    'rec', 'sup', 'spe', 'pas'
]
TARGETS = [
    'Party', '???', '???',
    '1 ally', 'All allies', 'Rand allies',
    '1 foe', 'All foes', '???',
    '???', '???', 'Universal'
]

SEEN = {}
FNAME = 'Content/Xrd777/Blueprints/common/Names/Dat{}DataAsset.tsv'
SKILLS = load_item_descs(FNAME.format('SkillName'), 'en')
NSKILLS = {}

for s_id, sname in SKILLS.items():
    if ord(sname[0]) > 127:
        continue
    if sname not in SEEN:
        SEEN[sname] = 0
    else:
        SEEN[sname] += 1
        sname = f"{sname} {chr(65 + SEEN[sname])}"
    NSKILLS[s_id] = { 'name': sname }

SKILLS = NSKILLS

def update_elem(entry, line):
    entry['a'] = [entry['name'], ELEMS[line['attr']], '-']
    entry['b'] = [str(line['targetLv'])] + ['-'] * 7
    entry['c'] = ['-']
    return entry

def update_nums(entry, line):
    cost = 1000 * (line['costtype'] - 1) + line['cost']
    if cost < 0:
        cost += 1000
    line['cost'] = cost
    entry['a'][2] = TARGETS[3 * line['targetarea'] + line['targettype']]
    entry['b'] = [entry['b'][0]] + [str(line[x]) for x in ['cost', 'hpn', 'targetcntmin', 'targetcntmax', 'hitratio', 'criticalratio', 'badratio']]
    entry['c']= [str(line['badstatus'])]
    return entry

UPDATERS = [
    ('Skill', update_elem),
    ('SkillNormal', update_nums)
]

FNAME = 'Content/Xrd777/Battle/Tables/Dat{}DataAsset.tsv'

for fname, updater in UPDATERS:
    for i, line in enumerate(iterate_int_tsvfile(FNAME.format(fname), skip_first=False)):
        if i in SKILLS:
            updater(SKILLS[i], line)

for s_id, entry in SKILLS.items():
    print(s_id, '\t'.join('\t'.join(entry[x]) for x in 'abc'), sep='\t')
