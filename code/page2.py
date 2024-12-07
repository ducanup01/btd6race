import streamlit as st

st.title("Race Time Calculator")
st.subheader("Feature Coming Soon")

# Initialize session state for 'streak1' if it doesn't exist
if 'streak1' not in st.session_state:
    st.session_state['streak1'] = 0

for i in range(1,4):
    if f"streak{i}" not in st.session_state:
        st.session_state[f"streak{1}"] = 0

# Define a callback function to handle changes
def update_streak():
    st.session_state['streak1'] = st.session_state['streak123']

def update(index):
    st.session_state[f"streak{index}"] = st.session_state[f"streak{index}key"]

col1, col2 = st.columns([1, 4])
with col1:
    st.number_input(
        "streak",
        0,
        10,
        key="streak123",
        value=st.session_state['streak1'],
        on_change=update_streak
    )

# Display the updated streak value
st.session_state['streak1']
