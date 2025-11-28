#!/usr/bin/python3
import yaml
import math
import re

class SaveFile:
    def __init__(self, config, calendar):
        self.config = config
        self.calendar = calendar
        self.confidants = { x: (0, 0, 0) for x in config['Confidants'] }
        self.social_stats = { x: (0, y[1], 1) for x, y in config['Social Stats'].items() }
        self.luck_reading = ('4/01', 'Knowledge')
        self.craft_of_cinema = False
        self.exam_coeff = 1
        self.countups = [0] * 6
        self.countup_unlockers = {
            'Bathhouse': self.bathhouse_unlocks,
            'Aojiru': self.aojiru_unlocks,
            'Convenience Store Job': self.conbini_unlocks,
            'Flower Shop Job': self.flowershop_unlocks,
            'Beef Bowl Job': self.beefbowl_unlocks,
            'Bar Crossroads Job': self.crossroads_unlocks,
            'Exam Results': self.exam_unlocks
        }

    def activity_unlocks(self, choice, date):
        return self.countup_unlockers[choice](date) if choice in self.countup_unlockers else []

    def bathhouse_unlocks(self, date):
        dow, _, rain = self.calendar[date]
        if rain:
            return ['Charm +3', 'Guts +2']
        elif dow == 'Sun':
            return ['Charm +5']
        else:
            return ['Charm +3']

    def aojiru_unlocks(self, date):
        unlocks = ['Charm', 'Proficiency', 'Guts', 'Kindness', 'Knowledge']
        unlocks = [f"{unlocks[self.countups[1] % 5]} +2"]
        self.countups[1] += 1
        return unlocks

    def conbini_unlocks(self, date):
        points = 5 if self.countups[2] > 0 and date.endswith('7') else 3
        self.countups[2] += 1
        return [f"Charm +{points}"]

    def flowershop_unlocks(self, date):
        dow = self.calendar[date][0]
        points = 3
        if self.countups[3] == 0:
            self.countups[3] += 1
        elif self.countups[3] == 1 or dow == 'Wed' or dow == 'Sat':
            points = 5
            self.countups[3] += 1
        return [f"Kindness +{points}"]

    def beefbowl_unlocks(self, date):
        points = 3
        if self.countups[4] == 0:
            pass
        elif self.countups[4] == 1 or date.endswith('2'):
            points = 5
        self.countups[4] += 1
        return [f"Proficiency +{points}"]

    def crossroads_unlocks(self, date):
        bonus = ['Guts +3'] if self.countups[5] > 0 and self.calendar[date][0] == 'Sun' else []
        self.countups[5] += 1
        return ['Kindness +3'] + bonus

    def exam_unlocks(self, date):
        points = 0
        if 1 < self.social_stats['Knowledge'][2]:
            points = 3
            self.exam_coeff = 1.24
        if 3 < self.social_stats['Knowledge'][2]:
            points = 5
            self.exam_coeff = 1.49
        return [f"Charm +{points}"]

    def update_unlocks(self, task, unlocks, date):
        new_unlocks = []
        cinema_bonus = 2 if self.craft_of_cinema and ('Movie' in task or 'DVDs' in task) else 0

        for unlock in unlocks:
            if ' +' in unlock:
                stat, points = unlock.split(' +')

                points = int(points) + cinema_bonus
                if (stat, date) == self.luck_reading:
                    points = math.floor(points * 1.5)

                new_unlock = f"{stat} +{points}"

                total, target, rank = self.social_stats[stat]
                total += points

                if rank < 5 and total >= target:
                    rank += 1
                    target = self.config['Social Stats'][stat][rank]
                    new_unlock = f"{new_unlock} ({stat} Lv. {rank})"

                self.social_stats[stat] = (total, target, rank)
                new_unlocks.append(new_unlock)
            else:
                pass

        return new_unlocks

    def set_luck_reading(self, stat, date):
        _ = self.social_stats[stat]
        self.luck_reading = (stat, date)

def expand_question(task, date, savefile, confidants):
    quest_type = task[:task.find(' Question: ')]
    unlocks = ['Knowledge +2']
    if quest_type == 'Class Lovers':
        unlocks = ['Charm +2']
    if quest_type == 'Exam':
        unlocks = []
    unlocks = savefile.update_unlocks(task, unlocks, date)
    return unlocks

def expand_confidant(task, date, savefile, confidants):
    parts = task.split(' ')
    arcana, event_type = parts[:2]
    event = ' '.join(parts[1:])

    if event_type == 'Invite' or (parts[2] == 'Jazz' and '/' not in event):
        event = f"{event} {date}"
    entry = confidants[arcana][event]
    if entry is None:
        entry = {}

    unlocks = savefile.update_unlocks(task, entry.get('Unlocks', []), date)
    return unlocks

def expand_activity(task, date, savefile, activities):
    unlocks = []

    if ' > ' in task:
        activity, choice = task.split(' > ')
        pages_left = 0

        if '/' in choice:
            choice, total, target = re.fullmatch(r"(.*) (\d)/(\d)", choice).groups()
            pages_left = int(target) - int(total)

        if activity == 'Luck Reading':
            savefile.set_luck_reading(choice, date)
        if choice == 'Craft of Cinema':
            savefile.craft_of_cinema = True

        unlocks = savefile.activity_unlocks(choice, date)

        if len(unlocks) > 0:
            pass
        elif activity == 'Books' and pages_left > 0:
            pass
        elif activity in activities:
            unlocks = activities[activity][choice]
        # else:
        #     print(task)

        unlocks = savefile.update_unlocks(task, unlocks, date)
    else:
        print(task)

    return unlocks

def expand_walkthrough(fname):
    with open(fname) as yamlfile:
        walkthrough = yaml.safe_load(yamlfile)
    with open('walkthrough/activities.yaml') as yamlfile:
        activities = yaml.safe_load(yamlfile)
    with open('walkthrough/class-questions.yaml') as yamlfile:
        quizes = yaml.safe_load(yamlfile)
    with open('walkthrough/social-links.yaml') as yamlfile:
        confidants = yaml.safe_load(yamlfile)
    with open('walkthrough/ace-config.yaml') as yamlfile:
        config = yaml.safe_load(yamlfile)
    with open('walkthrough/calendar.tsv') as tsvfile:
        next(tsvfile)
        calendar = {}
        for line in tsvfile:
            date, dow, daytime, evening = line.split()
            calendar[date] = (dow, 'Rain' in daytime, 'Rain' in evening)

    savefile = SaveFile(config, calendar)
    date_lookup = {}

    for month in config['Months']:
        for date, day in walkthrough[month].items():
            date = date[:date.find(' ')]
            date_lookup[date] = day

    for quiz in quizes:
        timeslot = quiz['Timeslot']
        for date, answer in quiz['Schedule'].items():
            if timeslot not in date_lookup[date]:
                date_lookup[date][timeslot] = []
            date_lookup[date][timeslot].insert(0, f"{quiz['Description']}: {answer}")

    for month in config['Months']:
        for date, day in walkthrough[month].items():
            date = date[:date.find(' ')]
            for timeslot in config['Timeslots']:
                for task in day.get(timeslot, []):
                    if 'Question' in task:
                        unlocks = expand_question(task, date, savefile, confidants)
                    elif task[:task.find(' ')] in config['Confidants']:
                        unlocks = expand_confidant(task, date, savefile, confidants)
                    else:
                        unlocks = expand_activity(task, date, savefile, activities)

                    # print(date, timeslot, task, unlocks)

if __name__ == '__main__':
    expand_walkthrough('walkthrough/ace-walkthrough.yaml')
