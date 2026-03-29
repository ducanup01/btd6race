import requests
import json
import csv
import os
import pandas as pd
import time
import aiohttp
import asyncio
from update_race_history import update_race_history


RACE_CONFIG = "gamedata/race_config.json"
race_leaderboard_file = "race_leaderboard.csv"
monkeys_file = "gamedata/monkeys.json"


def update_race_config():
    RACE_EVENT_URL = "https://data.ninjakiwi.com/btd6/races"

    # Base structure if file does not exist
    race_config = {
        "RACE_EVENT_URL": RACE_EVENT_URL,
        "CURRENT_RACE_NAME": "",
        "CURRENT_RACE_URL": "",
        "CURRENT_RACE_WINDOW": {
            "start": 0,
            "end": 0
        },
        "NEXT_RACE_NAME": "",
        "NEXT_RACE_URL": "",
        "NEXT_RACE_WINDOW": {
            "start": 0,
            "end": 0
        }
    }

    # If file exists, load and update instead of overwriting blindly
    if os.path.exists(RACE_CONFIG):
        with open(RACE_CONFIG, "r", encoding="utf-8") as f:
            try:
                race_config.update(json.load(f))
            except json.JSONDecodeError:
                print("Race config file is corrupted. Recreating...")

    # Fetch race data
    r = requests.get(RACE_EVENT_URL, timeout=10)
    r.raise_for_status()
    races = r.json().get("body", [])

    current = None
    next_race = None

    PLAYER_COUNT_THRESHOLD = 1

    for i, race in enumerate(races):
        if (race.get("totalScores", 0) > PLAYER_COUNT_THRESHOLD):
            current = race
            next_race = races[i - 1] if i > 0 else None
            break

    if current and (race["name"] != race_config["CURRENT_RACE_NAME"]):
        race_config["CURRENT_RACE_NAME"] = current["name"]
        race_config["CURRENT_RACE_URL"] = current["leaderboard"]
        race_config["CURRENT_RACE_WINDOW"]["start"] = current["start"]
        race_config["CURRENT_RACE_WINDOW"]["end"] = current["end"]

    if next_race:
        race_config["NEXT_RACE_NAME"] = next_race["name"]
        race_config["NEXT_RACE_URL"] = next_race["leaderboard"]
        race_config["NEXT_RACE_WINDOW"]["start"] = next_race["start"]
        race_config["NEXT_RACE_WINDOW"]["end"] = next_race["end"]
    else:
        race_config["NEXT_RACE_NAME"] = ""
        race_config["NEXT_RACE_URL"] = ""
        race_config["NEXT_RACE_WINDOW"]["start"] = 0
        race_config["NEXT_RACE_WINDOW"]["end"] = 0
        print("No upcoming race found.")

    # Ensure directory exists
    os.makedirs(os.path.dirname(RACE_CONFIG), exist_ok=True)

    with open(RACE_CONFIG, "w", encoding="utf-8") as f:
        json.dump(race_config, f, indent=4)

    print("Updated race config file.")

def clear_leaderboard(csv_path = race_leaderboard_file):
    # Read the headers
    with open(csv_path, 'r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Get the first row as headers

    # Write back only the headers, clearing all data
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

    print("Leaderboard cleared, preparing for a new race.")

def ensure_race_leaderboard_columns(csv_path = race_leaderboard_file):
    def create_columns(p=monkeys_file):
        with open(p, encoding="utf-8") as f:
            m = [x for v in json.load(f).values() for x in v] + ['gamecount', 'follower']
        return (
            ['name','time','time_left','last_online','last_update']
            + [f'init_{x}' for x in m]
            + m
            + ['url','pfp_url']
        )
    columns = create_columns()

    # If file exists, check header
    if os.path.isfile(csv_path):
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            existing = next(reader, None)

        # Header matches → do nothing
        if existing == columns:
            return

    # Either file doesn't exist OR header mismatch → erase & rewrite
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(columns)

    print(f"Reset '{csv_path}' with correct columns.")

def update_leaderboard():
    async def fetch_player(session, url, semaphore):
        async with semaphore:
            try:
                async with session.get(url, timeout=10) as r:
                    r.raise_for_status()
                    return await r.json()
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
                return None

    async def fetch_all_players(urls, max_concurrent=20):
        semaphore = asyncio.Semaphore(max_concurrent)
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_player(session, url, semaphore) for url in urls]
            return await asyncio.gather(*tasks)

    # Load leaderboard CSV
    df = pd.read_csv(race_leaderboard_file) if pd.io.common.file_exists(race_leaderboard_file) else pd.DataFrame()

    # fetch 2 pages
    with open(RACE_CONFIG, "r", encoding="utf-8") as f:
        race_config = json.load(f)

    leaderboard_data = []

    url = race_config["CURRENT_RACE_URL"]
    pages_fetched = 0
    MAX_PAGES = 2

    while isinstance(url, str) and pages_fetched < MAX_PAGES:
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        data = r.json()
        leaderboard_data.extend(data.get("body", []))

        url = data.get("next")
        pages_fetched += 1
    # end fetch 2 pages

    print(f"Updating leaderboard with {len(leaderboard_data)} players.")
    now_ms = int(time.time() * 1000)

    # Prepare URLs to fetch asynchronously
    player_urls = [p['profile'] for p in leaderboard_data if p.get('profile')]
    player_data_list = asyncio.run(fetch_all_players(player_urls))

    # Process each player one by one (row by row)
    for count, (entry, pdata) in enumerate(zip(leaderboard_data, player_data_list), start=1):
        player_url = entry.get('profile')
        if not pdata or not player_url:
            continue

        body = pdata.get('body', {})
        towers = body.get('towersPlaced', {})
        heroes = body.get('heroesPlaced', {})
        gameplay = body.get('gameplay', {})
        follower = body.get('followers', 0)
        gamecount = gameplay.get('gameCount', 0)
        racetime = entry.get('score', 0)
        time_left = entry.get('scoreParts', [{}])[1].get('score', 0)
        pfp_url = body.get('avatarURL', None)

        if player_url not in df['url'].values:
            # Add new row
            new_row = {
                'name': body.get('displayName'),
                'time': racetime,
                'time_left': time_left,
                'init_gamecount': gamecount,
                'init_follower': follower,
                'last_online': 0,
                'url': player_url,
                'pfp_url': pfp_url,
            }
            for key in towers:
                new_row[f'init_{key}'] = towers.get(key, 0)
                new_row[key] = 0
            for key in heroes:
                new_row[f'init_{key}'] = heroes.get(key, 0)
                new_row[key] = 0
            new_row['gamecount'] = 0
            new_row['follower'] = 0
            df.loc[len(df)] = new_row

        else:
            # Update existing row
            idx = df[df['url'] == player_url].index[0]
            if gamecount - df.at[idx, 'init_gamecount'] == df.at[idx, 'gamecount']:
                df.at[idx, 'last_online'] += (now_ms - df.at[0, 'last_update'])
            else:
                df.at[idx, 'last_online'] = 0

            df.at[idx, 'name'] = body.get('displayName')
            df.at[idx, 'pfp_url'] = pfp_url
            df.at[idx, 'gamecount'] = gamecount - df.at[idx, 'init_gamecount']
            df.at[idx, 'follower'] = follower - df.at[idx, 'init_follower']
            df.at[idx, 'time'] = racetime
            df.at[idx, 'time_left'] = time_left

            for key in towers:
                df.at[idx, key] = towers.get(key, 0) - df.at[idx, f'init_{key}']
            for key in heroes:
                df.at[idx, key] = heroes.get(key, 0) - df.at[idx, f'init_{key}']

        print(f"{count}/{len(leaderboard_data)} processed: {player_url}")

    # Update last update timestamp
    if len(df) > 0:
        df.at[0, 'last_update'] = now_ms

    df.to_csv(race_leaderboard_file, index=False)
    print("Race information updated!")

def schedule_task():
    with open(RACE_CONFIG, "r", encoding="utf-8") as f:
        race_config = json.load(f)

    current_race_start = race_config["CURRENT_RACE_WINDOW"]["start"]
    current_race_end = race_config["CURRENT_RACE_WINDOW"]["end"]
    next_race_start = race_config["NEXT_RACE_WINDOW"]["start"]

    current_ms = int(time.time() * 1000)

    HOUR_AFTER_RACE_START = 2 * (60 * 60 * 1000)
    MINUTES_AFTER_RACE_END = 15 * (60 * 1000)
    HOUR_UNTIL_NEXT_RACE = 4 * (60 * 60 * 1000)
    DAYS_AFTER_RACE_START = 6 * (24 * 60 * 60 * 1000)

    if current_ms <= current_race_start + HOUR_AFTER_RACE_START:
        print("Waiting for new race stats")
    
    # 2 hours after race starts and 15 minutes after it ends
    elif current_race_start + HOUR_AFTER_RACE_START < current_ms < current_race_end + MINUTES_AFTER_RACE_END:
        # update_leaderboard()
        pass


    elif next_race_start == 0:
        if current_ms < current_race_start + DAYS_AFTER_RACE_START:
            update_race_history()
        elif current_race_start + DAYS_AFTER_RACE_START < current_ms:
            clear_leaderboard()
        else:
            print("Race is dead")

    else:
        if current_ms < next_race_start - 3 * HOUR_UNTIL_NEXT_RACE:
            update_race_history()

        elif next_race_start - HOUR_UNTIL_NEXT_RACE < current_ms < next_race_start:
            clear_leaderboard()

        else:
            print("Doing nothing")

def main():
    update_race_config()
    ensure_race_leaderboard_columns()
    schedule_task()
    
if __name__ == "__main__":
    main()
    # update_leaderboard()
    # clear_leaderboard()
    # update_race_history()
