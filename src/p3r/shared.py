#!/usr/bin/python3
import json

def save_ordered_demons(demons, fname):
    for entry in demons.values():
        for stat_set in ['resmods', 'ailmods', 'stats']:
            if stat_set in entry:
                entry[stat_set] = '[' + ', '.join(str(x) for x in entry[stat_set]) + ']'
        for stat_set in ['skills', 'drops']:
            if stat_set in entry and isinstance(entry[stat_set], list):
                if len(entry[stat_set]) == 0:
                    entry[stat_set] = '[]'
                else:
                    entry[stat_set] = '[|' + '|, |'.join(x for x in entry[stat_set]) + '|]'
        if 'skills' in entry and not isinstance(entry['skills'], str):
            nskills = sorted(entry['skills'].items(), key=lambda x: x[1])
            nskills = '{||      ' + ',||      '.join(f'|{x[0]}|: {x[1]}' for x in nskills) + '||    }'
            entry['skills'] = nskills
        if 'drops' in entry and not isinstance(entry['drops'], str):
            entry['dodds'] = '{' + ', '.join(f'|{x[0]}|: {x[1]}' for x in entry['drops'].items()) + '}'
            del entry['drops']

    jstring = json.dumps(demons, indent=2, sort_keys=True)
    jstring = jstring.replace('||', '\n').replace('|', '"')
    jstring = jstring.replace('"[', '[').replace(']"', ']').replace('"{', '{').replace('}"', '}')

    with open(fname, 'w+') as jsonfile:
        jsonfile.write(jstring)

ITEMS = [
    ('Weapon',    0x0000),
    ('Armor',     0x1000),
    ('Shoes',     0x2000),
    ('Accs',      0x3000),
    ('Common',    0x4000),
    ('Evitem',    0x5000),
    ('Material',  0x6000),
    ('Skillcard', 0x7000),
    ('Costume',   0x8000)
]

def load_item_descs(fname, language, offset=0, max_flag=0):
    codes = {}
    with open(fname) as tsvfile:
        parts = next(tsvfile).strip().split('\t')
        col_index = parts.index(language)
        if max_flag == 0:
            for i, line in enumerate(tsvfile):
                iname = line.split('\t')[col_index].strip()
                if iname != '未使用':
                    codes[offset + i] = iname
        else:
            flag_index = parts.index('flag')
            for i, line in enumerate(tsvfile):
                parts = line.split('\t')
                flag = int(parts[flag_index])
                if 0 < flag and flag <= max_flag:
                    codes[offset + i] = parts[col_index].strip()
    return codes

def load_item_codes(language):
    item_files = 'Content/Xrd777/UI/Tables/DatItem{}NameDataAsset.tsv'
    codes = {}
    for fname, offset in ITEMS:
        codes.update(load_item_descs(item_files.format(fname), language, offset=offset))
    return codes

def load_item_prices():
    item_files = 'Content/Xrd777/UI/Tables/DatItem{}DataAsset.tsv'
    codes = {}
    for fname, offset in ITEMS:
        if fname == 'Evitem':
            continue
        codes.update(load_item_descs(item_files.format(fname), 'Price', offset=offset))
    return codes

def iterate_int_tsvfile(fname, skip_first=True):
    with open(fname) as tsvfile:
        headers = next(tsvfile).strip().split('\t')
        if skip_first:
            next(tsvfile)
        if headers[0] == 'ItemDef':
            for line in tsvfile:
                yield { headers[i]: int(x) for i, x in list(enumerate(line.split('\t')))[1:] }
        else:
            for line in tsvfile:
                yield { headers[i]: int(x) for i, x in enumerate(line.split('\t')) }

def table_header(values):
    return f"{table_row(values)}\n{table_row(['---'] * len(values))}"

def table_row(values):
    return f"| {' | '.join(values)} |"
