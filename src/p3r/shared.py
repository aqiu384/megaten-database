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

    jstring = json.dumps(demons, indent=2, sort_keys=True)
    jstring = jstring.replace('||', '\n').replace('|', '"')
    jstring = jstring.replace('"[', '[').replace(']"', ']').replace('"{', '{').replace('}"', '}')

    with open(fname, 'w+') as jsonfile:
        jsonfile.write(jstring)
