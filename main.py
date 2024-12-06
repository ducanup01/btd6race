import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
import streamlit_analytics2 as streamlit_analytics

with streamlit_analytics.track(unsafe_password="ducanup01"):
    st.set_page_config()

    home_page = st.Page(
        page="code/home.py",
        title="Home",
        icon=":material/home:",
    )
    page_1 = st.Page(
        page="code/page1.py",
        title="Race history overview",
        #icon=":material/home:"
    )
    page_2 = st.Page(
        page="code/page2.py",
        title="Race time calculator",
        #icon=":material/home:"
    )
    page_3 = st.Page(
        page="code/page3.py",
        title="Race announcements format",
        #icon=":material/home:"
        default=True,
    )
    page_4 = st.Page(
        page="code/page4.py",
        title="About",
        #icon=":material/home:"
    )
    pg = st.navigation(
        {
        "Section 1": [home_page],
        "Section 2": [page_1, page_2, page_3],
        "Section 3": [page_4],
        }
    )
    pg.run()