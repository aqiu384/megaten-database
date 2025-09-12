#!/usr/bin/python3
import sys
import json
import yaml
from jinja2 import Environment, FileSystemLoader

with open('data/tool-format.yaml') as yamlfile:
    config = yaml.safe_load(yamlfile)['demonData']['colFormat']
with open('../../../megaten-fusion-tool/src/app/sh2/data/skill-data.json') as jsonfile:
    skills = json.load(jsonfile)
with open('SkillInfo.tsv') as tsvfile:
    skill_effects = {}
    next(tsvfile)
    for line in tsvfile:
        s_id, desc = line.split('\t')
        skill_effects[s_id] = desc.strip()

ATTRIBUTES = {
    'phy': ('Physical', 'MP', 'Physical', 'Y', 'N'),
    'gun': ('Gunfire', 'MP', 'Physical', 'Y', 'N'),
    'fir': ('Fire', 'MP', 'Magical', 'Y', 'N'),
    'ice': ('Ice', 'MP', 'Magical', 'Y', 'N'),
    'ele': ('Electricity', 'MP', 'Magical', 'Y', 'N'),
    'for': ('Force', 'MP', 'Magical', 'Y', 'N'),
    'rui': ('Ruin', 'MP', 'Magical', 'Y', 'N'),
    'alm': ('Almighty', 'MP', 'Magical', 'Y', 'N'),
    'rec': ('Recovery', 'MP', '-', 'Y', 'N'),
    'sup': ('Support', 'MP', '-', 'Y', 'N'),
    'spe': ('Special', 'MP', '-', 'Y', 'N'),
    'pas': ('Passive', '-', '-', 'Y', 'N'),
    'sab': ('Tandem', '-', '-', 'Y', 'N')
}

TARGETS = {
    '-': '-',
    '1 foe': 'Single enemy',
    'All foes': 'All enemies',
    'Multi foes': 'Multiple enemies',
    '1 ally': 'Single ally',
    'All allies': 'All allies',
}

new_skills = []

for s_id, entry in skills.items():
    s_name, elem, target = entry['a']
    price, cost, power, min_hits, max_hits, accuracy, crit, chance = entry['b']
    hits = f"{min_hits}-{max_hits}" if min_hits != max_hits else (str(min_hits) if max_hits > 2 else '1')
    elem, cost_type, dmg_type, in_battle, out_battle = ATTRIBUTES[elem]
    new_skills.append({
	'id': s_name.lower(),
        'attribute': elem.lower(),
        'damagetype': dmg_type,
        'cost': cost,
        'costtype': cost_type,
        'target': TARGETS[target],
        'hit': hits,
        'power': power,
        'crit': crit,
        'acc': accuracy,
        'inbattle': in_battle,
        'outbattle': out_battle,
        'description': skill_effects[s_id].replace('"', '\\"'),
        'name': s_name
    })

new_skills.sort(key=lambda x: x['id'])

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('data-skill.txt')
output = template.render(skills=new_skills)
print(output)
