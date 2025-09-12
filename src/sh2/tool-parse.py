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

def load_lang_tsvfile(filename, key, language):
    lookup = {}
    for row in load_rows_tsvfile(filename):
        lookup[row[key]] = row[language]
    return lookup

def drop_unused_names(all_names, used_names, remapped_ids):
    seen = {}
    lookup = {}
    for id, name in all_names.items():
        if id not in used_names:
            continue

        if name not in seen:
            seen[name] = 0
        new_name = f"{name} {chr(65 + seen[name])}" if seen[name] > 0 else name
        seen[name] += 1

        lookup[id] = remapped_ids.get(new_name, new_name)
    return lookup

def json_dump_lookup(lookup):
    rows = ['{']
    for id, entry in lookup.items():
        rows.append(f"  \"{id}\": {json.dumps(entry, ensure_ascii=False)},")
    rows[-1] = rows[-1][:-1]
    rows.append('}\n')
    return '\n'.join(rows)

class CompendiumParser:
    def __init__(self, config):
        self.lookup_files = {}
        self.nullChecks = []
        self.parsers = []

        for lookup_key, lookup_config in config['lookupFiles'].items():
            filename, key, language = (lookup_config[k] for k in ['filename', 'key', 'language'])
            if language != '-':
                all_names = load_lang_tsvfile(filename, key, language)
                if 'remappedUniqueIds' in lookup_config:
                    all_names = drop_unused_names(all_names, all_names, lookup_config['remappedUniqueIds'])
                self.lookup_files[lookup_key] = all_names
            else:
                self.lookup_files[lookup_key] = { row[key]: str(list(row.values())) for row in load_rows_tsvfile(filename) }
                self.lookup_files[lookup_key]['0'] = '[]'

        for null_key, null_values in config['nullChecks'].items():
            self.nullChecks.append((null_key, null_values))

        def make_resist_parser(type_format, lvl_format, elems, lookup):
            def resist_parser(row):
                resists = []
                for elem in elems:
                    k = int(row[type_format.format(elem)]) * 1000 + int(row[lvl_format.format(elem)])
                    resists.append(lookup.get(k, f"_{k}_"))
                return ''.join(resists)
            return resist_parser

        def make_skill_parser(lookup_format, type_format, lvl_format, elems, skill_offset, lookup, one_line):
            def skill_parser(row):
                skills = {}
                innate_ind = 0

                for elem in elems:
                    s_id = int(row[type_format.format(elem)])
                    s_lvl = int(row[lvl_format.format(elem)])

                    if s_id == 0:
                        continue
                    if s_lvl == 0:
                        innate_ind += 1
                        s_lvl = innate_ind / 10

                    s_id = lookup_format.format(s_id + skill_offset)
                    skills[lookup.get(s_id, s_id)] = s_lvl

                parts =  [f'|{x[0]}|: {x[1]}' for x in skills.items()]
                if one_line:
                    return '{' + ', '.join(parts) + '}'
                else:
                    return '{||      ' + ',||      '.join(parts) + '||    }'
            return skill_parser

        def add_parser(parsers, col_key, col_format, lookup_files):
            if isinstance(col_format, str) and col_format == 'unknown':
                return
            new_col_key = col_format.get('rename', col_key)
            col_type = col_format['type']

            if col_type == 'integer':
                self.parsers.append((new_col_key, lambda row: int(row[col_key])))
            elif col_type == 'integerList':
                self.parsers.append((new_col_key, lambda row: str([int(row[x]) for x in col_format['keys']])))
            elif col_type == 'floatList':
                self.parsers.append((new_col_key, lambda row: str([float(row[x]) for x in col_format['keys']])))
            elif col_type == 'boolean':
                self.parsers.append((new_col_key, lambda row: row[col_key] == 1))
            elif col_type == 'lookupFile':
                self.parsers.append((new_col_key, lambda row: lookup_files[col_format['lookupFile']].get(row[col_key], 'MISSING')))
            elif col_type == 'lookup':
                lookup = { str(v): k for k, v in col_format['lookup'].items() }
                self.parsers.append((new_col_key, lambda row: lookup.get(row[col_key], f"UNKNOWN_{row[col_key]}")))
            elif col_type == 'resistList':
                self.parsers.append((new_col_key, make_resist_parser(
                    col_format['resistTypeFormat'],
                    col_format['resistLvlFormat'],
                    col_format['resistElems'],
                    { v: k for k, v in col_format['lookup'].items() }
                )))
            elif col_type == 'skillLookup':
                self.parsers.append((new_col_key, make_skill_parser(
                    col_format['skillLookupFormat'],
                    col_format['skillTypeFormat'],
                    col_format['skillLvlFormat'],
                    col_format['skillElems'],
                    col_format['skillOffset'],
                    { str(v): k for k, v in col_format['lookup'].items() },
                    True
                )))
            elif col_type == 'skillLookupFile':
                self.parsers.append((new_col_key, make_skill_parser(
                    col_format['skillLookupFormat'],
                    col_format['skillTypeFormat'],
                    col_format['skillLvlFormat'],
                    col_format['skillElems'],
                    col_format['skillOffset'],
                    lookup_files[col_format['lookupFile']],
                    False
                )))

        for col_key, col_format in config['colFormat'].items():
            add_parser(self.parsers, col_key, col_format, self.lookup_files)

    def has_nulls(self, row):
        return any(row[k] in vals for k, vals in self.nullChecks)

    def parse_row(self, row):
        return { k: parser(row) for k, parser in self.parsers }

def parse_skills(config, comp_parser):
    skills = {}

    for id, old_row in enumerate(load_rows_tsvfile(config['inputPath'])):
        if comp_parser.has_nulls(old_row):
            continue
        row = comp_parser.parse_row(old_row)
        skills[row['id']] = {
            'a': [row['name'], row['elem'].lower()[:3], row['target']],
            'b': [row['rank'], row['cost'], row['power'], row['minhits'], row['maxhits'], row['accuracy'], 0, 0],
            'c': ['-', '-', row['description'], '|'.join(row[f"m_SkillEffID0{i}"] for i in range(5))]
        }

    output = json_dump_lookup(skills)
    with open(config['outputPath'], 'w+') as jsonfile:
        jsonfile.write(output)

def parse_demons(config, comp_parser):
    demons = {}
    if config['importData']:
        with open(config['importData']) as jsonfile:
            demons = json.load(jsonfile)

    for id, old_row in enumerate(load_rows_tsvfile(config['inputPath'])):
        if comp_parser.has_nulls(old_row):
            continue
        row = comp_parser.parse_row(old_row)
        name = row['name']
        del row['name']
        if name not in demons:
            demons[name] = {}
        demons[name].update(row)

    output = json.dumps(demons, indent=2, sort_keys=True)
    output = output.replace('||', '\n').replace('|', '"')
    output = output.replace('"[', '[').replace(']"', ']').replace('"{', '{').replace('}"', '}')

    with open(config['outputPath'], 'w+') as jsonfile:
        jsonfile.write(output)

PARSERS = {
    'demonData': parse_demons,
    'skillData': parse_skills
}

with open(CONFIG_FILE) as yamlfile:
    CONFIG = yaml.safe_load(yamlfile)[CONFIG_SECTION]
COMP_PARSER = CompendiumParser(CONFIG)
PARSERS[CONFIG_SECTION](CONFIG, COMP_PARSER)
