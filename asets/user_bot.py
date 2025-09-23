import os
import json
import asyncio
import traceback
import pickle

from loguru import logger
from fastapi import FastAPI
import telethon
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import Channel, Chat, User

# Загрузка конфигурации
try:
    with open(os.path.join(os.getcwd(), 'asets', "user_bot_config.json"), "r") as json_settings:
        settings = json.load(json_settings)
except Exception as e:
    logger.debug('Error loading settings: ' + str(e))
    exit(1)

# Ваши данные
api_id = settings['API_ID']
api_hash = settings["API_HASH"]
phone_number = settings["PHONE_NUMBER"]
login_password = settings["passworld"]

app = FastAPI()

class Sigin:
    def __init__(self):
        self.client = TelegramClient('user_session', api_id, api_hash)

data = Sigin()

# Инициализация клиента
# Загрузка сессии
def load_session():
    try:
        with open('session.dat', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

# Сохранение сессии
def save_session(session):
    with open('session.dat', 'wb') as f:
        pickle.dump(session, f)

# Инициализация клиента
async def init():
    session = load_session()
    if session:
        data.client.session = session
    await data.client.start()
    if not data.client.is_user_authorized():
        await data.client.sign_in(phone_number)
        code = input("Введите код: ")
        await data.client.sign_in(code=code)
        save_session(data.client.session)

# Получение информации о пользователе
async def get_user_id(usernames: str) -> dict:
    try:
        if not usernames:
            logger.info("❌ Username не может быть пустым")
            return {"id":None, "username": None, "name": None, "error": "no username"}

        usernames = usernames.replace('@', '').replace(' ', '')
        client = data.client

        try:
            await client.connect()
            await asyncio.sleep(1)  # Задержка на 1 секунду
        except Exception as e:
            logger.info(f"❌ Ошибка подключения: {str(e)}")
            return {"id":None, "username": None, "name": None, "error": "error connect"}
        try:
            user = await client.get_entity(usernames)
        except telethon.errors.rpcerrorlist.UsernameInvalidError:return {"username": None, "name": None, "error": "error incorrect username"}
        logger.info(f"👤 Username: @{user.username}, 🆔 ID: {user.id}, 📛 Имя: {user.first_name}")
        return {"id":user.id,"username": user.username, "name": user.first_name, "error": None}

    except ValueError:
        logger.info(f"❌ Пользователь @{username} не найден")
        return {"id":None, "username": None, "name": None, "error": "username не найден"}

    except Exception as e:
        logger.info(f"❌ Ошибка авторизации: {str(e)}\n{traceback.format_exc()}")
        return {"id":None, "username": None, "name": None, "error": "error sign in"}
    
async def get_file_data(file_id):
    client = data.client
    file = await client.get_entity(file_id)
    if file.document:
        file = file.document
        fdata = await client.download_media(file)
        return {
            'id': file.id,
            'name': file.file_name,
            'size': file.size,
            'mime_type': file.mime_type,
            'data':fdata,
            'error':None
        }
    else:
        return {
            'id': None,
            'name': None,
            'size': None,
            'mime_type': None,
            'data': None,
            'error':'error the not document'
        }
    

async def get_members_advanced(chat_id:int)->dict:
    client = data.client

    try:
        entity = await client.get_entity(chat_id)
    except ValueError:
        return {'error':'the not chat', 'user_list':None}
        
    # Проверяем тип entity
    if not isinstance(entity, (Channel, Chat)):
        return {'error':'the not chat', 'user_list':None}
    
    user_list=[]
    async for user in client.iter_participants(entity):
        print(user)
        # Определяем тип участника
        user_type = ""
        if user.bot: user_type ="bot"
        elif user.admin_rights: user_type ="admin" 
        elif user.creator: user_type = "creator"
        else: user_type = "user"

        user_list.append({'type': user_type, 
                          'id': user.id, 
                          'user_name': user.username, 
                          'first_name': user.first_name, 
                          'last_name': user.last_name,
                          'phone_number': user.phone
                          })
    
    return {'error':None, 'user_list':user_list}

# Обработчик FastAPI
@app.on_event("startup")
async def startup_event():
    await init()

@app.get("/")
def ping():
    return 200

@app.get("/get_user")
async def get_user(user_name: str):
    return await get_user_id(user_name)

@app.get("/get_user_chat")
async def get_chat(chat_id:int):
    return await get_members_advanced(chat_id)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8800)  # Запуск FastAPI
