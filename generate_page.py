

import streamlit as st 
from streamlit import components

from st_bridge import bridge
from navigation import make_sidebar

import assets.clan_colors as clan_colors


def page_config(clan_description, 
                logo_path,
                clan_color):
    
    st.markdown("<style>@import url('https://fonts.googleapis.com/css2?family=Manufacturing+Consent&family=Oswald:wght@200..700&display=swap');</style>", unsafe_allow_html=True)

    make_sidebar(clan_description=clan_description, clan_color= clan_color)

    st.logo(logo_path, size="large")

    st.set_page_config(
            page_title="Clan: " + clan_description,
    )

    st.set_page_config(layout="wide")


def page_elements(clan_description,
                  graph_path,
                  default_iframe_link,
                  iframe_html_id,
                  clan_color):

    body = st.container()

    footer = st.container()

    with body: 
        with st.container(key="app_title"):

            title_format = f"""
                <h1 align='center' 
                    style='font-family: "Manufacturing Consent", system-ui; font-weight: 500; font-size: 80px; color: {clan_color}; padding: 0px; margin: 0px;'>
                        {clan_description}
                </h1>
            """

            st.markdown(title_format, unsafe_allow_html=True)


        with st.container(border=True, key="graph_container", height = 800):
            html_file = open(graph_path, 'r', encoding='utf-8')
            source_code = html_file.read()
            components.v1.html(source_code, width = 1500, height = 760, tab_index = 1)

        with open("assets/clan_page.css") as f:
            css = f.read()

        data = bridge("my-bridge", default={"current_link": default_iframe_link})

    with footer:

        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

        components.v1.html(f"""
                    <script>

                        window.parent.addEventListener('message', function handleMessage(event){{
                                if (event.data && event.data.type == "LINK"){{
                                    console.log("Event was received")
                                    window.parent.stBridges.send("my-bridge", {{ current_link: event.data.payload }});
                                    target = window.parent.document.getElementById('{iframe_html_id}')
                                    if (target) {{
                                        target.scrollIntoView({{behavior: 'smooth'}});
                                    }}
                                }}
                        }})

                    </script>
                    """)
        
    with body:

        if data:
            
            st.subheader("Link: " + data["current_link"], divider="grey")
            components.v1.iframe(data["current_link"], height = 1000, scrolling = True)


def generate_page(clan_description : str, 
                  logo_path, 
                  graph_path,
                  default_iframe_link,
                  iframe_html_id):
    
    clan_color=clan_colors.get_clan_color(clan_description.lower())

    page_config(
        clan_description=clan_description,
        logo_path=logo_path,
        clan_color=clan_color
    )

    page_elements(
        clan_description=clan_description,
        graph_path=graph_path,
        default_iframe_link=default_iframe_link,
        iframe_html_id=iframe_html_id,
        clan_color=clan_color
    )