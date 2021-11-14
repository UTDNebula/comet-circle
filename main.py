import streamlit as st
from streamlit.state.session_state import Value
from DateSelector import event
import data
import SessionState

# Majors

# Sidebar
data.assignMetaData()
side = st.sidebar
data.tagFilters = st.sidebar.multiselect('Filters', data.tags)
data.termFilters = st.sidebar.multiselect('Term', data.terms)

st.write(data.filterEvents(data.classes, data.termFilters, data.tagFilters))

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

# Plotly test
import plotly.express as px
data=[[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
fig = px.imshow(data,
                labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
                x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                y=['Morning', 'Afternoon', 'Evening']
               )
fig.update_xaxes(side="top")