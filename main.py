import streamlit as st

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

