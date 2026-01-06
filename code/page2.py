import streamlit as st
import pandas as pd
import math
import requests
from datetime import datetime, timedelta, timezone
import json, pathlib



# Convert seconds to minutes
def sectomin(time):
    min = int(time // 60)
    sec = time % 60
    sec = math.floor(sec * 100)
    while str(sec)[-1] not in ['0', '1', '3', '5', '6', '8']:
        sec += 1
    sec = sec/100
    sec = float(f"{sec:.2f}")
    return f"{min}:{sec:05.2f}"

def fetch_endround():
    NAME_MAP = json.loads(pathlib.Path("gamedata/name_mapping.json").read_text())
    races = requests.get("https://data.ninjakiwi.com/btd6/races")
    for i in range(8):
        if races.json()['body'][i]['totalScores'] > 0:
            ruleset_url = races.json()['body'][i]['metadata']
            leaderboard_url = races.json()['body'][i]['leaderboard']
            break
    else:
        ruleset_url = None
    if ruleset_url:
        ruleset = requests.get(ruleset_url)
        leaderboard = requests.get(leaderboard_url)
        # t1_time_current = leaderboard.json()['body'][0]['score']
        t1_time_current = None
        for j in range(0,48):
            if leaderboard.json()['body'][j]['profile'] in NAME_MAP:
                t1_time_current = leaderboard.json()['body'][j]['score']
                break

        endround = ruleset.json()['body']['endRound']
        if ruleset.json()['body']['mode'] == "AlternateBloonsRounds":
            game_mode_number = 1
        elif ruleset.json()['body']['mode'] == "Reverse":
            game_mode_number = 2
        else:
            game_mode_number = 0
    if endround and t1_time_current:
        return endround,t1_time_current,game_mode_number
    return 80,None,0

endround,t1_time_current,game_mode_number = fetch_endround()
virtual_start_round = 49 if endround > 49 else 0

# Page setup
st.title("Race Time Calculator (RTC)")
col1, col2, col3 = st.columns([3.2, 0.1, 5], vertical_alignment="top")
with col1:
    col1a, col1b = st.columns([1, 1])
    with col1a:
        start_round = st.number_input("Start round", min_value=0, max_value=139, value=virtual_start_round, step=1, key="start_round")
    with col1b:
        end_round = st.number_input("End round", min_value=1, max_value=140, step=1, value=endround, key="end_round")

    col1a, col1b = st.columns([4,3])
    # with col1a:
    #     send_time = st.number_input("Full send at:", min_value=-0.00, max_value=600.00, value=30.00, key="time_display", step=0.2000001)
    switch1 = st.toggle("Show segments")
    # switch2 = st.toggle("Show last bloons", value=True)
    with st.expander("External resources 📤", expanded=True):
        st.link_button("Topper's round info 🎩", "https://topper64.co.uk/nk/btd6/rounds/")
        st.link_button("HalfHydra's API explorer ⭐", "https://btd6apiexplorer.github.io/rounds")



with col3:

    # tab1, tab2, tab3 = st.tabs(["**Standard** :balloon:", "**Alternate Bloons Rounds** :exclamation:", "**Reverse** :rewind:"])
    game_mode = st.radio("Select Game Mode", ["**Standard** :balloon:", "**ABR** :exclamation:", "**Reverse** :rewind:"],index = game_mode_number,horizontal=True)
    st.write("\n")

    if game_mode=="**Standard** :balloon:":
    
        reg = pd.read_csv("gamedata/regular.csv")
        virtual_filtered_data = reg[(reg['round'] >= virtual_start_round+1) & (reg['round'] <= end_round)]
        virtual_length_from_send = virtual_filtered_data['length'] + (virtual_filtered_data['round'] - virtual_start_round - 1)*0.2
        virtual_largest_length_index = virtual_length_from_send.idxmax()
        virtual_largest_length = virtual_filtered_data.loc[virtual_largest_length_index, 'length']
        virtual_longest_round = virtual_filtered_data.loc[virtual_largest_length_index, 'round']
        virtual_send_time = (t1_time_current/1000) - (virtual_largest_length + (virtual_longest_round - virtual_start_round - 1) * 0.20001)


        hundredths = int(round(virtual_send_time * 100))

        if hundredths % 10 in (2, 4, 7, 9): 
            hundredths -= 1
            virtual_send_time = hundredths / 100
        with col1a:
            send_time = st.number_input("Full send at:", min_value=-0.00, max_value=600.00, value=virtual_send_time, key="time_display", step=0.2000001)
    # with tab1:
        
        if start_round >= end_round:
            st.error("Invalid round input", icon="❌")
        elif end_round > 140:
            st.error("Highest round for Regular is 140", icon="⚠️")
        else:
            filtered_data = reg[(reg['round'] >= start_round+1) & (reg['round'] <= end_round)]
            length_from_send = filtered_data['length'] + (filtered_data['round'] - start_round - 1)*0.2
            largest_length_index = length_from_send.idxmax()
            largest_length = filtered_data.loc[largest_length_index, 'length']
            longest_round = filtered_data.loc[largest_length_index, 'round']
            time = send_time + largest_length + (longest_round - start_round - 1) * 0.20001
            min = int(time // 60)
            sec = time % 60
            sec = math.floor(sec * 100)
            while str(sec)[-1] not in ['0', '1', '3', '5', '6', '8']:
                sec += 1
            sec = sec/100
            sec = float(f"{sec:.2f}")
            final_time = f"{min}:{sec:05.2f}"

            message1 = f":small_blue_diamond: You will get :blue-background[**{final_time}**] if you perfect clean :blue-background[**round {longest_round}**]. \n\n"
            last_bloon = filtered_data.loc[largest_length_index, 'last']
            message1 += f":small_blue_diamond: The last bloon you need to pop is a :blue-background[**{last_bloon}**]. \n\n"
            if switch1:
                if longest_round != end_round:
                    message1 += f":small_blue_diamond: If you only send to :blue-background[**round {longest_round}**], you need to: "
                    while longest_round < end_round:
                        start_round_2 = longest_round + 1
                        filtered_data_2 = reg[(reg['round'] >= start_round_2) & (reg['round'] <= end_round)]
                        length_from_send_2 = filtered_data_2['length'] + (filtered_data_2['round'] - start_round_2)*0.2
                        largest_length_index_2 = length_from_send_2.idxmax()
                        largest_length_2 = filtered_data_2.loc[largest_length_index_2, 'length']
                        longest_round_2 = filtered_data_2.loc[largest_length_index_2, 'round']
                        safe_time = sectomin((time - largest_length_2 - ((longest_round_2 - start_round_2)*0.20001)))
                        last_bloon_2 = filtered_data_2.loc[largest_length_index_2, 'last']
                        message1 += f"\n\n - send :blue-background[**round {longest_round_2}**] before :blue-background[**{safe_time}**] "
                        # if switch2:
                        message1 += f"({last_bloon_2}) \n\n"
                        longest_round = longest_round_2           
            st.write(message1)

    if game_mode == "**ABR** :exclamation:":
        abr = pd.read_csv("gamedata/abr.csv")
        virtual_filtered_data2 = abr[(abr['round'] >= virtual_start_round+1) & (abr['round'] <= end_round)]
        virtual_length_from_send2 = virtual_filtered_data2['length'] + (virtual_filtered_data2['round'] - virtual_start_round - 1)*0.2
        virtual_largest_length_index2 = virtual_length_from_send2.idxmax()
        virtual_largest_length2 = virtual_filtered_data2.loc[virtual_largest_length_index2, 'length']
        virtual_longest_round2 = virtual_filtered_data2.loc[virtual_largest_length_index2, 'round']
        virtual_send_time2 = (t1_time_current/1000) - (virtual_largest_length2 + (virtual_longest_round2 - virtual_start_round - 1) * 0.20001)

        hundredths2 = int(round(virtual_send_time2 * 100))

        if hundredths2 % 10 in (2, 4, 7, 9): 
            hundredths2 -= 1
            virtual_send_time2 = hundredths2 / 100
        with col1a:
            send_time = st.number_input("Full send at:", min_value=-0.00, max_value=600.00, value=virtual_send_time2, key="time_display2", step=0.2000001)
    # with tab2:
        if start_round >= end_round:
            st.error("Invalid round input", icon="❌")
        elif end_round > 140:
            st.error("Highest round for ABR is 140", icon="⚠️")
        else:
            abr = pd.read_csv("gamedata/abr.csv")
            filtered_data = abr[(abr['round'] >= start_round+1) & (abr['round'] <= end_round)]
            length_from_send = filtered_data['length'] + (filtered_data['round'] - start_round - 1)*0.2
            largest_length_index = length_from_send.idxmax()
            largest_length = filtered_data.loc[largest_length_index, 'length']
            longest_round = filtered_data.loc[largest_length_index, 'round']
            time = send_time + largest_length + (longest_round - start_round - 1) * 0.20001
            min = int(time // 60)
            sec = time % 60
            sec = math.floor(sec * 100)
            while str(sec)[-1] not in ['0', '1', '3', '5', '6', '8']:
                sec += 1
            sec = sec/100
            sec = float(f"{sec:.2f}")
            final_time = f"{min}:{sec:05.2f}"
            message1 = f":small_blue_diamond: You will get :blue-background[**{final_time}**] if you perfect clean :blue-background[**round {longest_round}**]. \n\n"
            last_bloon = filtered_data.loc[largest_length_index, 'last']
            message1 += f":small_blue_diamond: The last bloon you need to pop is a :blue-background[**{last_bloon}**]. \n\n"
            if switch1:
                if longest_round != end_round:
                    message1 += f":small_blue_diamond: If you only send to :blue-background[**round {longest_round}**], you need to: "
                    while longest_round < end_round:
                        start_round_2 = longest_round + 1
                        filtered_data_2 = abr[(abr['round'] >= start_round_2) & (abr['round'] <= end_round)]
                        length_from_send_2 = filtered_data_2['length'] + (filtered_data_2['round'] - start_round_2)*0.2
                        largest_length_index_2 = length_from_send_2.idxmax()
                        largest_length_2 = filtered_data_2.loc[largest_length_index_2, 'length']
                        longest_round_2 = filtered_data_2.loc[largest_length_index_2, 'round']
                        safe_time = sectomin((time - largest_length_2 - ((longest_round_2 - start_round_2)*0.20001)))
                        last_bloon_2 = filtered_data_2.loc[largest_length_index_2, 'last']
                        message1 += f"\n\n - send :blue-background[**round {longest_round_2}**] before :blue-background[**{safe_time}**] "
                        # if switch2:
                        message1 += f"({last_bloon_2}) \n\n"
                        longest_round = longest_round_2                
            st.write(message1)

    if game_mode=="**Reverse** :rewind:":
        rev = pd.read_csv("gamedata/reverse.csv")
        virtual_filtered_data3 = rev[(rev['round'] >= virtual_start_round+1) & (rev['round'] <= end_round)]
        virtual_length_from_send3 = virtual_filtered_data3['length'] + (virtual_filtered_data3['round'] - virtual_start_round - 1)*0.2
        virtual_largest_length_index3 = virtual_length_from_send3.idxmax()
        virtual_largest_length2 = virtual_filtered_data3.loc[virtual_largest_length_index3, 'length']
        virtual_longest_round3 = virtual_filtered_data3.loc[virtual_largest_length_index3, 'round']
        virtual_send_time3 = (t1_time_current/1000) - (virtual_largest_length2 + (virtual_longest_round3 - virtual_start_round - 1) * 0.20001)

        hundredths3 = int(round(virtual_send_time3 * 100))

        if hundredths3 % 10 in (2, 4, 7, 9): 
            hundredths3 -= 1
            virtual_send_time3 = hundredths3 / 100
        with col1a:
            send_time = st.number_input("Full send at:", min_value=-0.00, max_value=600.00, value=virtual_send_time3, key="time_display3", step=0.2000001)
    # with tab3:
        if start_round >= end_round:
            st.error("Invalid round input", icon="❌")
        elif end_round > 140:
            st.error("Highest round for Reverse is 140", icon="⚠️")
        else:
            rev = pd.read_csv("gamedata/reverse.csv")
            filtered_data = rev[(rev['round'] >= start_round+1) & (rev['round'] <= end_round)]
            length_from_send = filtered_data['length'] + (filtered_data['round'] - start_round - 1)*0.2
            largest_length_index = length_from_send.idxmax()
            largest_length = filtered_data.loc[largest_length_index, 'length']
            longest_round = filtered_data.loc[largest_length_index, 'round']
            time = send_time + largest_length + (longest_round - start_round - 1) * 0.20001
            min = int(time // 60)
            sec = time % 60
            sec = math.floor(sec * 100)
            while str(sec)[-1] not in ['0', '1', '3', '5', '6', '8']:
                sec += 1
            sec = sec/100
            sec = float(f"{sec:.2f}")
            final_time = f"{min}:{sec:05.2f}"

            message1 = f":small_blue_diamond: You will get :blue-background[**{final_time}**] if you perfect clean :blue-background[**round {longest_round}**]. \n\n"
            last_bloon = filtered_data.loc[largest_length_index, 'first']
            message1 += f":small_blue_diamond: The last bloon you need to pop is a :blue-background[**{last_bloon}**]. \n\n"
            if switch1:
                if longest_round != end_round:
                    message1 += f":small_blue_diamond: If you only send to :blue-background[**round {longest_round}**], you need to: "
                    while longest_round < end_round:
                        start_round_2 = longest_round + 1
                        filtered_data_2 = rev[(rev['round'] >= start_round_2) & (rev['round'] <= end_round)]
                        length_from_send_2 = filtered_data_2['length'] + (filtered_data_2['round'] - start_round_2)*0.2
                        largest_length_index_2 = length_from_send_2.idxmax()
                        largest_length_2 = filtered_data_2.loc[largest_length_index_2, 'length']
                        longest_round_2 = filtered_data_2.loc[largest_length_index_2, 'round']
                        safe_time = sectomin((time - largest_length_2 - ((longest_round_2 - start_round_2)*0.20001)))
                        last_bloon_2 = filtered_data_2.loc[largest_length_index_2, 'last']
                        message1 += f"\n\n - send :blue-background[**round {longest_round_2}**] before :blue-background[**{safe_time}**] "
                        # if switch2:
                        message1 += f"({last_bloon_2}) \n\n"
                        longest_round = longest_round_2                
            st.write(message1)


