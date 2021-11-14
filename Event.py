from anytree import Node


class Event:
    startTime = -1
    finishTime = -1
    tags = [Node("utd")]

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
