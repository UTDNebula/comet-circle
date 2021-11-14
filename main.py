import streamlit as st
from streamlit.state.session_state import Value
from DateSelector import event
import data
from Event import getDayTimeConflicts
import SessionState

dat = data.Data()
dat.assignMetaData()

# Sidebar
side = st.sidebar
tagFilters = st.sidebar.multiselect('Filters', dat.tags)
termFilters = st.sidebar.multiselect('Term', dat.terms)

filteredEvents = dat.filterEvents(dat.classes, termFilters, tagFilters)
#raise Exception(str(dat.search(filteredEvents, 'days', 'tbd')))
eventsByDay = dat.getEventListByDay(filteredEvents)
#st.write(dat.filterEvents(dat.classes, termFilters, tagFilters))

# View Settings
c1,c2 = st.sidebar.columns(2)
show_classes = c1.checkbox('Show classes', value=True)
show_events = c2.checkbox('Show events', value=True)

# View Debug
if show_classes:
    'show classes'
if show_events:
    'show events'

# Create Event
st.sidebar.write('''---''')
event(st.sidebar)
if st.sidebar.button("Create Event"):
    'Wow'

import plotly.graph_objects as go
import datetime
import numpy as np
np.random.seed(1)

week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

st.write("Length of filtered Events: " + str(len(filteredEvents)))
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

st.write(filteredEvents)
z = []
for day in eventsByDay:
    z.append(getDayTimeConflicts(eventsByDay[day], minHour, maxHour))
z = np.transpose(z)

fig = go.Figure(data=go.Heatmap(
        z=z,
        x=week,
        y=base,
        colorscale='Viridis'))
#fig.update_xaxes(side="top")
fig.update_layout(
    title='Comet Clique',
    xaxis_nticks=100)

st.plotly_chart(fig)

# Plotly test
import plotly.express as px
data=[[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
fig = px.imshow(data,
                labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
                x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                y=['Morning', 'Afternoon', 'Evening']
               )
fig.update_xaxes(side="top")