#!/usr/bin/python3
import re
import sys
import json
import yaml
import struct
import itertools

CONFIG_FILE, CONFIG_SECTION = sys.argv[1:3]

def load_rows_binfile(CONFIG):
    rows = []
    with open(CONFIG['inputPath'], 'rb') as binfile:
        binfile.read(CONFIG['rowOffset'])
        while True:
            row = binfile.read(CONFIG['rowLength'])
            if not row:
                break
            rows.append(row)
    return rows

def load_rows_tsvfile(filename):
    rows = []
    with open(filename, encoding='utf-8') as tsvfile:
        keys = next(tsvfile).strip().split('\t')
        for index, row in enumerate(tsvfile):
            rows.append({ keys[i]: v for i, v in enumerate(row.strip().split('\t')) })
            rows[-1]['index'] = index
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
                with open(filename) as jsonfile:
                    self.lookup_files[lookup_key] = json.load(jsonfile)

        type_offsets = { 'ubyte': (1, '<B'), 'ushort': (2, '<H'), 'ulong': (4, '<L') }

        def add_parser(parsers, col_key, col_format, lookup_files):
            if isinstance(col_format, str) and col_format == 'unknown':
                return
            new_col_key = col_format.get('rename', col_key)
            col_start = col_format['index']
            col_len, col_packed = type_offsets[col_format['type']]

            if 'lookup' in col_format:
                lookup = { v: k for k, v in col_format['lookup'].items() }
                def parse_col(row):
                    col_key = struct.unpack(col_packed, row[col_start:col_start + col_len])[0]
                    return lookup.get(col_key, f"MISSING_{col_key}")
                self.parsers.append((new_col_key, parse_col))
            else:
                self.parsers.append((new_col_key, lambda row: struct.unpack(col_packed, row[col_start:col_start + col_len])[0]))

        for col_key, col_format in config['colFormat'].items():
            add_parser(self.parsers, col_key, col_format, self.lookup_files)

    def has_nulls(self, row):
        return any(row[k] in vals for k, vals in self.nullChecks)

    def parse_row(self, row):
        return { k: parser(row) for k, parser in self.parsers }

def parse_skills(config, comp_parser):
    skills = {}
    cost_prefixes = { '-': 0, 'HP': 0, 'MP': 1000 }

    for id, old_row in enumerate(load_rows_binfile(CONFIG)):
        if comp_parser.has_nulls(old_row):
            continue

        row = comp_parser.parse_row(old_row)
        name = 'SKILL_L{:04}'.format(id)
        name = comp_parser.lookup_files['skillNames'].get(name, name)
        effect = 'DATSKILLHELP_L{:04}'.format(id)
        effect = comp_parser.lookup_files['skillDescs'].get(effect, effect)
        old_row = comp_parser.lookup_files['oldSkillData'].get(name, {})

        print(id, name, row)

        cost = cost_prefixes[row['costType']] + row['costAmount']
        power = 0 if row['powerScalesWith'] == '-' else row['power']
        accuracy = row['accuracyBase'] - row['accuracyPenalty']
        ailment_chance = row['ailmentChance'] if row['ailmentEffect'] == 'inflict' else 0

        skills[id] = {
            'a': [name, old_row.get('element', '-'), row['target']],
            'b': [old_row.get('rank', 99), cost, power, 1, row['maxhitsOverall'], accuracy, row['crit'], ailment_chance],
            'c': [row['ailmentType'], 'FMTExact' if ailment_chance != 0 else '-', old_row.get('requires', '-')[:3].lower()],
            'd': [effect]
        }

    for id in range(288, 500):
        name = 'SKILL_L{:04}'.format(id)
        name = comp_parser.lookup_files['skillNames'].get(name, name)
        effect = 'DATSKILLHELP_L{:04}'.format(id)
        effect = comp_parser.lookup_files['skillDescs'].get(effect, effect)
        old_row = comp_parser.lookup_files['oldSkillData'].get(name, {})

        skills[id] = {
            'a': [name, old_row.get('element', '-'), '-'],
            'b': [old_row.get('rank', 99), 0, 0, 1, 1, 0, 0, 0],
            'c': ['-', '-', old_row.get('requires', '-')[:3].lower()],
            'd': [effect]
        }

    output = json_dump_lookup(skills)
    with open(config['outputPath'], 'w+') as jsonfile:
        jsonfile.write(output)

PARSERS = {
    'skillData': parse_skills
}

with open(CONFIG_FILE) as yamlfile:
    CONFIG = yaml.safe_load(yamlfile)[CONFIG_SECTION]
COMP_PARSER = CompendiumParser(CONFIG)
PARSERS[CONFIG_SECTION](CONFIG, COMP_PARSER)
