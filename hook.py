import requests
import time
import sys

class hookBase:
    def __init__(self, username, interval=1):
        self.host = "https://discovery-b.mainnet.audius.radar.tech/v1"
        self.username = username
        self.id = self.getId()
        self.interval = interval*60 # Interval is set in minutes. Is the duration between checks (duh) for new tracks
        self.curTracks = 0 # Set persistent variable to check if a new track exists
    
    def getId(self):
        headers = {
            'Accept': 'application/json'
        }
        payload = {
            'query': self.username,  
            'app_name': 'amullerWebhook',
        }
        r = requests.get('https://discovery-b.mainnet.audius.radar.tech/v1/users/search', params=payload, headers=headers)
        for item in r.json()['data']:
            if item['handle'] == self.username:
                return item['id']
    
    def getTracks(self):
        headers = {
        'Accept': 'application/json'
        }
        payload = { 
            'user_id': self.id,
            'app_name': 'amullerWebhook',
        }
        r = requests.get(self.host+f"/users/{self.id}/tracks", params=payload, headers=headers)
        curLen = len(r.json()['data'])
        if curLen > self.curTracks:
            for i in range(curLen-self.curTracks):
                curData = r.json()['data'][i]
                print(f"New track found: {curData['title']}")
        self.curTracks = curLen

    def run(self):
        while True:
            self.getTracks()
            time.sleep(self.interval)


h = hookBase(sys.argv[1])
h.run()