from datetime import datetime, timedelta, timezone
import requests

def ms_to_week_day_hour(ms):

    # return week, date and hour from ms

    ANCHOR_MS = 1766534400000 # Wednesday 00:00 UTC
    ANCHOR_WEEK = 367

    MS_PER_WEEK = 7 * 24 * 60 * 60 * 1000

    # week calculation (race weeks)
    week = ANCHOR_WEEK + (ms - ANCHOR_MS) // MS_PER_WEEK

    # real calendar time for weekday + hour
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)

    return week, dt.weekday(), dt.hour

def fetch_player_data(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        
        # Check if 'body' exists in the response
        if 'body' in data:
            return data
        
        print(f"'body' key missing in response for URL: {url}")
    except (requests.RequestException, ValueError) as e:
        print(f"Request failed for URL: {url}, Error: {e}")
    
    print(f"Failed to fetch valid data for URL: {url}")
    return None