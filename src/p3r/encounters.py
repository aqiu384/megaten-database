#!/usr/bin/python3
import json
import sys

def parse_location(demon):
    parts = demon['area'].replace('II', 'I').replace(' I', '').split(' ')
    area = parts[0]
    floors = ' '.join(parts[1:])
    if '-' in floors:
        floors = floors.replace('-', 'F-') + 'F'
    elif 'D' in floors:
        floors = floors.replace('D', '[[Monad Door]] ')
    elif 'P' in floors:
        floors = floors.replace('P', '[[Monad Passage]] ')
    else:
        floors += ' Gatekeeper'
    return f"[[{area}]] {floors}"

def parse_arcana(demon):
    return demon['race'].replace(' B', '').replace(' P', '').replace('Hanged', 'Hanged Man')

KEYS = {
    'name': lambda x: x['name'],
    'level': lambda x: x['lvl'],
    'arcana': parse_arcana,
    'location': lambda x: f"'''{parse_location(x)}'''",
    'exp': lambda x: x['exp']
}

RESIST_LVLS = {
    'z': 'Wk',
    'w': 'Wk',
    'u': '-',
    'v': '-',
    '-': '-',
    's': 'Rs',
    't': 'Rs',
    'V': '-',
    '_': '-',
    'S': 'Rs',
    'T': 'Rs',
    'n': 'Nu',
    'r': 'Rp',
    'd': 'Dr'
}

RESIST_MODS = {
    'z': 125,
    'w': 125,
    'u': 250,
    'v': 200,
    '-': 100,
    's': 50,
    't': 25,
    'V': 200,
    '_': 100,
    'S': 50,
    'T': 25,
    'n': 100,
    'r': 100,
    'd': 100
}

AILMENT_LVLS = {
    'v': 'Wk',
    '-': '-',
    's': 'Rs',
    'n': 'Nu',
}

STATS = ['hp', 'sp', 'st', 'ma', 'en', 'ag', 'lu']
RESISTANCES = ['slash', 'strike', 'pierce', 'fire', 'ice', 'elec', 'wind', 'light', 'darkness', 'almighty']
AILMENTS = ['charm', 'poison', 'distress', 'confuse', 'fear', 'rage']

def parse_drops(demon):
    return [f"|drop{i + 1}={x}" for i, x in enumerate(demon['drops'].keys())] if 'drops' in demon else []
	
def parse_resists(demon):
    lines = []
    for i, lvl in enumerate(demon['resists']):
        if RESIST_LVLS[lvl] != '-':
            lines.append(f"|{RESISTANCES[i]}={RESIST_LVLS[lvl]}")
    for i, lvl in enumerate(demon['resists']):
        if RESIST_MODS[lvl] != 100:
            lines.append(f"|{RESISTANCES[i]}mod={RESIST_MODS[lvl]}")
    if 'ailments' in demon:
        for i, lvl in enumerate(demon['ailments']):
            if AILMENT_LVLS[lvl] != '-':
                lines.append(f"|{AILMENTS[i]}={AILMENT_LVLS[lvl]}")
    return lines

def parse_skills(demon):
    lines = ['|skills=']
    lines.extend(f"{{{{SkillE|P3R|{skill}}}}}" for skill in demon['skills'])
    return lines

def format_enemy(demon):
    lines = ['{{P3R Shadow Stats']
    lines.extend(f"|{k}={v(demon)}" for k, v in KEYS.items())
    lines.extend(f"|{x}={demon['stats'][i]}" for i, x in enumerate(STATS))
    lines.extend(parse_drops(demon))
    lines.extend(parse_resists(demon))
    lines.extend(parse_skills(demon))
    lines.append('}}')
    return '\n'.join(lines)

with open('../../../megaten-fusion-tool/src/app/p3r/data/enemy-data.json') as jsonfile:
    DEMONS = json.load(jsonfile)
for dname, entry in DEMONS.items():
    entry['name'] = dname

prefix = f"{sys.argv[1]} "

encounters = [x for x in DEMONS.values() if x['area'].startswith(prefix)]
encounters.sort(key=lambda x: x['area'])

print('{{Demon List/Header}}')
for entry in encounters:
    print(f"{{{{Demon List|[[{entry['name']}]]|{entry['lvl']}|{parse_location(entry)}|[[{parse_arcana(entry)}_(Arcana)|{parse_arcana(entry)} Arcana]]}}}}")
print('|}')
print('')

for entry in encounters:
    print('==={{link|game|P3R}}===')
    print(format_enemy(entry))
    print('')
