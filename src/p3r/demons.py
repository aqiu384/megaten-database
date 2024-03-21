#!/usr/bin/python3
from shared import save_ordered_demons, load_item_descs, load_item_codes, iterate_int_tsvfile

RESISTS = {
    20: '-',
    256: 'n',
    512: 'r',
    1024: 'd',
    2048: 'w',
    4096: 's'
}

FNAME = 'Content/Xrd777/Blueprints/common/Names/Dat{}DataAsset.tsv'

ITEMS = load_item_codes('en')
DEMONS = { x: { 'name': y } for x, y in load_item_descs(FNAME.format('PersonaName'), 'en', max_flag=1).items() }
RACES = load_item_descs(FNAME.format('Race'), 'en')
INHERITS = load_item_descs(FNAME.format('InheritType'), 'en')
SKILLS = load_item_descs(FNAME.format('SkillName'), 'en')

def update_stats(entry, line):
    entry.update({
        'race': RACES[line['race']],
        'lvl': line['level'],
        'stats': [line[f"params{x}"] for x in range(1, 6)],
        'inherits': INHERITS[line['succession']]
    })
    return entry

def update_resists(entry, line):
    resists = [RESISTS[line[f"attr{x}"]] for x in range(1, 11)]
    resists = resists[:7] + resists[8:] + resists[7:8]
    entry['resists'] = ''.join(resists)
    return entry

def update_skills(entry, line):
    dlvl = entry['lvl']
    learned = {}
    counter = 1
    entry['skills'] = learned

    for i in range(1, 17):
        s_id = line[f"skillId{i}"]
        slvl = line[f"skillLevel{i}"]

        if s_id < 1:
            continue
        if 0x6000 < s_id:
            entry['heart'] = ITEMS[s_id]
            entry['heartlvl'] = slvl + dlvl
            continue
        if slvl == 0:
            slvl = counter / 10
            counter += 1
        else:
            slvl += dlvl

        learned[SKILLS[s_id]] = slvl

    return entry

UPDATERS = [
    ('Persona', update_stats),
    ('PersonaAffinity', update_resists),
    ('PersonaGrowth', update_skills)
]

FNAME = 'Content/Xrd777/Battle/Tables/Dat{}DataAsset.tsv'

for fname, updater in UPDATERS:
    for i, line in enumerate(iterate_int_tsvfile(FNAME.format(fname), skip_first=False)):
        if i in DEMONS:
            updater(DEMONS[i], line)

for line in iterate_int_tsvfile(FNAME.format('BtlMixraidRelease'), skip_first=False):
    for letter in 'AB':
        DEMONS[line[f"Persona{letter}ID"]]['skills'][SKILLS[line['Skill']]] = 5217

DEMONS = { x['name']: x for x in DEMONS.values() }
for demon in DEMONS.values():
    del demon['name']

save_ordered_demons(DEMONS, 'demon-data.json')
