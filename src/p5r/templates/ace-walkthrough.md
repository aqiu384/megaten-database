{% for month, days in walkthrough.items() %}
## {{ month }}
{% for date, timeslots in days.items() %}
### {{ date }}
{% for timeslot in config['Timeslots'] %}
{% if timeslot in timeslots %}
#### {{ timeslot }}
{% for task in timeslots[timeslot] %}
* {{ task['Task'] }}{% for todo in task['Todo'] %} > {{ todo }}{% endfor %}

{% endfor %}
{% endif %}
{% endfor %}
{% endfor %}
{% endfor %}
