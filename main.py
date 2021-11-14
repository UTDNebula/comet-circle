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

# Plotly test
import plotly.express as px
data=[[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
fig = px.imshow(data,
                labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
                x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                y=['Morning', 'Afternoon', 'Evening']
               )
fig.update_xaxes(side="top")