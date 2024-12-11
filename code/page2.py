import streamlit as st
import pandas as pd
import math

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

# Page setup
st.title("Race Time Calculator (RTC)")
col1, col2, col3 = st.columns([3.2, 0.1, 5])
with col1:
    st.write("\n")
    col1a, col1b = st.columns([1, 1])
    with col1a:
        start_round = st.number_input("Start round", min_value=0, max_value=139, value=50, step=1, key="start_round")
    with col1b:
        end_round = st.number_input("End round", min_value=1, max_value=140, step=1, value=80, key="end_round")

    col1a, col1b = st.columns([4,3])
    with col1a:
        send_time = st.number_input("Full send at:", min_value=-0.00, max_value=600.00, value=30.00, key="time_display", step=0.05)
    switch1 = st.toggle("Show segments")
    switch2 = st.toggle("Show last bloons")

with col3:
    tab1, tab2, tab3 = st.tabs(["**Standard** :balloon:", "**Alternate Bloons Rounds** :exclamation:", "**Reverse** :rewind:"])
    with tab1:
        if start_round >= end_round:
            st.error("Invalid round input", icon="❌")
        else:
            reg = pd.read_csv("image/regular.csv")
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
                        if switch2:
                            message1 += f"({last_bloon_2}) \n\n"
                        longest_round = longest_round_2                
            st.write(message1)

    with tab2:
        if start_round >= end_round:
            st.error("Invalid round input", icon="❌")
        elif end_round > 100:
            st.error("Highest round for ABR is 100", icon="⚠️")
        else:
            abr = pd.read_csv("image/abr.csv")
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
                        if switch2:
                            message1 += f"({last_bloon_2}) \n\n"
                        longest_round = longest_round_2                
            st.write(message1)

    with tab3:
        if start_round >= end_round:
            st.error("Invalid round input", icon="❌")
        else:
            reg = pd.read_csv("image/regular.csv")
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
            last_bloon = filtered_data.loc[largest_length_index, 'first']
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
                        if switch2:
                            message1 += f"({last_bloon_2}) \n\n"
                        longest_round = longest_round_2                
            st.write(message1)