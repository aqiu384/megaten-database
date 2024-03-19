#!/usr/bin/python3
from shared import load_item_codes, load_item_descs, iterate_int_tsvfile, table_header, table_row

USERS = {
    2: 'Makoto',
    4: 'Yukari',
    8: 'Junpei',
    16: 'Akihiko',
    32: 'Mitsuru',
    128: 'Aigis',
    512: 'Koromaru',
    256: 'Ken',
    1024: 'Shinjiro',
    1306: 'Men',
    100: 'Women',
    1406: 'Unisex'
}

inames = load_item_codes('en')
shops = {}
packs = {}
requests = []

def add_shop(name, obtain):
    if name not in shops:
        shops[name] = []
    shops[name].append(obtain)

data_file = 'Content/Xrd777/Field/Data/DataTable/DT_FldDungeonTBoxItem.tsv'
chests = [f"{inames[x['itemID']]}{' x' + str(x['itemNum']) if x['itemNum'] > 1 else ''}" for x in iterate_int_tsvfile(data_file, skip_first=False)]

data_file = 'Content/Xrd777/Field/Data/DataTable/DT_FldDungeonTBoxPac.tsv'
for line in iterate_int_tsvfile(data_file):
    pacID = line['pacID']
    if pacID not in packs:
        packs[pacID] = []
    packs[pacID].append((chests[line['tboxID']], line['probability']))

data_file = 'walkthrough/chests-random.tsv'
with open(data_file) as tsvfile:
    chest_types = next(tsvfile).strip().split('\t')[1:]
    for line in tsvfile:
        parts = line.split('\t')
        floor = parts[0]
        for i, pack_id in enumerate([int(x) for x in parts[1:]]):
            if pack_id == 0:
                continue
            for pack in packs[pack_id]:
                chance = f"{floor} {chest_types[i]} ({pack[1]}%)"
                add_shop(pack[0], chance)


data_file = 'walkthrough/chests-set.tsv'
with open(data_file) as tsvfile:
    next(tsvfile)
    next(tsvfile)
    for line in tsvfile:
        floor, encounter, treasure, notes = line.split('\t')
        for name in treasure.split(', '):
            if ':' in name:
                name, lock = name.split(':')
                add_shop(name, floor + lock)
            else:
                for name in name.split(' + '):
                    add_shop(name, floor)

data_file = 'Content/Xrd777/Field/Data/DataTable/DT_FldMailOrderTable.tsv'
for line in iterate_int_tsvfile(data_file):
    for letter in 'AB':
        name = inames[line[f"Item{letter}_ID"]]
        available = f"TV Shopping {line['BuyMonth']}/{line['BuyDay']}"
        add_shop(name, f"{available} (Y{line['Price']})")

data_file = 'Content/Xrd777/UI/Tables/DisappearDataAsset.tsv'
for line in iterate_int_tsvfile(data_file):
    name = inames[line['AwardItemID']]
    available = f"{line['StartMonth']}/{line['StartDays']} Rescue Reward"
    add_shop(name, available)

data_file = 'Content/Xrd777/UI/Tables/DatWeaponShopLineupDataAsset.tsv'
for line in iterate_int_tsvfile(data_file):
    name = inames[line['Value']]
    available = f"Police {line['SaleMonth']}/{line['SaleDay']}"
    add_shop(name, available + ' (Y{})')

data_file = 'Content/Xrd777/UI/Tables/DatAntiqueShopLineupDataAssetCombineResults.tsv'
for line in iterate_int_tsvfile(data_file):
    name = inames[line['Value']]
    parts = [inames[line['BaseItemID']]]

    for i in range(1, 4):
        item_name = inames[line[f"TradeItemID{i}"]]
        item_num = line[f"TradeItemNum{i}"]
        if item_num != 0:
            parts.append(f"{item_name}{' x' + str(item_num) if item_num > 1 else ''}")

    add_shop(name, ' + '.join(parts))

data_file = 'Content/Xrd777/UI/Facility/BMD_Quest.tsv'
with open(data_file) as tsvfile:
    next(tsvfile)
    next(tsvfile)
    for line in tsvfile:
        num, title, summary, desc = line.split('\t')
        name = f"Request #{num}: {title}"
        requests.append(name)

data_file = 'Content/Xrd777/UI/Tables/VelvetRoomQuestDataAsset.tsv'
for i, line in enumerate(iterate_int_tsvfile(data_file)):
    if line['RewardItemID'] not in inames:
        continue
    name = inames[line['RewardItemID']]
    add_shop(name, requests[i])

for name, obtain in shops.items():
    shops[name] = ', '.join(obtain)

idescs = load_item_descs('Content/Xrd777/Help/BMD_ItemWeaponHelp.tsv', 'en')
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

stats = ['SellPrice', 'Attack', 'Accuracy']
header = ['Weapon', 'Sell', 'Atk', 'Acc', 'Stats', 'Elem', 'Skill', 'Acquisition']
users = {}
data_file = 'Content/Xrd777/UI/Tables/DatItemWeaponDataAsset.tsv'
print(f"# Persona 3 Reload")
print(f"## Inventory")
print(f"### Weapons")
for i, line in enumerate(iterate_int_tsvfile(data_file)):
    i += 1
    name = inames.get(i + 0x0000, '')
    if name == '' or name == 'No equipment':
        continue

    parts = [name] + [str(line[x]) if line[x] != 0 else '-' for x in stats]
    parts += [summarize_stats(list(line[x] for x in STATS)), ielems[line['AttrID']], ieffects[line['SkillID']]] # idescs[i]
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
    parts += [summarize_stats(list(line[x] for x in STATS)), ieffects[line['SkillID']]] # idescs[i]
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
    parts += [summarize_stats(list(line[x] for x in STATS)), ieffects[line['SkillID']]] # idescs[i]
    parts.append(shops.get(name, '-').format(line['Price']))
    lines.append(parts)
lines.sort(key=lambda x: int(x[3]))
for line in lines:
    print(table_row(line))

lines = []
stats = ['SellPrice']
header = ['Accesory', 'Sell', 'Stats', 'Skill', 'Acquisition']
data_file = 'Content/Xrd777/UI/Tables/DatItemAccsDataAsset.tsv'
print(f"### Accessories")
print(table_header(header))
for i, line in enumerate(iterate_int_tsvfile(data_file)):
    i += 1
    name = inames.get(i + 0x3000, '')
    if name == '':
        continue

    parts = [name] + [str(line[x]) if line[x] != 0 else '-' for x in stats]
    parts += [summarize_stats(list(line[x] for x in STATS)), ieffects[line['SkillID']]] # idescs[i]
    parts.append(shops.get(name, '-').format(line['Price']))
    lines.append(parts)
for line in lines:
    print(table_row(line))
