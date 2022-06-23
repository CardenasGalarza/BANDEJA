import streamlit as st
import pandas as pd


st.set_page_config(layout="wide", page_icon=":art:", page_title="Custom Theming")

blank, title_col, blank = st.columns([2,3.5,2])
title_col.title("Custom Themes :art:")
st.header("Lets change it up!")

#st.write("this is a bit of `code` in markdown")
#st.code("an st.code() block")

st.sidebar.write("Use the widgets to alter the graphs:")
chck = st.sidebar.checkbox("Use your theme colours on graphs", value=True) # get colours for graphs

# get colors from theme config file, or set the colours to altair standards
if chck:
    primary_clr = st.get_option("theme.primaryColor")
    txt_clr = st.get_option("theme.textColor")
    # I want 3 colours to graph, so this is a red that matches the theme:
    second_clr = "#d87c7c"
else:
    primary_clr = '#4c78a8'
    second_clr = '#f58517'
    txt_clr = '#e45756'


select = st.sidebar.multiselect("Lines to display on charts", ["a", "b", "c"],["a", "b", "c"]) # select one or more of lines a,b,c

slide = st.sidebar.slider("Change the domain (x-axis) on the graphs",0,20,(0,20)) # interact with x-axis

button = st.sidebar.button("New set of random numbers") #generate new set of random numbers


