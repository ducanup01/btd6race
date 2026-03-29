import streamlit as st
import requests
import math
import pandas as pd
import json
from copy_button import st_copy_to_clipboard

def milliseconds_to_race_number(milliseconds):
    # Define constants
    ms_in_a_second = 1000
    ms_in_a_minute = ms_in_a_second * 60
    ms_in_an_hour = ms_in_a_minute * 60
    ms_in_a_day = ms_in_an_hour * 24
    ms_in_a_week = ms_in_a_day * 7
    
    # Calculate weeks, days, and hours
    milliseconds += 172800000
    weeks = milliseconds // ms_in_a_week
    weeks -= 2554
    
    return weeks

st.markdown(
    """
    <style>
    [data-testid="stElementToolbar"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Race Announcement Formatter (RAF)")


df = pd.read_csv("race_history.csv")
reversed_df = df[::-1]

last_race5, last_race4, last_race3, last_race2, last_race1 = df['racetitle'].tail(5)

# st.subheader("Main info")
fetch_data = ""
col1x, col2x, col3x, col4x = st.columns([9,10,50,35],vertical_alignment="top")

# with col3x:
#     # racetitle = st.selectbox("Race title:", racetitle, disabled=True)
#     racetitle = st.selectbox("Race title:", (last_race1, last_race2, last_race3, last_race4))

# if racetitle == last_race1:                    
#     latest_race  = reversed_df.iloc[0]
#     reversed_df  = df[::-1]        

# elif racetitle == last_race2:                   # 2nd newest
#     latest_race  = reversed_df.iloc[1]
#     reversed_df  = df[::-2]

# elif racetitle == last_race3:                   # 3rd newest
#     latest_race  = reversed_df.iloc[2]
#     reversed_df  = df[::-3]

# elif racetitle == last_race4:                   # 4th newest
#     latest_race  = reversed_df.iloc[3]
#     reversed_df  = df[::-4]

with col3x:
    racetitle = st.selectbox(
        "Race title:",
        (last_race1, last_race2, last_race3, last_race4, last_race5)
    )

# how many bottom rows to drop
last_races = [last_race1, last_race2, last_race3, last_race4, last_race5]
idx        = last_races.index(racetitle)      # 0‥3
n_drop     = idx                              # 0..3

# trim & reverse
trimmed_df  = df.iloc[:-n_drop or None]               # drop bottom n_drop rows
reversed_df = trimmed_df.iloc[::-1]           # newest→oldest after trim

# single-row latest race
latest_race = reversed_df.iloc[0]   


raceno = milliseconds_to_race_number(int(latest_race['raceStart']))
racenosecret = 351 # to be updated when tobi uploads

with col2x:
    raceno = st.text_input("Race #", raceno, disabled=True)

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

def format_time_gap(ms):
    # Calculate time components
    seconds, milliseconds = divmod(ms, 1000)
    milliseconds = math.floor(milliseconds / 10)
    minutes, seconds = divmod(seconds, 60)
    
    # Adjust milliseconds if they end with 2, 4, 7, or 9
    if milliseconds % 10 in {2, 4, 7, 9}:
        milliseconds -= 1

    # Format the time string
    if minutes > 0:
        return f"{int(minutes):01}:{int(seconds):02}.{int(milliseconds):02}"
    else:
        return f"{int(seconds):01}.{int(milliseconds):02}"


def is_there_new_t3(url):
    player_data = requests.get(url).json()
    medals = player_data['body']['_medalsRace']

    if 'BlueDiamond' in medals and medals['BlueDiamond'] == 1 and not ('RedDiamond' in medals or 'BlackDiamond' in medals):
        return True
    if 'RedDiamond' in medals and medals['RedDiamond'] == 1 and not ('BlueDiamond' in medals or 'BlackDiamond' in medals):
        return True
    if 'BlackDiamond' in medals and medals['BlackDiamond'] == 1 and not ('BlueDiamond' in medals or 'RedDiamond' in medals):
        return True
    
    return False  


def parse_text(lines):
    parsed = []
    for line in lines:
        if ":" in line:
            left, right = line.split(": ", 1)
            parsed.append((left, right))
    return parsed

player1_streak=player2_streak=player3_streak=player4_streak=player5_streak=player1_streak5=player2_streak5=player3_streak5=player4_streak5=player5_streak5=0

#latest_leaderboard_url, latest_race_name, i = fetch_leaderboard()

# Define a dictionary mapping IGN to Player roles
with open("gamedata/name_mapping.json", "r") as f:
    name_mapping = json.load(f)




#this is for identifying new t3
if latest_race['new_t3'] == 1:
    is_player_1_streaking = is_there_new_t3(latest_race['url1'])
    is_player_2_streaking = is_there_new_t3(latest_race['url2'])
    is_player_3_streaking = is_there_new_t3(latest_race['url3'])
else:
    is_player_1_streaking = is_player_2_streaking = is_player_3_streaking = False

#this is the start of  loading block
# preamble

new_top3_racer = ""

# racetitle = latest_race['racetitle']



top_1_time = latest_race['time1']
top_5_time = latest_race['time5']
top_50_time = latest_race['top50_time']

ign1 = latest_race['name1']
time1 = format_time(latest_race['time1'])
player1 = name_mapping.get(latest_race['url1'], ign1)

ign2 = latest_race['name2']
time2 = format_time(latest_race['time2'])
player2 = name_mapping.get(latest_race['url2'], ign2)

ign3 = latest_race['name3']
time3 = format_time(latest_race['time3'])
player3 = name_mapping.get(latest_race['url3'], ign3)

ign4 = latest_race['name4']
time4 = format_time(latest_race['time4'])
player4 = name_mapping.get(latest_race['url4'], ign4)

ign5 = latest_race['name5']
time5 = format_time(latest_race['time5'])
player5 = name_mapping.get(latest_race['url5'], ign5)

# streak without new t3
last_top3 = 0
for value in reversed_df['new_t3']:
    if value == 1:
        break
    if value == 0:
        last_top3 += 1

#count t3 streak here
if last_top3 == 0:
    if is_player_1_streaking:
        new_top3_racer += f"{name_mapping.get(latest_race['url1'], player1)}"
        if is_player_2_streaking:
            new_top3_racer += f", {name_mapping.get(latest_race['url2'], player2)}"
        if is_player_3_streaking:
            new_top3_racer += f", {name_mapping.get(latest_race['url3'], player3)}"
    elif is_player_2_streaking:
        new_top3_racer += f"{name_mapping.get(latest_race['url2'], player2)}"
        if is_player_3_streaking:
            new_top3_racer += f", {name_mapping.get(latest_race['url3'], player3)}"
    elif is_player_3_streaking:
        new_top3_racer += f"{name_mapping.get(latest_race['url3'], player3)}"
    

player_profiles = [
    latest_race['url1'],
    latest_race['url2'],
    latest_race['url3'],
    latest_race['url4'],
    latest_race['url5']
]

streaks_top3 = {profile: 0 for profile in player_profiles[:3]}
streaks_top5 = {profile: 0 for profile in player_profiles}

def calculate_recent_streaks(profiles, columns):
    streaks = {profile: 0 for profile in profiles}

    for profile in profiles:
        current_streak = 0  # Track the current streak

        # Iterate through the DataFrame
        for _, row in reversed_df.iterrows():
            if profile in [row[col] for col in columns]:
                current_streak += 1
            else:
                break  # Stop at the first non-matching row

        # Only count streaks greater than 1
        streaks[profile] = current_streak if current_streak > 1 else 0

    return streaks

# Calculate recent streaks for top 3 and top 5
streaks_top3 = calculate_recent_streaks(player_profiles[:3], ['url1', 'url2', 'url3'])
streaks_top5 = calculate_recent_streaks(player_profiles, ['url1', 'url2', 'url3', 'url4', 'url5'])
top3streak = {k: v for k, v in streaks_top3.items() if v > 0}
top5streak = {k: v for k, v in streaks_top5.items() if v > 0}
top3_url_list = list(top3streak.keys())
top3_streak_list = list(top3streak.values())
top5_url_list = list(top5streak.keys())
top5_streak_list = list(top5streak.values())

if len(top3_streak_list) > 0 and top3_streak_list[0]:
    streak_player1 = name_mapping.get(top3_url_list[0], player1)
    player1_streak = top3_streak_list[0]

    if len(top3_streak_list) > 1 and top3_streak_list[1]:
        streak_player2 = name_mapping.get(top3_url_list[1], player2)
        player2_streak = top3_streak_list[1]

        if len(top3_streak_list) > 2 and top3_streak_list[2]:
            streak_player3 = name_mapping.get(top3_url_list[2], player3)
            player3_streak = top3_streak_list[2]
        else:
            streak_player3 = None
    else:
        streak_player2 = streak_player3 = None
else:
    streak_player1 = streak_player2 = streak_player3 = None


if len(top5_streak_list) > 0 and top5_streak_list[0]:
    streak5_player1 = name_mapping.get(top5_url_list[0], player1)
    player1_streak5 = top5_streak_list[0]

    if len(top5_streak_list) > 1 and top5_streak_list[1]:
        streak5_player2 = name_mapping.get(top5_url_list[1], player2)
        player2_streak5 = top5_streak_list[1]   

        if len(top5_streak_list) > 2 and top5_streak_list[2]:
            streak5_player3 = name_mapping.get(top5_url_list[2], player3)
            player3_streak5 = top5_streak_list[2]                       

            if len(top5_streak_list) > 3 and top5_streak_list[3]:
                streak5_player4 = name_mapping.get(top5_url_list[3], player4)
                player4_streak5 = top5_streak_list[3]

                if len(top5_streak_list) > 4 and top5_streak_list[4]:
                    streak5_player5 = name_mapping.get(top5_url_list[4], player5)
                    player5_streak5 = top5_streak_list[4]
                else:
                    streak5_player5 = None
            else:
                streak5_player4 = streak5_player5 = None
        else:
            streak5_player3 = streak5_player4 = streak5_player5 = None
    else:
        streak5_player2 = streak5_player3 = streak5_player4 = streak5_player5 = None
else:
    streak5_player1 = streak5_player2 = streak5_player3 = streak5_player4 = streak5_player5 = None

#this is the end of loading block


    
col0, col1, col2, col3, col4 = st.columns([9,24,24,12,35], vertical_alignment="bottom")
with col0:
    st.image("image/1th.webp", clamp=True, width='stretch')
with col1:
    player1 = st.text_input("Player (First place)", player1, disabled=True)
with col2:
    ign1 = st.text_input("In-game name", ign1, disabled=True)
with col3:
    time1 = st.text_input("Time", time1, disabled=True)
with col4:
    link1 = st.text_input("Link")

col0, col1, col2, col3, col4 = st.columns([9,24,24,12,35], vertical_alignment="bottom")
with col0:
    st.image("image/2th.webp", width='stretch')
with col1:
    player2 = st.text_input("Player (2nd place)", player2, disabled=True)
with col2:
    ign2 = st.text_input("In-game name", ign2, key=1, disabled=True)
with col3:
    time2 = st.text_input("Time", time2, key=5, disabled=True)
with col4:
    link2 = st.text_input("Link", key=9)

col0, col1, col2, col3, col4 = st.columns([9,24,24,12,35], vertical_alignment="bottom")
with col0:
    st.image("image/3th.webp", width='stretch')
with col1:
    player3 = st.text_input("Player (3rd place)", player3, disabled=True)
with col2:
    ign3 = st.text_input("In-game name", ign3, key=2, disabled=True)
with col3:
    time3 = st.text_input("Time", time3, key=6, disabled=True)
with col4:
    link3 = st.text_input("Link", key=10)

col0, col1, col2, col3, col4 = st.columns([9,24,24,12,35], vertical_alignment="bottom")
with col0:
    st.image("image/4th.webp", width='stretch')
with col1:
    player4 = st.text_input("Player (4th place)", player4, disabled=True)
with col2:
    ign4 = st.text_input("In-game name", ign4, key=3, disabled=True)
with col3:
    time4 = st.text_input("Time", time4, key=7, disabled=True)
with col4:
    link4 = st.text_input("Link", key=11)

col0, col1, col2, col3, col4 = st.columns([9,24,24,12,35], vertical_alignment="bottom")
with col0:
    st.image("image/4th.webp", width='stretch')
with col1:
    player5 = st.text_input("Player (5th place)", player5, disabled=True)
with col2:
    ign5 = st.text_input("In-game name", ign5, key=4, disabled=True)
with col3:
    time5 = st.text_input("Time", time5, key=8, disabled=True)
with col4:
    link5 = st.text_input("Link", key=12)


additional1 = ""

# Assign values without displaying input fields
streak_player1 = streak_player1
streak1 = player1_streak

if streak_player1:
    additional1 += f"Current Top 3 Streak: {streak_player1} ({streak1})"
    
    streak_player2 = streak_player2
    streak2 = player2_streak
    
    if streak_player2:
        additional1 += f", {streak_player2} ({streak2})"
        
        streak_player3 = streak_player3
        streak3 = player3_streak
        
        if streak_player3:
            additional1 += f", {streak_player3} ({streak3})"
else:
    additional1 = "Current Top 3 Streak: None"


additional2 = ""

# Assign values without displaying input fields
streak5_player1 = streak5_player1
streak51 = player1_streak5

if streak5_player1:
    additional2 += f"Current Top 5 Streak: {streak5_player1} ({streak51})"
    
    streak5_player2 = streak5_player2
    streak52 = player2_streak5
    
    if streak5_player2:
        additional2 += f", {streak5_player2} ({streak52})"
        
        streak5_player3 = streak5_player3
        streak53 = player3_streak5
        
        if streak5_player3:
            additional2 += f", {streak5_player3} ({streak53})"
            
            streak5_player4 = streak5_player4
            streak54 = player4_streak5
            
            if streak5_player4:
                additional2 += f", {streak5_player4} ({streak54})"
                
                streak5_player5 = streak5_player5
                streak55 = player5_streak5
                
                if streak5_player5:
                    additional2 += f", {streak5_player5} ({streak55})"
else:
    additional2 = "Current Top 5 Streak: None"

# Additional stats calculations without user inputs
additional3 = ""
streak_no3 = last_top3

if streak_no3 > 0:
    additional3 += f"Races without new Top 3: {streak_no3}"
else:
    if ',' in new_top3_racer:
        additional3 += f"**New Top 3 racers: {new_top3_racer}**"
    else:
        additional3 += f"**New Top 3 racer: {new_top3_racer}**"

additional4 = ""
no_upload = int(raceno) - int(racenosecret)
additional4 += f"Streak of no uploads by Tobi: {no_upload}"

additional6 = ""
top15gap = format_time_gap(top_5_time - top_1_time)
new_t50 = reversed_df.iloc[0]['new_t50']
if new_t50 <= 1:
    additional6 += f"New Top 50 racer: {new_t50}"
else:
    additional6 += f"New Top 50 racers: {new_t50}"

additional7 = ""
top150gap = format_time_gap(top_50_time - top_1_time)
additional7 += f"Gap between 1st - 50th: {top150gap}"

additional8 = ""




# Additional customizable info
additional5 = ""

# Constructing race announcements without input fields
race_announcements = (
    f"**Race #{raceno} \"{racetitle}\" Final Results:**\n"
)

line_format = lambda pos, player, ign, time, link: (
    f"{pos} - **{player} \"{ign}\"** ([{time}](<{remove(link)}>))\n" if link else
    f"{pos} - **{player} \"{ign}\"** ({time})\n"
)

race_announcements += line_format(":1st_Place:", player1, ign1, time1, link1)
race_announcements += line_format(":2nd_Place:", player2, ign2, time2, link2)
race_announcements += line_format(":3rd_Place:", player3, ign3, time3, link3)
race_announcements += line_format(":top50:", player4, ign4, time4, link4)
race_announcements += line_format(":top50:", player5, ign5, time5, link5) + "\n\n"

# Sorting additional info
default_order = ["Top 3 Streak", "Top 5 Streak", "Last Top 3", "empty line", "New T50", "1st - 50th Gap", "Last Tobi upload"]

to_be_sorted = {
    "Top 3 Streak": f"{additional1}\n",
    "Top 5 Streak": f"{additional2}\n",
    "Last Top 3": f"{additional3}\n",
    "Last Tobi upload": f"{additional4}\n",
    "New T50": f"{additional6}\n",
    "1st - 50th Gap": f"{additional7}s\n",
    "Others": f"{additional5}\n",
    "empty line": f"{additional8}\n"
}

sorted_info = "".join(to_be_sorted[info] for info in default_order)
additional_info = f"**Additional Info:**\n{sorted_info}\n"
race_announcements += additional_info

colleft, colright = st.columns([8,1])

with col4x:
    st_copy_to_clipboard(race_announcements)
