#!/usr/bin/python3
import struct
import json
from shared import load_id_file, printif_notequal, save_ordered_demons

GAME = 'pq'
INNATES =  [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

INHERITS = [
    "UNUSED",
    "almpp",
    "almpn",
    "baspp",
    "baspn",
    "icepp",
    "icepn",
    "firpp",
    "firpn",
    "winpp",
    "winpn",
    "elepp",
    "elepn",
    "darpp",
    "darpn",
    "ligpp",
    "ligpn",
    "almnp",
    "almnn",
    "icenp",
    "icenn",
    "firnp",
    "firnn",
    "winnp",
    "winnn",
    "elenp",
    "elenn",
    "darnp",
    "darnn",
    "lignp",
    "lignn",
    "psypp",
    "UNUSED",
    "nukpp"
]

with open(f"configs/{GAME}-comp-config.json") as jsonfile:
    COMP_CONFIG = json.load(jsonfile)

RACE_IDS = load_id_file(COMP_CONFIG['raceIds'])
DEMON_IDS = load_id_file(COMP_CONFIG['demonIds'])
SKILL_IDS = load_id_file(COMP_CONFIG['skillIds'])
OLD_DEMONS = {}

for fname in COMP_CONFIG['demonData']:
    with open(f"../../../megaten-fusion-tool/src/app/{fname}") as jsonfile:
        OLD_DEMONS.update(json.load(jsonfile))
with open(COMP_CONFIG['demonStatDump']['file'], 'rb') as binfile:
    NEW_DEMONS = binfile.read()

SEEN = { x: False for x in OLD_DEMONS }
LINE_LEN = COMP_CONFIG['demonStatDump']['length']
START_OFFSET = COMP_CONFIG['demonStatDump']['start']
END_OFFSET = COMP_CONFIG['demonStatDump']['end']
if END_OFFSET == -1:
    END_OFFSET = len(NEW_DEMONS)

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, included = DEMON_IDS[d_id].split('\t')

    user, race, lvl = struct.unpack('<H2B', line[0x00:0x04])
    stats = struct.unpack('<7H', line[0x04:0x12])
    resists = struct.unpack('<25H', line[0x12:0x44])
    zero, inherit = struct.unpack('<2H', line[0x44:0x48])
    unk_inherit = struct.unpack('<5B', line[0x48:0x4D])
    zeros = struct.unpack('<71B', line[0x4D:0x94])

    race = RACE_IDS[race]
    inherit = INHERITS[inherit]

    if int(included) < 1:
        continue

    entry = OLD_DEMONS[dname]
    SEEN[dname] = True

    printif_notequal(dname, 'lvl', lvl, entry['lvl'])
    printif_notequal(dname, 'race', race, entry['race'])
    printif_notequal(dname, 'inherit', inherit, entry['inherit'])

    entry.update({
        'inherit': inherit,
        # 'combat': entry['inherit'],
        'lvl': lvl,
        'race': race,
        'stats': [stats[0], stats[1]]
    })

with open(COMP_CONFIG['demonSkillDump']['file'], 'rb') as binfile:
    NEW_DEMONS = binfile.read()

LINE_LEN = COMP_CONFIG['demonSkillDump']['length']
START_OFFSET = COMP_CONFIG['demonSkillDump']['start']
END_OFFSET = COMP_CONFIG['demonSkillDump']['end']
if END_OFFSET == -1:
    END_OFFSET = len(NEW_DEMONS)
SKILL_LEN = (LINE_LEN - 8) >> 5

for d_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    line = NEW_DEMONS[line_start:line_start + LINE_LEN]
    dname, included = DEMON_IDS[d_id].split('\t')

    growths = struct.unpack('<8B', line[0x00:0x08])
    learned = struct.unpack(f"<{SKILL_LEN << 4}H", line[0x08:LINE_LEN])

    if int(included) < 1:
        continue

    entry = OLD_DEMONS[dname]
    dlvl = entry['lvl']
    skills = {}

    for i in range(16):
        slvl, sname = learned[SKILL_LEN*i:SKILL_LEN*i + 2]
        if sname == 0:
            continue
        slvl &= 0xFF
        slvl = INNATES[i] if slvl == 0 else slvl + dlvl
        sname &= 0x0FFF
        sname = SKILL_IDS[sname].split('\t')[0]
        skills[sname] = slvl

    printif_notequal(dname, 'skills', str(skills), str(entry['skills']))
    entry['skills'] = skills

for dname, seen in SEEN.items():
    if not seen:
        print('Not seen:', dname)

save_ordered_demons(OLD_DEMONS, 'new-demon-data.json')
