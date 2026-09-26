# All Confidant Events Walkthrough - Persona 5 Royal
### Legacy Walkthroughs
* [Normal and Battle Route Walkthroughs v1.1.3](./walkthrough-v113)
* [All Confidant Events Walkthrough v1.1.3](./ace-walkthrough-v113)

### Notes
* Optional Event: Will not affect progression. Event can be viewed or treated as free time without reloading.
* Optional Save/Reload Event: Will affect progression. Must reload last save after viewing, or the current day if not one designated.

{% for month, days in walkthrough.items() %}
### {{ month }}
{% for date, timeslots in days.items() %}
---
#### {{ date }}
{% for timeslot in config['Timeslots'] %}
{% if timeslot in timeslots and timeslots[timeslot]['Tasks']|length > 0 %}
##### {{ timeslot }}{% if timeslots[timeslot]['Rainy'] %} (Rain){% endif %}

{% for task in timeslots[timeslot]['Tasks'] %}
* {{ task['Task'] }}{% if 'Next Rank' in task %} ({{ task['Next Rank'] }} to rank up){% endif %}{% for unlock in task['Unlocks'] %} ({{ unlock }}){% endfor %}

    {% for requires in task['Requires'] %}
    1. {{ requires }} required
    {% endfor %}
    {% for choice in task['Choices'] %}
    1. {{ choice }}
    {% endfor %}
{% endfor %}
{% endif %}
{% endfor %}
{% endfor %}
{% endfor %}
