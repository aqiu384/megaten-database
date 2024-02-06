#!/usr/bin/python3
from shared import save_ordered_demons

MATERIAL_OFFSET = 0x6000
NAMES = []
RESISTS = {
    20: '-',
    256: 'n',
    512: 'r',
    1024: 'd',
    2048: 'w',
    4096: 's'
}

for fname in ['race', 'inherit', 'skill', 'material']:
    with open(f"en-names/{fname}-names.tsv") as tsvfile:
        next(tsvfile)
        NAMES.append([x.split('\t')[0].strip() for x in tsvfile])

RACES, INHERITS, SKILLS, MATERIALS = NAMES
INCLUDED = []
DEMONS = {}

with open('en-names/persona-names.tsv') as tsvfile:
    next(tsvfile)
    for line in tsvfile:
        dname, included = line.split('\t')
        INCLUDED.append(dname if 0 < int(included) else '')

def load_stats(dname, parts):
    _, race, lvl = parts[:3]
    stats = parts[3:8]
    _, inherits, _, _ = parts[8:]

    DEMONS[dname] = {
        'race': RACES[race],
        'lvl': lvl,
        'stats': stats,
        'inherits': INHERITS[inherits]
    }

def load_resists(dname, parts):
    resists = [RESISTS[x] for x in parts]
    resists = resists[:7] + resists[8:10] + resists[7:8]
    DEMONS[dname]['resists'] = ''.join(resists)

def load_skills(dname, parts):
    dlvl = DEMONS[dname]['lvl']
    learned = {}
    counter = 1

    for i in range(5, len(parts), 3):
        slvl, _, s_id = parts[i:i + 3]

        if s_id < 1:
            continue
        if 2000 < s_id:
            DEMONS[dname]['heart'] = MATERIALS[s_id - MATERIAL_OFFSET]
            DEMONS[dname]['heartlvl'] = slvl + dlvl
            continue
        if slvl == 0:
            slvl = counter / 10
            counter += 1
        else:
            slvl += dlvl

        learned[SKILLS[s_id]] = slvl

    DEMONS[dname]['skills'] = learned

PARSERS = [
    ('stats', load_stats),
    ('resists', load_resists),
    ('growths', load_skills)
]

for fname, parser in PARSERS:
    with open(f"fusion/persona-{fname}.tsv") as tsvfile:
        next(tsvfile)
        for i, line in enumerate(tsvfile):
            parts = [int(x) for x in line.split()]
            dname = INCLUDED[i]
            if dname != '':
                parser(dname, parts)

save_ordered_demons(DEMONS, 'demon-data.json')