import streamlit as st
from streamlit.state.session_state import Value
from DateSelector import event
import data
from Event import Event, getDayTimeConflicts
import datetime as dt

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

if 'eventsByDay' not in st.session_state:
	st.session_state.eventsByDay = {
        "Sunday": [],
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": []}

# Create Event
st.sidebar.write('''---''')
tab = st.sidebar
today = dt.datetime.today()
c1,c2 = tab.columns(2)
time_date = c1.date_input('Start date', today)
time_tags = c2.multiselect('Tags', dat.tags)
start = c1.text_input('Start time')
finish = c2.text_input('End time')
if st.sidebar.button("Create Event"):
    tab.success('Event created!')
    newEvent = Event(start, finish, time_tags)
    #st.session_state.eventsByDay[time_date.weekday()]


#Actions
filteredClasses = dat.filterEvents(dat.classes, termFilters, tagFilters)
    
classesByDay = dat.getEventListByDay(filteredClasses)


import plotly.graph_objects as go
import datetime
import numpy as np
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
    c1, c2 = st.columns(2)

if show_classes:
    c1.plotly_chart(fig)
if show_events:
    #c2.plotly_chart(fig)
    "lol"

# Plotly test
import plotly.express as px
data=[[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
fig = px.imshow(data,
                labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
                x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                y=['Morning', 'Afternoon', 'Evening']
               )
fig.update_xaxes(side="top")