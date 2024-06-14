#!/usr/bin/python3
import struct

LINE_LEN = 0xC0
LINE_LEN = 0xC4
START_OFFSET = 0x65
END_OFFSET = START_OFFSET + 400 * LINE_LEN
SKILL_TYPES = {
    0: 'Physical',
    1: 'Magic',
    2: 'Ailment',
    3: 'Recovery',
    4: 'Support',
    7: 'Revival Chant',
    8: 'Special',
    9: 'Summon',
    13: 'Scale Magic',
    14: 'Scale Phys',
    15: 'UNDEFINED'
}

USE_TYPES = {
    0: 'Support',
    4: 'Recovery',
    5: 'Ailment',
    257: 'USE_257',
    1282: 'Attack'
}

AFFINITIES = [
    'None',
    'Attack',
    'Ailment',
    'Recovery',
    'Support',
    'Other'
]

RESIST_ELEMS = [
    'UNDEFINED', 'phy1', 'phy2', 'fir',
    'ice', 'ele', 'for', 'lig', 'dar',
    'alm'
]

TARGETS = [
    '1 foe', 'All foes', '1 ally', 'All allies',
    'Self', 'UNDEFINED', 'Rand foes', '1 stock',
    'All stock'
]

DAMAGES = ['Boss', 'Element', 'Phys1', 'Phys2', 'Support']

ICONS = [
    'phy',
    'fir',
    'ice',
    'ele',
    'for',
    'lig',
    'dar',
    'alm',
    'ail',
    'sup',
    'rec',
    'spe',
    'pas',
    'mag'
]

PRESS_TURNS = {
    0: 'phy',
    1: 'fir',
    2: 'ice',
    3: 'ele',
    4: 'for',
    5: 'lig',
    6: 'dar',
    7: 'alm',
    8: 'poi',
    10: 'pan',
    11: 'cha',
    12: 'sle',
    13: 'sea',
    20: 'mir',
    32: ''
}

AILMENTS = [
    'Instakill',
    'Poison',
    'AILMENT_3',
    'Panic',
    'Charm',
    'Sleep',
    'Seal',
    'AILMENT_8',
    'AILMENT_9',
    'Mirage',
    'AILMENT_11',
    'AILMENT_12',
    'AILMENT_13',
    'AILMENT_14',
    'Mud',
    'Shroud'
]

AILMENT_CURES = {
    0: 'None',
    1: 'Instakill',
    16: 'Shroud',
    100: 'Normal',
    103: 'All'
}

SUPPORT_TYPES = {
    0: 'None',
    256: 'Barrier',
    768: 'Buff'
}

UNIQUES = {
    0: 0,
    257: 1
}

MOD_FLAGS = {
    1: 'Charge',
    2: 'Concentrate',
    3: 'Critical Aura',
    9: 'Taunt',
    13: 'Kannabi Veil',
    14: 'Attack',
    16: 'Donum Gladi',
    17: 'Donum Magici',
    20: 'Meseket\'s Path',
    21: 'Heliopolis Dawn',
    22: 'Tetrakarn',
    23: 'Makarakarn',
    24: 'Trafuri',
    25: 'Bowl of Hygieia 1',
    26: 'Bowl of Hygieia 2',
    27: 'Electrify',
    28: 'Rising Storm Dragon',
    29: 'Replication 1',
    30: 'False Replication',
    31: 'Replication 2',
    32: 'Contempt of God',
    35: 'Impaler\'s Animus Pierce',
    36: 'Impaler\'s Animus Charge',
    37: 'Magatsuhi Harvest',
    38: 'True Replication',
    39: 'Revival Chant',
    40: 'Estoma',
    41: 'NOT_USED_393',
    42: 'Chaotic Will',
    43: 'Escape',
    44: 'Red Capote',
    45: 'Omagatoki: Critical',
    46: 'Shield of God',
    47: 'Impaler\'s Glory Charge',
    48: 'Omagatoki: Pierce',
    49: 'Omagatoki: Hit 1',
    50: 'Omagatoki: Hit 2',
    51: 'Omagatoki: Adversity',
    52: 'Omagatoki: Free',
    53: 'Omagatoki: Doubler',
    54: 'Omagatoki: Dance',
    55: 'Omagatoki: Sincerity',
    56: 'Omagatoki: Savage',
    57: 'Omagatoki: Luck 1',
    58: 'Omagatoki: Luck 2',
    59: 'Omagatoki: Potential',
    60: 'Omagatoki: Charge',
    61: 'Soul Drain 1',
    62: 'Soul Drain 2',
    63: 'Dekajaon',
    64: 'Magatsuhi 1',
    65: 'Magatsuhi 2',
    66: 'Accursed Poison'
}

MOD_CONDS = {
    0: 'None',
    2: 'Weakness',
    3: 'Critical',
    4: 'Ailment',
    5: 'Single',
    6: 'Magatsuhi MP',
}
MOD_ADJUSTS = {
    0: 'None',
    1: 'Power',
    2: 'Instakill',
    8: 'Max Hits',
    9: 'Recover MP Percent',
    10: 'Recover MP Base'
}

RESIST_LVLS = ['RESIST_1', 'RESIST_2', 'Null', 'Repel']

USAGES = ['Boss', 'Field', 'Battle', 'Everywhere']

with open('Content/Blueprints/Gamedata/BinTable/Battle/Skill/SkillData.bin', 'rb') as binfile:
    NEW_SKILLS = binfile.read()
with open('Content/Blueprints/Gamedata/BinTable/Battle/Skill/SkillName.tsv') as tsvfile:
    next(tsvfile)
    SKILL_IDS = [x.strip() for x in tsvfile]

def printif_notequal(dname, field, lhs, rhs):
    if str(lhs) != str(rhs):
        print(dname, field, lhs, rhs)

def print_active(s_id, line_start):
    line = NEW_SKILLS[line_start:line_start + LINE_LEN]
    sname, desc = SKILL_IDS[s_id].split('\t')

    sid_name = line[0x00:0x20].decode('utf-8')

    new_s_id, zero, cost, s_type, elem = struct.unpack('<LLHBB', line[0x20:0x2C])
    press_turns = struct.unpack('<4B', line[0x2C:0x30])
    order_alpha, order_elem, owner, icon_one, icon_two, thirteen, affinity = struct.unpack('<LLl4B', line[0x30:0x40])
    new_s_id += zero
    s_type = SKILL_TYPES[s_type]
    elem = RESIST_ELEMS[elem]
    press_turns = [PRESS_TURNS[x] for x in press_turns]
    icon_one = ICONS[icon_one]
    icon_two = ICONS[icon_two]
    affinity = AFFINITIES[affinity]

    use_type, target, usage, min_hits, max_hits, crit, damages = struct.unpack('<HBBBBBB', line[0x40:0x48])
    dmg, n100, new_does_dmg, acc = struct.unpack('<LLLB', line[0x48:0x55])
    ailments = struct.unpack('<16B', line[0x55:0x65])
    use_type = USE_TYPES[use_type]
    target = TARGETS[target]
    usage = USAGES[usage]
    damages = DAMAGES[damages] if damages < len(DAMAGES) else 'unk_dmg'
    does_dmg = 100 if dmg > 0 else 0
    ailments = [AILMENTS[i] for i, x in enumerate(ailments) if x > 0]

    heal_over, pierce, ail_hit, ail_cure, support_type = struct.unpack('<BHBBH', line[0x65:0x6C])
    buffs = list(struct.unpack('<4l', line[0x6C:0x7C]))
    zero, barrier = struct.unpack('<LB', line[0x7C:0x81])
    ail_cure = AILMENT_CURES[ail_cure]
    support_type = SUPPORT_TYPES[support_type]

    barrier_elems = struct.unpack('<7B', line[0x81:0x88])
    heal_base, heal_perc, absorb_hp, absorb_mp, elem_two = struct.unpack('<LBBBB', line[0x88:0x90])
    rank, unique, talisman_flag, talisman = struct.unpack('<BHBL', line[0x90:0x98])
    unks_rank = struct.unpack('<LLLL', line[0x98:0xA8])
    barrier_elems = [f"{RESIST_LVLS[x]} {PRESS_TURNS[i]}" for i, x in enumerate(barrier_elems) if x > 0]
    elem_two = PRESS_TURNS[elem_two] if elem_two > 0 else elem
    unique = UNIQUES[unique]
    talisman = talisman_flag * 1000 + talisman

    mod_flags = struct.unpack('<BBBB', line[0xA8:0xAC])
    mod_flags = [MOD_FLAGS.get(x, f"mod_{x}") for x in mod_flags if x > 0]
    mod_adds = [f"{heal_base},{heal_perc}%,{absorb_hp},{absorb_mp}"]


    for i in range(2):
        mod_cond, mod_ailment, mod_adjust, _, mod_power = struct.unpack('<BBBBL', line[0xAC + 8*i:0xB4 + 8*i])
        mod_cond = MOD_CONDS[mod_cond]
        mod_ailment = AILMENTS[mod_ailment - 1] if mod_ailment > 0 else 'None'
        mod_adjust = MOD_ADJUSTS[mod_adjust]
        mod_str = f"{mod_power}|{mod_adjust}|{mod_cond}{mod_ailment}"
        if mod_str != '0|None|NoneNone':
            mod_adds.append(mod_str)

    unks_mods = list(struct.unpack('<BBBB', line[0xBC:0xC0]))

    printif_notequal(sname, 's_id', s_id, new_s_id)
    # printif_notequal(sname, 'n100', 100, n100)
    # printif_notequal(sname, 'does_dmg', does_dmg, new_does_dmg)
    # printif_notequal(sname, 'zero', 0, zero)
    # printif_notequal(sname, 'elem_two', elem_two, elem)
    stats = [rank, cost, dmg, min_hits, max_hits, acc, crit, ail_hit]
    prefix = [f"{s_id:03}", sname, icon_one, str(target)]
    suffix = [str(ailments), str(mod_flags), str(mod_adds), desc]

    if sname != desc:
        print('\t'.join(prefix + [str(x) for x in stats] + suffix))

for s_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    print_active(s_id + 1, line_start)

LINE_LEN = 0x68
LINE_LEN = 0x6C
START_OFFSET = END_OFFSET + 0x10
END_OFFSET = START_OFFSET + 400 * LINE_LEN

for s_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    s_id = s_id + 401
    line = NEW_SKILLS[line_start:line_start + LINE_LEN]
    sname, desc = SKILL_IDS[s_id].split('\t')

    new_s_id, = struct.unpack('<L', line[0x20:0x24])
    hp, mp, proc = struct.unpack('<3B', line[0x30:0x33])
    elem, res_lvl = struct.unpack('<2B', line[0x41:0x43])
    rank, = struct.unpack('<B', line[0x59:0x5A])
    target1, boost1, target2, boost2 = struct.unpack('<4H', line[0x64:0x6C])

    printif_notequal(sname, 's_id', s_id, new_s_id)

    if sname != desc:
        print(f"{s_id:03}", sname, hp, mp, proc, elem, res_lvl, rank, target1, boost1, target2, boost2, desc, sep='\t')

LINE_LEN = 0xC4
START_OFFSET = 0x1E2E5
END_OFFSET = START_OFFSET + 150 * LINE_LEN

for s_id, line_start in enumerate(range(START_OFFSET, END_OFFSET, LINE_LEN)):
    print_active(s_id + 801, line_start)
