#!/usr/bin/python3
import struct
import json
import re

NEUTRALS = r"[ST23459]"
WEAKS = r"[Z]"

def printif_notequal(dname, field, lhs, rhs):
    if str(lhs) != str(rhs):
        print(dname, field, lhs, rhs)

def save_ordered_demons(demons, fname):
    for entry in demons.values():
        for stat_set in ['resmods', 'ailmods', 'stats']:
            if stat_set in entry:
                entry[stat_set] = '[' + ', '.join(str(x) for x in entry[stat_set]) + ']'
        for stat_set in ['skills']:
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

def load_comp_config(fname):
    with open(fname) as jsonfile:
        comp_config = json.load(jsonfile)

    for hex_valued in ['itemsBegin']:
        v = comp_config[hex_valued]
        comp_config[hex_valued] = int(v, 16) if '0x' in v else int(v)

    for config_set in [['enemyStats', 'enemyResists', 'demonResists'], ['demonStats', 'demonSkills']]:
        offset = 0

        for cname in config_set:
            stat_config = comp_config[cname]

            for k, v in stat_config.items():
                stat_config[k] = int(v, 16) if '0x' in v else int(v)

            stat_config['begin'] = stat_config['begin'] + offset
            stat_config['end'] = stat_config['begin'] + stat_config['count'] * stat_config['length']
            offset = stat_config['end']

    comp_config['resistOrder'] = [comp_config['gameResists'].index(x) for x in comp_config['toolResists']]
    comp_config['ailmentOrder'] = [comp_config['gameAilments'].index(x) for x in comp_config['toolAilments']]
    comp_config['resistLvls'] = { int(x): y for x, y in comp_config['resistLvls'].items() }

    return comp_config

def check_resists(game_data, tool_data, demon_ids, stat_config, comp_config):
    resists_len = len(comp_config['gameResists'])
    ailments_len = len(comp_config['gameAilments'])
    resist_order = comp_config['resistOrder']
    ailment_order = comp_config['ailmentOrder']
    resist_lvls = comp_config['resistLvls']
    resist_mods = comp_config['resistMods']

    for d_id, line_start in enumerate(range(stat_config['begin'], stat_config['end'], stat_config['length'])):
        line = game_data[line_start:line_start + stat_config['length']]
        dname, in_comp = demon_ids[d_id].split('\t')

        if int(in_comp) < 1:
            continue

        demon = tool_data[dname]

        full_resists = struct.unpack(f"<{resists_len}H", line[:2*resists_len])
        full_ailments = struct.unpack(f"<{ailments_len}H", line[2*resists_len:2*(resists_len + ailments_len)])

        resists = ''.join(resist_lvls[full_resists[x] >> 8] for x in resist_order)
        ailments = ''.join(resist_lvls[full_ailments[x] >> 8] for x in ailment_order)
        res_mods = [5 * (full_resists[x] & 0xFF) for x in resist_order]
        ail_mods = [5 * (full_ailments[x] & 0xFF) for x in ailment_order]

        old_resists = demon['resists']
        old_ailments = demon.get('ailments', '-'*ailments_len)
        old_res_mods = demon.get('resmods', [0]*resists_len).copy()
        old_ail_mods = demon.get('ailmods', [0]*ailments_len).copy()

        for i, res_mod in enumerate(old_res_mods):
            if res_mod == 0:
                old_res_mods[i] = resist_mods[old_resists[i]]
        for i, ail_mod in enumerate(old_ail_mods):
            if ail_mod == 0:
                old_ail_mods[i] = resist_mods[old_ailments[i]]

        old_resists = re.sub(WEAKS, 'w', re.sub(NEUTRALS, '-', old_resists))
        old_ailments = re.sub(WEAKS, 'w', re.sub(NEUTRALS, '-', old_ailments))

        printif_notequal(dname, 'resists', old_resists, resists)
        printif_notequal(dname, 'ailments', old_ailments, ailments)
        printif_notequal(dname, 'res_mods', old_res_mods, res_mods)
        printif_notequal(dname, 'ail_mods', old_ail_mods, ail_mods)
