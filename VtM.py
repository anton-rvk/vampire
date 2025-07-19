import streamlit as st
from navigation import make_sidebar
from streamlit import components
from st_bridge import bridge
import time 

import assets.clan_colors as clan_colors

def open_page(url):
                open_script= """
                    <script type="text/javascript">
                        window.open('%s', '_blank').focus();
                    </script>
                """ % (url)
                st.components.v1.html(open_script)

make_sidebar()

st.set_page_config(
    page_title="VtM Genealogy",
    page_icon="🧛",
    layout="wide"
)

st.logo("assets/logos/vtm.png", size="large")


title_format = f"""
                <h1 align='center' 
                    style='font-family: "Manufacturing Consent", system-ui; font-weight: 500; font-size: 80px; color: #DC143C; padding: 0px; margin: 0px;'>
                        {"Vampire The Masquerade"}
                </h1>
                <h1 align='center' 
                    style='font-family: "Manufacturing Consent", system-ui; font-weight: 500; font-size: 80px; color: #ffffff; padding: 0px; margin: 0px;'>
                        {"Genealogy Tree"}
                </h1>
                
            """

st.markdown(title_format, unsafe_allow_html=True)

st.write("#####")

st.markdown("<p style='font-size:18px'>Vampire: The Masquerade is a roleplaying game of personal and political horror, set in the World of Darkness. " \
"Players portray vampires, struggling for survival, supremacy and their own fading Humanity—afraid of what they are capable of, and fearful of the inhuman (and human) conspiracies that surround them. " \
"All vampires suffer from Hunger, the relentless and terrible thirst for human blood. " \
"Refusal to deal with it eventually overcomes the vampire’s mind, and drives them to terrible acts to slake it.</p>", unsafe_allow_html=True)

st.divider()

with st.expander(r"$\textsf{\Large Premise}$"):
    st.markdown("""<p style='font-size:18px'>
        In <b style='color: #DC143C;'>Vampire: The Masquerade</b>, the players assume the role of vampires, immortal beings cursed with an unquenchable thirst for blood and vulnerability to sunlight – creatures forever bound to their inner Beast (the animal urges of hunger, fear and rage). 
        It is a game of personal horror, as the characters are continually forced to walk a moral tightrope between their need to survive and the horrific means by which they ensure it. <br><br>
        Most vampires live in cities, which are run feudally by the Princes; life in a city is one of constant political manipulation and paranoia, as the Cainites vie for food, territory, and power. 
        But while they must dwell in close contact with their source of sustenance, vampires largely fear the exposure to the mortal world, and since the Inquisition the majority of these creatures have lived under the Masquerade – an enforced campaign to hide their supernatural existences from humanity. 
    </p>""", unsafe_allow_html=True)

with st.expander(r"$\textsf{\Large Vampire History}$"):

    st.markdown("""<p style='font-size:18px'>
                <b style='color: #DC143C;'>The Cainites</b> (also called Kindred or Vampires), 
                are descendants of <b style='color: #DC143C;'>Caine</b>, cursed with a thirst for <b style='color: #DC143C;'>blood</b>, vulnerability to sunlight and immortality. 
                They are forever subject to the Beast, their raging animal urges of hunger, fear and rage.<br><br>
                Cainites' history begins with a homicidal farmer: Caine of the Biblical story. 
                According to Vampiric mythology (detailed in the Book of Nod), Caine killed his brother Abel and was exiled by God to Nod, East of Eden. 
                At this time, he was also cursed by God's Angels to be vulnerable to fire, sunlight and the treachery of his descendants.<br><br>
                Caine then traveled to Enoch, the First City of the human race. 
                There he embraced its ruler and became the God-King of the city, embracing three childer as <b style='color: #DC143C;'>the Second Generation</b>. 
                These three childer in turn embraced the <b style='color: #DC143C;'>thirteen Antediluvians</b>, the founders of the <b style='color: #DC143C;'>clans</b>.<br><br>
                Some time after this, the Antediluvians rebelled against the Second Generation, after which the Great Flood covered Enoch in water. 
                The Antediluvians survived for 40 days under water, devouring their own, until the floods receded.<br><br>
                Some time after the flood, the Antediluvians build the Second City, which they rule over as Gods, until Caine returns to pass judgement on them. 
                Caine curses each of the Clans, then leaves. The Antediluvians spread across the world at this time, travelling to various places and embracing further descendants.<br>
                </p>""", unsafe_allow_html=True)

with st.expander(r"$\textsf{\Large Vampire Clans}$"):

    st.markdown(f"""<p style='font-size:18px'>
                <b style='color: #DC143C;'>Clan</b> is a term used by vampires to describe the major groups of Cainites who share common characteristics passed on by the blood. 
                There are 14 known clans, each of which was reputedly founded by an Antediluvian (with an exception of <b style='color: {clan_colors.get_clan_color("tremere")};'>Tremere</b>), a member of the mythical Third Generation.<br><br>
                From the Dark Medieval into the Modern Nights, the fourteen recognized clans are: </p>
                <ul>
                    <li style='font-size:18px'>Clan <b style='color: {clan_colors.get_clan_color("banu haqim")};'>Banu Haqim</b> (formerly Assamite) - silent masters of assassination, killing for hire and collecting blood for rituals to bring them closer to their progenitor. </li>
                    <li style='font-size:18px'>Clan <b style='color: {clan_colors.get_clan_color("brujah")};'>Brujah</b> - once philosopher-kings of an ancient civilization, but now rebels and rogues with a fearsome inclination toward frenzy.</li>
                    <li style='font-size:18px'>Clan <b style='color: {clan_colors.get_clan_color("gangrel")};'>Gangrel</b>  - bestial and untamed, often coming to resemble the animals over which they demonstrate mastery.</li>
                    <li style='font-size:18px'>Clan <b style='color: {clan_colors.get_clan_color("hecata")};'>Hecata</b> - an insular, extended family of vampires who practice the art of commanding the dead while commanding global finances.</li>
                    <li style='font-size:18px'>Clan <b style='color: {clan_colors.get_clan_color("lasombra")};'>Lasombra</b>  - proud nobles who command the very essence of darkness and shadow — to the point of worshipping it, some say.</li>
                    <li style='font-size:18px'>Clan <b style='color: {clan_colors.get_clan_color("malkavian")};'>Malkavian</b>  - a clan fractured by madness, each member irrevocably suffering under the yoke of insanity.</li>
                    <li style='font-size:18px'>Clan <b style='color: {clan_colors.get_clan_color("ministry")};'>Ministry</b>  (formerly Followers of Set) - a religious movement that evangelizes the example of a chthonic god, while seeking out the world’s secret places and protecting ancient artifacts.</li>
                    <li style='font-size:18px'>Clan <b style='color: {clan_colors.get_clan_color("nosferatu")};'>Nosferatu</b>  - hideously disfigured by the Embrace, so they keep to the sewers shadows and traffic in the secrets they collect.</li>
                    <li style='font-size:18px'>Clan <b style='color: {clan_colors.get_clan_color("ravnos")};'>Ravnos</b>  - nomads and tricksters who can force the mind to see what isn’t there, though they are slaves to the vices they indulge in.</li>
                    <li style='font-size:18px'>Clan <b style='color: {clan_colors.get_clan_color("salubri")};'>Salubri</b>  - healers and warriors, guided by a third eye and hunted down almost to extinction.</li>
                    <li style='font-size:18px'>Clan <b style='color: {clan_colors.get_clan_color("toreador")};'>Toreador</b>  - Cainites that enjoy every sensual pleasure the world has to offer, idolizing physical beauty and the adoration of their thralls.</li>
                    <li style='font-size:18px'>Clan <b style='color: {clan_colors.get_clan_color("tremere")};'>Tremere</b>  - vampiric sorcerers that wield the supernatural power of their past as a hermetic house, though they became vampires through treachery and artifice.</li>
                    <li style='font-size:18px'>Clan <b style='color: {clan_colors.get_clan_color("tzimisce")};'>Tzimisce</b>  - eldritch Old World lords who have little in common with the mortal world and can manipulate flesh and bone at a whim.</li>
                    <li style='font-size:18px'>Clan <b style='color: {clan_colors.get_clan_color("ventrue")};'>Ventrue</b>  - observe the noblesse oblige of vampire society, though their entitlement and greed encourages them to seek ever more at the expense of others.</li>
                </ul>
                <p style='font-size:18px'>
                No every vampire belongs to clan. <b style='color: {clan_colors.get_clan_color("caitiff")};'>Caitiff</b> is the most common term used by kindred to describe a vampire of an unknown clan, or of no clan at all. 
                They are typically of high generation, where Caine's blood is too diluted to pass on any consistent characteristics. 
                The clanless have no inherent clan society, support, or even characteristics; they are like orphans among the great families of vampires. 
                <b style='color: {clan_colors.get_clan_color("caitiff")};'>Caitiff</b> have no inherent clan weakness, but no inherent disciplines as well. 
                </p>""", unsafe_allow_html=True)

st.divider()

st.subheader("To explore genealogy of different clans, click on the clan founder in the graph below or select that clan in a sidebar!")

with st.container(border=True, key="graph_container", height = 800):
            html_file = open("graphs/antediluvians.html", 'r', encoding='utf-8')
            source_code = html_file.read()
            components.v1.html(source_code, width = 1500, height = 760, tab_index = 1)


data = bridge("my-bridge", default={"current_link": None})


wiki_url = "https://whitewolf.fandom.com/wiki/"


if data["current_link"]:
    match data["current_link"]: # there is a better way to do this, but too lazy
        
        case "https://whitewolf.fandom.com/wiki/Ravnos_Antediluvian":
            st.switch_page("pages/☸️ Ravnos.py")

        case "https://whitewolf.fandom.com/wiki/Lasombra_Antediluvian":
            st.switch_page("pages/✝️ Lasombra.py")

        case "https://whitewolf.fandom.com/wiki/Saulot":
            st.switch_page("pages/❤️‍🩹 Salubri.py")
                
        case "https://whitewolf.fandom.com/wiki/Toreador_Antediluvian":
            st.switch_page("pages/🌹 Toreador.py")
                
        case "https://whitewolf.fandom.com/wiki/Tzimisce_Antediluvian":
            st.switch_page("pages/🏰 Tzimisce.py")
                
        case "https://whitewolf.fandom.com/wiki/Set_(VTM)":
            st.switch_page("pages/🐍 Ministry.py")

        case "https://whitewolf.fandom.com/wiki/Ennoia":
            st.switch_page("pages/🐺 Gangrel.py")

        case "https://whitewolf.fandom.com/wiki/Cappadocius":
            st.switch_page("pages/👻 Hecata.py")
                
        case "https://whitewolf.fandom.com/wiki/Brujah_Antediluvian":
            st.switch_page("pages/💢 Brujah.py")
                
        case "https://whitewolf.fandom.com/wiki/Absimiliard":
            st.switch_page("pages/💻 Nosferatu.py")
                
        case "https://whitewolf.fandom.com/wiki/Haqim":
            st.switch_page("pages/🗡️ Banu Haqim.py")
                
        case "https://whitewolf.fandom.com/wiki/Malkavian_Antediluvian":
            st.switch_page("pages/🫨 Malkavian.py")

        case "https://whitewolf.fandom.com/wiki/Ventrue_Antediluvian":
            st.switch_page("pages/👑 Ventrue.py")
        
        case _:
           
           placeholder = st.empty()

           with placeholder:
                open_page(data["current_link"])
                time.sleep(0.5)

           placeholder.empty()
        
        
with st.expander(r"$\textsf{\Large Learn More!}$", expanded=True):
    st.markdown("""
        Interested in learning more? Here are some sources:
        <ul>
                <li><a href="https://whitewolf.fandom.com/wiki/Vampire:_The_Masquerade">Unoffical White Wolf Wiki (Lore)</a></li>
                <li><a href="https://www.schrecknet.live/">Character Creator for Vampire the Masquerade V5</a></li>
                <li><a href="https://vtm.paradoxwikis.com/VTM_Wiki">Paradox Wiki for VtM V5</a></li>
        </ul>
        These resources have been used to construct this application.
    """, unsafe_allow_html=True)

#######


st.markdown("<style>@import url('https://fonts.googleapis.com/css2?family=Manufacturing+Consent&family=Oswald:wght@200..700&display=swap');</style>", unsafe_allow_html=True)

st.markdown("""<style>
  div[data-testid="stSidebarHeader"] > img, div[data-testid="collapsedControl"] > img {
      height: 4rem;
      width: auto;
  }
  
  div[data-testid="stSidebarHeader"], div[data-testid="stSidebarHeader"] > *,
  div[data-testid="collapsedControl"], div[data-testid="collapsedControl"] > * {
      display: flex;
      align-items: center;
  }
</style>""", unsafe_allow_html=True) # makr logo larger


components.v1.html(f"""
                    <script>

                        window.parent.addEventListener('message', function handleMessage(event){{
                                if (event.data && event.data.type == "LINK"){{
                                    window.parent.stBridges.send("my-bridge", {{ current_link: event.data.payload }});
                        
                                }}
                        }})

                    </script>
                    """)

st.markdown("""<style>
            div[data-testid="stExpander"] div[role="button"] p {
                font-size: 4rem;
            }</style>""", unsafe_allow_html=True) # DOES NOT WORK, increase expander size