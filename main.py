import streamlit as st
import data
from Event import Event
from anytree import RenderTree

data.assignTags()
st.write("TEst")
st.write(RenderTree(data.rootTag))

st.write("Test")

# sidebar 
add_multiselect = st.sidebar.multiselect(
    'School',
    ['All', 'AH', 'ATEC', 'BBS' ,'ECS', 'EPPS', 'IS'
     'NSM', 'SOM']
)

add_checkbox = st.sidebar.checkbox(
    'Show classes'
)

add_checkbox = st.sidebar.checkbox(
    'Show events'
)

