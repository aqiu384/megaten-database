{% for month, days in walkthrough.items() %}
## {{ month }}
{% for date, timeslots in days.items() %}
### {{ date }}
{% for timeslot in config['Timeslots'] %}
{% if timeslot in timeslots and timeslots[timeslot]['Tasks']|length > 0 %}
#### {{ timeslot }}{% if timeslots[timeslot]['Rainy'] %} (Rain){% endif %}

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
