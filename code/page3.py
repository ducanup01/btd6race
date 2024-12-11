import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
import requests
import math
import time


# Initialize session state variables
# Initialize session state variables with default values


def remove(link):
    if "?si=" in link:
        base_link = link.split("?si=")[0]
    else:
        base_link = link
    return base_link

def format_time(ms):
    seconds, milliseconds = divmod(ms, 1000)
    milliseconds = math.floor(milliseconds/10)
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes):01}:{int(seconds):02}.{int(milliseconds):02}"

def fetch_leaderboard():
    # Fetch race data
    races = requests.get("https://data.ninjakiwi.com/btd6/races")
    latest_leaderboard_url = races.json()['body'][0]['leaderboard']
    latest_leaderboard = requests.get(latest_leaderboard_url)
    return latest_leaderboard.json()['body']

def fetch_race_name():
    races = requests.get("https://data.ninjakiwi.com/btd6/races")
    race_data = races.json()['body'][0]  # Get the first race entry
    return race_data['name']  # Retrieve the race title

def parse_text(lines):
    parsed = []
    for line in lines:
        if ":" in line:
            left, right = line.split(": ", 1)
            parsed.append((left, right))
    return parsed

st.session_state.update({
    "raceno": st.session_state.get("raceno", ""),
    "racetitle": st.session_state.get("racetitle", ""),
    "custom": st.session_state.get("custom", ""),
    "check": st.session_state.get("check", {1: False, 2: False, 3: False, 4: False, 5: False}),
})

# Define a function to initialize session state keys
def init_session_state(keys, default_value):
    for key, value in keys.items():
        for i in range(1, value + 1):
            if f"{key}{i}" not in st.session_state:
                st.session_state[f"{key}{i}"] = default_value[key]

# Keys and their respective default values
defaults = {
    "player": "",
    "ign": "",
    "time": "",
    "link": "",
    "additional": "",
    "streak": 2,
    "streak5": 2,
    "streak_player": "",
    "streak5_player": "",
    "check": False,
}

# Keys and their range limits
key_ranges = {
    "player": 5,
    "ign": 5,
    "time": 5,
    "link": 5,
    "additional": 4,
    "streak": 3,
    "streak5": 5,
    "streak_player": 3,
    "streak5_player": 5,
    "check": 5,
}

if 'leaderboard_visible' not in st.session_state:
    st.session_state['leaderboard_visible'] = False  # Track visibility state

# Initialize session states
init_session_state(key_ranges, defaults)


def flip(index):
    st.session_state.check[index] = not st.session_state.check[index]

st.title("Race announcement formatter (RAF)")
fetch_data = ""
col1, col2, col3, col4 = st.columns([9,10,45,35])
with col2:
    st.session_state.raceno = st.text_input("Race #", st.session_state.raceno)
with col4:
    st.markdown('<div style="padding-top: 28px;"></div>', unsafe_allow_html=True)
    if st.button("Fetch leaderboard"):
        st.session_state['leaderboard_visible'] = True
        players = fetch_leaderboard()
        with st.container():
            st.text("Leaderboard (Top 5):")
            
            # Display leaderboard entries in two columns
            for x in range(5):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.text(players[x]['displayName'])
                with col2:
                    st.text(format_time(players[x]['score']))

        race_name = fetch_race_name()
        st.session_state.racetitle = race_name

        for i in range(5):
            st.session_state[f'ign{i+1}'] = players[i]['displayName']
            st.session_state[f'time{i+1}'] = format_time(players[i]['score'])
        
        if st.button("Close"):
            st.session_state['leaderboard_visible'] = False
with col3:
    st.session_state.racetitle = st.text_input("Race title:", st.session_state.racetitle)
with col1:
    pass

col0, col1, col2, col3, col4 = st.columns([9,22,22,11,36], vertical_alignment="bottom")
with col0:
    st.image("image/1st.webp", clamp=True, use_container_width="auto")
with col1:
    st.session_state.player1 = st.text_input("Player (First place)", st.session_state.player1)
with col2:
    st.session_state.ign1 = st.text_input("In-game name", st.session_state.ign1)
with col3:
    st.session_state.time1 = st.text_input("Time", st.session_state.time1)
with col4:
    st.session_state.link1 = st.text_input("Link", st.session_state.link1)

col0, col1, col2, col3, col4 = st.columns([9,22,22,11,36], vertical_alignment="bottom")
with col0:
    st.image("image/2nd.webp", use_container_width="auto")
with col1:
    st.session_state.player2 = st.text_input("Player (2nd place)", st.session_state.player2)
with col2:
    st.session_state.ign2 = st.text_input("In-game name", st.session_state.ign2, key=1)
with col3:
    st.session_state.time2 = st.text_input("Time", st.session_state.time2, key=5)
with col4:
    st.session_state.link2 = st.text_input("Link", st.session_state.link2, key=9)

col0, col1, col2, col3, col4 = st.columns([9,22,22,11,36], vertical_alignment="bottom")
with col0:
    st.image("image/3rd.webp", use_container_width="auto")
with col1:
    st.session_state.player3 = st.text_input("Player (3rd place)", st.session_state.player3)
with col2:
    st.session_state.ign3 = st.text_input("In-game name", st.session_state.ign3, key=2)
with col3:
    st.session_state.time3 = st.text_input("Time", st.session_state.time3, key=6)
with col4:
    st.session_state.link3 = st.text_input("Link", st.session_state.link3, key=10)

col0, col1, col2, col3, col4 = st.columns([9,22,22,11,36], vertical_alignment="bottom")
with col0:
    st.image("image/top50.webp", use_container_width="auto")
with col1:
    st.session_state.player4 = st.text_input("Player (4th place)", st.session_state.player4)
with col2:
    st.session_state.ign4 = st.text_input("In-game name", st.session_state.ign4, key=3)
with col3:
    st.session_state.time4 = st.text_input("Time", st.session_state.time4, key=7)
with col4:
    st.session_state.link4 = st.text_input("Link", st.session_state.link4, key=11)

col0, col1, col2, col3, col4 = st.columns([9,22,22,11,36], vertical_alignment="bottom")
with col0:
    st.image("image/top50.webp", use_container_width="auto")
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

# Current Top 3 Streak
col1, col2, col3, col4 = st.columns([20,20,15,20], vertical_alignment="top")
with col1:
    st.session_state.check1 = st.checkbox("Current Top 3 Streak:", value=st.session_state.check[1], key="check_1", on_change=flip, args=(1,))

additional1 = ""
if st.session_state.check1:
    with col2:
        st.session_state.streak_player1 = st.text_input("Player 1", st.session_state.streak_player1)
    with col3:
        streak1 = st.number_input("Streak of Player 1", 2, 20, key="streak1key")
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
    st.session_state.check2 = st.checkbox("Current Top 5 Streak:", value=st.session_state.check[2], key="check_2", on_change=flip, args=(2,))

additional2 = "" 
if st.session_state.check2:      
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
    st.session_state.check3 = st.checkbox("Races without new Top 3:", value=st.session_state.check[3], key="check_3", on_change=flip, args=(3,))
    if st.session_state.check3:
        with col2:
            streak_no3 = st.number_input("", 0, 100, key="no3")
            additional3 += f"Races without new Top 3: {streak_no3}"

# Streak of no uploads by Tobi
additional4 = ""
col1, col2, col3 = st.columns([17,10,25], vertical_alignment="bottom")
with col1:
    st.session_state.check4 = st.checkbox("Streak of no uploads by Tobi:", value=st.session_state.check[4], key="check_4", on_change=flip, args=(4,))
    if st.session_state.check4:
        with col2:
            no_upload = st.number_input("", 0, 100, key="no_upload")
            additional4 += f"Streak of no uploads by Tobi: {no_upload}"

# Others
st.session_state.additional5 = ""
st.session_state.check5 = st.checkbox("Others", value=st.session_state.check[5], key="check_5", on_change=flip, args=(5,))
if st.session_state.check5:
    st.session_state.custom = st.text_area("Customize info here", st.session_state.custom, key="custom_info")
    if st.session_state.custom:
        st.session_state.additional5 += f"{st.session_state.custom}"



linea1 = f":1st_Place: - **{st.session_state.player1} \"{st.session_state.ign1}\"** ([{st.session_state.time1}]({remove(st.session_state.link1)}))"
lineb1 = f":1st_Place: - **{st.session_state.player1} \"{st.session_state.ign1}\"** ({st.session_state.time1})"

linea2 = f"\n\n :2nd_Place: - **{st.session_state.player2} \"{st.session_state.ign2}\"** ([{st.session_state.time2}]({remove(st.session_state.link2)}))"
lineb2 = f"\n :2nd_Place: - **{st.session_state.player2} \"{st.session_state.ign2}\"** ({st.session_state.time2})"

linea3 = f"\n :3rd_Place: - **{st.session_state.player3} \"{st.session_state.ign3}\"** ([{st.session_state.time3}]({remove(st.session_state.link3)}))"
lineb3 = f"\n :3rd_Place: - **{st.session_state.player3} \"{st.session_state.ign3}\"** ({st.session_state.time3})"

linea4 = f"\n 4th - **{st.session_state.player4} \"{st.session_state.ign4}\"** ([{st.session_state.time4}]({remove(st.session_state.link4)}))"
lineb4 = f"\n 4th - **{st.session_state.player4} \"{st.session_state.ign4}\"** ({st.session_state.time4})"

linea5 = f"\n 5th - **{st.session_state.player5} \"{st.session_state.ign5}\"** ([{st.session_state.time5}]({remove(st.session_state.link5)})) \n\n\n"
lineb5 = f"\n 5th - **{st.session_state.player5} \"{st.session_state.ign5}\"** ({st.session_state.time5}) \n\n\n"

race_announcements = ( 
    f"**Race #{st.session_state.raceno} \"{st.session_state.racetitle}\" Final Results:** \n" 
)

if not st.session_state.link1 or st.session_state.link1.lower() == "n/a":
    race_announcements += lineb1
else:
    race_announcements += linea1

if not st.session_state.link2 or st.session_state.link2.lower() == "n/a":
    race_announcements += lineb2
else:
    race_announcements += linea2

if not st.session_state.link3 or st.session_state.link3.lower() == "n/a":
    race_announcements += lineb3
else:
    race_announcements += linea3

if not st.session_state.link4 or st.session_state.link4.lower() == "n/a":
    race_announcements += lineb4
else:
    race_announcements += linea4

if not st.session_state.link5 or st.session_state.link5.lower() == "n/a":
    race_announcements += lineb5
else:
    race_announcements += linea5

additional_info = (
    f"**Additional Info:** \n"
    f"{additional1} \n"
    f"{additional2} \n"
    f"{additional3} \n"
    f"{additional4} \n"
    f"{st.session_state.additional5} \n"
)

race_announcements += additional_info

st.subheader("Announcement preview :mag:")
st.text(race_announcements)

st_copy_to_clipboard(race_announcements)