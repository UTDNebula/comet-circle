import requests
import json

NEBULA_API_KEY = "dd1h55UQUb8x5nQIPW2iJ1ABaIDx9iv7"

headers = {"Authorization": NEBULA_API_KEY}

response = requests.get("https://api.utdnebula.com/v1/sections/search?=", headers=headers)
classes = json.loads(response.text)

conflictDays = {'Monday' : 0,
                'Tuesday' : 0,
                'Wednesday' : 0,
                'Thursday' : 0,
                'Friday' : 0,
                'Saturday' : 0,
                'Sunday' : 0}


for event in classes:
    if "Monday" in event['days']:
        conflictDays['Monday'] += 1
    if "Tuesday" in event['days']:
        conflictDays['Tuesday'] += 1
    if "Wednesday" in event['days']:
        conflictDays['Wednesday'] += 1
    if "Thursday" in event['days']:
        conflictDays['Thursday'] += 1
    if "Friday" in event['days']:
        conflictDays['Friday'] += 1
    if "Saturday" in event['days']:
        conflictDays['Saturday'] += 1
    if "Sunday" in event['days']:
        conflictDays['Sunday'] += 1

def search(property, value):
    events = []
    for event in classes:
        if event[property] == value:
            events.append(event)
    return events
