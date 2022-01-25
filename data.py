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
    response = requests.get("https://api-ilknlukhca-uc.a.run.app/v1/sections/search?=", headers=headers)
    if response.status_code != 200:
        st.error("Error retrieving data from api")
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

        #print(RenderTree(self.rootTag))
        
        
        self.tags = list(set(self.schools + self.prefixes))
        self.tags.sort()
        self.terms.sort()

    def getNodeListNames(nodeList):
        nodeListNames = []
        for node in nodeList:
            nodeListNames.append(node.name)
        return nodeListNames


    def getSchoolPrefixTags(self, schoolTag):
        #st.write(self.rootTag.children)
        prefixTagList = []
        for prefix in self.rootTag.children[schoolTag].children:
            prefixTagList.append(prefix.name)
        return prefixTagList

    def getSchoolTags(self):
        schoolsTagList = []
        for node in self.rootTag.children:
            schoolsTagList.append(node.name)
        return schoolsTagList



    def filterEvents(self, _events, termFilters, tagFilters):
        filteredEvents = []
        # expand all school tags to all their class prefixes
        tagFiltersExpanded = []
        for tag in tagFilters:
            tagFiltersExpanded += self._getTagsFromPrefix(tag)
        tagFilters = set(tagFiltersExpanded) # Remove duplicates

        for event in _events:
            tag = event['course_prefix']
            term = event['term']
            if (len(termFilters) == 0 or term in termFilters) and (len(tagFilters) == 0 or tag in tagFilters):
                filteredEvents.append(event)
        return filteredEvents

    def search(self, _events, property, value):
        newEvents = []
        for event in _events:
            if event[property] == value:
                newEvents.append(event)
        return newEvents

    def _getTagsFromPrefix(self, prefix):
        _tags = []
        if prefix in self.schools:
            schoolIndex = self.schools.index(prefix)
            _prefixNodes = self.schoolsNodes[schoolIndex].children
            for node in _prefixNodes:
                _tags.append(node.name)
        else:
            _tags.append(prefix)
        return _tags
