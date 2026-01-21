
import streamlit as st
import pandas as pd
import requests
import json
import time

RACE_CONFIG = "gamedata/race_config.json"
NAME_MAPPING = "gamedata/name_mapping.json"

race_leaderboard_file = "race_leaderboard.csv"
df = pd.read_csv(race_leaderboard_file)

with open(RACE_CONFIG, "r", encoding="utf-8") as f:
    race_config = json.load(f)

with open(NAME_MAPPING, "r") as f:
    name_mapping = json.load(f)

current_ms = int(time.time() * 1000)


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

def last_online_counter_to_time(last_online):
    if last_online == 0:
        return f"🟢"
    elif last_online == -1:
        return f""
    elif last_online < 59:
        return f"{last_online}m"
    elif last_online < 1439:
        hours = last_online // 60
        return f"{hours}h"
    else:
        days = last_online // 1440
        return f">{days}d"
    
def fetch_player():
    races = requests.get("https://data.ninjakiwi.com/btd6/races").json()
    race_url = races['body'][0]['leaderboard']  # Get the first race entry
    race_data = requests.get(race_url).json()
    player_url = race_data['body'][1]['profile']
    player_data = requests.get(player_url).json()
    return player_data['body']

def add_space(s: str) -> str:
    result = []
    for char in s:
        if char.isupper():
            result.append(f" {char}")
        else:
            result.append(char)
    
    # Capitalize the first letter of each word
    words = "".join(result).split()  # Split the string into words
    capitalized_words = [word.capitalize() for word in words]  # Capitalize each word
    return " ".join(capitalized_words)  # Join the capitalized words back together

def add_commas(number: int) -> str:
    return "{:,}".format(number)  # Wbuilt-in function to add commas

def format_race_time(ms):
    seconds = ms // 1000
    milliseconds = (ms % 1000) // 10

    minutes = seconds // 60
    seconds = seconds % 60

    return (
        minutes.astype(int).astype(str)
        + ":"
        + seconds.astype(int).astype(str).str.zfill(2)
        + "."
        + milliseconds.astype(int).astype(str).str.zfill(2)
    )

def format_ms_to_date_string(ms: int) -> str:
    seconds = int(ms // 1000)

    days, seconds = divmod(seconds, 86400)   # 24 * 60 * 60
    hours, seconds = divmod(seconds, 3600)
    minutes, _ = divmod(seconds, 60)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")

    return " ".join(parts) if parts else "0m"

def format_ms_to_last_pb_string(ms: int) -> str:
    seconds = int(ms // 1000)

    if seconds < 60:
        return "🟢"

    days, seconds = divmod(seconds, 86400)   # 24 * 60 * 60
    hours, seconds = divmod(seconds, 3600)
    minutes, _ = divmod(seconds, 60)

    parts = []

    if days > 0:
        parts.append(f"{days}d")
        if hours >= 0:
            parts.append(f"{hours}h")
        return " ".join(parts)

    if hours > 0:
        parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        return " ".join(parts)

    # no days, no hours → minutes only
    return f"{minutes}m"



def main():
    global df, current_ms, race_config, name_mapping

    current_race_start = race_config["CURRENT_RACE_WINDOW"]["start"]
    current_race_end = race_config["CURRENT_RACE_WINDOW"]["end"]
    next_race_start = race_config["NEXT_RACE_WINDOW"]["start"]


    HOURS_AFTER_RACE_START = 4 * (60 * 60 * 1000)
    HOURS_BEFORE_RACE_END = 24 * (60 * 60 * 1000)
    HOUR_UNTIL_NEXT_RACE = 4 * (60 * 60 * 1000)

    # df = df.dropna(subset=['name', 'gamecount'])
    df['time_formatted'] = format_race_time(df['time'])

    df['time_ago'] = (
        current_ms
        - df['time_left']
        - race_config["CURRENT_RACE_WINDOW"]["start"]
    ).astype(int).apply(format_ms_to_last_pb_string)

    df['last_online_time'] = df['last_online'].apply(format_ms_to_last_pb_string)
    
    df['known_name'] = df['url'].apply(lambda x: name_mapping.get(x, df.loc[df['url'] == x, 'name'].values[0]))

    # Streamlit title
    st.title("Race Activity Leaderboard (RAL)")
    if current_race_start + HOURS_AFTER_RACE_START < current_ms < current_race_end - HOURS_BEFORE_RACE_END:
        st.markdown(f"Current race: __**\"{race_config["CURRENT_RACE_NAME"]}\"**__", unsafe_allow_html=True)
        st.markdown(f"Last update: **{format_ms_to_date_string(current_ms - df["last_update"][0])}** ago")

    elif current_race_end - HOURS_BEFORE_RACE_END <= current_ms < current_race_end:
        st.markdown(f"Current race: __**\"{race_config["CURRENT_RACE_NAME"]}\"**__", unsafe_allow_html=True)
        st.markdown(f"Last update: **{format_ms_to_date_string(current_ms - df["last_update"][0])}** ago")
        st.markdown(f"Race ends in **{format_ms_to_date_string(current_race_end - current_ms)}**")

    elif not next_race_start:
        st.markdown(f"__**\"{race_config["CURRENT_RACE_NAME"]}\"**__ has ended.", unsafe_allow_html=True)
        df['last_online_time'] = ""

    elif current_race_end <= current_ms < next_race_start - HOUR_UNTIL_NEXT_RACE:
        st.markdown(f"__**\"{race_config["CURRENT_RACE_NAME"]}\"**__ has ended.", unsafe_allow_html=True)
        st.markdown(f"Activity Leaderboard expires in __**\"{format_ms_to_date_string(next_race_start - HOUR_UNTIL_NEXT_RACE - current_ms)}\"**__")
        st.markdown(f"__**\"{race_config["NEXT_RACE_NAME"]}\"**__ will start in **{format_ms_to_date_string(next_race_start - current_ms)}**")

    elif current_race_end - HOUR_UNTIL_NEXT_RACE <= current_ms < next_race_start:
        st.subheader(f"__**\"{race_config["NEXT_RACE_NAME"]}\"**__ starting in:")
        st.markdown(f"<h2 style='text-align: center; '>{format_ms_to_date_string(next_race_start - current_ms)}</h2>", unsafe_allow_html=True)
        return

    else:
        st.subheader("Ongoing race:")
        st.markdown(f"<h2 style='text-align: center; '>{race_config["CURRENT_RACE_NAME"]}</h2>", unsafe_allow_html=True)
        st.write("\n")
        st.subheader("Activity leaderboard will be available in:")

        st.markdown(f"<h2 style='text-align: center; '>{format_ms_to_date_string(current_race_start + HOURS_AFTER_RACE_START - current_ms)}</h2>", unsafe_allow_html=True)
        return
    

    # User selects sorting column
    col1, col2, col4 = st.columns([1.2,2.2,0.9], vertical_alignment="bottom")
    with col1:
        sort_option = st.selectbox("Sort by:", 
                                ["time", "gamecount", "time_left", "follower"], 
                                format_func=lambda x: {
                                    "time": "Time",
                                    "gamecount": "Play count",
                                    "time_left": "Recent PB",
                                    "follower": "Followers gained"
                                }[x],
                                index=0)
        # Apply sorting based on user selection with special handling for "time"
        if sort_option == "time":
            df = df.sort_values(by=sort_option, ascending=True)  # Time sorted in ascending
            # df = df.head(50)
        else:
            df = df.sort_values(by=sort_option, ascending=False)  # Other columns descending
            
        #check until first known
        known_urls = set(name_mapping.keys())
        # Find position of first known user AFTER sorting
        first_known_pos = df["url"].isin(known_urls).idxmax()
        # If no known user exists at all, omit leaderboard
        if not df.loc[first_known_pos, "url"] in known_urls:
            df = df.iloc[0:0]
        else:
            df = df.loc[first_known_pos:]

        df = df.head(100)

    with col2:

        compare = st.text_input("Search/Compare players", placeholder="Search a player to view profile details...")
        if compare:
            compare_names = [name.strip() for name in compare.replace(',', ' ').split()]
            pattern = '|'.join([f'({name})' for name in compare_names])
            df = df[df[['name', 'gamecount', 'known_name', 'time']].apply(lambda row: row.astype(str).str.contains(pattern, case=False, na=False).any(), axis=1)]
    if len(df) == 1:
        with col4:            
            player_url = df.iloc[0]['url']
            player_data = requests.get(player_url).json()
            player_info = player_data['body']
            show_profile = st.button('View profile 📑', use_container_width=True)
        if show_profile:
            with st.expander(f"**{player_info['displayName']}**", expanded=True):
                st.image(player_info['bannerURL'])
                col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([2.5,1,1,1,0.9,1.1,1.15,0.95,0.95,0.8])
                with col1:
                    st.image(player_info['avatarURL'], use_container_width=True)
                if 'BlackDiamond' in player_info['_medalsRace']:
                    with col2:
                        st.image("image/1th.webp", use_container_width=True)
                        st.markdown(f"**<div style='text-align: center; font-size: 24px; margin-top: -40px; margin-left: -1px;'>{player_info['_medalsRace']['BlackDiamond']}</div>**", unsafe_allow_html=True)
                if 'RedDiamond' in player_info['_medalsRace']:
                    with col3:
                        st.image("image/2th.webp", use_container_width=True)
                        st.markdown(f"**<div style='text-align: center; font-size: 24px; margin-top: -39px; margin-left: -1px;'>{player_info['_medalsRace']['RedDiamond']}</div>**", unsafe_allow_html=True)
                if 'BlueDiamond' in player_info['_medalsRace']:
                    with col4:
                        st.image("image/3th.webp", use_container_width=True)
                        st.markdown(f"**<div style='text-align: center; font-size: 24px; margin-top: -37px; margin-left: -1px;'>{player_info['_medalsRace']['BlueDiamond']}</div>**", unsafe_allow_html=True)
                if 'GoldDiamond' in player_info['_medalsRace']:
                    with col5:
                        st.image("image/4th.webp", use_container_width=True)
                        st.markdown(f"**<div style='text-align: center; font-size: 24px; margin-top: -37px; margin-left: -1px;'>{player_info['_medalsRace']['GoldDiamond']}</div>**", unsafe_allow_html=True)
                if 'DoubleGold' in player_info['_medalsRace']:
                    with col6:
                        st.image("image/5th.webp", use_container_width=True)
                        st.markdown(f"**<div style='text-align: center; font-size: 24px; margin-top: -37px; margin-left: -1px;'>{player_info['_medalsRace']['DoubleGold']}</div>**", unsafe_allow_html=True)
                if 'GoldSilver' in player_info['_medalsRace']:
                    with col7:
                        st.image("image/6th.webp", use_container_width=True)
                        st.markdown(f"**<div style='text-align: center; font-size: 24px; margin-top: -39px; margin-left: -1px;'>{player_info['_medalsRace']['GoldSilver']}</div>**", unsafe_allow_html=True)
                if 'DoubleSilver' in player_info['_medalsRace']:
                    with col8:
                        st.image("image/7th.webp", use_container_width=True)
                        st.markdown(f"**<div style='text-align: center; font-size: 24px; margin-top: -41px; margin-left: -1px;'>{player_info['_medalsRace']['DoubleSilver']}</div>**", unsafe_allow_html=True)
                if 'Silver' in player_info['_medalsRace']:
                    with col9:
                        st.image("image/8th.webp", use_container_width=True)
                        st.markdown(f"**<div style='text-align: center; font-size: 24px; margin-top: -42px; margin-left: -1px;'>{player_info['_medalsRace']['Silver']}</div>**", unsafe_allow_html=True)
                if 'Bronze' in player_info['_medalsRace']:
                    with col10:
                        st.image("image/9th.webp", use_container_width=True)
                        st.markdown(f"**<div style='text-align: center; font-size: 24px; margin-top: -42px; margin-left: -1px;'>{player_info['_medalsRace']['Bronze']}</div>**", unsafe_allow_html=True)

                tab1, tab2, tab3, tab4, tab5 = st.tabs(['Profile Overview 📑', 'Gameplay History 🕰️', 'Towers Placed 🐵', 'Heroes Placed 👑', 'Total Bloons Popped 🎈'])

                with tab1:
                    cola, colb, colc = st.columns([1.4,1.8,2])
                    with cola:
                        if player_info.get('rank', float('inf')) < 155:
                            st.write(f"**Level:** {player_info.get('rank', 'N/A')}")
                        else:
                            st.write(f"**Veteran Level:** {player_info.get('veteranRank', 'N/A')}")
                        st.write(f"**Daily Rewards:** {add_commas(player_info.get('gameplay', {}).get('dailyRewards', 'N/A'))}")   

                    with colb:
                        st.write(f"**Followers:** {add_commas(player_info.get('followers', 'N/A'))}")
                        st.write(f"**Total Games Played:** {add_commas(player_info.get('gameplay', {}).get('gameCount', 'N/A'))}")                        
                    with colc:             
                        st.write(f"**Highest Round:** {add_commas(player_info.get('gameplay', {}).get('highestRound', 'N/A'))}")
                        st.write(f"**Most Exp Monkey:** {add_space(player_info.get('mostExperiencedMonkey', 'N/A'))}")

                with tab2:
                    st.subheader("Gameplay Stats")
                    col1, col2 = st.columns([1,1])
                    with col1:
                        st.write(f"**Cash Earned:** {add_commas(player_info.get('gameplay', {}).get('cashEarned', 'N/A'))}")
                        st.write(f"**Coop Cash Given:** {add_commas(player_info.get('gameplay', {}).get('coopCashGiven', 'N/A'))}")
                        st.write(f"**Challenges Completed:** {add_commas(player_info.get('gameplay', {}).get('challengesCompleted', 'N/A'))}")
                        st.write(f"**Daily Rewards:** {add_commas(player_info.get('gameplay', {}).get('dailyRewards', 'N/A'))}")
                        st.write(f"**Collection Chest Opened:** {add_commas(player_info.get('gameplay', {}).get('collectionChestsOpened', 'N/A'))}")
                        st.write(f"**Total Game Count:** {add_commas(player_info.get('gameplay', {}).get('gameCount', 'N/A'))}")
                        st.write(f"**Games Won:** {add_commas(player_info.get('gameplay', {}).get('gamesWon', 'N/A'))}")
                        st.write(f"**Highest Round:** {add_commas(player_info.get('gameplay', {}).get('highestRound', 'N/A'))}")
                        st.write(f"**Highest Round CHIMPS:** {add_commas(player_info.get('gameplay', {}).get('highestRoundCHIMPS', 'N/A'))}")
                        st.write(f"**Highest Round Deflation:** {add_commas(player_info.get('gameplay', {}).get('highestRoundDeflation', 'N/A'))}")


                    with col2:
                        st.write(f"**Powers Used:** {add_commas(player_info.get('gameplay', {}).get('powersUsed', 'N/A'))}")
                        st.write(f"**Total Odysseys Completed:** {add_commas(player_info.get('gameplay', {}).get('totalOdysseysCompleted', 'N/A'))}")
                        st.write(f"**Total Odyssey Stars:** {add_commas(player_info.get('gameplay', {}).get('totalOdysseyStars', 'N/A'))}")
                        st.write(f"**Total Trophies Earned:** {add_commas(player_info.get('gameplay', {}).get('totalTrophiesEarned', 'N/A'))}")
                        st.write(f"**Damage Done to Bosses:** {add_commas(player_info.get('gameplay', {}).get('damageDoneToBosses', 'N/A'))}")
                        st.write(f"**Abilities Used:** {add_commas(player_info.get('gameplay', {}).get('abilitiesUsed', 'N/A'))}")
                        st.write(f"**Insta Monkeys Used:** {add_commas(player_info.get('gameplay', {}).get('instaMonkeysUsed', 'N/A'))}")
                        st.write(f"**Monkeys Placed:** {add_commas(player_info.get('gameplay', {}).get('monkeysPlaced', 'N/A'))}")
                        st.write(f"**Insta Monkey Collection:** {add_commas(player_info.get('gameplay', {}).get('instaMonkeyCollection', 'N/A'))}")
                        st.write(f"**Monkey Teams Win:** {add_commas(player_info.get('gameplay', {}).get('monkeyTeamsWins', 'N/A'))}")

                with tab3:
                    col1, col2 = st.columns([1,1])
                    with col1:
                        st.subheader("Primary")
                        st.write(f"**Dart Monkey:** {add_commas(player_info.get('towersPlaced', {}).get('DartMonkey', 'N/A'))}")
                        st.write(f"**Boomerang Monkey:** {add_commas(player_info.get('towersPlaced', {}).get('BoomerangMonkey', 'N/A'))}")
                        st.write(f"**Bomb Shooter:** {add_commas(player_info.get('towersPlaced', {}).get('BombShooter', 'N/A'))}")
                        st.write(f"**Tack Shooter:** {add_commas(player_info.get('towersPlaced', {}).get('TackShooter', 'N/A'))}")
                        st.write(f"**Ice Monkey:** {add_commas(player_info.get('towersPlaced', {}).get('IceMonkey', 'N/A'))}")
                        st.write(f"**Glue Gunner:** {add_commas(player_info.get('towersPlaced', {}).get('GlueGunner', 'N/A'))}")
                        st.write("\n")
                        st.subheader("Magic")
                        st.write(f"**Wizard Monkey:** {add_commas(player_info.get('towersPlaced', {}).get('WizardMonkey', 'N/A'))}")
                        st.write(f"**Super Monkey:** {add_commas(player_info.get('towersPlaced', {}).get('SuperMonkey', 'N/A'))}")
                        st.write(f"**Ninja Monkey:** {add_commas(player_info.get('towersPlaced', {}).get('NinjaMonkey', 'N/A'))}")
                        st.write(f"**Alchemist:** {add_commas(player_info.get('towersPlaced', {}).get('Alchemist', 'N/A'))}")
                        st.write(f"**Druid:** {add_commas(player_info.get('towersPlaced', {}).get('Druid', 'N/A'))}")
                        st.write(f"**Mermonkey:** {add_commas(player_info.get('towersPlaced', {}).get('Mermonkey', 'N/A'))}")
                    with col2:
                        st.subheader("Military")
                        st.write(f"**Sniper Monkey:** {add_commas(player_info.get('towersPlaced', {}).get('SniperMonkey', 'N/A'))}")
                        st.write(f"**Monkey Sub:** {add_commas(player_info.get('towersPlaced', {}).get('MonkeySub', 'N/A'))}")
                        st.write(f"**Monkey Buccaneer:** {add_commas(player_info.get('towersPlaced', {}).get('MonkeyBuccaneer', 'N/A'))}")
                        st.write(f"**Monkey Ace:** {add_commas(player_info.get('towersPlaced', {}).get('MonkeyAce', 'N/A'))}")
                        st.write(f"**Heli Pilot:** {add_commas(player_info.get('towersPlaced', {}).get('HeliPilot', 'N/A'))}")
                        st.write(f"**Mortar Monkey:** {add_commas(player_info.get('towersPlaced', {}).get('MortarMonkey', 'N/A'))}")
                        st.write(f"**Dartling Gunner:** {add_commas(player_info.get('towersPlaced', {}).get('DartlingGunner', 'N/A'))}")
                        st.write("\n")
                        st.subheader("Support")
                        st.write(f"**Banana Farm:** {add_commas(player_info.get('towersPlaced', {}).get('BananaFarm', 'N/A'))}")
                        st.write(f"**Spike Factory:** {add_commas(player_info.get('towersPlaced', {}).get('SpikeFactory', 'N/A'))}")
                        st.write(f"**Monkey Village:** {add_commas(player_info.get('towersPlaced', {}).get('MonkeyVillage', 'N/A'))}")
                        st.write(f"**Engineer Monkey:** {add_commas(player_info.get('towersPlaced', {}).get('EngineerMonkey', 'N/A'))}")
                        st.write(f"**Beast Handler:** {add_commas(player_info.get('towersPlaced', {}).get('BeastHandler', 'N/A'))}")

                with tab4:
                    st.subheader("Heroes")
                    col1, col2 = st.columns([1,1])
                    with col1:
                        st.write(f"**Admiral Brickell:** {add_commas(player_info.get('heroesPlaced', {}).get('AdmiralBrickell', 'N/A'))}")
                        st.write(f"**Adora:** {add_commas(player_info.get('heroesPlaced', {}).get('Adora', 'N/A'))}")
                        st.write(f"**Benjamin:** {add_commas(player_info.get('heroesPlaced', {}).get('Benjamin', 'N/A'))}")
                        st.write(f"**Etienne:** {add_commas(player_info.get('heroesPlaced', {}).get('Etienne', 'N/A'))}")
                        st.write(f"**Geraldo:** {add_commas(player_info.get('heroesPlaced', {}).get('Geraldo', 'N/A'))}")
                        st.write(f"**Gwendolin:** {add_commas(player_info.get('heroesPlaced', {}).get('Gwendolin', 'N/A'))}")
                        st.write(f"**Obyn Greenfoot:** {add_commas(player_info.get('heroesPlaced', {}).get('ObynGreenfoot', 'N/A'))}")
                        st.write(f"**Pat Fusty:** {add_commas(player_info.get('heroesPlaced', {}).get('PatFusty', 'N/A'))}")
                    with col2:
                        st.write(f"**Psi:** {add_commas(player_info.get('heroesPlaced', {}).get('Psi', 'N/A'))}")
                        st.write(f"**Quincy:** {add_commas(player_info.get('heroesPlaced', {}).get('Quincy', 'N/A'))}")
                        st.write(f"**Sauda:** {add_commas(player_info.get('heroesPlaced', {}).get('Sauda', 'N/A'))}")
                        st.write(f"**Striker Jones:** {add_commas(player_info.get('heroesPlaced', {}).get('StrikerJones', 'N/A'))}")
                        st.write(f"**Ezili:** {add_commas(player_info.get('heroesPlaced', {}).get('Ezili', 'N/A'))}")
                        st.write(f"**Captain Churchill:** {add_commas(player_info.get('heroesPlaced', {}).get('CaptainChurchill', 'N/A'))}")
                        st.write(f"**Corvus:** {add_commas(player_info.get('heroesPlaced', {}).get('Corvus', 'N/A'))}")
                        st.write(f"**Rosalia:** {add_commas(player_info.get('heroesPlaced', {}).get('Rosalia', 'N/A'))}")


                with tab5:
                    col1, col2 = st.columns([1,1])
                    with col1:
                        st.subheader("Bloons")
                        st.write(f"**Bloons Popped:** {add_commas(player_info.get('bloonsPopped', {}).get('bloonsPopped', 'N/A'))}")
                        st.write(f"**Bloons Leaked:** {add_commas(player_info.get('bloonsPopped', {}).get('bloonsLeaked', 'N/A'))}")
                        st.write(f"**Camos Popped:** {add_commas(player_info.get('bloonsPopped', {}).get('camosPopped', 'N/A'))}")
                        st.write(f"**Regrows Popped:** {add_commas(player_info.get('bloonsPopped', {}).get('regrowsPopped', 'N/A'))}")
                        st.write(f"**Purples Popped:** {add_commas(player_info.get('bloonsPopped', {}).get('purplesPopped', 'N/A'))}")
                        st.write(f"**Leads Popped:** {add_commas(player_info.get('bloonsPopped', {}).get('leadsPopped', 'N/A'))}")
                        st.write(f"**Ceramics Popped:** {add_commas(player_info.get('bloonsPopped', {}).get('ceramicsPopped', 'N/A'))}")
                        st.write(f"**Golden Bloons Popped:** {add_commas(player_info.get('bloonsPopped', {}).get('goldenBloonsPopped', 'N/A'))}")
                        st.write(f"**Necro Bloons Reanimated:** {add_commas(player_info.get('bloonsPopped', {}).get('necroBloonsReanimated', 'N/A'))}")
                        st.write(f"**Transforming Tonic Used:** {add_commas(player_info.get('bloonsPopped', {}).get('transformingTonicsUsed', 'N/A'))}")
                    with col2:
                        st.subheader("MOABs & Bosses")
                        st.write(f"**Moabs Popped:** {add_commas(player_info.get('bloonsPopped', {}).get('moabsPopped', 'N/A'))}")
                        st.write(f"**BFBs Popped:** {add_commas(player_info.get('bloonsPopped', {}).get('bfbsPopped', 'N/A'))}")
                        st.write(f"**ZOMGs Popped:** {add_commas(player_info.get('bloonsPopped', {}).get('zomgsPopped', 'N/A'))}")
                        st.write(f"**DDTs Popped:** {add_commas(player_info.get('bloonsPopped', {}).get('ddtsPopped', 'N/A'))}")
                        st.write(f"**Bads Popped:** {add_commas(player_info.get('bloonsPopped', {}).get('badsPopped', 'N/A'))}")
                        st.write(f"**Coop Bloons Popped:** {add_commas(player_info.get('bloonsPopped', {}).get('coopBloonsPopped', 'N/A'))}")
                        st.write(f"**Bosses Popped:** {add_commas(player_info.get('bloonsPopped', {}).get('bossesPopped', 'N/A'))}")

                st.button("Close", use_container_width=True)


## starts here

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["General statistics ℹ️", "Primary count 🪃", "Military count 🪖", "Magic count 🪄", "Support count 🛖", "Hero count 👑"])
        
    with tab1:

        st.dataframe(
            df[['pfp_url', 'name', 'known_name', 'gamecount', 'follower', 'time_formatted', 'time_ago', 'last_online_time']],
            column_config={
                'pfp_url': st.column_config.ImageColumn(label="PFP", width=29),  # Profile picture
                'name': st.column_config.Column(label='Player name 🗨️', width=121, help="Player name"),
                'known_name': st.column_config.Column(label='Known as 📜', width=121, help="Originally registered name"),
                'gamecount': st.column_config.Column(label='Play count 🎮', help="Total games played"),
                'follower': st.column_config.Column(label='Followers 👥', help="Followers gained"),
                'time_formatted': st.column_config.Column(label='PB ⏱️', help="Personal best"),
                'time_ago': st.column_config.Column(label='Last PB 🏁', help="Time since last PB"),
                'last_online_time': st.column_config.Column(label='Active', help="Last active")
            },
            use_container_width=True,
            hide_index=True,
            on_select="ignore"
        )

    with tab2:
        st.dataframe(
            df[['pfp_url', 'name', 'DartMonkey', 'BoomerangMonkey', 'BombShooter', 'TackShooter', 'IceMonkey', 'GlueGunner', 'Desperado']],
            column_config={
                'pfp_url': st.column_config.ImageColumn(label="PFP", width=2),  # Profile picture
                'name': st.column_config.Column(label='Player name 🗨️', width=94),
                'DartMonkey': st.column_config.NumberColumn(label='Dart'),
                'BoomerangMonkey': st.column_config.NumberColumn(label='Boomer'),
                'BombShooter': st.column_config.NumberColumn(label='Bomb'),
                'TackShooter': st.column_config.NumberColumn(label='Tack'),
                'IceMonkey': st.column_config.NumberColumn(label='Ice'),
                'GlueGunner': st.column_config.NumberColumn(label='Glue'),
                'Desperado': st.column_config.NumberColumn(label='Desperado'),
            },
            use_container_width=True,
            hide_index=True,
        )
    
    with tab3:
        st.dataframe(
            df[['pfp_url', 'name', 'SniperMonkey', 'MonkeySub', 'MonkeyBuccaneer', 'MonkeyAce', 'HeliPilot', 'MortarMonkey', 'DartlingGunner']],
            column_config={
                'pfp_url': st.column_config.ImageColumn(label="PFP", width=15),  # Profile picture
                'name': st.column_config.Column(label='Player name 🗨️', width=107),
                'SniperMonkey': st.column_config.NumberColumn(label='Sniper'),
                'MonkeySub': st.column_config.NumberColumn(label='Sub'),
                'MonkeyBuccaneer': st.column_config.NumberColumn(label='Boat'),
                'MonkeyAce': st.column_config.NumberColumn(label='Ace'),
                'HeliPilot': st.column_config.NumberColumn(label='Heli'),
                'MortarMonkey': st.column_config.NumberColumn(label='Mortar'),
                'DartlingGunner': st.column_config.NumberColumn(label='Dartling'),
            },
            use_container_width=True,
            hide_index=True,
        )

    with tab4:
        st.dataframe(
            df[['pfp_url', 'name', 'WizardMonkey', 'SuperMonkey', 'NinjaMonkey', 'Alchemist', 'Druid', 'Mermonkey']],
            column_config={
                'pfp_url': st.column_config.ImageColumn(label="PFP", width=7),  # Profile picture
                'name': st.column_config.Column(label='Player name 🗨️', width=99),
                'WizardMonkey': st.column_config.NumberColumn(label='Wizard'),
                'SuperMonkey': st.column_config.NumberColumn(label='Super'),
                'NinjaMonkey': st.column_config.NumberColumn(label='Ninja'),
                'Alchemist': st.column_config.NumberColumn(label='Alch'),
                'Druid': st.column_config.NumberColumn(label='Druid'),
                'Mermonkey': st.column_config.NumberColumn(label='Mermonkey'),
            },
            use_container_width=True,
            hide_index=True,
        )

    with tab5:
        st.dataframe(
            df[['pfp_url', 'name', 'BananaFarm', 'SpikeFactory', 'MonkeyVillage', 'EngineerMonkey', 'BeastHandler']],
            column_config={
                'pfp_url': st.column_config.ImageColumn(label="PFP", width=-1),  # Profile picture
                'name': st.column_config.Column(label='Player name 🗨️', width=91),
                'BananaFarm': st.column_config.NumberColumn(label='Farm'),
                'SpikeFactory': st.column_config.NumberColumn(label='Spactory'),
                'MonkeyVillage': st.column_config.NumberColumn(label='Village'),
                'EngineerMonkey': st.column_config.NumberColumn(label='Engineer'),
                'BeastHandler': st.column_config.NumberColumn(label='Beast handler'),
            },
            use_container_width=True,
            hide_index=True,
        )
        
    with tab6:
        st.dataframe(
            df[['pfp_url', 'name', 'StrikerJones', 'Gwendolin', 'Benjamin', 'CaptainChurchill', 'Sauda', 'Corvus']],
            column_config={
                'pfp_url': st.column_config.ImageColumn(label="PFP", width=16),  # Profile picture
                'name': st.column_config.Column(label='Player name 🗨️', width=108),
                'StrikerJones': st.column_config.NumberColumn(label='Striker'),
                'Gwendolin': st.column_config.NumberColumn(label='Gwendolin'),
                'Benjamin': st.column_config.NumberColumn(label='Benjamin'),
                'CaptainChurchill': st.column_config.NumberColumn(label='Churchill'),
                'Sauda': st.column_config.NumberColumn(label='Sauda'),
                'Corvus': st.column_config.NumberColumn(label='Corvus'),
            },
            use_container_width=True,
            hide_index=True,
        )

## ends here
    st.write(f"Player count: {len(df[['name']])}")
    
main()
