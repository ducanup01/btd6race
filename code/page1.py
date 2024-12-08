import streamlit as st

# Title and Subheader
st.title("Race History Overview")
st.subheader("Feature Coming Soon")

# Create tabs that span the entire width
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

# Create a single checkbox outside the tabs
button = st.checkbox("Toggle Me!")

# Tab 1 content
with tab1:
    if button:
        st.write("Result for Tab 1")

# Tab 2 content
with tab2:
    if button:
        st.write("Result for Tab 2")

# Tab 3 content
with tab3:
    if button:
        st.write("Result for Tab 3")
