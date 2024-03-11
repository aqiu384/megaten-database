#!/usr/bin/python3
from shared import load_item_codes, iterate_int_tsvfile

SHUFFLE_SWORD = 'Content/Xrd777/Battle/Tables/Shuffle/DatShuffleSwordArcanaDataAsset.tsv'

seen_skills = {}
icodes = load_item_codes('en')

for line in iterate_int_tsvfile(SHUFFLE_SWORD):
    skill = icodes[line['ItemtID']]
    drop = (line['RankID'], line['Prob'])

    if skill in seen_skills:
        print(skill, seen_skills[skill], drop)
    seen_skills[skill] = drop
