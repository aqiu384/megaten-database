#!/usr/bin/python3
def load_names(fname, local_names):
    SEEN = {}
    NAMES = []

    with open('Content/Blueprints/Gamedata/BinTable/' + fname) as tsvfile:
        next(tsvfile)
        for s_id, skill in enumerate(tsvfile):
            sname, desc = skill.split('\t')
            desc = desc.strip()
            if sname not in SEEN:
                SEEN[sname] = 0
            else:
                SEEN[sname] += 1
                sname = f"{sname} {chr(SEEN[sname] + 64)}"
            NAMES.append(f"{local_names.get(str(s_id), sname)}\t{desc}")

    return NAMES

LOCAL_DEMONS = {
    "46": "Dis",
    "391": "Lilith"
}

def load_demons():
    return load_names('Common/CharacterName.tsv', LOCAL_DEMONS)

LOCAL_SKILLS = {
    "117": "Heavenly Counter A",
    "190": "Counter A",
    "191": "Retaliate A",
    "251": "Souffle D'eclair",
    "255": "Moonlight Frost A",
    "259": "Heliopolis Dawn A",
    "277": "Matriarch's Love A",
    "279": "Matriarch's Love",
    "336": "Gaea Rage B",
    "338": "Javelin Rain A",
    "340": "Deadly Fury A",
    "372": "Javelin Rain",
    "373": "Deadly Fury",
    "374": "Chaotic Will A",
    "394": "Gaea Rage",
    "395": "Chaotic Will",
    "434": "Counter",
    "435": "Retaliate",
    "436": "Heavenly Counter",
    "701": "Qadistu Mandate",
    "702": "Qadistu Artifice",
    "703": "Qadistu Deception",
    "704": "Qadistu Savagery",
    "709": "Qadistu Cohort",
    "826": "Qadistu Entropy",
    "849": "Recalcitrant Execution A",
    "858": "Heliopolis Dawn",
    "874": "Recalcitrant Execution",
    "889": "Qadistu Entropy A",
    "907": "Qadistu Entropy B",
    "924": "Moonlight Frost"
}

def load_skills():
    return load_names('Battle/Skill/SkillName.tsv', LOCAL_SKILLS)
