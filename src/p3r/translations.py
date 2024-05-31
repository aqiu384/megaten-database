#!/usr/bin/python3
import json
import re

LANGUAGES = ['ja', 'zh-Hans']
LANG_LEN = len(LANGUAGES)
OLD_PATH = '../../../megaten-fusion-tool/src/app/p3r/data/{}.json'
NEW_PATH = 'Content/Xrd777/Blueprints/common/Names/Dat{}DataAsset.tsv'
VARIANT = r" ([A-Z])$"

OLD_NAMES = { 'en': [x.replace('zh-Hans', 'zh-cn') for x in LANGUAGES] }

with open(OLD_PATH.format('comp-config')) as jsonfile:
    config = json.load(jsonfile)
    OLD_NAMES.update({ x: [] for x in config['races'] })
for fname in ['demon-data', 'party-data', 'enemy-data', 'skill-data']:
    with open(OLD_PATH.format(fname)) as jsonfile:
        OLD_NAMES.update({ x: [] for x in json.load(jsonfile) })
for en_name in ['Phys Attack', 'Unknown']:
    OLD_NAMES[en_name] = [en_name] * LANG_LEN

OLD_SEEN = { x: False for x in  OLD_NAMES }

for fname in ['Race', 'PersonaName', 'EnemyName', 'SkillName']:
    with open(NEW_PATH.format(fname)) as tsvfile:
        langs = next(tsvfile).split('\t')
        en_ind = langs.index('en')
        lang_inds = [langs.index(x) for x in LANGUAGES]
        for line in tsvfile:
            parts = line.split('\t')
            en_name = parts[en_ind]
            if en_name in OLD_NAMES and not OLD_SEEN[en_name]:
                OLD_SEEN[en_name] = True
                variant = re.search(VARIANT, en_name)
                suffix = variant.group(1) if variant else ''
                for i in lang_inds:
                    OLD_NAMES[en_name].append(parts[i] + suffix)

for en_name, entry in OLD_NAMES.items():
    if len(entry) != LANG_LEN:
        print(en_name)
    OLD_NAMES[en_name] = '[' + '|, |'.join(entry) + ']'

with open('translations.json', 'w+') as jsonfile:
    outlines = json.dumps(OLD_NAMES, indent=2, ensure_ascii=False)
    outlines = outlines.replace('"[', '["').replace(']"', '"]').replace('|', '"')
    jsonfile.write(outlines)
