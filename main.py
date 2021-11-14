import streamlit as st
import data
from Event import Event
from anytree import RenderTree

data.assignTags()
st.write("TEst")
st.write(RenderTree(data.rootTag))

