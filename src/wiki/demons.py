#!/usr/bin/python3
import json
import sys
from math import floor

GAME, RACE = sys.argv[1:]

with open(f"configs/{GAME}.json") as jsonfile:
    comp_config = json.load(jsonfile)

def load_data(dataset):
    merged = {}
    for fname in comp_config.get(dataset, []):
        prefix, fname = fname.split('/')
        prefix = comp_config['dataDirs'][int(prefix)]
        with open(prefix + fname) as jsonfile:
            merged.update(json.load(jsonfile))
    return merged

demon_data = load_data('demonDatas')
skill_data = load_data('skillDatas')
align_data = load_data('alignmentDatas')
evolve_to = load_data('evolutions')
fusion_prereqs = load_data('fusionPrereqs')
special_recipes = load_data('specialRecipes')
comp_params = comp_config['params']

AFFINITY_ELEMS = comp_params.get('affinitySkills', [])
skill_elems = { entry['a'][0]: entry['a'][1] for entry in skill_data.values() }
skill_elems = { skill: AFFINITY_ELEMS.index(elem) if elem in AFFINITY_ELEMS else -1 for skill, elem in skill_elems.items() }
evolve_from = { result['result']: { 'ingred': ingred, 'lvl': result['lvl'] } for ingred, result in evolve_to.items() }

def format_align(demon):
    align = align_data.get(demon['name'], align_data.get(demon['race'], ''))
    return f"|{comp_params['alignment']}={align}" if align != '' else ''

def format_base_stats(demon):
    stats = demon['stats']
    lines = [f"|{x}={stats[i]}" for i, x in enumerate(comp_params['baseStats'])]
    return '\n'.join(lines)

def format_smt4_base_stats(demon):
    stats = demon['stats']
    lvl = floor(demon['lvl'])
    hp = stats[0] + lvl * stats[2]
    mp = floor(0.45 * (stats[1] + lvl * stats[3]))
    stats = [hp, mp] + stats[4:]
    lines = [f"|{x}={stats[i]}" for i, x in enumerate(comp_params['smt4BaseStats'])]
    return '\n'.join(lines)

SMT4F_MP_GROWS = [0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 4, 5]
def format_smt4f_base_stats(demon):
    stats = demon['stats']
    lvl = floor(demon['lvl'] - 1)
    hp = stats[0] + lvl * stats[2]
    mp = stats[1] + lvl * SMT4F_MP_GROWS[stats[3]]
    stats = [hp, mp] + stats[4:]
    lines = [f"|{x}={stats[i]}" for i, x in enumerate(comp_params['smt4fBaseStats'])]
    return '\n'.join(lines)

def format_fusion_prereq(demon):
    dname = demon['name']
    prereq = fusion_prereqs.get(dname, '')
    if prereq.startswith('Clear'):
        prereq = prereq.replace('"', ']]"').replace(' ]]"', ' "[[')
    elif 'efeat' in prereq:
        prereq = f'Defeat [[{dname}]]'
    elif prereq == 'Fusion Accident':
        prereq = ''
    return f"|{comp_params['fusionPrereq']}={prereq}" if prereq != '' else ''

def format_special_recipe(demon):
    dname = demon['name']
    recipe = ''
    if 'Fusion Accident' in fusion_prereqs.get(dname, ''):
        recipe = '[[Fusion Accident]] only'
    elif dname in  special_recipes:
        recipe = f"[[Special Fusion]]{{{{Exp|{' x '.join(special_recipes[dname])}}}}}"
    return f"|{comp_params['specialRecipe']}={recipe}" if recipe != '' else ''

def format_evolutions(demon):
    params = comp_params['evolution']
    dname = demon['name']
    lines = []
    if dname in evolve_from:
        lines.append(f"|{params[0]}={evolve_from[dname]['ingred']}")
        lines.append(f"|{params[1]}={evolve_from[dname]['lvl']}")
    if dname in evolve_to:
        lines.append(f"|{params[2]}={evolve_to[dname]['result']}")
        lines.append(f"|{params[3]}={evolve_to[dname]['lvl']}")
    return '\n'.join(lines)

def format_resist_elems(demon):
    elems = comp_params['resistElems']
    codes = comp_params['resistElemCodes']
    resists = [codes[x] for x in demon['resists']]
    lines = [f"|{x}={resists[i]}" for i, x in enumerate(elems) if resists[i] != '-']
    return '\n'.join(lines)

DEFAULT_RESIST_MODS = [0] * len(comp_params.get('resistFracs', []))
def format_resist_fracs(demon):
    elems = comp_params['resistFracs']
    codes = comp_params['resistFracCodes']
    resmods = demon.get('resmods', DEFAULT_RESIST_MODS)
    resists = [resmods[i] / 100 if resmods[i] != 0 else codes[x] for i, x in enumerate(demon['resists'])]
    lines = [f"|{x}frac={resists[i]}" for i, x in enumerate(elems) if resists[i] != 1]
    return '\n'.join(lines)

DEFAULT_AILMENTS = ''.join(['-'] * len(comp_params.get('ailmentFracs', [])))
DEFAULT_AILMENT_MODS = [0] * len(comp_params.get('ailmentFracs', []))
def format_ailment_fracs(demon):
    elems = comp_params['ailmentFracs']
    codes = comp_params['ailmentFracCodes']
    resmods = demon.get('ailmods', DEFAULT_AILMENT_MODS)
    resists = [resmods[i] / 100 if resmods[i] != 0 else codes[x] for i, x in enumerate(demon.get('ailments', DEFAULT_AILMENTS))]
    lines = [f"|{x}={resists[i]}" for i, x in enumerate(elems) if resists[i] != 1]
    return '\n'.join(lines)

def format_affinity_lvl(lvl):
    return f" {'+' if lvl > 0 else ''}{lvl}" if lvl != 0 else ''

def format_affinity_elems(demon):
    affinities = demon['affinities']
    elems = comp_params['affinityElems']
    lines = [f"|{x}={format_affinity_lvl(affinities[i]).strip()}" for i, x in enumerate(elems) if affinities[i] != 0]
    return '\n'.join(lines)

def format_smt4_attack(demon):
    params = comp_params['smt4Attack']
    if 'attack' not in demon:
        return ''
    elem, target = demon['attack'].split(', ')
    elem, hits = elem.split(' x')
    lines = []
    if elem != 'Phys':
        lines.append(f"|{params[0]}={elem}")
    if hits != '1':
        lines.append(f"|{params[1]}={hits}")
    if target != '1 foe':
        lines.append(f"|{params[2]}={target}")
    return '\n'.join(lines)

def format_skills(demon):
    skills = [(sname, slvl) for sname, slvl in demon['skills'].items()]
    lines = [f"{{{{{comp_params['skillTemplate']}|{sname}|{'-' if slvl < 2 else slvl}}}}}" for sname, slvl in skills]
    return '|skills=' + '\n'.join(lines)

def format_affinity_skills(demon):
    affinities = demon['affinities'] + [0]
    skills = [(sname, affinities[skill_elems[sname]], '-' if slvl < 2 else floor(slvl)) for sname, slvl in demon['skills'].items()]
    lines = [f"{{{{{comp_params['skillTemplate']}|{sname}{format_affinity_lvl(saffinity)}|{slvl}}}}}" for sname, saffinity, slvl in skills]
    return '|skills=' + '\n'.join(lines)

PARAM_FORMATS = {
    'race': lambda demon: f"|{comp_params['race']}={demon['race']}",
    'alignment': format_align,
    'lvl': lambda demon: f"|{comp_params['lvl']}={demon['lvl']}",
    'cost': lambda demon: f"|{comp_params['cost']}={2 * demon['price']}",
    'baseStats': format_base_stats,
    'smt4BaseStats': format_smt4_base_stats,
    'smt4fBaseStats': format_smt4f_base_stats,
    'fusionPrereq': format_fusion_prereq,
    'specialRecipe': format_special_recipe,
    'evolution': format_evolutions,
    'resistElems': format_resist_elems,
    'resistFracs': format_resist_fracs,
    'ailmentFracs': format_ailment_fracs,
    'affinityElems': format_affinity_elems,
    'smt4Attack': format_smt4_attack,
    'skills': format_skills,
    'affinitySkills': format_affinity_skills
}

for dname, entry in sorted(demon_data.items(), key=lambda x: x[1]['lvl'], reverse=True):
    race = entry['race']
    entry['name'] = dname
    if race != RACE:
        continue
    lines = [dname, '{{' + comp_params['template']]
    for param, format in PARAM_FORMATS.items():
        if param in comp_params:
            lines.append(format(entry))
    lines.append('}}')
    print('\n'.join(x for x in lines if x != ''))
