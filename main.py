import streamlit as st
from DateSelector import event
import SessionState
#from pages import main, DateSelector


#Create button 
c1 = st.sidebar
#createState = SessionState.get(value=False)

# sidebar 
add_multiselect = st.sidebar.multiselect(
'Filters',
['All', 'AH', 'ATEC', 'BBS' ,'ECS', 'EPPS', 'IS',
    'NSM', 'SOM']
)

term_select = st.sidebar.multiselect('Term', ["Fall", "Spring"])

c1,c2 = st.sidebar.columns(2)
add_checkbox = c1.checkbox(
    'Show classes'
)

add_checkbox = c2.checkbox(
    'Show events'
)

if add_checkbox:
    'hello'

st.sidebar.write('''---''')
event(st.sidebar)
if st.sidebar.button("Create Event"):
    print()
