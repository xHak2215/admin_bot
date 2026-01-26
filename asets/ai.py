"""its an API for using AI (Not used)"""
import os
import time
import dictt
import string

from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, AutoTokenizer, AutoModelForSequenceClassification
import torch
from fastapi import FastAPI
from fastapi.responses import JSONResponse


class MessageClassifier:
    def __init__(self):
        self.model_path = {
            "oskorb": "cointegrated/rubert-tiny",
            "spam": "RUSpam/spam_deberta_v4"
        }
        self.tokenizer_oskorb = DistilBertTokenizer.from_pretrained(self.model_path['oskorb'])
        self.model_oskorb = DistilBertForSequenceClassification.from_pretrained(self.model_path['oskorb'], num_labels=2)

        self.tokenizer_spam = AutoTokenizer.from_pretrained(self.model_path["spam"])
        self.model_spam = AutoModelForSequenceClassification.from_pretrained(self.model_path["spam"])

    def scan_oscorb_message(self, message: str):
        """
        проверяет оскорбительное ли сообщение 

        потдерживает лиш русский
        """
        inputs = self.tokenizer_oskorb(message, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model_oskorb(**inputs)
        predictions = torch.argmax(outputs.logits, dim=1)
        return predictions.item() == 1, predictions.item()

    def detect_spam_in_message(self, message: str) ->bool:
        """
        проверяет сообщение на спам

        потдерживает лиш русский

        arg:
            message(str):само сообщение

        return:
            Trye если признано спамом false если нет  
        """
        inputs = self.tokenizer_spam(message, return_tensors="pt", truncation=True, max_length=256)
        with torch.no_grad():
            outputs = self.model_spam(**inputs)
            logits = outputs.logits
            predicted_class = torch.argmax(logits, dim=1).item()
        return predicted_class == 1

ai_analis = MessageClassifier()
app = FastAPI()
 
@app.get("/")
def status():
    return 200

@app.get("/spam")
def spam_detect(message:str):
    error=None
    try:
        timer=time.time()
        relust=ai_analis.detect_spam_in_message(message)
        timer=time.time()-timer
    except Exception as e:
        error=e
        relust=None
        timer=None

    return {"detect":relust, "error":error, "timer":timer}

@app.get("/affront_detect")
def affront_detect(message:str):
    error=None
    try:
        timer=time.time()
        detect,item=ai_analis.scan_oscorb_message(message)
        timer=time.time()-timer
    except Exception as e:
        error=e
        detect,item=None,None
        timer=None

    return {"detect": detect, "coficent":item, "error":error, "timer":timer}


# Запуск сервера
if __name__ == '__main__':
    import uvicorn 
    uvicorn.run(app, host="127.0.0.2", port=8080)
