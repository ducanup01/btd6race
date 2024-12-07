import streamlit as st
import pandas as pd
import math

# Convert seconds to minutes
def sectomin(time):
    min = int(time // 60)
    sec = time % 60
    sec = math.floor(sec * 100)
    
    # Loop until the last digit of sec is one of [0, 1, 3, 5, 6, 8]
    while str(sec)[-1] not in ['0', '1', '3', '5', '6', '8']:
        sec += 1
    sec = sec/100
    sec = float(f"{sec:.2f}")
    return f"{min}:{sec:05.2f}"

# Initialize session state
if "time" not in st.session_state:
    st.session_state.time = 30.00

# Load data
reg = pd.read_csv("image/regular.csv")

# Page setup
st.title("Race Time Calculator")



tab1, tab2, tab3 = st.tabs(["**Standard** :balloon:", "**Alternate Bloons Rounds** :exclamation:", "**Reverse** :rewind:"])
with tab1:
    col1, col2, col3 = st.columns([3.2, 0.1, 5])
    with col1:
        col1a, col1b = st.columns([1, 1])
                   
        with col1b:
            end_round = st.number_input("End round", min_value=1, max_value=100, step=1, value=80, key="end_round")

        with col1a:
            start_round = st.number_input("Start round", min_value=0, max_value=99, value=50, step=1, key="start_round")
                    
        col1a, col1b = st.columns([1, 1])
        with col1a:
            send_time = st.number_input("Full send at", min_value=-0.00, max_value=600.00, value=30.00, key="time_display", step=0.05)
            switch1 = st.checkbox("Pit stop")
        with col1b:
            if switch1:
                dock = st.number_input("but need to pause at", min_value=start_round, max_value=end_round, value = 50, step=1)

        # Data filtering and calculation
        if start_round is not None and end_round is not None:
            
            if end_round <= start_round:
                st.error("Invalid round inputs")
            else:
                filtered_data = reg[(reg['round'] >= start_round) & (reg['round'] <= end_round)]

                if not filtered_data.empty:
                    length_from_send = filtered_data['length'] + (filtered_data['round'] - start_round - 1)*0.2

                    largest_length_index = length_from_send.idxmax()

                    largest_length = filtered_data.loc[largest_length_index, 'length']

                    longest_round = filtered_data.loc[largest_length_index, 'round']
                    
                    # Calculate final time
                    time = send_time + largest_length + (longest_round - start_round - 1) * 0.20001

                    min = int(time // 60)
                    sec = time % 60
                    sec = math.floor(sec * 100)
                    
                    # Loop until the last digit of sec is one of [0, 1, 3, 5, 6, 8]
                    while str(sec)[-1] not in ['0', '1', '3', '5', '6', '8']:
                        sec += 1
                    sec = sec/100
                    sec = float(f"{sec:.2f}")
                    final_time = f"{min}:{sec:05.2f}"

                    message1 = f"- You will get :blue-background[**{final_time}**] if you perfectly clean :blue-background[**round {longest_round}**]. \n\n"
                    last_bloon = filtered_data.loc[largest_length_index, 'last']
                    message1 += f"- The last bloon you need to pop is a :blue-background[**{last_bloon}**]. \n\n"
                    
                    
                    if switch1:

                        if dock < end_round:

                            start_round_2 = dock + 1
                            
                            filtered_data_2 = reg[(reg['round'] >= start_round_2) & (reg['round'] <= end_round)]

                            length_from_send_2 = filtered_data_2['length'] + (filtered_data_2['round'] - start_round_2)*0.2

                            largest_length_index_2 = length_from_send_2.idxmax()

                            largest_length_2 = filtered_data_2.loc[largest_length_index_2, 'length']

                            longest_round_2 = filtered_data_2.loc[largest_length_index_2, 'round']

                            safe_time = sectomin((time - largest_length_2 - ((longest_round_2 - start_round_2)*0.20001)))
                            
                            last_bloon_2 = filtered_data_2.loc[largest_length_index_2, 'last']

                            message1 += f"- If you pause at round {dock}, you have to send :blue-background[**round {end_round}**] before :blue-background[**{safe_time}**] before losing more time. \n"

                            message1 += f"- The second longest round is :blue-background[**round {longest_round_2}**], ending with a :blue-background[**{last_bloon_2}**]."
                else:
                    st.write("No data found in the specified range of rounds.")

            
    with col3:
        st.write(message1)
        
with tab2:
    st.write("Under construction")

with tab3:
    st.write("Under construction")       
        
