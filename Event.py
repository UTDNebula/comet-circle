
class Event:
    def __init__(self, startTime, finishTime, tags, desc = ''):
        self.startTime = startTime
        self.finishTime = finishTime
        self.description = desc # potentially used for an on-hover

        _tags = []
        for tag in tags:
            _tags.append(tag)
        self.tags = _tags



    def __str__(self):
        return str(self.startTime) + " - " + str(self.finishTime) + " | " + str(self.tags)
