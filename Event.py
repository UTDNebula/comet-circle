from anytree import Node

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

    def convertToStringTimeToInts(self, timesStr):
        times = timesStr.split(' - ')
        if len(times) != 2:
            Exception("time not formatted correctly" + timesStr)
        if times[0] == 'tbh' or times[1] == 'tbh':
            self.startTime = -1
            self.finishTime = -1
            return self.startTime, self.finishTime

        start = times[0].split(":")
        finish = times[1].split(":")
        if len(start) + len(finish) != 4:
            Exception("time not formatted correctly" + timesStr)

        self.startTime = int(start[0] + start[1])
        self.finishTime = int(finish[0] + finish[1])
        return self.startTime, self.finishTime

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