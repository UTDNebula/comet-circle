import requests
import json
from anytree import Node, findall, RenderTree
from Event import Event
from datetime import time
import streamlit as st


# API reference https://about.utdnebula.com/docs/api-docs/nebula-api
@st.cache(suppress_st_warning=True)
def get_classes():
    NEBULA_API_KEY = "dd1h55UQUb8x5nQIPW2iJ1ABaIDx9iv7"
    headers = {"Authorization": NEBULA_API_KEY}
    response = requests.get("https://api.utdnebula.com/v1/sections/search?=", headers=headers)
    st.write(response)
    return json.loads(response.text)

class Data:

    def __init__(self):
        self.classes = get_classes()
        self.terms = []
        self.tags = []
        self.schools = []
        self.prefixes = []
        self.schoolsNodes = []
        self.prefixesNodes = []
        self.rootTag = Node("utd")
        self.assignMetaData()

    def assignMetaData(self):

        for _class in self.classes:
            # School abbreviation to name:
            # "ah" => School of Arts and Humanities
            # "atec" => School of Arts, Technology, and Emerging Communication
            # "bbs" => School of Behavioral and Brain Sciences
            # "eps" => School of Economic, Political and Policy Sciences
            # "ecs" => Erik Jonsson School of Engineering and Computer Science
            # "is" => School of Interdisciplinary Studies
            # "mgt" => Naveen Jindal School of Management
            # "nsm" => School of Natural Sciences and Mathematics
            # "hons" => honors
            # "ug" => Undergraduate (undeclared)?
            # 

            classSchool = _class['school']
            classPrefix = _class['course_prefix']
            classTerm = _class['term']

            if classSchool not in self.schools:
                self.schools.append(classSchool)
                self.schoolsNodes.append(Node(classSchool, parent=self.rootTag))
            if classPrefix not in self.prefixes:
                self.prefixes.append(classPrefix)
                schoolIndex = self.schools.index(classSchool)
                self.prefixesNodes.append(Node(classPrefix, parent=self.schoolsNodes[schoolIndex]))
            if classTerm not in self.terms:
                self.terms.append(classTerm)

        print(RenderTree(self.rootTag))
        
        
        self.tags = list(set(self.schools + self.prefixes))
        self.tags.sort()
        self.terms.sort()

    def getNodeListNames(nodeList):
        nodeListNames = []
        for node in nodeList:
            nodeListNames.append(node.name)
        return nodeListNames


    def getSchoolPrefixTags(self, schoolTag):
        st.write(self.rootTag.children)
        prefixTagList = []
        for prefix in self.rootTag.children[schoolTag].children:
            prefixTagList.append(prefix.name)
        return prefixTagList

    def getSchoolTags(self):
        schoolsTagList = []
        for node in self.rootTag.children:
            schoolsTagList.append(node.name)
        return schoolsTagList


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
            _times = (None, None) if len(_days) <= 0 else self._convertToStringTimeToInts(event['times'])
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
        # print(timesStr)
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

        #print (timesStr + " -> " + str(_start) + " - " + str(_finish))
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
