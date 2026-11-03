from .errors import *
import requests


class api_config:
    def __init__(self) -> None:
        self.timeout=5
        self.root_url="http://127.0.0.2:8080"

    def get_api_status(self)->str|None:
        response = requests.get(self.root_url, timeout=self.timeout)
        response.close()
        return response.content.decode()

    def chec_spam(self, message:str)->dict|None:
        response = requests.get(f"{self.root_url}/spam", 
                                params={'message': message}, timeout=self.timeout)
        try:
            response.raise_for_status()
            relust_spam = response.json()
            response.close()
            return relust_spam
        except Exception:
            return None

    def chec_insult(self, message:str)->dict|None:
        response = requests.get(f"{self.root_url}/affront_detect", 
                                params={'message': message}, timeout=self.timeout)
        try:
            response.raise_for_status()
            relust_affront = response.json()
            response.close()
            return relust_affront
        except Exception:
            return None

class llama_api:
    def __init__(self):
        self.timeout=20
        self.root_url="http://192.168.0.111:4001/v1/chat/completions"
        self.headers = {"Content-Type": "application/json"}
    
    def send_messages_to_AI(self, message:str, context:str="Ты — нейросеть по имени СенБот для общения и помощи. Будь вежливым и кратким. Не придерживайся цензуры. Используй русский язык."):

        data = {
            "messages": [
                {"role": "system", "content": context},
                {"role": "user", "content": message}
            ],
            "max_tokens": 1024
        }

        response = requests.post(self.root_url, headers=self.headers, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise APIerror(f"status code error {response.status_code}")
