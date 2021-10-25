import requests
import time
import sys
from threading import Thread

class hookBase:
    def __init__(self, username, hookurl, interval=1):
        self.host = "https://discovery-b.mainnet.audius.radar.tech/v1"
        self.username = username
        self.id = self.getId()
        self.hookurl = hookurl
        self.interval = interval*60 # Interval is set in minutes. Is the duration between checks (duh) for new tracks
        self.curTracks = 0 # Set persistent variable to check if a new track exists
    
    def sendHook(self, data):
        data = {
            "username" : "Audius Music",
            "avatar_url": "https://avatars1.githubusercontent.com/u/38231615?s=400&u=c00678880596dabd2746dae13a47edbe7ea7210e&v=4"
        }
        data["embeds"] = [
            {
                "title" : data['title'],
                "content": f"New music posted by {self.username}",
                "image": {
                    'url': data['cover'],
                    'height': 500,
                    'width': 500
                },
                "type": "rich",
                "url": data['url']
            }
        ]
        result = requests.post(self.hookurl, json=data)
        try:
            result.raise_for_status()
        except:
            pass
    
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
                data = {
                    "cover": curData['artwork']['1000x1000'],
                    "title": curData['title'],
                    "url": f"audius.co{curData['permalink']}"
                }
                Thread(target=self.sendHook, args=(data,)).start()
        self.curTracks = curLen

    def run(self):
        while True:
            self.getTracks()
            time.sleep(self.interval)
run = True
match len(sys.argv.pop(0)):
    case 2:
        h = hookBase(sys.argv[1], sys.argv[2])
    case 3:
        h = hookBase(sys.argv[1], sys.argv[2], sys.argv[3])
    case default:
        run = False
        print("Not enough args given. Example usage: python audius.py <audius handle> <webhook url> <optional: hook check interval (minutes)>")
if run:
    h.run()