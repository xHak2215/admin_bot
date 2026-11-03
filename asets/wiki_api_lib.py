import requests
import time
import json
from loguru import logger

class wiki: 
    def __init__(self):
        self.time_out = 20
        self.api_url = "https://ru.wikipedia.org/w/api.php"
        self.user_agent = {
        'User-Agent': 'Mozilla/5.0'
        }

    def api_url_edit(self,url):self.api_url=url
    def time_out_edit(self,time_out):self.time_out=time_out

    def search(self,promt)->str | None:
        params = {
            "action": "query",
            "titles": promt,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "format": "json"
        }
        response = requests.get(self.api_url, params=params,headers=self.user_agent,timeout=self.time_out)
        try:
            data = response.json()
        except json.decoder.JSONDecodeError as e:
            logger.error(f"error {e} data:{response}")
            return None
        # Извлечение текста статьи
        page = next(iter(data['query']['pages'].values()))
        return page['extract']

    def search_query(self,search_query,limit=5)->list | None:
        """
        ### получение статей по теме запроса

        :parm1: promt

        :parm2: лимит на количество предлагаемых статей

        return:
            список содержащий словори с ключами `page`-содержит заголовок найденой статьи , `link` - ссылку на найденую статью
        """
        params = {
            "action": "opensearch",
            "search": search_query,
            "limit": limit,
            "namespace": 0,
            "format": "json"
        }

        response = requests.get(self.api_url, params=params, headers=self.user_agent, timeout=self.time_out)
        try:
            data = response.json()
        except json.decoder.JSONDecodeError as e:
            logger.error(f"error {e} data:{response}")
            return None

        # Извлечение названий статей и ссылок
        titles = data[1]
        links = data[3]

        out_data=[]

        for title, link in zip(titles, links):
            out_data.append({'page':title, 'link':link}) 
        return out_data
    
    def title_to_page(self,title)->str|None:

        params = {
        "action": "query",
        "titles": title,
        "prop": "extracts",
        "explaintext": True,
        "format": "json"
        }

        response = requests.get(self.api_url, params=params, headers=self.user_agent, timeout=self.time_out)
        try :
            data = response.json()
        except json.decoder.JSONDecodeError as e:
            logger.error(f"error {e} data:{response}")
            return None

        # Извлечение текста статьи
        page = next(iter(data['query']['pages'].values()))
        return page.get('extract', None)
    
    def wiki_ping(self)->dict:
        """
        ### проверяет пинг wiki (`self.api_url`)
        

        возврощяет словарь с ключами `time_out` -время задержки , `code` - статус код при ошибках `None`, `error` - ошибка если ее нет но `None`
        """
        t=time.time()
        try:
            response=requests.get(self.api_url, timeout=self.time_out,headers=self.user_agent)
        except Exception as e:
            return {'time_out':time.time()-t,'code':None,'error':e}
        return {'time_out':time.time()-t,'code':response.status_code,'error':None}
    

def test():
    api=wiki()

    promt='привет'

    print("ping:",api.wiki_ping())
    print("searh:",api.search(promt))
    print("page:",api.search_query(promt))
    
#test()

