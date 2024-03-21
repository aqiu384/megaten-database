#!/usr/bin/python3
import json
from shared import load_item_codes, load_item_descs, iterate_int_tsvfile, table_header, table_row

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

inames = load_item_codes('en')
shops = {}
packs = {}
requests = []

def add_shop(name, obtain):
    if name not in shops:
        shops[name] = []
    shops[name].append(obtain)

def pluralize(amount):
    return ' x' + str(amount) if amount > 1 else ''

def to_date(month, day):
    return '' if month == 4 and day == 1 else f"{month}/{day}: "

def stat_to_str(stat):
    return str(stat) if stat != 0 else '-'

ranks = [str(x) for x in range(1, 11)] + ['J', 'Q', 'K']
data_file = 'Content/Xrd777/Battle/Tables/Shuffle/DatShuffleSwordArcanaDataAsset.tsv'
for i, line in enumerate(iterate_int_tsvfile(data_file, skip_first=False)):
    name = inames[line['ItemtID']]
    add_shop(name, f"Sword {ranks[line['RankID']]} ({line['Prob']}%)")

data_file = 'Content/Xrd777/UI/Tables/DatItemShopLineupDataAsset.tsv'
for line in iterate_int_tsvfile(data_file, skip_first=False):
    name = inames[line['Value']]
    available = f"{to_date(line['SaleMonth'], line['SaleDay'])}Pharmacy"
    add_shop(name, available + ' (Y{})')

data_file = 'Content/Xrd777/UI/Tables/DatWeaponShopLineupDataAsset.tsv'
for line in iterate_int_tsvfile(data_file, skip_first=False):
    name = inames[line['Value']]
    available = f"{to_date(line['SaleMonth'], line['SaleDay'])}Police"
    add_shop(name, available + ' (Y{})')

SHOPS = [
    '???', 'Florist', 'School', 'Octopia',
    'Dorms 2F', 'Dorms 3F', 'Port Island', 'Iwatodai 3F',
    'Iwatodai Station', 'Kyoto 1F', 'Kyoto 2F', 'Kyoto 3F',
    'Beef Bowl', 'Net Cafe', 'URL Seller', 'Club Escapade'
]
data_file = 'Content/Xrd777/UI/Tables/SimpleShop/SimpleShopDataAsset.tsv'
for line in iterate_int_tsvfile(data_file, skip_first=False):
    name = inames[line['ItemID']]
    available = to_date(line['LiftMonth'], line['LiftDays']) + SHOPS[line['ShopID']]
    add_shop(name, available + ' (Y{})')

data_file = 'Content/Xrd777/UI/Tables/DatAntiqueShopLineupDataAssetCombineResults.tsv'
for line in iterate_int_tsvfile(data_file, skip_first=False):
    name = inames[line['Value']]
    parts = [inames[line['BaseItemID']]]

    for i in range(1, 4):
        item_name = inames[line[f"TradeItemID{i}"]]
        item_num = line[f"TradeItemNum{i}"]
        if item_num != 0:
            parts.append(f"{item_name}{pluralize(item_num)}")

    add_shop(name, ' + '.join(parts))

data_file = 'Content/Xrd777/UI/Tables/DatAntiqueShopLineupDataAssetTradeData.tsv'
for line in iterate_int_tsvfile(data_file, skip_first=False):
    name = inames[line['Value']]
    parts = []

    for i in range(1, 4):
        item_name = inames[line[f"TradeItemID{i}"]]
        item_num = line[f"TradeItemNum{i}"]
        if item_num != 0:
            parts.append(f"{item_name}{pluralize(item_num)}")

    add_shop(name, f"{to_date(line['SaleMonth'], line['SaleDay'])}{' + '.join(parts)}")

data_file = 'Content/Xrd777/Field/Data/DataTable/DT_FldDungeonTBoxItem.tsv'
chests = [(inames[x['itemID']], pluralize(x['itemNum'])) for x in iterate_int_tsvfile(data_file, skip_first=False)]

data_file = 'Content/Xrd777/Field/Data/DataTable/DT_FldDungeonTBoxPac.tsv'
for line in iterate_int_tsvfile(data_file, skip_first=False):
    pacID = line['pacID']
    if pacID not in packs:
        packs[pacID] = []
    packs[pacID].append((chests[line['tboxID']], line['probability']))

data_file = 'walkthrough/chests-set.tsv'
with open(data_file) as tsvfile:
    next(tsvfile)
    next(tsvfile)
    for line in tsvfile:
        floor, encounter, treasure, notes = line.split('\t')
        for name in treasure.split(', '):
            chest = ''
            chance = ''
            if ': ' in name:
                chest, name = name.split(': ')
                chance = ' (100%)'
                chest = ' ' + chest
            for name in name.split(' + '):
                count = ''
                if ' x' in name:
                    name, count = name.split(' x')
                    count = ' x' + count
                add_shop(name, floor + chest + count + chance)

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
                chance = f"{floor} {chest_types[i]}{pack[0][1]} ({pack[1]}%)"
                add_shop(pack[0][0], chance)

data_file = 'Content/Xrd777/Battle/Tables/DatPersonaGrowthDataAsset.tsv'
ieffects = load_item_descs('Content/Xrd777/Blueprints/common/Names/DatPersonaNameDataAsset.tsv', 'en', max_flag=2)
with open('../../../megaten-fusion-tool/src/app/p3r/data/demon-data.json') as jsonfile:
    DEMONS = json.load(jsonfile)
for i, line in enumerate(iterate_int_tsvfile(data_file, skip_first=False)):
    if i not in ieffects:
        continue
    name = ieffects[i]
    for j in range(1, 17):
        skillId = line[f"skillId{j}"]
        skillLvl = line[f"skillLevel{j}"]
        if skillId > 0x6000:
            add_shop(inames[skillId], f"{name} ({DEMONS[name]['lvl'] + skillLvl})")

data_file = 'Content/Xrd777/Battle/Tables/DatEnemyDataAsset.tsv'
ieffects = load_item_descs('Content/Xrd777/Blueprints/common/Names/DatEnemyNameDataAsset.tsv', 'en', max_flag=3)
for i, line in enumerate(iterate_int_tsvfile(data_file, skip_first=False)):
    if i not in ieffects:
        continue
    name = ieffects[i]
    for j in range(1, 5):
        skillId = line[f"itemId{j}"]
        skillLvl = line[f"itemProb{j}"]
        if skillLvl > 0:
            add_shop(inames[skillId], f"{name} ({skillLvl}%)")

data_file = 'Content/Xrd777/Field/Data/DataTable/DT_FldMailOrderTable.tsv'
for line in iterate_int_tsvfile(data_file, skip_first=False):
    for letter in 'AB':
        name = inames[line[f"Item{letter}_ID"]]
        num = line[f"Item{letter}_Num"]
        add_shop(name, f"{to_date(line['BuyMonth'], line['BuyDay'])}TV Shopping{pluralize(num)} (Y{line['Price']})")

data_file = 'Content/Xrd777/UI/Tables/DisappearDataAsset.tsv'
for line in iterate_int_tsvfile(data_file, skip_first=False):
    name = inames[line['AwardItemID']]
    num = line['AwardItemNum']
    available = f"{to_date(line['StartMonth'], line['StartDays'])}Rescue Reward{pluralize(num)}"
    add_shop(name, available)

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
    add_shop(name, f"{requests[i]}{pluralize(line['RewardItemNum'])}")

for name, obtain in shops.items():
    shops[name] = ', '.join(obtain)

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
