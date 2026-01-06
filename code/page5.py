import streamlit as st

st.title("About Me")
st.write("I created this website for fun and as a way to learn coding :D")

st.header("Update History")

# Version 6
with st.expander('Version 6 – *"Talk is cheap. Show me the code!"*', expanded=True):
    st.markdown("""
    - **v6.2.0** Update RHA backend to adapt to any arbitrary race start and end time – 26/12/2025
    - **v6.1.0** Bugfix UI, improve accuracy for last online and PB time – 25/12/2025
    - **v6.0.0** RAL now shows top 100 races thanks to improved backend – 24/12/2025
    """)

# Version 5
with st.expander('Version 5 – *“Study the past if you would define the future.”*'):
    st.markdown("""
    - **v5.6.0** RHA added filter by map – 14/09/2025
    - **v5.5.5** RHA includes number of new T50 players since race #337 – 11/06/2025
    - **v5.5.4** RAL accommodates races starting 6 hours earlier – 30/05/2025
    - **v5.5.3** RAF posts number of new T50 racers in place of 1st-5th gap – 21/05/2025
    - **v5.5.2** RAF archives the past 6 races – 20/05/2025
    - **v5.5.1** RTC no longer breaks when current T1 is a hacker – 19/05/2025
    - **v5.5.0** RAL now displays known names (registered on first T50 since race #326) – 21/03/2025
    - **v5.4.0** Database keeps track of everyone in T50 starting from Race #326 – 14/03/2025
    - **v5.3.0** RTC updates to 140 rounds for ABR mode – 07/03/2025
    - **v5.2.0** RAF updates instantly – 05/03/2025
    - **v5.1.0** RHA updated to contain ALL races ever – 24/01/2025
    - **v5.0.0** RHA is 100% automatic and archives races from #312 – 14/01/2025
    """)

# Version 4
with st.expander('Version 4 – *“The only way to discover the limits of the possible is to go beyond them into the impossible.”*'):
    st.markdown("""
    - **v4.2.0** RAL shows players' online status – 10/01/2025
    - **v4.1.1** RAL is available 24 hours after race starts – 04/01/2025
    - **v4.1.0** RAL initiates 1 hour after race starts – 04/01/2025
    - **v4.0.0** RAL includes all tower counts – 02/01/2025
    """)

# Version 3
with st.expander('Version 3 – *“It has become appallingly obvious that our technology has exceeded our humanity.”*'):
    st.markdown("""
    - **v3.2.0** RAF now automates 90% of the work – 27/12/2024
    - **v3.1.1** Various quality of life improvements – 24/12/2024
    - **v3.1.0** Added follower tracker to RAL – 24/12/2024
    - **v3.0.0** Introduced race activity leaderboard – 20/12/2024
    """)

# Version 2
with st.expander('Version 2 – *“The best way to find yourself is to lose yourself in the service of others.”*'):
    st.markdown("""
    - **v2.1.1** YouTube links automatically remove shareID – 12/12/2024
    - **v2.1.0** Added 'fetch leaderboard' to RAF – 11/12/2024
    - **v2.0.1** Added 'show segments' and 'show last bloons' to RTC – 09/12/2024
    - **v2.0.0** Introduced race time calculator – 08/12/2024
    """)

# Version 1
with st.expander('Version 1 – *“The journey of a thousand miles begins with a single step.”*'):
    st.markdown("""
    - **v1.0.0** First launch – 06/12/2024
    """)
