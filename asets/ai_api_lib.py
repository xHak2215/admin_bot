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

ai_api=api_config()
