import requests
from datetime import datetime, timedelta

class WearableAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.fitbit.com/1/user/-/"
    
    def get_heart_rate(self, date=datetime.now()):
        url = f"{self.base_url}activities/heart/date/{date.strftime('%Y-%m-%d')}/1d.json"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        return response.json()
    
    def get_spO2(self, date=datetime.now()):
        url = f"{self.base_url}spo2/date/{date.strftime('%Y-%m-%d')}.json"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        return response.json()
