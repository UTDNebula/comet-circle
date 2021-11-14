import requests
import json
from anytree import Node, findall

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

tagFilters = []
termFilters = []

events = []
#meta data
schools = []
tags = []
terms = []
prefixes = []
schoolsNodes = []
prefixesNodes = []
rootTag = Node("utd")

def assignMetaData():
    for event in classes:
        if event['school'] not in schools:
            schools.append(event['school'])
            schoolsNodes.append(Node(event['school'], parent=rootTag))
        if event['course_prefix'] not in prefixes:
            prefixes.append(event['course_prefix'])
            schoolIndex = schools.index(event['school'])
            prefixesNodes.append(Node(event['course_prefix'], parent=schoolsNodes[schoolIndex]))
        if event['term'] not in terms:
            terms.append(event['term'])
    tags = list(set(schools + prefixes))
    
    
assignMetaData()

def filterEvents(_events, termFilters, tagFilters):
    filteredEvents = []
    for event in _events:
        if event['term'] not in termFilters:
            continue
        if event['coursePrefix'] not in tagFilters or event['school'] not in tagFilters:
            continue
        
        filteredEvents.append(event)


    return filterEvents
        


def getEventList(_events):
    
    for event in _events:
        _tags = []
        tag = event['course_prefix']
        if tag in schools:
            schoolIndex = schools.index(tag)
            _prefixNodes = findall(schoolsNodes[schoolIndex])
            for node in _prefixNodes:
                _tags.append(node)
        else:
            _tags.append(tag)
        





def conflicts(_events):
    for event in events:
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

def search(property, value, _events = classes):
    newEvents = []
    for event in events:
        if event[property] == value:
            newEvents.append(event)
    return newEvents
