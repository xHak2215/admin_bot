import sqlite3
from loguru import logger

import time
import traceback
import os
import json

def update_user(id, chat, reputation=None, ps_reputation=None, soob_num=None ,day_message_num=None ,reputation_time=None):
    # Создаем подключение к базе данных
    connection = sqlite3.connect('Users_base.db', timeout=5000)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL")

    # Формируем запрос для обновления
    query = "UPDATE Users SET "
    params = []
    updates = []
    
    if reputation is not None:
        updates.append("reputation = ?")
        params.append(reputation)
    
    if ps_reputation is not None:
        updates.append("auto_reputation = ?")
        params.append(ps_reputation)
    
    if soob_num is not None:
        updates.append("num_message = ?")
        params.append(soob_num)
        
    if day_message_num is not None:
        updates.append("day_message = ?")
        params.append(day_message_num)
        
    if reputation_time is not None:
        updates.append("auto_reputation_data = ?")
        params.append(reputation_time)
        
    # Проверяем, были ли добавлены параметры
    if not updates:
        connection.close()
        logger.warning("update_user Нет параметров для обновления.")
        return None
    
    query += ", ".join(updates)
    query += " WHERE warn_user_id = ? AND chat_id = ?"
    params.append(id)
    params.append(chat)
    
    try:
        cursor.execute(query, params)
        connection.commit()
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        return None
    finally:
        connection.close()
        
def data_base(chat_id, warn_user_id, nfkaz=0, soob_num=0, ps_reputation_upt=0, time_v=0) -> list: # data_base(message.chat.id,message.from_user.id,0,0,0) (вызов без изменения базы ) выход: [resperens,ps_reputation_new,int(soob_num),time.time()] (репутация,2 репутация_ps,каличество сообщений,время входа) 
    '''
    data_base(chat_id, warn_user_id, nfkaz=0, soob_num=0, ps_reputation_upt=0, time_v=0)
    
    взаимодействует с базой данных
    
    :param1: id чата
    
    :param2: id пользевателя
    
    :param3: количество отнимаемой репутации
    
    :param4: количество прибавляемых сообщений
    
    :param5: прибавление к авто/псевдо репутации
    
    :param6: дата входа задаеться при входе
    
    ## return
    
    ### list
    
    - 0-resperens — количество репутации
    
    - 1-ps_reputation_new — количество авто репутации 
    
    - 2-soob_num — количество сообщений
    
    - 3-time_v — дата входа если нет то возворощяет 0
    
    - 3-reputation_time — дана изменения авто репутации содержит `dict` словарь
    '''

    if ps_reputation_upt == 0:
        reputation_time=None
    else:
        reputation_time=time.time()
    
    resperens = 5
    # Создаем подключение к базе данных
    connection = sqlite3.connect('Users_base.db',timeout=10000)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA busy_timeout = 10000")  # Ждать разблокировки до 10 сек
    cursor.execute("PRAGMA cache_size = -50000")  # Кеш 50MB
    try:
        # Создаем таблицу (если она еще не существует)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            chat_id INTEGER NOT NULL,
            reputation INTEGER NOT NULL,
            warn_user_id INTEGER NOT NULL,
            warn_time INTEGER ,
            num_message INTEGER NOT NULL,
            day_message INTEGER NOT NULL,
            auto_reputation INTEGER NOT NULL,
            auto_reputation_data TEXT , 
            vhod_data INTEGER NOT NULL,
            temp REAL
        )
        ''')
        
        # Создаем индекс (если он еще не существует)
        cursor.execute('CREATE INDEX IF NOT EXISTS warn_user_id_index ON Users (warn_user_id)')
        
        # Проверяем, существует ли пользователь с данным warn_user_id
        cursor.execute('SELECT * FROM Users WHERE warn_user_id = ? AND chat_id = ?', (warn_user_id,chat_id))
        result = cursor.fetchone()
        ps_reputation_new=0+ps_reputation_upt
        
        if result is not None:
            # Извлекаем репутацию из результата
            current_reputation = result[2]  # репутация находится в третьем столбце
            ps_reputation = result[7]
            chat = result[1]  # id чата
            text = result[5] # кол.во сообщений
            vhod_data = result[9]
            day_message = result[6]
            
            if text is None:
                text=1
            if current_reputation is None:
                current_reputation=0

            if chat == chat_id:
                ps_reputation_new=ps_reputation+ps_reputation_upt
                new_reputation = current_reputation - nfkaz
                # Обновляем репутацию пользователя
                update_user(warn_user_id, chat, new_reputation, ps_reputation_new, text+soob_num ,result[6]+soob_num ,reputation_time)# Передаем id,chat и данные пользователя для обновления
                connection.commit()
                connection.close()
                return [new_reputation,ps_reputation_new,int(text+soob_num),vhod_data,reputation_time]# ,day_message
            else:
                resperens = 5 - nfkaz
                cursor.execute('INSERT INTO Users (chat_id, reputation, warn_user_id, num_message, auto_reputation, vhod_data ,day_message ,auto_reputation_data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (chat_id, resperens, warn_user_id, soob_num, ps_reputation_new, time_v, soob_num ,reputation_time))
                connection.commit()
                connection.close()
                return [resperens,ps_reputation_new,int(text+soob_num),time_v,reputation_time]# ,day_message
        else:
            # Если пользователь не найден, добавляем его
            resperens = 5 - nfkaz
            cursor.execute('INSERT INTO Users (chat_id, reputation, warn_user_id, num_message, auto_reputation, vhod_data ,day_message ,auto_reputation_data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (chat_id, resperens, warn_user_id, soob_num, ps_reputation_new, time_v, soob_num ,reputation_time))
            connection.commit()
            connection.close()
            return [resperens,ps_reputation_new,int(soob_num),time_v,reputation_time]

    except Exception as e:
        logger.error(f'Ошибка в операции с базой данных: {e}\n{traceback.format_exc()}')
        connection.close()
        return [None,None,None,None]  # Возвращаем None в случае ошибки
    finally:
        # Закрываем соединение
        connection.close()
        
def set_day_message():#я не смог это реализовать я походу тупой 
    file_path = os.path.join(os.getcwd(), 'asets', 'set_day_message_time.json')
    # Создаем папку asets, если её нет
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        if os.path.isfile(file_path):
            with open(file_path, "r") as json_settings:
                data = json.load(json_settings)
                timer = data.get('reset_time', 0)
        else:
            timer = 0
    except (json.JSONDecodeError, KeyError):
        timer = 0
    # Если таймер не установлен или прошло больше суток
    if timer == 0 or time.time() - timer >= 1*86400:
        # Обновляем базу данных
        connection = sqlite3.connect('Users_base.db', timeout=10)
        cursor = connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute('UPDATE Users SET day_message = 0')
        connection.commit()
        # Обновляем время последнего сброса
        try:
            with open(file_path, 'w') as json_settings:
                json.dump({"reset_time": time.time()}, json_settings)
            return True
        except IOError as e:
            logger.error(f"File write error: {e}")
            return False
    return False

class team_data_bese():
    def __init__(self):
        pass

    def team_bese_init(self,chat_id: int, team_name: str, users: list, team_info: dict) -> list:
        '''
        :param1: chat id

        :param2: team neme 

        :param3: users - список поьзователей где каждый элимент списка имеет словарь и информацией о пользователе `{'username':'@username', 'id'123456, 'in_time':13133.013, 'status':'user' }`

        :param4: team info информация о команде в формате словоря `{'creat_time':465456.2116, 'creator_id':12335444, 'creator_user_name':'username'}`

        :return: список с порамитрами 

        '''
        connection = sqlite3.connect('Users_base.db',timeout=10000)
        cursor = connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA busy_timeout = 10000")  # Ждать разблокировки до 10 сек
        cursor.execute("PRAGMA cache_size = -50000")  # Кеш 50MB

        # Создаем таблицу (если она еще не существует)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS team (
            id INTEGER PRIMARY KEY,
            chat_id INTEGER NOT NULL,
            team_name STRING NOT NULL,
            users STRING NOT NULL,
            team_info STRING NOT NULL
        )
        ''')
        
        # Создаем индекс (если он еще не существует)
        cursor.execute('CREATE INDEX IF NOT EXISTS team_name ON team (team_name)')
        cursor.execute('INSERT INTO team (chat_id, team_name, users, team_info) VALUES (?, ?, ?, ?)', (chat_id, team_name, json.dumps(users), json.dumps(team_info)))
        connection.commit()
        cursor.close()
        return [chat_id, team_name, json.dumps(users), json.dumps(team_info)]

    def upades(self, team_name, chat_id, users, team_info):
        connection = sqlite3.connect('Users_base.db',timeout=10000)
        cursor = connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA busy_timeout = 10000")  # Ждать разблокировки до 10 сек
        cursor.execute("PRAGMA cache_size = -50000")  # Кеш 50MB

        query = "UPDATE team SET "
        params = []
        updates = []
        
        if team_name:
            updates.append("team_name = ?")
            params.append(team_name)
        
        if users:
            updates.append("users = ?")
            params.append(json.dumps(users))
            print(123)
        
        if team_info:
            updates.append("team_info = ?")
            params.append(json.dumps(team_info))
            
        # Проверяем, были ли добавлены параметры
        if not updates:
            connection.close()
            logger.warning("update_user Нет параметров для обновления.")
            return[None,None,None,None]

        query += ", ".join(updates)
        query += " WHERE team_name = ? AND chat_id = ?"
        params.append(team_name)
        params.append(chat_id)
        
        try:
            cursor.execute(query, params)
            connection.commit()
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return[None,None,None,None]
        finally:
            connection.close()
            connection.close()

    def data_bese_colonium(self,c_name='team', colonium_name='team_name')->list|None:
        '''
        получение списка с данными определенной колонки
        '''
        connection = sqlite3.connect('Users_base.db',timeout=10000)
        cursor = connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA busy_timeout = 10000")  # Ждать разблокировки до 10 сек
        cursor.execute("PRAGMA cache_size = -50000")  # Кеш 50MB

        cursor.execute(f"SELECT {colonium_name} FROM {c_name}")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    
    def data_seah(self,chat_id:int, name:str)->list|None:
        '''
        получение данных определенной команды
        '''
        connection = sqlite3.connect('Users_base.db',timeout=10000)
        cursor = connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA busy_timeout = 10000")  # Ждать разблокировки до 10 сек
        cursor.execute("PRAGMA cache_size = -50000")  # Кеш 50MB

        cursor.execute('SELECT * FROM team WHERE team_name = ? AND chat_id = ?', (name, chat_id))#поиск
        data=cursor.fetchall()
        cursor.close()
        connection.close()
        data_list=[]
        for i in data:
            for a in i:
                data_list.append(a)
        return data_list
        
