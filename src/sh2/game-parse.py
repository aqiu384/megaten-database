#!/usr/bin/python3
import sys
import json
import yaml
import itertools

ID_NAME = 'id'
CONFIG_FILE, CONFIG_SECTION = sys.argv[1:3]

def load_row_data(filename, row_location_nesting):
    with open(filename, encoding='utf-8') as datafile:
        if filename.endswith('.json'):
            row_data = json.load(datafile)
        else:
            for _ in range(3):
                next(datafile)
            row_data = yaml.safe_load(datafile)
    for k in row_location_nesting:
        row_data = row_data[k]
    return row_data

def load_lang_table(config):
    table = {}
    col_format = [(x, y) for x, y in config['colFormat'].items()]

    for lang in config['languages']:
        for row in load_row_data(config['inputPath'].format(lang), CONFIG['rowLocationNesting']):
            curr_id = None
            for col_key, col_name in col_format:
                if col_name == ID_NAME:
                    curr_id = row[col_key]
                    if curr_id not in table:
                        table[curr_id] = []
                else:
                    curr_name = row[col_key]
                    if isinstance(curr_name, list):
                        curr_name = '\\n'.join(x if x is not None else 'Null' for x in curr_name)
                    table[curr_id].append(curr_name)

    new_table = {}

    for row_id, row_data in table.items():
        if all(x is not None and x not in config['nullValues'] for x in row_data):
            new_table[row_id] = row_data

    return new_table

FLATTEN_ROW = {
    'stringList': lambda r, c: r,
    'stringDict': lambda r, c: [r[k] for k in c['format']],
    'objectList': lambda r, c: itertools.chain(r[i][k] for k in c['format'] for i in range(c['length']))
}

def load_data_table(config):
    table = []
    col_formats = [(x, y) for x, y in config['colFormat'].items()]

    for row in load_row_data(config['inputPath'], CONFIG['rowLocationNesting']):
        table.append([])
        for col_key, col_config in col_formats:
            if col_config is None:
                table[-1].append(row[col_key])
            else:
                table[-1].extend(FLATTEN_ROW[col_config['datatype']](row[col_key], col_config))

    return table

FLATTEN_HEADER = {
    'stringList': lambda c: [f"{c['key']}{i}" for i in range(c['length'])],
    'stringDict': lambda c: list(c['format'].values()),
    'objectList': lambda c: itertools.chain(f"{v}{i}" for v in c['format'].values() for i in range(c['length']))
}

def get_data_table_headers(config):
    headers = []

    for col_key, col_config in config['colFormat'].items():
        if col_config is None:
            headers.append(col_key)
        else:
            headers.extend(FLATTEN_HEADER[col_config['datatype']](col_config))

    return headers

with open(CONFIG_FILE) as yamlfile:
    ALL_CONFIGS = yaml.safe_load(yamlfile)
    CONFIG = ALL_CONFIGS[CONFIG_SECTION]
if 'baseLanguageConfig' in CONFIG:
    new_config = json.loads(json.dumps(ALL_CONFIGS.get(CONFIG['baseLanguageConfig'], {})))
    new_config.update(CONFIG)
    CONFIG = new_config
    table = load_lang_table(CONFIG)
    with open(CONFIG['outputPath'], 'w+', encoding='utf8') as tsvfile:
        tsvfile.write(f"{ID_NAME}\t{'\t'.join(CONFIG['languages'])}\n")
        for row_id, row_data in table.items():
            tsvfile.write(f"{row_id}\t{'\t'.join(x.replace('\n', '\\n').replace('"', "''") for x in row_data)}\n")
else:
    table = load_data_table(CONFIG)
    with open(CONFIG['outputPath'], 'w+', encoding='utf8') as tsvfile:
        tsvfile.write(f"{'\t'.join(get_data_table_headers(CONFIG))}\n")
        for row in table:
            tsvfile.write(f"{'\t'.join(str(x) for x in row)}\n")
