import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
from forms.contact import contact_form

@st.dialog("Anonymous feedback form")
def show_contact_form():
    contact_form()

# Initialize session state variables
if "raceno" not in st.session_state:
    st.session_state.raceno = ""
if "racetitle" not in st.session_state:
    st.session_state.racetitle = ""
if "custom" not in st.session_state:
    st.session_state.custom = ""
    
for i in range(1,6):
    if f"player{i}" not in st.session_state:
        st.session_state[f"player{i}"] = ""

for i in range(1,6):
    if f"ign{i}" not in st.session_state:
        st.session_state[f"ign{i}"] = ""

for i in range(1,6):
    if f"time{i}" not in st.session_state:
        st.session_state[f"time{i}"] = ""

for i in range(1,6):
    if f"link{i}" not in st.session_state:
        st.session_state[f"link{i}"] = ""

for i in range(1,5):
    if f"additional{i}" not in st.session_state:
        st.session_state[f"additional{i}"] = ""

for i in range (1,4):
    if f"streak{i}" not in st.session_state:
        st.session_state[f"streak{i}"] = ""

for i in range (1,6):
    if f"streak5{i}" not in st.session_state:
        st.session_state[f"streak5{i}"] = ""

for i in range (1,4):
    if f"streak_player{i}" not in st.session_state:
        st.session_state[f"streak_player{i}"] = ""

for i in range (1,6):
    if f"streak5_player{i}" not in st.session_state:
        st.session_state[f"streak5_player{i}"] = ""

for i in range (1,6):
    if f"check{i}" not in st.session_state:
        st.session_state[f"check{i}"] = True

for i in range (1,4):
    if f"streak_player{i}" not in st.session_state:
        st.session_state[f"streak_player{i}"] = ""

for i in range (1,4):
    if f"streak{i}" not in st.session_state:
        st.session_state[f"streak{i}"] = ""

st.title("Race announcement formatter (RAF)")

col1, col2, col3, col4, col5 = st.columns([10,10,50,20,10])
with col1:
    pass
with col2:
    st.session_state.raceno = st.text_input("Race #", st.session_state.raceno)
with col3:
    st.session_state.racetitle = st.text_input("Race title:", st.session_state.racetitle)

st.write("\n")

col1, col2, col3, col4 = st.columns([25,25,13,37])
with col1:
    st.session_state.player1 = st.text_input("Player (First place)", st.session_state.player1)
with col2:
    st.session_state.ign1 = st.text_input("In-game name", st.session_state.ign1)
with col3:
    st.session_state.time1 = st.text_input("Time", st.session_state.time1)
with col4:
    st.session_state.link1 = st.text_input("Link", st.session_state.link1)

col1, col2, col3, col4 = st.columns([25,25,13,37])
with col1:
    st.session_state.player2 = st.text_input("Player (2nd place)", st.session_state.player2)
with col2:
    st.session_state.ign2 = st.text_input("In-game name", st.session_state.ign2, key=1)
with col3:
    st.session_state.time2 = st.text_input("Time", st.session_state.time2, key=5)
with col4:
    st.session_state.link2 = st.text_input("Link", st.session_state.link2, key=9)

col1, col2, col3, col4 = st.columns([25,25,13,37])
with col1:
    st.session_state.player3 = st.text_input("Player (3rd place)", st.session_state.player3)
with col2:
    st.session_state.ign3 = st.text_input("In-game name", st.session_state.ign3, key=2)
with col3:
    st.session_state.time3 = st.text_input("Time", st.session_state.time3, key=6)
with col4:
    st.session_state.link3 = st.text_input("Link", st.session_state.link3, key=10)

col1, col2, col3, col4 = st.columns([25,25,13,37])
with col1:
    st.session_state.player4 = st.text_input("Player (4th place)", st.session_state.player4)
with col2:
    st.session_state.ign4 = st.text_input("In-game name", st.session_state.ign4, key=3)
with col3:
    st.session_state.time4 = st.text_input("Time", st.session_state.time4, key=7)
with col4:
    st.session_state.link4 = st.text_input("Link", st.session_state.link4, key=11)

col1, col2, col3, col4 = st.columns([25,25,13,37])
with col1:
    st.session_state.player5 = st.text_input("Player (5th place)", st.session_state.player5)
with col2:
    st.session_state.ign5 = st.text_input("In-game name", st.session_state.ign5, key=4)
with col3:
    st.session_state.time5 = st.text_input("Time", st.session_state.time5, key=8)
with col4:
    st.session_state.link5 = st.text_input("Link", st.session_state.link5, key=12)

st.write("\n")

st.subheader("Additional info")
st.write(":warning: Warning: Progress of this part might be lost upon changing page :warning:")

# Current Top 3 Streak
col1, col2, col3, col4 = st.columns([20,20,15,20], vertical_alignment="top")
with col1:
    check1 = st.checkbox("Current Top 3 Streak:", key="check1x")

additional1 = ""
if check1:
    with col2:
        st.session_state.streak_player1 = st.text_input("Player 1", st.session_state.streak_player1)
    with col3:
        streak1 = st.number_input("Streak of Player 1", 2, 20, key="streak1x")
    additional1 += f"Current Top 3 Streak: {st.session_state.streak_player1} ({streak1})"

    if not st.session_state.streak_player1:
        additional1 = "Current Top 3 Streak: None"
    else:
        col1, col2, col3, col4 = st.columns([20,20,15, 20], vertical_alignment="top")
        with col2:
            st.session_state.streak_player2 = st.text_input("Player 2", st.session_state.streak_player2)
        with col3:
            streak2 = st.number_input("Streak of Player 2", 2, 20, key="streak2x")
        if st.session_state.streak_player2:
            additional1 += f", {st.session_state.streak_player2} ({streak2})"
            col1, col2, col3, col4 = st.columns([20,20,15, 20], vertical_alignment="top")
            with col2:
                st.session_state.streak_player3 = st.text_input("Player 3", st.session_state.streak_player3)
            with col3:
                streak3 = st.number_input("Streak of Player 3", 2, 20, key="streak3x")
            if st.session_state.streak_player3:
                additional1 += f", {st.session_state.streak_player3} ({streak3})"


# Current Top 5 Streak
col1, col2, col3, col4 = st.columns([20,20,15, 20], vertical_alignment="top")
with col1:
    check2 = st.checkbox("Current Top 5 Streak:", key="check2x")

additional2 = "" 
if check2:      
    with col2:
        st.session_state.streak5_player1 = st.text_input("Player 1", st.session_state.streak5_player1, key="top51")
    with col3:
        streak51 = st.number_input("Streak of Player 1", 2, 20, key="streak51x")
    additional2 += f"Current Top 5 Streak: {st.session_state.streak5_player1} ({streak51})"

    if not st.session_state.streak5_player1:
        additional2 = "Current Top 5 Streak: None"
    else:
        col1, col2, col3, col4 = st.columns([20,20,15, 20], vertical_alignment="top")
        with col2:
            st.session_state.streak5_player2 = st.text_input("Player 2", st.session_state.streak5_player2, key="top52")
        with col3:
            streak52 = st.number_input("Streak of Player 2", 2, 20, key="streak52x")
        if st.session_state.streak5_player2:
            additional2 += f", {st.session_state.streak5_player2} ({streak52})"
            col1, col2, col3, col4 = st.columns([20,20,15, 20], vertical_alignment="top")
            with col2:
                st.session_state.streak5_player3 = st.text_input("Player 3", st.session_state.streak5_player3, key="top53")
            with col3:
                streak53 = st.number_input("Streak of Player 3", 2, 20,  key="streak53x")
            if st.session_state.streak5_player3:
                additional2 += f", {st.session_state.streak5_player3} ({streak53})"
                col1, col2, col3, col4 = st.columns([20,20,15, 20], vertical_alignment="top")
                with col2:
                    st.session_state.streak5_player4 = st.text_input("Player 4", st.session_state.streak5_player4, key="top54x")
                with col3:
                    streak54 = st.number_input("Streak of player 4", 2, 20, key="streak54x")
                if st.session_state.streak5_player4:
                    additional2 += f", {st.session_state.streak5_player4} ({streak54})"
                    col1, col2, col3, col4 = st.columns([20,20,15, 20], vertical_alignment="top")
                    with col2:
                        st.session_state.streak5_player5 = st.text_input("Player 5", st.session_state.streak5_player5, key="top55x")
                    with col3:
                        streak55 = st.number_input("Streak of player 5", 2, 20, key="streak55x")
                        if st.session_state.streak5_player5:
                            additional2 += f", {st.session_state.streak5_player5} ({streak55})"

# Races without new top 3
additional3 = ""
col1, col2, col3 = st.columns([17,10,25], vertical_alignment="bottom")
with col1:
    check3 = st.checkbox("Races without new Top 3: ")
    if check3:
        with col2:
            streak_no3 = st.number_input("", 0, 100, key="no3")
            additional3 += f"Races without new Top 3: {streak_no3}"

# Streak of no uploads by Tobi
additional4 = ""
col1, col2, col3 = st.columns([17,10,25], vertical_alignment="bottom")
with col1:
    check4 = st.checkbox("Streak of no uploads by Tobi:")
    if check4:
        with col2:
            no_upload = st.number_input("", 0, 100, key="no_upload")
            additional4 += f"Streak of no uploads by Tobi: {no_upload}"

# Others
additional5 = ""
check5 = st.checkbox("Others")
if st.session_state.check5:
    custom = st.text_area("Customize info here")
    additional5 += f"{custom}"

race_announcements = ( 
    f"**Race #{st.session_state.raceno} \"{st.session_state.racetitle}\" Final Results:** \n" 
    f":1st_Place: - **{st.session_state.player1} \"{st.session_state.ign1}\"** ({st.session_state.time1}): {st.session_state.link1} \n"
    f":2nd_Place: - **{st.session_state.player2} \"{st.session_state.ign2}\"** ({st.session_state.time2}): {st.session_state.link2} \n"
    f":3rd_Place: - **{st.session_state.player3} \"{st.session_state.ign3}\"** ({st.session_state.time3}): {st.session_state.link3} \n"
    f"4th - **{st.session_state.player4} \"{st.session_state.ign4}\"** ({st.session_state.time4}): {st.session_state.link4} \n"
    f"5th - **{st.session_state.player5} \"{st.session_state.ign5}\"** ({st.session_state.time5}): {st.session_state.link5} \n\n\n"
    f"**Additional Info:** \n"
    f"{additional1} \n"
    f"{additional2} \n"
    f"{additional3} \n"
    f"{additional4} \n"
    f"{additional5} \n"
)

st.subheader("Announcement preview :mag:")
st.text(race_announcements)

st_copy_to_clipboard(race_announcements)


if st.button(":email: Anonymous feedback"):
        show_contact_form()