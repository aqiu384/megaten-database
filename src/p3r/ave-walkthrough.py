#!/usr/bin/python3
import json
import math
import re

WALKTHROUGH = 'walkthrough/ave-walkthrough-base.md'
EVENT = re.compile('^\* [A-Za-z]+ (?:Flag|Rank) [0-9\.]+(?: Romantic| Platonic|)')
NEEDS_PERSONA = ' (Needs matching persona)'
FIRST_BONUS = '* **1st Social Link bonus'
SECOND_BONUS = '* **2nd Social Link bonus'

links = {}

with open('walkthrough/social-links.json') as jsonfile:
    for race, events in json.load(jsonfile).items():
        for event, choices in events.items():
            links[race + ' ' + event] = choices

def display_choices(event, bonus_count, notes):
    coeff = 5 * 1.51 ** bonus_count
    choices = iter(links[event].items())

    display = []
    earned_points = 0
    rankup_type = ''
    rankup_points = 0

    for i, (choice, base_points) in enumerate(choices):
        if base_points > 5:
            rankup_type = choice
            rankup_points = base_points
        elif base_points > 0:
            points = math.floor(coeff * base_points)
            plural = '' if base_points == 1 else 's'
            earned_points += points
            display.append(f"  * Choice {choice} (+{points}, {base_points} note{plural})")
        elif base_points < 0:
            display.append(f"  * **Choice {choice} (+0, 0 notes)**")
        elif choice.startswith('Any'):
            display.append('  * Any')
        else:
            display.append('  * ' + choice)

    if rankup_type == 'Next Rank':
        display.insert(0, f"* {event}{notes}: {earned_points}/{rankup_points} points to next rank")
    else:
        display.insert(0, f"* {event}{notes}")

    return display

bonus1 = 0
bonus2 = 0

with open(WALKTHROUGH) as mdfile:
    for line in mdfile:
        if line.startswith(FIRST_BONUS):
            bonus1 = 1
        if line.startswith(SECOND_BONUS):
            bonus2 = 1

        found = EVENT.match(line)
        if found and 'Auto' not in line:
            event = found.group(0)[2:]
            bonus3 = 1 if NEEDS_PERSONA in line else 0
            notes = NEEDS_PERSONA if bonus3 == 1 else ''
            display = display_choices(event, bonus1 + bonus2 + bonus3, notes)
            print('\n'.join(display))
        else:
            print(line, end='')
