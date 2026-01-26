import requests

timeout=5

def chec_spam(message:str)->dict|None:
    response = requests.get(r"http://127.0.0.2:8080/spam", 
                            params={'message': message},timeout=timeout)
    try:
        response.raise_for_status()
        relust_spam = response.json()
        return relust_spam
    except Exception:
        return None

def chec_insult(message:str)->dict|None:
    response = requests.get(r"http://127.0.0.2:8080/affront_detect", 
                            params={'message': message},timeout=timeout)
    try:
        response.raise_for_status()
        relust_affront = response.json()
        return relust_affront
    except Exception:
        return None
