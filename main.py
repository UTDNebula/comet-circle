import streamlit as st
import data
from anytree import Node, RenderTree

utd = Node("UTD")
bbs = Node("bbs", parent=utd)
acn = Node("acn", parent=bbs)



st.write("TEst")
st.write(data.search('course_prefix', 'bis'))
