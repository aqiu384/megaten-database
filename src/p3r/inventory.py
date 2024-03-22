#!/usr/bin/python3
import json
from shared import load_item_codes, load_item_descs, iterate_int_tsvfile, table_header, table_row
from shopper import load_items_to_shops

USERS = {
    2: 'Makoto',
    4: 'Yukari',
    8: 'Junpei',
    16: 'Akihiko',
    32: 'Mitsuru',
    64: 'Fuuka',
    128: 'Aigis',
    512: 'Koromaru',
    256: 'Ken',
    1024: 'Shinjiro',
    1306: 'Men',
    100: 'Women',
    1406: 'Unisex',
}

print(f"## Inventory")
print('''* Inventory items may be obtained through several means
  * Buying from the Police Station on the date they become available (Prices given in parantheses)
  * Opening chests in Tartarus (Random chest probabilities given in parantheses)
  * Crafting or trading from Mayoido Antiques using materials and gems
  * Completing Elizabeth and Rescue Requests
  * Other social activities e.g. performing well during exams''')

def stat_to_str(stat):
    return str(stat) if stat != 0 else '-'

inames = load_item_codes('en')
shops = load_items_to_shops()

ieffects = load_item_descs('Content/Xrd777/Help/BMD_ItemAddEffectHelp.tsv', 'en')
ielems = load_item_descs('Content/Xrd777/Blueprints/common/Names/DatAttrNameDataAsset.tsv', 'en')
ieffects[0] = '-'

STATS = ['Strength', 'Magic', 'Endurance', 'Agility', 'Luck']

def summarize_stats(stats):
    total = sum(stats)
    if total == 0:
        return '-'
    parts = []
    for i, stat in enumerate(stats):
        if 5*stat == total:
            return f"All Stats +{stat}"
        elif stat != 0:
            parts.append(f"{STATS[i][:2]} +{stat}")
    return ', '.join(parts)

users = {}
stats = ['SellPrice', 'Attack', 'Accuracy']
header = ['Weapon', 'Sell', 'Atk', 'Acc', 'Stats', 'Elem', 'Skill', 'Acquisition']
data_file = 'Content/Xrd777/UI/Tables/DatItemWeaponDataAsset.tsv'
print(f"### Weapons")
for i, line in enumerate(iterate_int_tsvfile(data_file)):
    i += 1
    name = inames.get(i + 0x0000, '')
    if name == '' or name == 'No equipment':
        continue

    parts = [name] + [str(line[x]) if line[x] != 0 else '-' for x in stats]
    parts += [summarize_stats(list(line[x] for x in STATS)), ielems[line['AttrID']], ieffects[line['SkillID']]]
    parts.append(shops.get(name, '-').format(line['Price']))

    user = line['EquipID']
    if user not in users:
        users[user] = []
    users[user].append(parts)

for user in users:
    print(f"#### {USERS[user]}")
    print(table_header(header))
    users[user].sort(key=lambda x: int(x[2]))
    for line in users[user]:
        print(table_row(line))

lines = []
stats = ['SellPrice', 'Defence']
header = ['Armor', 'User', 'Sell', 'Def', 'Stats', 'Skill', 'Acquisition']
data_file = 'Content/Xrd777/UI/Tables/DatItemArmorDataAsset.tsv'
print(f"### Armor")
print(table_header(header))
for i, line in enumerate(iterate_int_tsvfile(data_file)):
    i += 1
    name = inames.get(i + 0x1000, '')
    if name == '':
        continue

    parts = [name, USERS[line['EquipID']]] + [str(line[x]) if line[x] != 0 else '-' for x in stats]
    parts += [summarize_stats(list(line[x] for x in STATS)), ieffects[line['SkillID']]]
    parts.append(shops.get(name, '-').format(line['Price']))
    lines.append(parts)
lines.sort(key=lambda x: int(x[3]))
for line in lines:
    print(table_row(line))

lines = []
stats = ['SellPrice', 'Evasion']
header = ['Shoes', 'User', 'Sell', 'Eva', 'Stats', 'Skill', 'Acquisition']
data_file = 'Content/Xrd777/UI/Tables/DatItemShoesDataAsset.tsv'
print(f"### Shoes")
print(table_header(header))
for i, line in enumerate(iterate_int_tsvfile(data_file)):
    i += 1
    name = inames.get(i + 0x2000, '')
    if name == '':
        continue

    parts = [name, USERS[line['EquipID']]] + [str(line[x]) if line[x] != 0 else '-' for x in stats]
    parts += [summarize_stats(list(line[x] for x in STATS)), ieffects[line['SkillID']]]
    parts.append(shops.get(name, '-').format(line['Price']))
    lines.append(parts)
lines.sort(key=lambda x: int(x[3]))
for line in lines:
    print(table_row(line))

lines = []
stats = ['SellPrice']
header = ['Accessory', 'Sell', 'Stats', 'Skill', 'Acquisition']
data_file = 'Content/Xrd777/UI/Tables/DatItemAccsDataAsset.tsv'
print(f"### Accessories")
print(table_header(header))
for i, line in enumerate(iterate_int_tsvfile(data_file)):
    i += 1
    name = inames.get(i + 0x3000, '')
    if name == '':
        continue

    parts = [name] + [str(line[x]) if line[x] != 0 else '-' for x in stats]
    parts += [summarize_stats(list(line[x] for x in STATS)), ieffects[line['SkillID']]]
    parts.append(shops.get(name, '-').format(line['Price']))
    lines.append(parts)
for line in lines:
    print(table_row(line))

lines = []
header = ['Costume', 'User', 'Acquisition']
data_file = 'Content/Xrd777/UI/Tables/DatItemCostumeDataAsset.tsv'
print(f"### Costumes")
print(table_header(header))
for i, line in list(enumerate(iterate_int_tsvfile(data_file)))[:88]:
    i += 1
    name = inames.get(i + 0x8000, '')
    if name == '':
        continue

    parts = [name, USERS[line['EquipID']], shops.get(name, '-')]
    lines.append(parts)
for line in lines:
    print(table_row(line))

lines = []
header = ['Card', 'Acquisition']
data_file = 'Content/Xrd777/UI/Tables/DatItemSkillcardDataAsset.tsv'
print(f"### Skill Cards")
print(table_header(header))
for i, line in enumerate(iterate_int_tsvfile(data_file)):
    i += 1
    name = inames.get(i + 0x7000, '')
    if name == '':
        continue

    parts = [name, shops.get(name, '-')]
    lines.append(parts)
for line in lines:
    print(table_row(line))

MATERIAL_TYPES = {
    2097152: 'Base Models',
    32768: 'Gems',
    4194304: 'Heart Items',
    65536: 'Sellables'
}

users = {}
stats = ['SellPrice']
header = ['Material', 'Sell', 'Acquisition']
data_file = 'Content/Xrd777/UI/Tables/DatItemMaterialDataAsset.tsv'
print(f"### Materials")
for i, line in enumerate(iterate_int_tsvfile(data_file)):
    i += 1
    name = inames.get(i + 0x6000, '')
    if name == '':
        continue

    parts = [name, stat_to_str(line['SellPrice']), shops.get(name, '-').replace('{}', str(line['Price']))]
    user = line['ItemType']
    if user not in users:
        users[user] = []
    users[user].append(parts)

for i, user in MATERIAL_TYPES.items():
    print(f"#### {user}")
    print(table_header(header))
    for line in users[i]:
        print(table_row(line))

MATERIAL_TYPES = {
    6: 'Recovery',
    4: 'Battle',
    2: 'Food and Incense',
    16: 'Gifts',
    8: 'Other'
}

users = {}
header = ['Item', 'Effect', 'Acquisition']
idescs = load_item_descs('Content/Xrd777/Help/BMD_ItemCommonHelp.tsv', 'en')
data_file = 'Content/Xrd777/UI/Tables/DatItemCommonDataAsset.tsv'
print(f"### Consumables")
for i, line in enumerate(iterate_int_tsvfile(data_file)):
    i += 1
    name = inames.get(i + 0x4000, '')
    if name == '' or name == 'Money Distributor' or name == 'Item Distributor':
        continue

    parts = [name, idescs[i], shops.get(name, '-').replace('{}', str(line['Price']))]
    user = line['UsePlaceID']
    if user not in users:
        users[user] = []
    users[user].append(parts)

for i, user in MATERIAL_TYPES.items():
    print(f"#### {user}")
    print(table_header(header))
    for line in users[i]:
        print(table_row(line))

lines = []
header = ['Item', 'Effect', 'Acquisition']
idescs = load_item_descs('Content/Xrd777/Help/BMD_ItemEvitemHelp.tsv', 'en')
data_file = 'Content/Xrd777/UI/Tables/DatItemEvitemDataAsset.tsv'
print(f"### Key Items")
print(table_header(header))
for i, line in enumerate(iterate_int_tsvfile(data_file)):
    i += 1
    name = inames.get(i + 0x5000, '')
    if name == '':
        continue

    parts = [name, idescs[i], shops.get(name, '-')]
    lines.append(parts)
for line in lines:
    print(table_row(line))
