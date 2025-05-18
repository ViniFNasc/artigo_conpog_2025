import requests
import time

class Connection:

    def __init__(self, esporte=None, data=None):

        self.esporte = esporte
        self.data = data

        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50"
                        ,"Cache-Control": "max-age=0"}

        self.tempo_request = 0.1


    def get_events(self):

        url = f'https://www.sofascore.com/api/v1/sport/{self.esporte}/scheduled-events/{self.data}'
        response = requests.get(url,timeout=5, headers=self.headers)
        time.sleep(self.tempo_request)
        obj = response.json()
        events = obj['events']

        return events
    

    def get_markets(self, match_id):
        
        url = f'https://www.sofascore.com/api/v1/event/{match_id}/odds/1/all'
        response = requests.get(url, timeout=5, headers=self.headers)
        time.sleep(self.tempo_request)
        obj = response.json()
        markets = obj['markets']

        return markets

    
    def get_statistics(self, match_id):

        url = f"https://www.sofascore.com/api/v1/event/{match_id}/statistics"
        response = requests.get(url, timeout=5, headers=self.headers)
        # time.sleep(self.tempo_request)
        time.sleep(0.5)
        obj = response.json()
        statistics = obj['statistics']

        return statistics


    def get_season(self,match_id):

        url = f"https://www.sofascore.com/api/v1/event/{match_id}"
        response = requests.get(url, timeout=5, headers=self.headers)
        time.sleep(self.tempo_request)
        obj = response.json()
        event = obj['event']

        return event