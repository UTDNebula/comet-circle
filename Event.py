class Event:
    def __init__(self, startTime, finishTime, tags):
        self.startTime = startTime
        self.finishTime = finishTime
        self.tags = tags

    def __str__(self):
        return str(self.startTime) + " - " + str(self.finishTime) + " | " + str(self.tags)


def getDayTimeConflicts(events, minHour, maxHour):
    conflicts = [0] * ((maxHour - minHour) * 4 + 1)
    for event in events:
        if event.startTime is not None and event.finishTime is not None:
            startIndex = (event.startTime.hour - minHour) + (event.startTime.minute // 15)
            endIndex = (event.finishTime.hour - minHour) + (event.finishTime.minute // 15)
            if startIndex >= 0 and endIndex < len(conflicts):
                for i in range(startIndex, endIndex):
                    conflicts[i] += 1
            else:
                print("event time out of bounds: " + str(event.startTime) + " - " + str(event.finishTime))
    return conflicts
