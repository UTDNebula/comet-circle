from hashlib import new
import streamlit as st
from streamlit.state.session_state import Value
from DateSelector import event
import data
from Event import Event, getDayTimeConflicts
import datetime as dt
import plotly.graph_objects as go
import numpy as np



dat = data.Data()
dat.assignMetaData()

# Sidebar
side = st.sidebar
tagFilters = st.sidebar.multiselect('Filters', dat.tags)
termFilters = st.sidebar.multiselect('Term', dat.terms)


# View Settings
c1,c2 = st.sidebar.columns(2)
show_classes = c1.checkbox('Show classes', value=True)
show_events = c2.checkbox('Show events', value=True)

if 'events' not in st.session_state:
	st.session_state.events = {
            "Sunday": [],
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": []
        }

# Create Event
st.sidebar.write('''---''')
tab = st.sidebar
today = dt.datetime.today()
event_name = tab.text_input('Event Name', value='Event name')
c1,c2 = tab.columns(2)
time_date = c1.date_input('Start date', today)
time_tags = c2.multiselect('Tags', dat.tags)
c1,c2 = tab.columns(2)
start = c1.text_input('Start time')
finish = c2.text_input('End time')
if st.sidebar.button("Create Event"):
    tab.success('Event created!')
    start = dt.datetime.strptime(start, '%H:%M')
    finish = dt.datetime.strptime(finish, '%H:%M')
    newEvent = Event(start, finish, time_tags, event_name)
    st.session_state.events[['Monday', 'Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][time_date.weekday()]].append(newEvent)
st.sidebar.write('''---''')
st.sidebar.button("Import from Presence")


#Actions
filteredClasses = dat.filterEvents(dat.classes, termFilters, tagFilters)

classesByDay = dat.getEventListByDay(filteredClasses)



np.random.seed(1)

week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

#st.write("Length of filtered Events: " + str(len(filteredEvents)))
times = []
minHour = 6
maxHour = 24

for hour in range(minHour, maxHour):
    for i in range(0, 4):
        min = i * 15
        min = "0" + str(min) if min < 10 else str(min)
        timeStr = str(hour-12) + ":" + min + " PM" if hour > 12 else str(hour) + ":" + min + " AM"
        times.append(timeStr)

timeStr = str(maxHour-12) + ":" + "00" + " PM" if maxHour > 12 else str(maxHour) + ":" + "00" + " AM"
times.append(timeStr)
times.reverse()

base = times
#dates = base - np.arange(180) * datetime.timedelta(days=1)
#z = np.random.poisson(size=(len(week), len(base)))

z = []
for day in classesByDay:
    z.append(getDayTimeConflicts(classesByDay[day], minHour, maxHour))
z = np.transpose(z)
#st.write(z)

colorscale=[[0.0, 'rgb(255,255,255)'], [0.1, 'rgb(0,255,0)'], [0.55, 'rgb(255,255,0)'], [1.0, 'rgb(255, 0, 0)']]
colorscale2=[[0.0, 'rgb(255,255,255)'], [1.0, 'rgb(0,255,0)']]

fig = go.Figure(data=go.Heatmap(
        z=z,
        x=week,
        y=base,
        colorscale=colorscale))
#fig.update_xaxes(side="top")
fig.update_layout(
    title='Classes',
    xaxis_nticks=100)

'''# Comet Circle'''
c1, c2 = st, st
if show_events and show_classes:
    c1, c2 = st,st

def eventConflicts(events, minHour, maxHour):
    conflicts = [0] * ((maxHour - minHour) * 4 + 1)
    descs = [""] * ((maxHour - minHour) * 4 + 1)
    for event in events:
        if event.startTime is not None and event.finishTime is not None:
            startIndex = (event.startTime.hour - minHour) * 4 + (event.startTime.minute // 15)
            finishIndex = (event.finishTime.hour - minHour) * 4 + (event.finishTime.minute // 15)
            if startIndex >= 0 and finishIndex < len(conflicts):
                for i in range(startIndex, finishIndex):
                    conflicts[i] += 1 
                    descs[i] += event.description + "\n"
    conflicts.reverse()

    return conflicts, descs
import plotly.figure_factory as ff
if show_classes:
    c1.plotly_chart(fig)
if show_events: 
    #c2.plotly_chart(fig)
    z2 = []
    z3 = []
    for day in st.session_state.events:
        f,g=eventConflicts(st.session_state.events[day], minHour, maxHour)
        z2.append(f)
        z3.append(g)
        
    z2 = np.transpose(z2)
    z3 = np.transpose(z3)
    #fig2 = go.Figure(data=go.Heatmap(
    #    z=z2,
    #    x=week,
    #    y=base,
    #    colorscale=colorscale))

    #fig2 = ff.create_annotated_heatmap(z=z2, x=week, y=base, text=g,
    #                             colorscale=colorscale, hoverinfo='text')
    #fig2.update_layout(title_text='Events')

    fig2 = go.Figure(data=go.Heatmap(
        z=z2,
        x=week,
        y=base,
        colorscale=colorscale2))
    fig2.update_layout(
    title='Events',
    xaxis_nticks=100)
    c2.plotly_chart(fig2)