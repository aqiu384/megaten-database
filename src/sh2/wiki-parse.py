#!/usr/bin/python3
import sys
import json
import yaml
from jinja2 import Environment, FileSystemLoader

name = sys.argv[1]

with open('data/tool-format.yaml') as yamlfile:
    config = yaml.safe_load(yamlfile)['demonData']['colFormat']
with open('data/demon-data.json') as jsonfile:
    demons = [y.update({ 'name': x }) or y for x, y in json.load(jsonfile).items()]
    demons.sort(key=lambda x: x['lvl'])

RESIST_TYPES = { 'w': 'Wk', '-': '-', 's': 'Rs', 'n': 'Nu', 'r': 'Rp', 'd': 'Dr' }
RESIST_FRACS = { 'w': 150, 's': 50 }

env = Environment(loader=FileSystemLoader('templates'))
env.filters['resist_type_format'] = lambda x: RESIST_TYPES.get(x, x)
env.filters['resist_frac_format'] = lambda x: RESIST_FRACS.get(x, 100)
env.filters['skill_lvl_format'] = lambda x: '-' if x < 2 else str(x)
template = env.get_template('ally-demon-stats.txt')

for demon in demons:
    if not demon['name'].startswith(name):
        continue
    output = template.render(demon=demon, col_format=config)
    print()
    print(output)
