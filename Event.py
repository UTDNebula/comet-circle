
class Event:
    def __init__(self, startTime, finishTime, tags, desc = ''):
        self.startTime = startTime
        self.finishTime = finishTime
        _tags = []
        self.description = desc

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
    conflicts.reverse()
    return conflicts
