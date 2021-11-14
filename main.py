import streamlit as st
import data
from Event import Event
from anytree import RenderTree

data.assignTags()
st.write("TEst")
tags = list(set(data.schools + data.prefixes))
# sidebar
data.tagFilters = st.sidebar.multiselect(
    'School',
    tags
)
add_checkbox = st.sidebar.checkbox(
    'Show classes'
)

add_checkbox = st.sidebar.checkbox(
    'Show events'
)

