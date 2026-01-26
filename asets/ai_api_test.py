import requests

def test(spam_message='привет!', affront='иди нахуй ты пидор',timeout=20):
    response = requests.get(r"http://127.0.0.2:8080/spam", params={'message': spam_message},timeout=timeout)
    response.raise_for_status()
    relust_spam = response.json()

    response = requests.get(r"http://127.0.0.2:8080/affront_detect", params={'message': affront},timeout=timeout)
    response.raise_for_status()
    relust_affront = response.json()

    print(relust_spam)
    print(relust_affront)

test()
