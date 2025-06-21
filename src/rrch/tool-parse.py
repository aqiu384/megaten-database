#!/usr/bin/python3
import re
import sys
import json
import yaml
import itertools

CONFIG_FILE, CONFIG_SECTION = sys.argv[1:3]

def load_rows_tsvfile(filename):
    rows = []
    with open(filename, encoding='utf-8') as tsvfile:
        keys = next(tsvfile).strip().split('\t')
        for row in tsvfile:
            rows.append({ keys[i]: v for i, v in enumerate(row.strip().split('\t')) })
    return rows

def load_lang_tsvfile(filename, language):
    lookup = {}
    for row in load_rows_tsvfile(filename):
        lookup[int(re.findall(r'\d{3,4}', row['id'])[-1])] = row[language]
    return lookup

def drop_unused_names(all_names, used_names):
    seen = {}
    lookup = {}
    for id, name in all_names.items():
        if id not in used_names:
            continue

        if name not in seen:
            seen[name] = 0
        new_name = f"{name} {chr(65 + seen[name])}" if seen[name] > 0 else name
        seen[name] += 1

        lookup[id] = new_name
    return lookup

def json_dump_lookup(lookup):
    rows = ['{']
    for id, entry in lookup.items():
        rows.append(f"  \"{id}\": {json.dumps(entry)},")
    rows[-1] = rows[-1][:-1]
    rows.append('}\n')
    return '\n'.join(rows)

class CompendiumParser:
    def __init__(self, config):
        col_format = config['commonData']['colFormat']
        load_lookup = lambda x: load_lang_tsvfile(col_format[x]['inputPath'], config['commonData']['language'])

        self.all_demons = load_lookup('demonNames')
        self.used_demon_descs = load_lookup('demonDescs')
        self.used_demons = drop_unused_names(self.all_demons, self.used_demon_descs)

        self.all_skills = load_lookup('skillNames')
        self.used_skill_descs = load_lookup('skillDescs')
        self.used_skills = drop_unused_names(self.all_skills, self.used_skill_descs)

        self.all_items = load_lookup('itemNames')
        self.used_item_descs = load_lookup('itemDescs')
        self.used_items = drop_unused_names(self.all_items, self.used_item_descs)

        self.races = load_lookup('races')
        self.invest_skills = load_lookup('investSkillNames')

        self.elements = { x: 'pas' for x in range(20) }
        self.elements[-1] = 'spe'
        for id, element in load_lookup('elements').items():
            self.elements[id] = element[:3].lower()

        resist_keys = col_format['resists']['resistKeys']
        self.resist_lvls = { str(y): x for x, y in col_format['resists']['resistCodes'].items() }
        self.resists = []
        for row in load_rows_tsvfile(col_format['resists']['inputPath']):
            self.resists.append([row[k] for k in resist_keys])

    def get_resists(self, id):
        return(''.join(self.resist_lvls[x] for x in self.resists[id]))

def parse_demons(config, comp_parser):
    demons = {}
    for id, row in enumerate(load_rows_tsvfile(config['inputPath'])):
        lookup_key = lambda x: int(row[config['colFormat'][x]])
        lookup_keys = lambda x: [int(row[k]) for k in config['colFormat'][x]['keys']]

        if id not in comp_parser.used_demons:
            continue

        name = comp_parser.used_demons[id]
        entry = {
            'race': comp_parser.races[lookup_key('race')],
            'lvl': lookup_key('lvl'),
            'resists': comp_parser.get_resists(lookup_key('resists')),
            'stats': lookup_keys('stats'),
            'skills': [comp_parser.used_skills[x] for x in lookup_keys('skills') if x != 0]
        }

        if lookup_key('skilli') != 255:
            entry['skilli'] = comp_parser.invest_skills[lookup_key('skilli')]

        demons[name] = entry

    formatters = {
        'numberList': lambda x: str(x),
        'stringList': lambda x: f"[|{'|, |'.join(x)}|]"
    }
    to_string = lambda x, k: formatters[config['colFormat'][k]['datatype']](x[k])

    new_demons = {}
    for name, entry in demons.items():
        new_demons[name] = entry.copy()
        new_demons[name]['stats'] = to_string(entry, 'stats')
        new_demons[name]['skills'] = to_string(entry, 'skills')

    output = json.dumps(new_demons, indent=2, sort_keys=True)
    output = output.replace('"[', '[').replace(']"', ']').replace('|', '"')

    with open(config['outputPath'], 'w+') as jsonfile:
        jsonfile.write(output)

def parse_skills(config, comp_parser):
    skills = {}
    for id, row in enumerate(load_rows_tsvfile(config['inputPath'])):
        lookup_key = lambda x: int(row[config['colFormat'][x]])

        if id not in comp_parser.used_skills:
            continue

        name = comp_parser.used_skills[id]
        skills[id] = {
            'a': [name, comp_parser.elements[lookup_key('element').bit_length() - 1], '-'],
            'b': [
                0,
                lookup_key('cost'),
                lookup_key('power'),
                lookup_key('minhit'),
                lookup_key('maxhit'),
                99,
                0,
                lookup_key('chance')
            ],
            'c': ['-', comp_parser.used_skill_descs[id].split(' | <')[0], '-']
        }

    output = json_dump_lookup(skills)
    with open(config['outputPath'], 'w+') as jsonfile:
        jsonfile.write(output)

def parse_confine_drops(config, comp_parser):
    drops = {}
    demons = load_rows_tsvfile(config['colFormat']['demon']['inputPath'])

    for id, row in enumerate(load_rows_tsvfile(config['inputPath'])):
        lookup_key = lambda x: int(row[config['colFormat'][x]])
        lookup_keys = lambda x: [int(row[k]) for k in config['colFormat'][x]['keys']]
        id += config['colFormat']['demon']['offset']
        id = int(demons[id][config['colFormat']['demon']['key']])

        if lookup_key('failureRate') == 100 or id not in comp_parser.all_demons:
            continue

        name = comp_parser.all_demons[id]
        entry = {
            'items': [comp_parser.used_items.get(x, '-') for x in lookup_keys('dropItems')],
            'rates': lookup_keys('dropRates')
        }

        if name not in drops:
            drops[name] = entry
        if len(str(drops[name]['items'])) < len(str(entry)):
            drops[name] = entry
    
    output = json_dump_lookup(drops)
    with open(config['outputPath'], 'w+') as jsonfile:
        jsonfile.write(output)

PARSERS = {
    'demonData': parse_demons,
    'skillData': parse_skills,
    'confineDropData': parse_confine_drops
}

with open(CONFIG_FILE) as yamlfile:
    CONFIG = yaml.safe_load(yamlfile)
COMP_PARSER = CompendiumParser(CONFIG)
PARSERS[CONFIG_SECTION](CONFIG[CONFIG_SECTION], COMP_PARSER)
