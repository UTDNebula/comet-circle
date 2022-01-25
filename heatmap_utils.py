from Event import Event
from datetime import time
import plotly.graph_objects as go
import numpy as np

week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def createHeatMapFromCourses(courses, title="Classes", minHour=6, maxHour=24, colorscale=[[0.0, 'rgb(255,255,255)'], [0.1, 'rgb(0,255,0)'], [0.55, 'rgb(255,255,0)'], [1.0, 'rgb(255, 0, 0)']]):
    
    eventsByDay = getEventListByDay(courses)
    
    z = []
    for day in eventsByDay:
        z.append(getDayTimeConflicts(eventsByDay[day], minHour, maxHour))
    z = np.transpose(z)

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=week,
        y=generateTimeFrame(minHour, maxHour),
        colorscale=colorscale))
    fig.update_layout(
        title=title,
        xaxis_nticks=100)
    return fig

def createHeatMapFromEvents(events, title="Events", minHour=6, maxHour=24, colorscale=[[0.0, 'rgb(255,255,255)'], [1.0, 'rgb(0,255,0)']]):
    
    
    z = []
    for day in events:
        z.append(getDayTimeConflicts(events[day], minHour, maxHour))
    z = np.transpose(z)

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=week,
        y=generateTimeFrame(minHour, maxHour),
        colorscale=colorscale))
    fig.update_layout(
        title=title,
        xaxis_nticks=100)
    return fig



def generateTimeFrame(minHour, maxHour):
    
    times = []
    for hour in range(minHour, maxHour):
        for i in range(0, 4):
            min = i * 15
            min = "0" + str(min) if min < 10 else str(min)
            timeStr = str(hour-12) + ":" + min + " PM" if hour > 12 else str(hour) + ":" + min + " AM"
            times.append(timeStr)

    timeStr = str(maxHour-12) + ":" + "00" + " PM" if maxHour > 12 else str(maxHour) + ":" + "00" + " AM"
    times.append(timeStr)
    times.reverse()
    return times


def getEventListByDay(courses):
    coursesDict = dict()
    for day in week:
        coursesDict[day] = []

    for _class in courses:
        _tags = _class['course_prefix']
        _days = _getDays(_class['days'])
        _times = (None, None) if len(_days) <= 0 else _convertTimeStringToInts(_class['times'])
        for day in _days:
            coursesDict[day].append(Event(_times[0], _times[1], _tags))

    return coursesDict


# Takes a list of events on a certain day in a given time frame
# Returns a int list of conflicts of size ((maxHour - minHour) * 4 + 1) in 
# increments of 15, so
# conflicts[0] = the conflicts at minHour, 
# conflicts[conflicts.length - 1] = the conflicts at maxHour
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



def _convertTimeStringToInts(timesStr):
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

    return _start, _finish

def _getDays(daysString):
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
