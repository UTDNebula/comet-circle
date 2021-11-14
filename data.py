import requests
import json
from anytree import Node, findall
from Event import Event
from datetime import time


class Data:

    def __init__(self):
        NEBULA_API_KEY = "dd1h55UQUb8x5nQIPW2iJ1ABaIDx9iv7"

        headers = {"Authorization": NEBULA_API_KEY}

        response = requests.get("https://api.utdnebula.com/v1/sections/search?=", headers=headers)
        self.classes = json.loads(response.text)
        self.terms = []
        self.tags = []
        self.schools = []
        self.prefixes = []
        self.schoolsNodes = []
        self.prefixesNodes = []
        self.rootTag = Node("utd")
        self.assignMetaData()
        self.debugTimes = []

    def assignMetaData(self):

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

    def getEventListByDay(self, _events):

        _eventsDict = {
            "Sunday": [],
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": []
        }

        for event in _events:
            _tags = self._getTagsFromPrefix(event['course_prefix'])
            _days = self._getDays(event['days'])
            _times = (None, None) if len(_days) > 0 else self._convertToStringTimeToInts(event['times'])
            for day in _days:
                _eventsDict[day].append(Event(_times[0], _times[1], _tags))

        return _eventsDict

    def filterEvents(self, _events, termFilters, tagFilters):
        filteredEvents = []
        for event in _events:
            tag = event['course_prefix']
            term = event['term']
            _days = self._getDays(event['days'])
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

    def search(self, _events, property, value):
        newEvents = []
        for event in _events:
            if event[property] == value:
                newEvents.append(event)
        return newEvents

    def _getTagsFromPrefix(self, tag):
        _tags = []
        if tag in self.schools:
            schoolIndex = self.schools.index(tag)
            _prefixNodes = findall(self.schoolsNodes[schoolIndex])
            for node in _prefixNodes:
                _tags.append(node)
        else:
            _tags.append(tag)
        return _tags

    def _convertToStringTimeToInts(self, timesStr):
        _start = None
        _finish = None
        #print(timesStr)
        if ":" not in timesStr:
            return _start, _finish
        times = timesStr.split(' - ')
        if len(times) != 2:
            print(Exception("time not formatted correctly " + timesStr))
            return _start, _finish

        start = times[0].split(":")
        finish = times[1].split(":")
        if len(start) != 2 and len(finish) != 2:
            print(Exception("time not formatted correctly " + timesStr))
            return _start, _finish

        _start = time(int(start[0]), int(start[1]))
        _finish = time(int(finish[0]), int(finish[1]))

        print (timesStr + " -> " + str(_start) + " - " + str(_finish))
        return _start, _finish

    def _getDays(self, daysString):
        _days = []
        if "Sunday" in daysString:
            _days.append('Sunday')
        if "Monday" in daysString:
            _days.append("Monday")
        if "Tuesday" in daysString:
            _days.append('Tuesday')
        if "Wednesday" in daysString:
            _days.append('Wednesday')
        if "Thursday" in daysString:
            _days.append('Thursday')
        if "Friday" in daysString:
            _days.append('Friday')
        if "Saturday" in daysString:
            _days.append('Saturday')
        return _days
