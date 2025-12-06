#!/usr/bin/python3
import yaml
import math
import re
from jinja2 import Environment, FileSystemLoader


class SaveFile:
    def __init__(self, config, calendar):
        self.config = config
        self.calendar = calendar
        self.has_personas = { x: False for x in config['Confidants'] }
        self.social_stats = { x: (0, y[1], 1) for x, y in config['Social Stats'].items() }
        self.luck_reading = ('4/01', 'Knowledge')
        self.craft_of_cinema = False
        self.exam_coeff = 1
        self.countups = [0] * 6
        self.flower_counter = 0
        self.flower_choices  = [
            'Scarlet Rose > Gold Gerbera > Gecko Orchid',
            'Justice Jasmine > Fluorescent Freesia > Enamored Orchid'
        ]
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
        unlocks = [f"+¥{7400 if points == 5 else 3500}", f"Charm +{points}"]

        if self.countups[2] > 2 and int(date.replace('/', '')) > 803:
            unlocks.append('Calling for Justice for Cats Request')
        return unlocks

    def flowershop_unlocks(self, date):
        dow = self.calendar[date][0]
        points = 5 if self.countups[3] == 1 or dow == 'Wed' or dow == 'Sat' else 3
        unlocks = [self.flower_choices[self.flower_counter]] if points == 5 else []
        self.countups[3] += 1
        unlocks = unlocks + [f"+¥{7800 if points == 5 else 3200}", f"Kindness +{points}"]

        if points == 5:
            self.flower_counter += 1
        if self.countups[3] > 2 and int(date.replace('/', '')) > 802:
            unlocks.append("Who's Been Assaulting People? Request")
        return unlocks

    def beefbowl_unlocks(self, date):
        points = 5 if self.countups[4] == 1 or date.endswith('2') else 3
        self.countups[4] += 1
        return [f"+¥{8800 if points == 5 else 3600}", f"Proficiency +{points}"]

    def crossroads_unlocks(self, date):
        bonus = ['Guts +3'] if self.countups[5] > 0 and self.calendar[date][0] == 'Sun' else []
        self.countups[5] += 1
        unlocks = [f"+¥{12000 if len(bonus) > 0 else 7200}", 'Kindness +3'] + bonus

        if self.countups[5] > 1 and int(date.replace('/', '')) > 801:
            unlocks.append("We Aren't Just Your Slaves Request")
        return unlocks

    def exam_unlocks(self, date):
        points = 0
        knowledge_lvl = self.social_stats['Knowledge'][2]
        if 1 < knowledge_lvl:
            points = 3
        if 3 < knowledge_lvl:
            points = 5
            self.exam_coeff = 1.2
        if 4 < knowledge_lvl:
            self.exam_coeff = 1.5
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

                new_unlocks.append(f"{stat} +{points}")

                total, target, rank = self.social_stats[stat]
                total += points

                if rank < 5 and total >= target:
                    rank += 1
                    target = self.config['Social Stats'][stat][rank]
                    new_unlocks.append(f"{stat} Lv. {rank}")

                self.social_stats[stat] = (total, target, rank)
            elif unlock[0] == '¥' or unlock[1] == '¥':
                new_unlocks.append(unlock)
            else:
                new_unlocks.append(f"{unlock} unlocked")

        return new_unlocks

    def update_choices(self, task, choices, next_rank):
        confidant, event = task.split(' ')[:2]
        total = 0
        new_choices = []
        todo = { 'Choices': new_choices }
        point_coeff = (1.5 if self.has_personas[confidant] else 1) * (
            self.exam_coeff if confidant in self.config['Exam Confidants'] else 1
        )

        for choice in choices:
            if choice != 'Any':
                choice, points = choice.split(' +')
                points = math.floor(int(points) * point_coeff)
                total += points
                new_choices.append(f"{'' if choice.startswith('Phone') else 'Choice '}{choice} +{points}")
            else:
                new_choices.append('Any')
        if next_rank >= 0:
            todo['Next Rank'] = f"{total}/{next_rank}"
        return todo

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
    return { 'Unlocks': unlocks }

def expand_confidant(task, date, savefile, confidants):
    parts = task.split(' ')
    arcana, event_type = parts[:2]
    event = ' '.join(parts[1:])

    if event_type == 'Invite' or (parts[2] == 'Jazz' and '/' not in event):
        event = f"{event} {date}"
    entry = confidants[arcana][event]
    if entry is None:
        entry = {}

    todo = savefile.update_choices(task, entry.get('Choices', []), entry.get('Next Rank', -1))
    todo['Unlocks'] = savefile.update_unlocks(task, entry.get('Unlocks', []), date)
    todo['Requires'] = entry.get('Requires', [])
    return todo

def expand_activity(task, date, savefile, activities):
    unlocks = []

    if task != 'Auto' and task != 'Free Time':
        activity, choice = task.split(' > ')
        pages_left = 0

        if activity.endswith('Palace'):
            return { 'Unlocks': unlocks }
        if '/' in choice:
            choice, total, target = re.fullmatch(r"(.*) (\d)/(\d)", choice).groups()
            pages_left = int(target) - int(total)

        if activity == 'Luck Reading':
            savefile.set_luck_reading(choice, date)
        elif activity == 'Obtain Personas':
            for arcana in choice.split(', '):
                if not savefile.has_personas[arcana]:
                    savefile.has_personas[arcana] = True
        elif choice == 'Craft of Cinema':
            savefile.craft_of_cinema = True

        unlocks = savefile.activity_unlocks(choice, date)

        if len(unlocks) > 0:
            pass
        elif activity == 'Books' and pages_left > 0:
            pass
        else:
            options = activities[activity]
            unlocks = options['All'] if choice not in options else options[choice]

        unlocks = savefile.update_unlocks(task, unlocks, date)

    return { 'Unlocks': unlocks }

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
    with open('walkthrough/sakaya-trader.tsv') as tsvfile:
        next(tsvfile)
        trades = []
        for line in tsvfile:
            date, timeslot, action = line.split('\t')
            action = action.strip()
            trades.append((date, timeslot, action))
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
                new_tasks = []

                for task in day.get(timeslot, []):
                    choices = []

                    if 'Question' in task:
                        new_entry = expand_question(task, date, savefile, confidants)
                    elif task[:task.find(' ')] in config['Confidants']:
                        new_entry = expand_confidant(task, date, savefile, confidants)
                    else:
                        new_entry = expand_activity(task, date, savefile, activities)

                    new_entry['Task'] = task
                    new_tasks.append(new_entry)

                if len(new_tasks) > 0 and new_tasks[0]['Task'] != 'Auto':
                    day[timeslot] = { 'Rainy': False, 'Tasks': new_tasks }

            if date in calendar:
                dow, day_rain, eve_rain = calendar[date]
                if day_rain:
                    day['Daytime']['Rainy'] = True
                if eve_rain:
                    day['Evening']['Rainy'] = True

    for date, timeslot, action in trades:
        date_lookup[date][timeslot]['Tasks'].insert(0, { 'Task': action })

    env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True, lstrip_blocks=True)
    env.filters['resist_type_format'] = lambda x: RESIST_TYPES.get(x, x)
    env.filters['resist_frac_format'] = lambda x: RESIST_FRACS.get(x, 100)
    env.filters['skill_lvl_format'] = lambda x: '-' if x < 2 else str(x)
    template = env.get_template('ace-walkthrough.md')
    output = template.render(walkthrough=walkthrough, config=config)

    with open('walkthrough.md', 'w+') as mdfile:
        mdfile.write(output)

if __name__ == '__main__':
    expand_walkthrough('walkthrough/ace-walkthrough.yaml')
