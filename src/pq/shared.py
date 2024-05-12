#!/usr/bin/python3
import json

def load_id_file(fname):
    with open('pq1-data/battle/table/' + fname) as tsvfile:
        next(tsvfile)
        return [x.strip() for x in tsvfile]

def printif_notequal(dname, field, lhs, rhs):
    if str(lhs) != str(rhs):
        print(dname, field, lhs, rhs)

def save_ordered_demons(demons, fname):
    for entry in demons.values():
        for stat_set in ['resmods', 'ailmods', 'stats']:
            if stat_set in entry:
                entry[stat_set] = '[' + ', '.join(str(x) for x in entry[stat_set]) + ']'
        if 'skills' in entry and isinstance(entry['skills'], list):
            if len(entry['skills']) == 0:
                entry['skills'] = '[]'
            else:
                entry['skills'] = '[|' + '|, |'.join(x for x in entry['skills']) + '|]'
        if 'drops' in entry:
            if len(entry['drops']) == 0:
                entry['drops'] = '{}'
            else:
                entry['drops'] = '{' + ', '.join(f'|{x}|: {y}' for x, y in entry['drops'].items()) + '}'
        if 'skills' in entry and not isinstance(entry['skills'], str):
            nskills = sorted(entry['skills'].items(), key=lambda x: x[1])
            nskills = '{||      ' + ',||      '.join(f'|{x[0]}|: {x[1]}' for x in nskills) + '||    }'
            entry['skills'] = nskills

    jstring = json.dumps(demons, indent=2, sort_keys=True)
    jstring = jstring.replace('||', '\n').replace('|', '"')
    jstring = jstring.replace('"[', '[').replace(']"', ']').replace('"{', '{').replace('}"', '}')

    with open(fname, 'w+') as jsonfile:
        jsonfile.write(jstring)
