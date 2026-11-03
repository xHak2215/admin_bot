from .errors import *

import requests
from bs4 import BeautifulSoup, Comment
from loguru import logger
from cloakbrowser import launch

promt = "sdgsadg https://github.com/xHak2215/admin_bot sdzfg"

def scan_url(promt:str) ->tuple:
    probel_pos = 0
    url = ""

    if "https" in promt:
        protacol = "https"
    elif "http" in promt:
        protacol = "http"
    else:
        return None

    obr = promt.split(protacol, 1)[1]

    if ' ' in obr:
        for inx in range(0, len(obr)):
            if obr[inx] == ' ':
                probel_pos = inx
                break

        for inx in range(0, probel_pos):
            url += obr[inx]
        return (protacol + url, obr)
    else: 
        return (protacol + obr, obr)

def recursive_scan_url(promt:str) -> list|None:
    datas = []

    while True:
        if "https" in promt or "http" in promt:
            result = scan_url(promt)
            if result: 
                datas.append(result[0])
                promt = result[1]
            else:
                return None
        else:
            return datas

def get_data_With_url(url:str):
    browser = launch(
    geoip=True,       # match timezone + locale to proxy IP
    headless=False,    # some sites detect headless even with C++ patches
    humanize=True,     # human-like mouse, keyboard, scroll
    )
    page = browser.new_page()

    referer = url.replace("https://", '').replace("http://", '').split("/", 1)[0]

    page.goto(url, wait_until="domcontentloaded")
    
    soup = BeautifulSoup(page.inner_text("body").replace("<hr>", "\n"), 'lxml')

    DEL_TAGS = ['head', 'script', 'button', 'link', 'picture', 'header', 'circle', 'article', 'dialog', 'kbd', 'aside', 'react-partial', 'meta', 'template', 'cookie-consent-link', 'react-app', 'turbo-frame']  
    OPEN_TAGS = ['body', 'html', 'span', 'div', 'svg', 'pre', 'path', 'input', 'a', 'nav', 'details', 'box', 'main', 'tool-tip', 'th', 'td', 'li', 'lu', 'tr', 'tbody', 'thead', 'ghcc-consent']

    # удалить коментарии
    for c in soup.find_all(string=lambda text: isinstance(text, Comment)):    
        c.extract()

    # убрать лишние теги
    for tag in soup.find_all(True):
        if tag.name in DEL_TAGS:
            tag.extract()
    
    # раскрыть некотрые теги
    for tag in soup.find_all(True):
        if tag.name in OPEN_TAGS:
            tag.unwrap()

    return str(soup).replace("<!---->", "").replace("<!DOCTYPE html>", "").strip()

def parsing_text_to_data(promt) -> dict|None:
    result = recursive_scan_url(promt)
    data_pack = {}

    if result:
        for url in result:
            try:
                data_pack[url] = get_data_With_url(url)[:2000]
            except Exception as e:
                logger.warning(e)
                data_pack[url] = "не удалось получить данные, игнорируй это и извенись за ошибку"
    else:
        return None

    return data_pack