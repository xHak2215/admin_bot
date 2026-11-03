from .errors import *
import requests


def get_adstract(q:str):
    response = requests.get(f"https://api.duckduckgo.com", 
                                params={'q': q, 'format':'json', 'no_html':'1', 'skip_disambig':'1', 'kl':'ru-ru'})
    
    if response.status_code == 200 or response.status_code == 202:
        return response.json()
    else:
        raise APIerror(f"status code error {response.status_code}")