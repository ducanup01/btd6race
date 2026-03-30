import streamlit as st
import pandas as pd
import streamlit as st
from datetime import datetime, timezone
import pandas as pd
import math
import pytz
import json
import re

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
st.title("Race History Archive (RHA)")

# def convert_ms_to_date(start_ms):
#     """
#     To convert NK's start date from ms to date

#     Parameters
#     ----------
#     start_ms: non-negative integer (usually a few billions)

#     Returns
#     ----------
#     return value: string
#         - For example: November 1st 2019
#     """
#     # Convert the start timestamp from milliseconds to seconds
#     start_seconds = start_ms / 1000

#     # Convert to a timezone-aware datetime object in UTC
#     date = datetime.fromtimestamp(start_seconds, tz=timezone.utc)

#     # Subtract 1 week (7 days) to correct the date
#     corrected_date = date - timedelta(days=7)

#     # Return the formatted date string
#     return corrected_date.strftime('%Y-%m-%d')

def format_time(ms):
    """
    Convert ms to time string

    Parameters
    ----------
    ms : int
        Time duration in miliseconds. Must be non-negative

    Returns
    -------
    str
        Formatted time string in m:ss.cc format, where
        - m = minutes
        - ss = seconds (zero-padded to 2 digits)
        - cc = centiseconds
    """
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

def safe_get(value, default=None):
    return value if pd.notna(value) else default

def get_ordinal_suffix(day):
    """Return the ordinal suffix for a given day in superscript."""
    if 11 <= day <= 13:  # Handle special cases like 11th, 12th, 13th
        return "<sup>th</sup>"
    if day % 10 == 1:  # Ends in 1, e.g., 1st, 21st
        return "<sup>st</sup>"
    if day % 10 == 2:  # Ends in 2, e.g., 2nd, 22nd
        return "<sup>nd</sup>"
    if day % 10 == 3:  # Ends in 3, e.g., 3rd, 23rd
        return "<sup>rd</sup>"
    return "<sup>th</sup>"  # Default to "th"

def convert_milliseconds_to_date(milliseconds, timezone_name="UTC"):
    # Convert milliseconds to seconds
    seconds = milliseconds / 1000
    # Convert seconds to a timezone-aware datetime object in UTC
    utc_time = datetime.fromtimestamp(seconds, tz=timezone.utc)
    # Convert to the desired timezone
    tz = pytz.timezone(timezone_name)
    local_time = utc_time.astimezone(tz)
    # Get the day with the correct ordinal suffix
    day_with_suffix = f"**{local_time.day}**{get_ordinal_suffix(local_time.day)}"
    # Format the date
    formatted_date = f"**{local_time.strftime('%B')}** {day_with_suffix}&nbsp;&nbsp;**{local_time.year}**"
    return formatted_date
    

def load_and_process_csv(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    # # Reverse the DataFrame rows
    # df = leaderboard_tracking.iloc[::-1]
    return df


def preprocess_dataframe(df):
    df["formatted_date"] = df["raceStart"].apply(lambda x: convert_milliseconds_to_date(x))
    df["racetime1"] = df["time1"].apply(lambda x: format_time(x))
    df["racetime2"] = df["time2"].apply(lambda x: format_time(x))
    df["racetime3"] = df["time3"].apply(lambda x: format_time(x))
    df["racetime4"] = df["time4"].apply(lambda x: format_time(x))
    df["racetime5"] = df["time5"].apply(lambda x: format_time(x))
    return df


def normalize_map_name(name: str) -> str:
    """
    Convert a map name into a universal format for matching:
    - Remove spaces
    - Lowercase everything
    """
    return re.sub(r"\s+", "", name).lower()


# Usage example
file_path = 'race_history.csv'
df = load_and_process_csv(file_path)
df = preprocess_dataframe(df)

with open("gamedata/name_mapping.json", "r") as f:
    name_mapping = json.load(f)

# --- Load map naming JSON ---
with open("gamedata/map_naming.json", "r") as f:
    maps_by_difficulty = json.load(f)

image_paths = {
    "1th": "image/1th.webp",
    "2th": "image/2th.webp",
    "3th": "image/3th.webp",
    "4th": "image/4th.webp"
}

# Step 1: Radio that cannot be disabled (always has one active)
mode = st.radio("Filter by:", ["Year 📆", "Map 🏔️"])

import re

def normalize_map_name(name: str) -> str:
    """
    Normalize map names for matching:
    - Remove spaces
    - Lowercase everything
    """
    return re.sub(r"\s+", "", name).lower()

# Step 2: Show different input depending on mode
if mode == "Year 📆":
    # Extract year numbers from formatted_date column
    df["year"] = df["formatted_date"].str.extract(r"(\d{4})")[0].astype(int)

    years = sorted(df["year"].unique(), reverse=True)  # descending order

    # Build labels like "2018: #1 - #9"
    year_labels = []
    for y in years:
        year_df = df[df["year"] == y]
        start_race = year_df["raceno"].min()
        end_race = year_df["raceno"].max()
        year_labels.append(f"{y}: {start_race} - {end_race}")

    # Let radio store index, but show labels
    year_idx = st.radio(
        "Select a year:",
        range(len(years)),
        format_func=lambda i: year_labels[i],
        key="year_choice"
    )
    year_choice = years[year_idx]
    selected_chunk = df[df["year"] == year_choice]


elif mode == "Map 🏔️":

    # --- Step 1 & 2: Split into two columns ---
    col1, col2 = st.columns([9,24])

    with col1:
        difficulty = st.radio(
            "Select difficulty level:",
            list(maps_by_difficulty.keys()),
            key="difficulty"
        )

    with col2:
        map_choice = st.selectbox(
            "Select a map:",
            maps_by_difficulty[difficulty],
            key="map_choice"
        )

        # --- Normalize for matching ---
        df["map_normalized"] = df["map"].apply(normalize_map_name)
        selected_map_norm = normalize_map_name(map_choice)

        # --- Filter DataFrame ---
        selected_chunk = df[df["map_normalized"] == selected_map_norm].drop(columns=["map_normalized"])

        # --- Show race count (outside columns) ---
        if len(selected_chunk) == 0:
            st.warning(f"No races on {map_choice}!")
        else:
            st.info(f"Race count on {map_choice}: **{len(selected_chunk)}**")


# Iterate through races in reverse order (latest race first)
for id in selected_chunk.index[::-1]:
    st.subheader(f"Race #{df.at[id, 'raceno']}: {df.at[id, 'racetitle']}")

    colleft, colmid, colright = st.columns([11, 1, 8])
    with colleft:
        col1, col2 = st.columns([1, 8], vertical_alignment="center")
        with col1:
            st.image(image_paths["1th"], use_container_width = True)

        with col2:
            if id in {47, 91, 101, 106}:  # Set of special IDs
                st.write(f" :rainbow-background[{safe_get(df.at[id, 'url1'], 'N/A') if not str(safe_get(df.at[id, 'url1'], '')).startswith('https://') else name_mapping.get(safe_get(df.at[id, 'url1']), safe_get(df.at[id, 'name1'], 'N/A'))}: {format_time(safe_get(df.at[id, 'time1'], 0))}] ")
            else:
                st.write(f" :grey-background[{df.at[id, 'url1'] if not str(df.at[id, 'url1']).startswith('https://') else name_mapping.get(df.at[id, 'url1'], df.at[id, 'name1'])}] "
                        f"**\"{df.at[id, 'name1']}\": {df.at[id, 'racetime1']}**")

        col1, col2 = st.columns([1, 8], vertical_alignment="center")
        with col1:
            st.image(image_paths["2th"], use_container_width = True)

        with col2:
            st.write(f" :red-background[{df.at[id, 'url2'] if not str(df.at[id, 'url2']).startswith('https://') else name_mapping.get(df.at[id, 'url2'], df.at[id, 'name2'])}] "
                    f"**\"{df.at[id, 'name2']}\": {df.at[id, 'racetime2']}**")

        col1, col2 = st.columns([1, 8], vertical_alignment="center")
        with col1:
            st.image(image_paths["3th"], use_container_width = True)

        with col2:
            st.write(f" :blue-background[{df.at[id, 'url3'] if not str(df.at[id, 'url3']).startswith('https://') else name_mapping.get(df.at[id, 'url3'], df.at[id, 'name3'])}] "
                    f"**\"{df.at[id, 'name3']}\": {df.at[id, 'racetime3']}**")

        col1, col2 = st.columns([1, 8], vertical_alignment="center")
        with col1:
            st.image(image_paths["4th"], use_container_width = True)

        with col2:
            st.write(f" {df.at[id, 'url4'] if not str(df.at[id, 'url4']).startswith('https://') else name_mapping.get(df.at[id, 'url4'], df.at[id, 'name4'])} "
                    f"**\"{df.at[id, 'name4']}\": {df.at[id, 'racetime4']}**")

        col1, col2 = st.columns([1, 8], vertical_alignment="center")
        with col1:
            st.image(image_paths["4th"], use_container_width = True)

        with col2:
            st.write(f" {df.at[id, 'url5'] if not str(df.at[id, 'url5']).startswith('https://') else name_mapping.get(df.at[id, 'url5'], df.at[id, 'name5'])} "
                    f"**\"{df.at[id, 'name5']}\": {df.at[id, 'racetime5']}**")

    with colright:
        if df.at[id, 'new_t50'] != 0 or df.at[id, 'raceno'] > 336:
            new_t50 = df.at[id, 'new_t50']
            if new_t50 <= 1:
                st.write(f'New T50 racer: {new_t50}')
            else:
                st.write(f'New T50 racers: {new_t50}')

        if df.at[id, 'top50_time'] != 0:
            st.write(f"1st - 50th gap: **{format_time_gap(safe_get(df.at[id, 'top50_time'], 0) - safe_get(df.at[id, 'time1'], 0))}s**")

        if df.at[id, 'totalPlayer'] != 0:
            st.write(f"Number of players: **{format(df.at[id, 'totalPlayer'], ',')}**")

        st.markdown(f"Start date: {df.at[id, 'formatted_date']}", unsafe_allow_html=True)

    st.divider()
