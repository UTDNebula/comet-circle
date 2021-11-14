class Event:
    def __init__(self, startTime, finishTime, tags):
        self.startTime = startTime
        self.finishTime = finishTime
        _tags = []

        for tag in tags:

            _tags.append(tag)
        self.tags = _tags



    def __str__(self):
        return str(self.startTime) + " - " + str(self.finishTime) + " | " + str(self.tags)


def getDayTimeConflicts(events, minHour, maxHour):
    conflicts = [0] * ((maxHour - minHour) * 4 + 1)
    for event in events:
        if event.startTime is not None and event.finishTime is not None:
            startIndex = (event.startTime.hour - minHour) * 4 + (event.startTime.minute // 15)
            finishIndex = (event.finishTime.hour - minHour) * 4 + (event.finishTime.minute // 15)
            if startIndex >= 0 and finishIndex < len(conflicts):
                for i in range(startIndex, finishIndex):
                    conflicts[i] += 1

    return conflicts

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
            _tags = self._getTagsFromPrefix(event.tags)
            _times = (None, None) if len(_days) <= 0 else self._convertToStringTimeToInts(event['times'])
            for day in _days:
                _eventsDict[day].append(Event(_times[0], _times[1], _tags))

        return _eventsDict