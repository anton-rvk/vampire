import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit_javascript import st_javascript
import numpy as np
import pandas as pd
import re
import os

def get_current_page(body, footer):
    with footer: 
        url = st_javascript("await fetch('').then(r => window.parent.location.href)")

    with body:
        if url != 0:
            current_page = url.rsplit('/',1)[1]
        else: 
            current_pagsse = ""

        return current_page

def sort_clans(current_page):

        clans = []

        for file in os.listdir("./pages"):
            clans.append(file[:-3])    


        #clans =  ["Brujah", "Ventrue"]

        short_clans = []
        for clan in clans: 
            emoji_pattern = re.compile("["
                    u"\U0001F600-\U0001F64F"  # emoticons
                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                    u"\U00002500-\U00002BEF"  # chinese char
                    u"\U00002702-\U000027B0"
                    u"\U000024C2-\U0001F251"
                    u"\U0001f926-\U0001f937"
                    u"\U00010000-\U0010ffff"
                    u"\u2640-\u2642" 
                    u"\u2600-\u2B55"
                    u"\u200d"
                    u"\u23cf"
                    u"\u23e9"
                    u"\u231a"
                    u"\ufe0f"  # dingbats
                    u"\u3030"
                "]+", re.UNICODE)
            short_clans.append(emoji_pattern.sub(r'', clan)[1:]) # no emoji
            
        #print(np.argsort(short_clans))

        #print(current_page)
        sorted_indices = list(np.argsort(short_clans))
        if current_page in short_clans:
            #short_clans.remove(current_page)
            sorted_indices.remove(short_clans.index(current_page))

        clans = [clans[i] for i in sorted_indices]

        return clans


def add_description(clan_description, clan_color):
    descriptions = pd.read_csv("data/clan_descriptions/clan_descriptions.csv")
    
    markdown_description = ""
    markdown_header = ""
    for row in descriptions.iterrows():
        if row[1]["Clan"] == clan_description:
            markdown_header = row[1]["Clan"]
            markdown_description = row[1]["Description"]

    #st.header(markdown_header)

    st.markdown(f"<h3 style='color: {clan_color}; font-weight: bold;'>{markdown_header}</h3>", unsafe_allow_html=True)
    st.markdown(markdown_description)

    #st.image("assets/diablerist.png")

def add_legend():

    st.divider()

    st.header("Legend:")

    col1, col2 = st.columns(2, gap=None, vertical_alignment= "center")

    with col1: 
        st.image("assets/normal.png")
    
    with col2:
        st.write("&nbsp; ->&nbsp;  Normal")

    col1, col2 = st.columns(2, gap=None, vertical_alignment= "center")

    with col1: 
        st.image("assets/diablerist.png")
    
    with col2:
        url = "https://whitewolf.fandom.com/wiki/Diablerie_(VTM)"
        st.write("&nbsp; ->&nbsp;  [Diablerist](%s)" % url)

    col1, col2 = st.columns(2, gap=None, vertical_alignment= "center")
    
    with col1: 
        st.image("assets/unknown_generation.png")
    
    with col2:
        st.write("&nbsp; -> &nbsp;Unknown", unsafe_allow_html=True)

    
    st.divider()
    
    st.markdown("""
                <p>How to use?</p>
            <ul>
                <li>Click on the node to open the wiki page</li>
                <li>Filter by nodes (vampires) or edges (relationships)</li>
                <li>Drag and rearrange nodes around</li>
            </ul>""", unsafe_allow_html=True)

def make_sidebar(clan_description="", clan_color = "#5d641a"):
    with st.sidebar: 

        url = st_javascript("await fetch('').then(r => window.parent.location.href)")
        
        st.sidebar.page_link("VtM.py", label="-> Main Page")

        
        if url != 0:
            current_page = url.rsplit('/',1)[1]
        else: 
            current_page = ""

        clans = sort_clans(current_page)

        if current_page == "":
            current_page = "None"

        current_page = re.sub("_", " ", current_page)

        page = st.sidebar.selectbox("Select Clan:", clans, index = None, placeholder = f"{current_page}")

        if page != None:

            st.switch_page(f"pages/{page}.py")

        add_description(clan_description, clan_color=clan_color)

        if current_page != "None":
            add_legend()


