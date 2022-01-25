from jinja2 import utils
import streamlit as st
from streamlit.state.session_state import Value
import data
from Event import Event
import datetime as dt
import heatmap_utils

st.set_page_config(page_title='CometCircle', page_icon='💫')

dat = data.Data()
dat.assignMetaData()

# Sidebar
side = st.sidebar
tagFilters = side.multiselect('Filters', dat.tags)
termFilters = side.multiselect('Term', dat.terms)


# View Settings
c1,c2 = side.columns(2)
show_classes = c1.checkbox('Show classes', value=True)
show_events = c2.checkbox('Show events', value=False) # disabled originally because functionality isn't really useful currently

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

# Create Event Form
if show_events:
    st.sidebar.write('''---''')
    tab = st.sidebar
    today = dt.datetime.today()

    # Event Form
    form = st.sidebar.form(key="event_form", clear_on_submit= True, )
    form.title("Create Event")
    event_name = form.text_input('Event Name', value='Event name')
    c1,c2 = form.columns(2)
    time_date = c1.date_input('Start date', today)
    time_tags = c2.multiselect('Tags', dat.tags)
    c1,c2 = form.columns(2)
    start = c1.text_input('Start time')
    finish = c2.text_input('End time')
    submit = form.form_submit_button("Submit")

    if submit:
        tab.success('Event created!')
        start = dt.datetime.strptime(start, '%H:%M')
        finish = dt.datetime.strptime(finish, '%H:%M')
        newEvent = Event(start, finish, time_tags, event_name)
        st.session_state.events[['Monday', 'Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][time_date.weekday()]].append(newEvent)


# Import from presence button (does nothing)
# st.sidebar.write('''---''')
# st.sidebar.button("Import from Presence")


#Actions
filteredClasses = dat.filterEvents(dat.classes, termFilters, tagFilters)


# Main Content (Heatmaps)

st.title("CometCircle")
classes, events = st, st

if show_classes:
    classes.plotly_chart(heatmap_utils.createHeatMapFromCourses(filteredClasses))

if show_events:
    events.plotly_chart(heatmap_utils.createHeatMapFromEvents(st.session_state.events))
