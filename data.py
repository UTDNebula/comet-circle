import requests
import json
from anytree import Node, findall



class Data:
    
    def __init__(self):
        NEBULA_API_KEY = "dd1h55UQUb8x5nQIPW2iJ1ABaIDx9iv7"

        headers = {"Authorization": NEBULA_API_KEY}

        response = requests.get("https://api.utdnebula.com/v1/sections/search?=", headers=headers)
        self.classes = json.loads(response.text)

            
    def assignMetaData(self):
        self.terms = []
        self.tags = []
        self.schools = []
        self.prefixes = []
        self.schoolsNodes = []
        self.prefixesNodes = []
        self.rootTag = Node("utd")
        
        for event in self.classes:
            if event['school'] not in self.schools:
                self.schools.append(event['school'])
                self.schoolsNodes.append(Node(event['school'], parent=self.rootTag))
            if event['course_prefix'] not in self.prefixes:
                self.prefixes.append(event['course_prefix'])
                schoolIndex = self.schools.index(event['school'])
                self.prefixesNodes.append(Node(event['course_prefix'], parent=self.schoolsNodes[schoolIndex]))
            if event['term'] not in self.terms:
                self.terms.append(event['term'])

        self.tags = list(set(self.schools + self.prefixes))
        self.tags.sort()
        self.terms.sort()
    

    def getEventList(self, _events):
        
        for event in _events:
            _tags = []
            tag = event['course_prefix']
            if tag in self.schools:
                schoolIndex = self.schools.index(tag)
                _prefixNodes = findall(self.schoolsNodes[schoolIndex])
                for node in _prefixNodes:
                    _tags.append(node)
            else:
                _tags.append(tag)

                
    events = []

    def filterEvents(self, _events, termFilters, tagFilters):
        filteredEvents = []
        for event in _events:
            tag = event['course_prefix']
            term = event['term']
            if (len(termFilters) == 0 or term in termFilters) and (len(tagFilters) == 0 or tag in tagFilters):
                filteredEvents.append(event)
        return filteredEvents
            
    def conflicts(self, _events):
        conflictDays = {}
        for event in _events:
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

    def search(property, value, _events):
        newEvents = []
        for event in _events:
            if event[property] == value:
                newEvents.append(event)
        return newEvents

            
