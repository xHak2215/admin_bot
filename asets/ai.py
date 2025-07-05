from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
import logging
import string
from googletrans import Translator

import dictt

model_path={
            'oskorb':"cointegrated/rubert-tiny",
            "spam":"RUSpam/spam_deberta_v4"
            }



translator = Translator()
conf = translator.detect()
#result = translator.translate('' , src=conf.lang, dest='ru')

def scan_oscorb_message(message:str):
    tokenizer = DistilBertTokenizer.from_pretrained(model_path['oskorb'])
    model = DistilBertForSequenceClassification.from_pretrained(model_path['oskorb'], num_labels=2)
    if message in list(string.ascii_lowercase):
        message=''.join(dictt.translit_ru.get(c, c) for c in message)
    # Пример предсказания
    inputs = tokenizer(message, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=1)
    return True,predictions.item() if predictions.item() == 1 else False,predictions.item()

def detect_spam_in_message(message:str):
    tokenizer = AutoTokenizer.from_pretrained(model_path["spam"])
    model = AutoModelForSequenceClassification.from_pretrained(model_path["spam"])
    inputs = tokenizer(message, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
    return True if predicted_class == 1 else False

