#!/usr/bin/python3
import re
from shared import table_header, table_row
from shopper import load_shops_to_items, iterate_tv_shopping, iterate_missing_people, iterate_elizabeth_requests

shops = load_shops_to_items()

def shop_inventory(shop_id):
    if shop_id == 'Antiques':
        antiques_shopping()
    elif shop_id == 'TV Shopping':
        cols = ['Buy', 'Receive', 'Items', 'Price']
        print(table_header(cols))
        for line in iterate_tv_shopping():
            print(table_row(str(line[x]) for x in cols))
    elif shop_id == 'Elizabeth Requests':
        cols = ['Availability', 'Num', 'Prereq', 'Request', 'Hint', 'Reward']
        print(table_header(cols))
        for line in iterate_elizabeth_requests():
            print(table_row(str(line.get(x, '-')) for x in cols))
    elif shop_id == 'Missing People':
        cols = ['Missing', 'Limit', 'Name', 'Reward']
        print(table_header(cols))
        for line in iterate_missing_people():
            print(table_row(str(line[x]) for x in cols))
    else:
        print(table_header(['Unlocks', 'Item', 'Price']))
        for item in shops[shop_id].split(', '):
            unlocks = '-'
            if ': ' in item:
                unlocks, item = item.split(': ')
            item, price = item.split(' (Y')
            price = price.replace(')', '')
            print(table_row([unlocks, item, price]))

def antiques_shopping():
    print(table_header(['Unlocks', 'Item', 'Trade For']))
    for shop in shops:
        if ' x' in shop or ' + ' in shop:
            for item in shops[shop].split(', '):
                unlocks = '-'
                if ': ' in item:
                    unlocks, item = item.split(': ')
                print(table_row([unlocks, item, shop]))

FILLERS = {
    'shop_inventory': shop_inventory,
}

SUBME = re.compile("\{\{ (\w+)\('(.*)'\) \}\}\n")

with open('walkthrough/overworld.md') as mdfile:
    for line in mdfile:
        matching = SUBME.match(line)
        if matching:
            FILLERS[matching.group(1)](matching.group(2))
        else:
            print(line, end='')
