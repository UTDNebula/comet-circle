import streamlit as st
import data
from anytree import Node, RenderTree
from Event import Event

utd = Node("UTD")
bbs = Node("bbs", parent=utd)
acn = Node("acn", parent=bbs)



st.write("TEst")
st.write(data.search(''))
st.write(Event(0, 15, ['bis']))

