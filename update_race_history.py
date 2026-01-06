import os
import csv
import json
import aiohttp
import asyncio
import pandas as pd
from functions import ms_to_week_day_hour

race_history = 'race_history.csv'
race_leaderboard_file = "race_leaderboard.csv"
RACE_CONFIG = "gamedata/race_config.json"
with open(RACE_CONFIG, "r", encoding="utf-8") as f:
    race_config = json.load(f)

def ensure_race_history_columns(csv_path = race_history):
    columns = [
        'raceno', 'racetitle', 'map',
        'name1', 'name2', 'name3', 'name4', 'name5',
        'time1', 'time2', 'time3', 'time4', 'time5',
        'new_t3', 'new_t50', 'top50_time', 'totalPlayer', 'raceStart',
        'url1', 'url2', 'url3', 'url4', 'url5',
        'raceurl', 'race_metadata'   
    ]

    # If file exists, check header
    if os.path.isfile(csv_path):
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            existing = next(reader, None)

        # Header matches → do nothing
        assert existing == columns, f"Header mismatch in {csv_path}"

async def fetch_json(session, url):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            resp.raise_for_status()
            return await resp.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None
    
async def fetch_race_data(race_config):
    async with aiohttp.ClientSession() as session:
        # Fetch races
        races_json = await fetch_json(session, race_config["RACE_EVENT_URL"])
        races = races_json.get("body", [])

        # Find the current race
        current_race = next((r for r in races if r.get("totalScores")), None)
        if current_race is None:
            return None, None, None  # No race found

        # Prepare URLs
        leaderboard_url = race_config['CURRENT_RACE_URL']
        metadata_url = leaderboard_url.rsplit("/", 1)[0] + "/metadata"

        # Fetch leaderboard and metadata concurrently
        leaderboard_json, metadata_json = await asyncio.gather(
            fetch_json(session, leaderboard_url),
            fetch_json(session, metadata_url),
        )

        leaderboard = leaderboard_json.get("body", [])
        map_name = metadata_json.get("body", {}).get("map", "")

        return current_race, map_name, leaderboard

async def is_there_new_t3_and_t50(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_json(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    new_t3 = 0
    new_t50 = 0
    
    # Check top 3 for new_t3
    for entry in results[:3]:
        if entry is None:
            continue
        medals = entry.get('body', {}).get('_medalsRace', {})
        if not any(k in medals for k in ['BlackDiamond', 'RedDiamond', 'BlueDiamond']):
            new_t3 = 1
            break

    # Count new_t50 across all
    for entry in results:
        if entry is None:
            continue
        medals = entry.get('body', {}).get('_medalsRace', {})
        if 'GoldDiamond' not in medals:
            new_t50 += 1
    
    return new_t3, new_t50

def update_race_history():

    def updating_name_mapping(urls, names, name_mapping_file="gamedata/name_mapping.json"):
        """
        Updates the name mapping JSON file by adding new URL-to-name mappings if missing.

        Args:
        - urls: List of URLs (url1 to url5)
        - names: List of corresponding names (name1 to name5)
        - name_mapping_file: Path to the JSON file storing the mappings
        """
        # Load existing name mapping file or create an empty dictionary
        if os.path.exists(name_mapping_file):
            with open(name_mapping_file, "r", encoding="utf-8") as f:
                name_mapping = json.load(f)

            updated = False  # Track whether changes were made
            
            # Iterate through URLs and names
            for url, name in zip(urls, names):
                if url and url not in name_mapping:  # Ensure URL is valid and not already in the mapping
                    name_mapping[url] = name
                    updated = True

            # Save updated mapping back to the JSON file
            if updated:
                with open(name_mapping_file, "w", encoding="utf-8") as f:
                    json.dump(name_mapping, f, indent=4)
                print("Name mapping updated very successfully.")
            else:
                print("No new mappings were added.")
        else:
            print(f"Name mapping file {name_mapping_file} does not exist. Skipping update.")


    current_race, map, leaderboard_data = asyncio.run(fetch_race_data(race_config))

    race_no, _, __ = ms_to_week_day_hour(current_race['start'])

    urls = [entry['profile'] for entry in leaderboard_data[:50]]
    names = [entry['displayName'] for entry in leaderboard_data[:50]]

    updating_name_mapping(urls, names)

    new_t3, new_t50 = asyncio.run(is_there_new_t3_and_t50(urls))

    assert len(leaderboard_data) >= 50, "Leaderboard has less than 50 entries"
    top50_time = leaderboard_data[-1]['score']

    new_row = {
        'raceno': race_no,
        'racetitle': current_race['name'],
        'map': map,

        'new_t3': new_t3,
        'new_t50': new_t50,
        'top50_time': top50_time,
        'totalPlayer': current_race['totalScores'],
        'raceStart': current_race['start'],

        'raceurl': current_race['leaderboard'],
        'race_metadata': current_race['metadata']
    }

    for i, entry in enumerate(leaderboard_data[:5], start=1):
        new_row[f'name{i}'] = entry.get('displayName', '')
        new_row[f'time{i}'] = entry.get('score', 0)
        new_row[f'url{i}'] = entry.get('profile', '')

    df = pd.read_csv(race_history)

    if df.iloc[-1]['raceno'] != new_row['raceno']:
        # Append new row
        df.loc[len(df)] = new_row
        print(f"Appended new row for raceno {new_row['raceno']}")
        print("Race history updated!")

    elif df.iloc[-1]['top50_time'] != new_row['top50_time']:
        print("T50 time has changed")
        # Update last row only if values actually differ
        last_row = df.iloc[-1]
        changes = {k: (last_row[k], v) for k, v in new_row.items()
                if k not in ['new_t3', 'new_t50'] and k in last_row and last_row[k] != v}

        for k, (_, new_val) in changes.items():
            df.at[df.index[-1], k] = new_val

        if changes:
            print(f"Updated last row for raceno {new_row['raceno']}:")
            for k, (old, new) in changes.items():
                print(f" - {k}: {old} -> {new}")
    else:
        print("No changes to latest race")


    # Save changes back to CSV
    df.to_csv(race_history, index=False)


    return

# update_race_history()
