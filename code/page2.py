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

# Page setup
st.title("Race Time Calculator (RTC)")



tab1, tab2, tab3 = st.tabs(["**Standard** :balloon:", "**Alternate Bloons Rounds** :exclamation:", "**Reverse** :rewind:"])
with tab1:
    # Load data
    reg = pd.read_csv("image/regular.csv")
    col1, col2, col3 = st.columns([3.2, 0.1, 5])
    with col1:
        col1a, col1b = st.columns([1, 1])
                   
        with col1b:
            end_round = st.number_input("End round", min_value=1, max_value=140, step=1, value=80, key="end_round")

        with col1a:
            start_round = st.number_input("Start round", min_value=0, max_value=139, value=50, step=1, key="start_round")

        col1a, col1b = st.columns([1, 1], vertical_alignment="top")
        with col1a:
            send_time = st.number_input("Full send at", min_value=-0.00, max_value=600.00, value=30.00, key="time_display", step=0.05)
        switch1 = st.toggle("Show segments")
        switch2 = st.toggle("Show last bloons")
        if start_round > end_round:
            st.error("Invalid round inputs")

        # Data filtering and calculation       
    
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

            message1 = f":small_blue_diamond: You will get :blue-background[**{final_time}**] if you perfect clean :blue-background[**round {longest_round}**]. \n\n"
            last_bloon = filtered_data.loc[largest_length_index, 'last']
            message1 += f":small_blue_diamond: The last bloon you need to pop is a :blue-background[**{last_bloon}**]. \n\n"
        else:
            message1 = ""
            
    with col3:
        if not switch1:
            st.write(message1)
        elif start_round == end_round:
            st.write(message1)
        elif start_round > end_round:
            pass
        elif longest_round == end_round:

            st.write(message1)
        elif longest_round < end_round:
            
            start_round_2 = longest_round + 1
            
            filtered_data_2 = reg[(reg['round'] >= start_round_2) & (reg['round'] <= end_round)]

            length_from_send_2 = filtered_data_2['length'] + (filtered_data_2['round'] - start_round_2)*0.2

            largest_length_index_2 = length_from_send_2.idxmax()

            largest_length_2 = filtered_data_2.loc[largest_length_index_2, 'length']

            longest_round_2 = filtered_data_2.loc[largest_length_index_2, 'round']

            safe_time = sectomin((time - largest_length_2 - ((longest_round_2 - start_round_2)*0.20001)))
            
            last_bloon_2 = filtered_data_2.loc[largest_length_index_2, 'last']

            message1 += f":small_blue_diamond: If you only send to :blue-background[**round {longest_round}**], you need to: \n\n - send :blue-background[**round {longest_round_2}**] before :blue-background[**{safe_time}**] "
            if switch2:
                message1 += f"({last_bloon_2}) \n\n"
            
            if longest_round_2 == end_round:

                st.write(message1)
            
            else:
                start_round_3 = longest_round_2 + 1
            
                filtered_data_3 = reg[(reg['round'] >= start_round_3) & (reg['round'] <= end_round)]

                length_from_send_3 = filtered_data_3['length'] + (filtered_data_3['round'] - start_round_3)*0.2

                largest_length_index_3 = length_from_send_3.idxmax()

                largest_length_3 = filtered_data_3.loc[largest_length_index_3, 'length']

                longest_round_3 = filtered_data_3.loc[largest_length_index_3, 'round']

                safe_time_2 = sectomin((time - largest_length_3 - ((longest_round_3 - start_round_3)*0.20001)))
                
                last_bloon_3 = filtered_data_3.loc[largest_length_index_3, 'last']

                message1 += f"\n\n - send :blue-background[**round {longest_round_3}**] before :blue-background[**{safe_time_2}**] "

                if switch2:

                    message1 += f"({last_bloon_3}) \n\n"

                if longest_round_3 == end_round:
                    st.write(message1)
                else:
                    start_round_4 = longest_round_3 + 1
            
                    filtered_data_4 = reg[(reg['round'] >= start_round_4) & (reg['round'] <= end_round)]

                    length_from_send_4 = filtered_data_4['length'] + (filtered_data_4['round'] - start_round_4)*0.2

                    largest_length_index_4 = length_from_send_4.idxmax()

                    largest_length_4 = filtered_data_4.loc[largest_length_index_4, 'length']

                    longest_round_4 = filtered_data_4.loc[largest_length_index_4, 'round']

                    safe_time_3 = sectomin((time - largest_length_4 - ((longest_round_4 - start_round_4)*0.20001)))
                    
                    last_bloon_4 = filtered_data_4.loc[largest_length_index_4, 'last']

                    message1 += f"\n\n - send :blue-background[**round {longest_round_4}**] before :blue-background[**{safe_time_3}**] "

                    if switch2:
                        message1 += f"({last_bloon_4}) \n\n"    

                    if longest_round_4 == end_round:
                        st.write(message1)
                    else:
                        start_round_5 = longest_round_4 + 1
                
                        filtered_data_5 = reg[(reg['round'] >= start_round_5) & (reg['round'] <= end_round)]

                        length_from_send_5 = filtered_data_5['length'] + (filtered_data_5['round'] - start_round_5)*0.2

                        largest_length_index_5 = length_from_send_5.idxmax()

                        largest_length_5 = filtered_data_5.loc[largest_length_index_5, 'length']

                        longest_round_5 = filtered_data_5.loc[largest_length_index_5, 'round']

                        safe_time_4 = sectomin((time - largest_length_5 - ((longest_round_5 - start_round_5)*0.20001)))
                        
                        last_bloon_5 = filtered_data_5.loc[largest_length_index_5, 'last']

                        message1 += f" \n\n - send :blue-background[**round {longest_round_5}**] before :blue-background[**{safe_time_4}**] "

                        if switch2:
                            message1 += f"({last_bloon_5}) \n\n"

                        if longest_round_5 == end_round:
                            st.write(message1)
                        else:
                            start_round_6 = longest_round_5 + 1
                
                            filtered_data_6 = reg[(reg['round'] >= start_round_6) & (reg['round'] <= end_round)]

                            length_from_send_6 = filtered_data_6['length'] + (filtered_data_6['round'] - start_round_6)*0.2

                            largest_length_index_6 = length_from_send_6.idxmax()

                            largest_length_6 = filtered_data_6.loc[largest_length_index_6, 'length']

                            longest_round_6 = filtered_data_6.loc[largest_length_index_6, 'round']

                            safe_time_5 = sectomin((time - largest_length_6 - ((longest_round_6 - start_round_6)*0.20001)))
                            
                            last_bloon_6 = filtered_data_6.loc[largest_length_index_6, 'last']

                            message1 += f" \n\n - send :blue-background[**round {longest_round_6}**] before :blue-background[**{safe_time_5}**] "

                            if switch2:
                                message1 += f"({last_bloon_6}) \n\n"

                            if longest_round_6 == end_round:
                                st.write(message1)
                            else:
                                start_round_7 = longest_round_6 + 1
                
                                filtered_data_7 = reg[(reg['round'] >= start_round_7) & (reg['round'] <= end_round)]

                                length_from_send_7 = filtered_data_7['length'] + (filtered_data_7['round'] - start_round_7)*0.2

                                largest_length_index_7 = length_from_send_7.idxmax()

                                largest_length_7 = filtered_data_7.loc[largest_length_index_7, 'length']

                                longest_round_7 = filtered_data_7.loc[largest_length_index_7, 'round']

                                safe_time_6 = sectomin((time - largest_length_7 - ((longest_round_7 - start_round_7)*0.20001)))
                                
                                last_bloon_7 = filtered_data_7.loc[largest_length_index_7, 'last']

                                message1 += f" \n\n - send :blue-background[**round {longest_round_7}**] before :blue-background[**{safe_time_6}**] "

                                if switch2:
                                    message1 += f"({last_bloon_7}) \n\n"

                                if longest_round_7 == end_round:
                                    st.write(message1)
                                else:
                                    start_round_8 = longest_round_7 + 1
                
                                    filtered_data_8 = reg[(reg['round'] >= start_round_8) & (reg['round'] <= end_round)]

                                    length_from_send_8 = filtered_data_8['length'] + (filtered_data_8['round'] - start_round_8)*0.2

                                    largest_length_index_8 = length_from_send_8.idxmax()

                                    largest_length_8 = filtered_data_8.loc[largest_length_index_8, 'length']

                                    longest_round_8 = filtered_data_8.loc[largest_length_index_8, 'round']

                                    safe_time_7 = sectomin((time - largest_length_8 - ((longest_round_8 - start_round_8)*0.20001)))
                                    
                                    last_bloon_8 = filtered_data_8.loc[largest_length_index_8, 'last']

                                    message1 += f" \n\n - send :blue-background[**round {longest_round_8}**] before :blue-background[**{safe_time_7}**] "

                                    if switch2:
                                        message1 += f"({last_bloon_8}) \n\n"

                                    st.write(message1)

        
with tab2:
    # Load data
    abr = pd.read_csv("image/abr.csv")
    col1, col2, col3 = st.columns([3.2, 0.1, 5])
    with col1:
        col1a, col1b = st.columns([1, 1])
                   
        with col1b:
            end_round = st.number_input("End round", min_value=1, max_value=140, step=1, value=80, key="end_round_abr")

        with col1a:
            start_round = st.number_input("Start round", min_value=0, max_value=139, value=50, step=1, key="start_round_abr")

        col1a, col1b = st.columns([1, 1], vertical_alignment="top")
        with col1a:
            send_time = st.number_input("Full send at", min_value=-0.00, max_value=600.00, value=30.00, key="time_display_abr", step=0.05)
        switch1 = st.toggle("Show segments", key="abr")
        switch2 = st.toggle("Show last bloons", key="toggle_abr")
        if start_round > end_round:
            st.error("Invalid round inputs")

        # Data filtering and calculation       
    
        filtered_data = abr[(abr['round'] >= start_round) & (abr['round'] <= end_round)]

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

            message1 = f":small_blue_diamond: You will get :blue-background[**{final_time}**] if you perfect clean :blue-background[**round {longest_round}**]. \n\n"
            last_bloon = filtered_data.loc[largest_length_index, 'last']
            message1 += f":small_blue_diamond: The last bloon you need to pop is a :blue-background[**{last_bloon}**]. \n\n"
        else:
            message1 = ""
            
    with col3:
        if not switch1:
            st.write(message1)
        elif start_round == end_round:
            st.write(message1)
        elif start_round > end_round:
            pass
        elif longest_round == end_round:

            st.write(message1)
        elif longest_round < end_round:
            
            start_round_2 = longest_round + 1
            
            filtered_data_2 = abr[(abr['round'] >= start_round_2) & (abr['round'] <= end_round)]

            length_from_send_2 = filtered_data_2['length'] + (filtered_data_2['round'] - start_round_2)*0.2

            largest_length_index_2 = length_from_send_2.idxmax()

            largest_length_2 = filtered_data_2.loc[largest_length_index_2, 'length']

            longest_round_2 = filtered_data_2.loc[largest_length_index_2, 'round']

            safe_time = sectomin((time - largest_length_2 - ((longest_round_2 - start_round_2)*0.20001)))
            
            last_bloon_2 = filtered_data_2.loc[largest_length_index_2, 'last']

            message1 += f":small_blue_diamond: If you only send to :blue-background[**round {longest_round}**], you need to: \n\n - send :blue-background[**round {longest_round_2}**] before :blue-background[**{safe_time}**] "
            if switch2:
                message1 += f"({last_bloon_2}) \n\n"
            
            if longest_round_2 == end_round:

                st.write(message1)
            
            else:
                start_round_3 = longest_round_2 + 1
            
                filtered_data_3 = abr[(abr['round'] >= start_round_3) & (abr['round'] <= end_round)]

                length_from_send_3 = filtered_data_3['length'] + (filtered_data_3['round'] - start_round_3)*0.2

                largest_length_index_3 = length_from_send_3.idxmax()

                largest_length_3 = filtered_data_3.loc[largest_length_index_3, 'length']

                longest_round_3 = filtered_data_3.loc[largest_length_index_3, 'round']

                safe_time_2 = sectomin((time - largest_length_3 - ((longest_round_3 - start_round_3)*0.20001)))
                
                last_bloon_3 = filtered_data_3.loc[largest_length_index_3, 'last']

                message1 += f"\n\n - send :blue-background[**round {longest_round_3}**] before :blue-background[**{safe_time_2}**] "

                if switch2:

                    message1 += f"({last_bloon_3}) \n\n"

                if longest_round_3 == end_round:
                    st.write(message1)
                else:
                    start_round_4 = longest_round_3 + 1
            
                    filtered_data_4 = abr[(abr['round'] >= start_round_4) & (abr['round'] <= end_round)]

                    length_from_send_4 = filtered_data_4['length'] + (filtered_data_4['round'] - start_round_4)*0.2

                    largest_length_index_4 = length_from_send_4.idxmax()

                    largest_length_4 = filtered_data_4.loc[largest_length_index_4, 'length']

                    longest_round_4 = filtered_data_4.loc[largest_length_index_4, 'round']

                    safe_time_3 = sectomin((time - largest_length_4 - ((longest_round_4 - start_round_4)*0.20001)))
                    
                    last_bloon_4 = filtered_data_4.loc[largest_length_index_4, 'last']

                    message1 += f"\n\n - send :blue-background[**round {longest_round_4}**] before :blue-background[**{safe_time_3}**] "

                    if switch2:
                        message1 += f"({last_bloon_4}) \n\n"    

                    if longest_round_4 == end_round:
                        st.write(message1)
                    else:
                        start_round_5 = longest_round_4 + 1
                
                        filtered_data_5 = abr[(abr['round'] >= start_round_5) & (abr['round'] <= end_round)]

                        length_from_send_5 = filtered_data_5['length'] + (filtered_data_5['round'] - start_round_5)*0.2

                        largest_length_index_5 = length_from_send_5.idxmax()

                        largest_length_5 = filtered_data_5.loc[largest_length_index_5, 'length']

                        longest_round_5 = filtered_data_5.loc[largest_length_index_5, 'round']

                        safe_time_4 = sectomin((time - largest_length_5 - ((longest_round_5 - start_round_5)*0.20001)))
                        
                        last_bloon_5 = filtered_data_5.loc[largest_length_index_5, 'last']

                        message1 += f" \n\n - send :blue-background[**round {longest_round_5}**] before :blue-background[**{safe_time_4}**] "

                        if switch2:
                            message1 += f"({last_bloon_5}) \n\n"

                        if longest_round_5 == end_round:
                            st.write(message1)
                        else:
                            start_round_6 = longest_round_5 + 1
                
                            filtered_data_6 = abr[(abr['round'] >= start_round_6) & (abr['round'] <= end_round)]

                            length_from_send_6 = filtered_data_6['length'] + (filtered_data_6['round'] - start_round_6)*0.2

                            largest_length_index_6 = length_from_send_6.idxmax()

                            largest_length_6 = filtered_data_6.loc[largest_length_index_6, 'length']

                            longest_round_6 = filtered_data_6.loc[largest_length_index_6, 'round']

                            safe_time_5 = sectomin((time - largest_length_6 - ((longest_round_6 - start_round_6)*0.20001)))
                            
                            last_bloon_6 = filtered_data_6.loc[largest_length_index_6, 'last']

                            message1 += f" \n\n - send :blue-background[**round {longest_round_6}**] before :blue-background[**{safe_time_5}**] "

                            if switch2:
                                message1 += f"({last_bloon_6}) \n\n"

                            if longest_round_6 == end_round:
                                st.write(message1)
                            else:
                                start_round_7 = longest_round_6 + 1
                
                                filtered_data_7 = abr[(abr['round'] >= start_round_7) & (abr['round'] <= end_round)]

                                length_from_send_7 = filtered_data_7['length'] + (filtered_data_7['round'] - start_round_7)*0.2

                                largest_length_index_7 = length_from_send_7.idxmax()

                                largest_length_7 = filtered_data_7.loc[largest_length_index_7, 'length']

                                longest_round_7 = filtered_data_7.loc[largest_length_index_7, 'round']

                                safe_time_6 = sectomin((time - largest_length_7 - ((longest_round_7 - start_round_7)*0.20001)))
                                
                                last_bloon_7 = filtered_data_7.loc[largest_length_index_7, 'last']

                                message1 += f" \n\n - send :blue-background[**round {longest_round_7}**] before :blue-background[**{safe_time_6}**] "

                                if switch2:
                                    message1 += f"({last_bloon_7}) \n\n"

                                if longest_round_7 == end_round:
                                    st.write(message1)
                                else:
                                    start_round_8 = longest_round_7 + 1
                
                                    filtered_data_8 = abr[(abr['round'] >= start_round_8) & (abr['round'] <= end_round)]

                                    length_from_send_8 = filtered_data_8['length'] + (filtered_data_8['round'] - start_round_8)*0.2

                                    largest_length_index_8 = length_from_send_8.idxmax()

                                    largest_length_8 = filtered_data_8.loc[largest_length_index_8, 'length']

                                    longest_round_8 = filtered_data_8.loc[largest_length_index_8, 'round']

                                    safe_time_7 = sectomin((time - largest_length_8 - ((longest_round_8 - start_round_8)*0.20001)))
                                    
                                    last_bloon_8 = filtered_data_8.loc[largest_length_index_8, 'last']

                                    message1 += f" \n\n - send :blue-background[**round {longest_round_8}**] before :blue-background[**{safe_time_7}**] "

                                    if switch2:
                                        message1 += f"({last_bloon_8}) \n\n"

                                    st.write(message1)

with tab3:
    # Load data
    reg = pd.read_csv("image/regular.csv")
    col1, col2, col3 = st.columns([3.2, 0.1, 5])
    with col1:
        col1a, col1b = st.columns([1, 1])
                   
        with col1b:
            end_round = st.number_input("End round", min_value=1, max_value=140, step=1, value=80, key="end_round_rev")

        with col1a:
            start_round = st.number_input("Start round", min_value=0, max_value=139, value=50, step=1, key="start_round_rev")

        col1a, col1b = st.columns([1, 1], vertical_alignment="top")
        with col1a:
            send_time = st.number_input("Full send at", min_value=-0.00, max_value=600.00, value=30.00, key="time_display_rev", step=0.05)
        switch1 = st.toggle("Show segments", key="rev")
        switch2 = st.toggle("Show last bloons", key="toggle_rev")
        if start_round > end_round:
            st.error("Invalid round inputs")

        # Data filtering and calculation       
    
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

            message1 = f":small_blue_diamond: You will get :blue-background[**{final_time}**] if you perfect clean :blue-background[**round {longest_round}**]. \n\n"
            last_bloon = filtered_data.loc[largest_length_index, 'first']
            message1 += f":small_blue_diamond: The last bloon you need to pop is a :blue-background[**{last_bloon}**]. \n\n"
        else:
            message1 = ""
            
    with col3:
        if not switch1:
            st.write(message1)
        elif start_round == end_round:
            st.write(message1)
        elif start_round > end_round:
            pass
        elif longest_round == end_round:

            st.write(message1)
        elif longest_round < end_round:
            
            start_round_2 = longest_round + 1
            
            filtered_data_2 = reg[(reg['round'] >= start_round_2) & (reg['round'] <= end_round)]

            length_from_send_2 = filtered_data_2['length'] + (filtered_data_2['round'] - start_round_2)*0.2

            largest_length_index_2 = length_from_send_2.idxmax()

            largest_length_2 = filtered_data_2.loc[largest_length_index_2, 'length']

            longest_round_2 = filtered_data_2.loc[largest_length_index_2, 'round']

            safe_time = sectomin((time - largest_length_2 - ((longest_round_2 - start_round_2)*0.20001)))
            
            last_bloon_2 = filtered_data_2.loc[largest_length_index_2, 'first']

            message1 += f":small_blue_diamond: If you only send to :blue-background[**round {longest_round}**], you need to: \n\n - send :blue-background[**round {longest_round_2}**] before :blue-background[**{safe_time}**] "
            if switch2:
                message1 += f"({last_bloon_2}) \n\n"
            
            if longest_round_2 == end_round:

                st.write(message1)
            
            else:
                start_round_3 = longest_round_2 + 1
            
                filtered_data_3 = reg[(reg['round'] >= start_round_3) & (reg['round'] <= end_round)]

                length_from_send_3 = filtered_data_3['length'] + (filtered_data_3['round'] - start_round_3)*0.2

                largest_length_index_3 = length_from_send_3.idxmax()

                largest_length_3 = filtered_data_3.loc[largest_length_index_3, 'length']

                longest_round_3 = filtered_data_3.loc[largest_length_index_3, 'round']

                safe_time_2 = sectomin((time - largest_length_3 - ((longest_round_3 - start_round_3)*0.20001)))
                
                last_bloon_3 = filtered_data_3.loc[largest_length_index_3, 'first']

                message1 += f"\n\n - send :blue-background[**round {longest_round_3}**] before :blue-background[**{safe_time_2}**] "

                if switch2:

                    message1 += f"({last_bloon_3}) \n\n"

                if longest_round_3 == end_round:
                    st.write(message1)
                else:
                    start_round_4 = longest_round_3 + 1
            
                    filtered_data_4 = reg[(reg['round'] >= start_round_4) & (reg['round'] <= end_round)]

                    length_from_send_4 = filtered_data_4['length'] + (filtered_data_4['round'] - start_round_4)*0.2

                    largest_length_index_4 = length_from_send_4.idxmax()

                    largest_length_4 = filtered_data_4.loc[largest_length_index_4, 'length']

                    longest_round_4 = filtered_data_4.loc[largest_length_index_4, 'round']

                    safe_time_3 = sectomin((time - largest_length_4 - ((longest_round_4 - start_round_4)*0.20001)))
                    
                    last_bloon_4 = filtered_data_4.loc[largest_length_index_4, 'first']

                    message1 += f"\n\n - send :blue-background[**round {longest_round_4}**] before :blue-background[**{safe_time_3}**] "

                    if switch2:
                        message1 += f"({last_bloon_4}) \n\n"    

                    if longest_round_4 == end_round:
                        st.write(message1)
                    else:
                        start_round_5 = longest_round_4 + 1
                
                        filtered_data_5 = reg[(reg['round'] >= start_round_5) & (reg['round'] <= end_round)]

                        length_from_send_5 = filtered_data_5['length'] + (filtered_data_5['round'] - start_round_5)*0.2

                        largest_length_index_5 = length_from_send_5.idxmax()

                        largest_length_5 = filtered_data_5.loc[largest_length_index_5, 'length']

                        longest_round_5 = filtered_data_5.loc[largest_length_index_5, 'round']

                        safe_time_4 = sectomin((time - largest_length_5 - ((longest_round_5 - start_round_5)*0.20001)))
                        
                        last_bloon_5 = filtered_data_5.loc[largest_length_index_5, 'first']

                        message1 += f" \n\n - send :blue-background[**round {longest_round_5}**] before :blue-background[**{safe_time_4}**] "

                        if switch2:
                            message1 += f"({last_bloon_5}) \n\n"

                        if longest_round_5 == end_round:
                            st.write(message1)
                        else:
                            start_round_6 = longest_round_5 + 1
                
                            filtered_data_6 = reg[(reg['round'] >= start_round_6) & (reg['round'] <= end_round)]

                            length_from_send_6 = filtered_data_6['length'] + (filtered_data_6['round'] - start_round_6)*0.2

                            largest_length_index_6 = length_from_send_6.idxmax()

                            largest_length_6 = filtered_data_6.loc[largest_length_index_6, 'length']

                            longest_round_6 = filtered_data_6.loc[largest_length_index_6, 'round']

                            safe_time_5 = sectomin((time - largest_length_6 - ((longest_round_6 - start_round_6)*0.20001)))
                            
                            last_bloon_6 = filtered_data_6.loc[largest_length_index_6, 'first']

                            message1 += f" \n\n - send :blue-background[**round {longest_round_6}**] before :blue-background[**{safe_time_5}**] "

                            if switch2:
                                message1 += f"({last_bloon_6}) \n\n"

                            if longest_round_6 == end_round:
                                st.write(message1)
                            else:
                                start_round_7 = longest_round_6 + 1
                
                                filtered_data_7 = reg[(reg['round'] >= start_round_7) & (reg['round'] <= end_round)]

                                length_from_send_7 = filtered_data_7['length'] + (filtered_data_7['round'] - start_round_7)*0.2

                                largest_length_index_7 = length_from_send_7.idxmax()

                                largest_length_7 = filtered_data_7.loc[largest_length_index_7, 'length']

                                longest_round_7 = filtered_data_7.loc[largest_length_index_7, 'round']

                                safe_time_6 = sectomin((time - largest_length_7 - ((longest_round_7 - start_round_7)*0.20001)))
                                
                                last_bloon_7 = filtered_data_7.loc[largest_length_index_7, 'first']

                                message1 += f" \n\n - send :blue-background[**round {longest_round_7}**] before :blue-background[**{safe_time_6}**] "

                                if switch2:
                                    message1 += f"({last_bloon_7}) \n\n"

                                if longest_round_7 == end_round:
                                    st.write(message1)
                                else:
                                    start_round_8 = longest_round_7 + 1
                
                                    filtered_data_8 = reg[(reg['round'] >= start_round_8) & (reg['round'] <= end_round)]

                                    length_from_send_8 = filtered_data_8['length'] + (filtered_data_8['round'] - start_round_8)*0.2

                                    largest_length_index_8 = length_from_send_8.idxmax()

                                    largest_length_8 = filtered_data_8.loc[largest_length_index_8, 'length']

                                    longest_round_8 = filtered_data_8.loc[largest_length_index_8, 'round']

                                    safe_time_7 = sectomin((time - largest_length_8 - ((longest_round_8 - start_round_8)*0.20001)))
                                    
                                    last_bloon_8 = filtered_data_8.loc[largest_length_index_8, 'first']

                                    message1 += f" \n\n - send :blue-background[**round {longest_round_8}**] before :blue-background[**{safe_time_7}**] "

                                    if switch2:
                                        message1 += f"({last_bloon_8}) \n\n"

                                    st.write(message1)      
        
