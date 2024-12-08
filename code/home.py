import streamlit as st
from forms.contact import contact_form

@st.dialog("Anonymous feedback form")
def show_contact_form():
    contact_form()

st.title("Home")
st.write("Last update on December 8th")



st.write("")
col1, col2 = st.columns([1,2], vertical_alignment="center")
with col1:
    st.write("Send me a secret message :point_right:")     
with col2:
    if st.button(":email: Anonymous feedback"): show_contact_form()