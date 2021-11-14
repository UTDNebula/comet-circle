import streamlit as st
from streamlit.state.session_state import Value
from DateSelector import event
import data
import SessionState

dat = data.Data()
dat.assignMetaData()

# Sidebar
side = st.sidebar
tagFilters = st.sidebar.multiselect('Filters', dat.tags)
termFilters = st.sidebar.multiselect('Term', dat.terms)

st.write(tagFilters)
st.write(termFilters)
st.write(dat.filterEvents(dat.classes, termFilters, tagFilters))

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

times = []

for i in range(24, 5,-1):
    hour = ((i-1) % 12) + 1
    #hour2 = ((i-1) % 12) + 1
    pm = i >= 12 and i < 24 and " PM" or " AM"
    times.append(str(hour) + pm)
    #times.append(str(hour2) +":30 " + pm)
    #times.append(str(hour) +":30 " + pm)
   # times.append(str(hour) +":45 "+ pm)


base = times
#dates = base - np.arange(180) * datetime.timedelta(days=1)
#z = np.random.poisson(size=(len(week), len(base)))



z=[[100,200],[0,1]] #class density data goes here

fig = go.Figure(data=go.Heatmap(
        z=z,
        x=week,
        y=base,
        colorscale='Viridis'))
#fig.update_xaxes(side="top")
fig.update_layout(
    title='Comet Clique',
    xaxis_nticks=100)

fig.show()

# Plotly test
import plotly.express as px
data=[[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
fig = px.imshow(data,
                labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
                x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                y=['Morning', 'Afternoon', 'Evening']
               )
fig.update_xaxes(side="top")