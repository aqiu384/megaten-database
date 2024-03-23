#!/usr/bin/python3
import json
from shared import load_item_codes, load_item_prices, load_item_descs, iterate_int_tsvfile

def pluralize(amount):
    return f" x{str(amount)}" if amount > 1 else ''

def to_date(month, day):
    return '' if month == 4 and day == 1 else f"{month}/{day}: "

def stat_to_str(stat):
    return str(stat) if stat != 0 else '-'

def iterate_tv_shopping():
    inames = load_item_codes('en')
    data_file = 'Content/Xrd777/Field/Data/DataTable/DT_FldMailOrderTable.tsv'
    for line in iterate_int_tsvfile(data_file, skip_first=False):
        yield {
            'Buy': f"{line['BuyMonth']}/{line['BuyDay']}",
            'Receive': f"{line['ReceiveMonth']}/{line['ReceiveDay']}",
            'Items': f"{inames[line['ItemA_ID']]}{pluralize(line['ItemA_Num'])} + " +
                     f"{inames[line['ItemB_ID']]}{pluralize(line['ItemB_Num'])}",
            'Price': line['Price']
        }

def iterate_missing_people():
    inames = load_item_codes('en')
    ipeople = load_item_descs('Content/Xrd777/Help/BMD_DisappearHelp.tsv', 'en', offset=-1)
    data_file = 'Content/Xrd777/UI/Tables/DisappearDataAsset.tsv'
    for i, line in enumerate(iterate_int_tsvfile(data_file, skip_first=False)):
        reward = f"(-Y{line['AwardMoney']})"
        if line['AwardMoney'] == 0:
            reward = f"{inames[line['AwardItemID']]}{pluralize(line['AwardItemNum'])}"
        yield {
            'Missing': f"{line['StartMonth']}/{line['StartDays']}",
            'Limit': f"{line['LimitMonth']}/{line['LimitDays']}",
            'Name': ipeople[i].split('\\n')[0],
            'Reward': reward
        }

def list_requests():
    requests = []
    data_file = 'Content/Xrd777/UI/Facility/BMD_Quest.tsv'
    with open(data_file) as tsvfile:
        next(tsvfile)
        next(tsvfile)
        for line in tsvfile:
            num, title, _, _ = line.split('\t')
            name = f"Request #{num}: {title}"
            requests.append(name)
    return requests

def iterate_elizabeth_requests():
    inames = load_item_codes('en')
    requests = list_requests()
    lines = []
    data_file = 'Content/Xrd777/UI/Tables/VelvetRoomQuestDataAsset.tsv'
    for i, line in enumerate(iterate_int_tsvfile(data_file)):
        money = line['RewardMoney']
        item_id = line['RewardItemID']
        if money == 0 and item_id == 0:
            continue
        reward = f"(-Y{money})" if money > 0 else f"{inames[item_id]}{pluralize(line['RewardItemNum'])}"
        unlocks = f"{line['StartMonth']}/{line['StartDay']}" if line['StartMonth'] > 4 else '5/10'
        limit = f"-{line['EndMonth']}/{line['EndDay']}" if line['EndMonth'] > 0 else ''
        lines.append({
            'Availability': unlocks + limit,
            'Num': int(line['QuestIndex']),
            'Request': requests[i][requests[i].index(':') + 2:],
            'Reward': reward
        })
    lines.sort(key=lambda x: x['Num'])
    for line in lines:
        yield line

def parse_set_chest(line, callback):
    floor, _, treasure, _ = line.split('\t')
    for item in treasure.split(', '):
        chest = ''
        chance = ''
        if ': ' in item:
            chest, item = item.split(': ')
            chance = ' (100%)'
            chest = ' ' + chest
        shop = floor + chest
        for item in item.split(' + '):
            count = ''
            if ' x' in item:
                item, count = item.split(' x')
                count = ' x' + count
            format = f"{{}}{count}{chance}"
            if item != '-':
                callback(shop, item, format)

def load_items_to_shops():
    items = {}
    def callback(shop, item, format):
        if item not in items:
            items[item] = []
        items[item].append(format.format(shop))
    load_data(callback)
    for item in items:
        items[item] = ', '.join(items[item])
    return items

def load_shops_to_items():
    shops = {}
    def callback(shop, item, format):
        if shop not in shops:
            shops[shop] = []
        shops[shop].append(format.format(item))
    load_data(callback)
    for shop in shops:
        shops[shop] = ', '.join(shops[shop])
    return shops

def load_data(callback):
    inames = load_item_codes('en')
    iprices = load_item_prices()

    def load_shuffle(data_file, shop_name, item_lookup):
        ranks = list(range(1, 51)) if shop_name == 'Persona' else [str(x) for x in range(1, 11)] + ['J', 'Q', 'K']
        for line in iterate_int_tsvfile(data_file, skip_first=False):
            shop = f"{shop_name} {ranks[line['RankID'] if 'RankID' in line else line['RankId']]}"
            item_id = 'ItemtID' if 'ItemtID' in line else 'EffectID' if 'EffectID' in line else 'PersonaId'
            item = item_lookup[line[item_id]]
            format = f"{{}}{pluralize(line['Num'])} ({line['Prob']}%)" if 'Num' in line else f"{{}} ({line['Prob']}%)"
            callback(shop, item, format)

    ieffects = load_item_descs('Content/Xrd777/Blueprints/common/Names/DatPersonaNameDataAsset.tsv', 'en', max_flag=1)
    load_shuffle('Content/Xrd777/Battle/Tables/Shuffle/DatShufflePersonaArcanaDataAsset.tsv', 'Persona', ieffects)
    load_shuffle('Content/Xrd777/Battle/Tables/Shuffle/DatShuffleSwordArcanaDataAsset.tsv', 'Sword', inames)
    with open('walkthrough/shuffle-cups.tsv') as tsvfile:
        ieffects = [line.strip() for line in tsvfile]
    load_shuffle('Content/Xrd777/Battle/Tables/Shuffle/DatShuffleCupArcanaDataAsset.tsv', 'Cup', ieffects)

    def load_police(data_file, shop):
        for line in iterate_int_tsvfile(data_file):
            item = inames[line['Value']]
            format = f"{to_date(line['SaleMonth'], line['SaleDay'])}{{}}{'*' if line['OpenFLG'] > 0 else ''} (Y{iprices[line['Value']]})"
            callback(shop, item, format)

    load_police('Content/Xrd777/UI/Tables/DatItemShopLineupDataAsset.tsv', 'Pharmacy')
    load_police('Content/Xrd777/UI/Tables/DatWeaponShopLineupDataAsset.tsv', 'Police')

    packs = [
        '???', 'Florist', 'School', 'Octopia',
        'Dorms 2F', 'Dorms 3F', 'Port Island', 'Iwatodai 3F',
        'Iwatodai Station', 'Kyoto 1F', 'Kyoto 2F', 'Kyoto 3F',
        'Beef Bowl', 'Net Cafe', 'URL Seller', 'Club Escapade'
    ]
    data_file = 'Content/Xrd777/UI/Tables/SimpleShop/SimpleShopDataAsset.tsv'
    for line in iterate_int_tsvfile(data_file, skip_first=False):
        shop = packs[line['ShopID']]
        item = inames[line['ItemID']]
        format = f"{to_date(line['LiftMonth'], line['LiftDays'])}{{}}{'*' if line['OpenFlag'] > 0 else ''} (Y{iprices[line['ItemID']]})"
        callback(shop, item, format)

    def load_antiques(data_file, has_base_item):
        for line in iterate_int_tsvfile(data_file):
            item = inames[line['Value']]
            shop = [inames[line['BaseItemID']]] if has_base_item else []
            for i in range(1, 4):
                item_name = inames[line[f"TradeItemID{i}"]]
                item_num = line[f"TradeItemNum{i}"]
                if item_num != 0:
                    shop.append(f"{item_name}{pluralize(item_num)}")
            format = f"{to_date(line['SaleMonth'], line['SaleDay'])}{{}}{'*' if line['OpenFLG'] > 0 else ''}"
            callback(' + '.join(shop), item, format)

    load_antiques('Content/Xrd777/UI/Tables/DatAntiqueShopLineupDataAssetCombineResults.tsv', True)
    load_antiques('Content/Xrd777/UI/Tables/DatAntiqueShopLineupDataAssetTradeData.tsv', False)

    data_file = 'walkthrough/chests-set.tsv'
    with open(data_file) as tsvfile:
        next(tsvfile)
        next(tsvfile)
        for line in tsvfile:
            parse_set_chest(line, callback)

    data_file = 'Content/Xrd777/Field/Data/DataTable/DT_FldDungeonTBoxItem.tsv'
    chests = [(inames[x['itemID']], pluralize(x['itemNum'])) for x in iterate_int_tsvfile(data_file, skip_first=False)]

    packs = {}
    data_file = 'Content/Xrd777/Field/Data/DataTable/DT_FldDungeonTBoxPac.tsv'
    for line in iterate_int_tsvfile(data_file, skip_first=False):
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
                    shop = f"{floor} {chest_types[i]}"
                    item = pack[0][0]
                    format = f"{{}}{pack[0][1]} ({pack[1]}%)"
                    callback(shop, item, format)

    data_file = '../../../megaten-fusion-tool/src/app/p3r/data/demon-data.json'
    with open(data_file) as jsonfile:
        for shop, entry in json.load(jsonfile).items():
            if 'heart' in entry:
                item = entry['heart']
                format = f"{{}} (Lv. {entry['heartlvl']})"
                callback(shop, item, format)

    data_file = 'Content/Xrd777/Battle/Tables/DatEnemyDataAsset.tsv'
    ieffects = load_item_descs('Content/Xrd777/Blueprints/common/Names/DatEnemyNameDataAsset.tsv', 'en', max_flag=3)
    for i, line in enumerate(iterate_int_tsvfile(data_file, skip_first=False)):
        if i not in ieffects:
            continue
        shop = ieffects[i]
        for j in range(1, 5):
            itemId = line[f"itemId{j}"]
            itemProb = line[f"itemProb{j}"]
            if itemProb > 0:
                item = inames[itemId]
                format = f"{{}} ({itemProb}%)"
                callback(shop, item, format)

    load_shuffle('Content/Xrd777/Battle/Tables/Shuffle/DatShuffleMagicianArcanaDataAsset.tsv', 'Magician Card', inames)
    load_shuffle('Content/Xrd777/Battle/Tables/Shuffle/DatShuffleHangedmanArcanaDataAsset.tsv', 'Hanged Card', inames)

    data_file = 'Content/Xrd777/Field/Data/DataTable/DT_FldMailOrderTable.tsv'
    for line in iterate_int_tsvfile(data_file, skip_first=False):
        for letter in 'AB':
            shop = 'TV Shopping'
            item = inames[line[f"Item{letter}_ID"]]
            num = line[f"Item{letter}_Num"]
            format = f"{to_date(line['BuyMonth'], line['BuyDay'])}{{}}{pluralize(num)} (Y{line['Price']})"
            callback(shop, item, format)

    data_file = 'Content/Xrd777/UI/Tables/DisappearDataAsset.tsv'
    for line in iterate_int_tsvfile(data_file, skip_first=False):
        shop = 'Rescue Reward'
        item = inames[line['AwardItemID']]
        format = f"{to_date(line['StartMonth'], line['StartDays'])}{{}}{pluralize(line['AwardItemNum'])}"
        callback(shop, item, format)

    requests = list_requests()
    data_file = 'Content/Xrd777/UI/Tables/VelvetRoomQuestDataAsset.tsv'
    for i, line in enumerate(iterate_int_tsvfile(data_file)):
        if line['RewardItemID'] == 0:
            continue
        shop = requests[i]
        item = inames[line['RewardItemID']]
        format = f"{{}}{pluralize(line['RewardItemNum'])}"
        callback(shop, item, format)
