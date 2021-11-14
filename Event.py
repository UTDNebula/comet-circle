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
