import requests
import os
from datetime import datetime, timezone
import dotenv

API_URL = 'https://osu.ppy.sh/api/v2'
TOKEN_URL = 'https://osu.ppy.sh/oauth/token'

HOURS = {
    "00:00": 0, "01:00": 0, "02:00": 0, "03:00": 0,
    "04:00": 0, "05:00": 0, "06:00": 0, "07:00": 0,
    "08:00": 0, "09:00": 0, "10:00": 0, "11:00": 0,
    "12:00": 0, "13:00": 0, "14:00": 0, "15:00": 0,
    "16:00": 0, "17:00": 0, "18:00": 0, "19:00": 0,
    "20:00": 0, "21:00": 0, "22:00": 0, "23:00": 0,
}

dotenv.load_dotenv()

def get_token():
    
    data = {
        'client_id': os.getenv("CLIENT_ID"),
        'client_secret': os.getenv("CLIENT_SECRET"),
        'grant_type': 'client_credentials',
        'scope': 'public'
    }
    
    response = requests.post(TOKEN_URL, data=data)
    
    return response.json().get('access_token')

def process_scores(data):
        
    times = [element['created_at'] for element in data]

    localized_times = [datetime.fromisoformat(element).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z') for element in times]

    one_digit = [int(element[12:13]) for element in localized_times if str(element[11:13]).startswith("0")]
    two_digit = [int(element[11:13]) for element in localized_times if not str(element[11:13]).startswith("0")]
    
    final = one_digit + two_digit
    
    return [f"{str(time)}:00" if len(str(time)) > 1 else f"0{str(time)}:00" for time in final]


def frequency(data):
    
    score_frequency = HOURS

    for item in data:
        if item in score_frequency:
            score_frequency[item] += 1

    return dict(sorted(score_frequency.items(), key=lambda item: item[1]))    
 
def calculate(username):
    
    token = get_token()
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    params = {
        "mode": "osu",
        "include_fails": 0,
        "limit": 100,
    }
    
    resp = requests.get(f"https://osu.ppy.sh/users/{username}")
        
    response = requests.get(f'{API_URL}/users/{resp.url[25:]}/scores/best', params=params, headers=headers)
    
    data = response.json()
    
    scores = process_scores(data)
    
    return frequency(scores)