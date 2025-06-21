#!/usr/bin/python3
import re
import sys
import json
import yaml
import itertools

CONFIG_FILE, CONFIG_SECTION = sys.argv[1:3]

def load_rows_tsvfile(filename):
    rows = []
    with open(filename) as tsvfile:
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

class DemonParser:
    def __init__(self, config):
        self.language = config['language']
        self.col_format = config['colFormat']
        load_lookup = lambda x: load_lang_tsvfile(self.col_format[x]['inputPath'], self.language)

        demons = load_lookup('name')
        descriptions = load_lookup('description')
        self.demons = drop_unused_names(demons, descriptions)

        skills = load_lookup('skills')
        descriptions = load_lookup('skillEffects')
        self.skills = drop_unused_names(skills, descriptions)

        resist_keys = self.col_format['resists']['resistKeys']
        self.resist_lvls = { str(y): x for x, y in self.col_format['resists']['resistCodes'].items() }
        self.resists = []
        for row in load_rows_tsvfile(self.col_format['resists']['inputPath']):
            self.resists.append([row[k] for k in resist_keys])

        self.races = load_lookup('race')
        self.skilli = load_lookup('skilli')

    def get_resists(self, id):
        return(''.join(self.resist_lvls[x] for x in self.resists[id]))

    def demons_to_string(self, demons):
        formatters = {
            'numberList': lambda x: str(x),
            'stringList': lambda x: f"[|{'|, |'.join(x)}|]"
        }
        to_string = lambda x, k: formatters[self.col_format[k]['datatype']](x[k])

        new_demons = {}
        for name, entry in demons.items():
            new_demons[name] = entry.copy()
            new_demons[name]['stats'] = to_string(entry, 'stats')
            new_demons[name]['skills'] = to_string(entry, 'skills')

        output = json.dumps(new_demons, indent=2, sort_keys=True)
        output = output.replace('"[', '[').replace(']"', ']').replace('|', '"')
        return output

class SkillParser:
    def __init__(self, config):
        self.language = config['language']
        self.col_format = config['colFormat']
        load_lookup = lambda x: load_lang_tsvfile(self.col_format[x]['inputPath'], self.language)

        skills = load_lookup('name')
        self.descriptions = load_lookup('description')
        self.skills = drop_unused_names(skills, self.descriptions)

        self.elements = { x: 'pas' for x in range(20) }
        self.elements[-1] = 'spe'
        for id, element in load_lookup('element').items():
            self.elements[id] = element[:3].lower()

    def skills_to_string(self, skills):
        rows = ['{']
        for id, entry in skills.items():
            rows.append(f"  \"{id}\": {json.dumps(entry)},")
        rows[-1] = rows[-1][:-1]
        rows.append('}\n')
        return '\n'.join(rows)

def parse_demons(config):
    demon_parser = DemonParser(config)
    demons = {}
    for id, row in enumerate(load_rows_tsvfile(config['inputPath'])):
        if id not in demon_parser.demons:
            continue

        lookup_key = lambda x: int(row[config['colFormat'][x]['key']])
        lookup_keys = lambda x: [int(row[k]) for k in config['colFormat'][x]['keys']]
        name = demon_parser.demons[id]
        entry = {
            'race': demon_parser.races[lookup_key('race')],
            'lvl': lookup_key('lvl'),
            'resists': demon_parser.get_resists(lookup_key('resists')),
            'stats': lookup_keys('stats'),
            'skills': [demon_parser.skills[x] for x in lookup_keys('skills') if x != 0]
        }

        if lookup_key('skilli') != 255:
            entry['skilli'] = demon_parser.skilli[lookup_key('skilli')]

        demons[name] = entry
    
    output = demon_parser.demons_to_string(demons)
    with open(config['outputPath'], 'w+') as jsonfile:
        jsonfile.write(output)

def parse_skills(config):
    skill_parser = SkillParser(config)
    skills = {}
    for id, row in enumerate(load_rows_tsvfile(config['inputPath'])):
        if id not in skill_parser.skills:
            continue

        lookup_key = lambda x: int(row[config['colFormat'][x]['key']])
        name = skill_parser.skills[id]
        skills[id] = {
            'a': [name, skill_parser.elements[lookup_key('element').bit_length() - 1], '-'],
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
            'c': ['-', skill_parser.descriptions[id].split(' | <')[0], '-']
        }

    output = skill_parser.skills_to_string(skills)
    with open(config['outputPath'], 'w+') as jsonfile:
        jsonfile.write(output)

PARSERS = {
    'demonData': parse_demons,
    'skillData': parse_skills
}

with open(CONFIG_FILE) as yamlfile:
    CONFIG = yaml.safe_load(yamlfile)
PARSERS[CONFIG_SECTION](CONFIG[CONFIG_SECTION])
