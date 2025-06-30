import os
import os.path
import json
import re
import sys
import time
import random
from datetime import timedelta
from datetime import datetime
import traceback
from collections import Counter
#import threading
import io
import binascii

import asets.ffmpeg_tool

try:
    from vosk import Model, KaldiRecognizer
    import telebot
    from telebot import types
    from telebot.types import InlineKeyboardButton
    from telebot import formatting , util
    from collections import defaultdict
    import psutil
    import schedule
    import requests
    from requests import get
    import subprocess
    from loguru import logger
    import sqlite3
    from PIL import Image, ImageDraw, ImageFont
    from googletrans import Translator
except ImportError:
    print('\33[31m error no libs start auto install (не найдены нужные библиотеки запускаю авто установку)')
    print('full error message>>\n'+traceback.format_exc())
    i=0
    if os.name == 'nt':
        if not os.path.exists(os.path.join(os.getcwd(), 'virtual')):
            print('\33[0m Created venv')
            i=i+os.system('python -m venv virtual')
        print('\33[0m pip upgrade')
        i=i+os.system(os.path.join(os.getcwd(), 'virtual','Scripts','python')+'-m pip install --upgrade pip')
        print('\33[0m libs install')
        i=i+os.system(os.path.join(os.getcwd(), 'virtual','Scripts','pip3')+' -r requirements.txt')
        if i < 1:
            print('\33[32m suppress (успешно)')
        else:
            print('\33[31m error install (что то пошло не так )')
    else: 
        print('\33[0m Created venv')
        i=i+os.system('python3 -m venv virtual')
        print('\33[0m pip upgrade')
        i=i+os.system(os.path.join(os.getcwd(), 'virtual','bin','python3')+" -m pip install --upgrade pip")
        print('\33[0m libs install')
        i=i+os.system(os.path.join(os.getcwd(), 'virtual','bin','pip3')+' install -r requirements.txt') 
        if i<1:
            print('\33[32m suppress (успешно)')
        else:
            print('\33[32m error install (что то пошло не так )')

try:
    with open("TOKEN", "r") as t:
        TOKEN=t.read().replace(' ','')
except FileNotFoundError:
    print('\33[31m error no file TOKEN ,the file auto creat please write you token to file TOKEN \33[0m')
    with open(os.path.join(os.getcwd(), 'TOKEN'), 'w') as f:
        f.write('please write you token')
    sys.exit(1)
    
def umsettings():
    global bambam,DELET_MESSADGE,admin_grops,SPAM_LIMIT,SPAM_TIMEFRAME,BAN_AND_MYTE_COMMAND,CONSOLE_CONTROL
    bambam=False
    DELET_MESSADGE=True
    admin_grops="-1002284704738"
    SPAM_LIMIT = 10 # Максимальное количество сообщений
    SPAM_TIMEFRAME = 4  # Время в секундах для отслеживания спама
    BAN_AND_MYTE_COMMAND = True
    CONSOLE_CONTROL = False
    AUTO_TRANSLETE = False

try:
    with open("settings.json", "r") as json_settings:
        settings= json.load(json_settings)
except:
    logger.debug('error settings import ')
    umsettings()
    
help_user = '/report — забань дебила в чате\n/я — узнать свою репутацию и количество сообщений\n/info — узнать информацию о пользователе\n/translite (сокращено /t) — перевод сообщения на русский перевод своего сообщения на другой язык:<code>/t любой текст:eg</code> поддерживаться bin и hex кодировки\n/download (сокращено /dow) — скачивание стикеров,ГС и аудио дорожек видео при скачивании можно изменить формат пример: <code>/download png</code> для дополнительный инструкций введите <code>/download -help</code> \n/to_text — перевод ГС в текст\nЕсли есть вопросы задайте его добавив в сообщение [help] и наши хелперы по возможности помогут вам \n/admin_command команды администраторов' 
admin_command = '/monitor — показатели сервера \n/warn — понижение репутации на 1\n/reput — повышение репутации на 1\n/data_base — вся база данных\n/info — узнать репутацию пользователя\n/ban — отправляет в бан пример: <code>/бан reason:по рофлу</code>\n/мут — отправляет в мут <code>/мут reason:причина time:1.h</code>\n .h — часы (по умолчанию) , .d — дни , .m — минуты\n/blaklist — добавляет стикер в черный список\n/unblaklist — убирает стикер из черного списка'

logse="nan"
i=0
admin_list=["@HITHELL","@mggxst"]
random.seed(round(time.time())+int(round(psutil.virtual_memory().percent)))#создание уникального сида

# Инициализация логирования
logger.add("cats_message.log", level="TRACE", encoding='utf-8', rotation="500 MB")
try:
    bambam=bool(settings['bambam'])
    DELET_MESSADGE=bool(settings['delet_messadge'])
    admin_grops=str(settings['admin_grops'])
    SPAM_LIMIT=int(settings['spam_limit'])
    SPAM_TIMEFRAME=int(settings['spam_timer'])
    BAN_AND_MYTE_COMMAND=bool(settings['ban_and_myte_command'])
    CONSOLE_CONTROL=bool(settings['console_control'])
    AUTO_TRANSLETE=dict(settings['auto_translete'])
except:
    umsettings()
    logger.debug('error settings init')

bot = telebot.TeleBot(TOKEN)
#updater = Updater(token=TOKEN)
#dispatcher = updater.dispatcher
warn=0
print('\33[0m'+os.getcwd())

if os.path.exists(os.path.join(os.getcwd(), 'asets' ,'hello.gif')):
    print('gif OK')
else:
    warn=warn+1
    print('error no hello.gif')
if os.path.exists(os.path.join(os.getcwd(), 'asets' ,'blacklist.json')):pass
else:
    warn=warn+1
if os.path.exists(os.path.join(os.getcwd(), 'settings.json')):
    print('settings.json OK')
else:
    warn=warn+1
    print('error no settings.json')
if os.path.exists(os.path.join(os.getcwd(), 'requirements.txt')) != True:
    warn=warn+1
if os.path.exists(os.path.join(os.getcwd(), 'Users_base.db')):
    print('data base ok')
else:
    warn=warn+1
    print("error no bata base ")
if warn >=3:
    bot.send_message(admin_grops, f"обнаружены не критичные ошибки возможны неполадки\nwarn level:{warn}")

date = datetime.now().strftime("%H:%M")

bot.send_message(admin_grops, f"бот запущен ")
logger.info("бот запущен")
    
# Функция для мониторинга ресурсов
def monitor_resources():
    response_time,response_time,cpu_percent,ram_percent,disk_percent=0,0,0,0,0
    popitki=5
    #пинг в среднем 5 (можно изменять в popitki )попыток
    for i in range(popitki):
        start_time = time.time()
        response=requests.get('https://core.telegram.org/')
        if response.status_code==200:
            scode= ''
            pass
        else:
            scode=f' status code {response.status_code}'
        response_time+= time.time() - start_time
        cpu_percent += float(psutil.cpu_percent())
        ram_percent +=float(psutil.virtual_memory().percent)
        if sys.platform.startswith('win'):
            disk_percent +=float(psutil.disk_usage('C:/').percent)
        else:
            disk_percent +=float(psutil.disk_usage('/').percent)
    shutka=' '
    if cpu_percent==round(cpu_percent/popitki,1):
        shutka='процессор шя рванет 🤯'
    print(f"CPU: {round(cpu_percent/popitki)}%,\nRAM: {round(ram_percent/popitki)}%,\nDisk: {round(disk_percent/popitki)}%,\nPing: {response_time} \n{shutka}")
    return round(cpu_percent/popitki,1), round(ram_percent/popitki,1), round(disk_percent/popitki,1), str(str(round(response_time/popitki,3))+'s'+scode+f'\n{shutka}')

# Команда /help
@bot.message_handler(commands=['help','помощь','sos'])
def send_help(message):
    if message.date - time.time() <= 60:
        bot.reply_to(message, help_user ,parse_mode='HTML')

@bot.message_handler(commands=['admin_command'])
def handle_warn(message):
    if message.date - time.time() <= 60:
        bot.reply_to(message, admin_command ,parse_mode='HTML')
    
# Команда /log
@bot.message_handler(commands=['log'])
def send_help(message):
    try:
        bot.send_document(message.chat.id,reply_to_message_id=message.message_id,document=open('cats_message.log', 'r',encoding='utf-8', errors='replace'))
    except Exception as e:
        bot.send_message(admin_grops,f"error logs file>> {e} ")
        logger.error(f"log error >> {e}")
        
#очищение логов /null_log
@bot.message_handler(commands=['null_log'])
def send_help(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator'] or message.from_user.id =='5194033781':
        try:
        #проверка на админа
            if message.chat.id==admin_grops or message.from_user.id =='5194033781':
                if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator']:
                    bot.send_message(admin_grops,f"логи очищены очистил : @{message.from_user.username}")
                    file = open('cats_message.log', "w")
                #    Изменяем содержимое файла
                    file.write("log null")
                    # Закрываем файл
                    file.close()
                    logger.debug(f"логи очищены, очистил:  @{message.from_user.username}")
                else:
                    bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])
            else:
                bot.reply_to(message,'команда доступна только из группы администрации')
        except Exception as e:
            bot.send_message(admin_grops,f"error logs file>> {e} ")
            logger.error(f"log null error >> {e}")
    else:
        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])
#очищение списка репортов  /null_report
@bot.message_handler(commands=['null_report'])
def send_help(message):
    try:
        #проверка на админа
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator'] or message.from_user.id =='5194033781':
            try:
                del report_data
            except:
                pass
            bot.send_message(admin_grops,f"report очищен очистил : @{message.from_user.username}")
            logger.debug(f"report очищен, очистил:  @{message.from_user.username}")
        else:
            bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])
    except Exception as e:
        bot.send_message(admin_grops,f"error >> {e} ")
        logger.error(f"error >> {e}")
        
#report data список с кол.во. репортами /report_data 
@bot.message_handler(commands=['report_data'])
def send_help(message):
    try:
        #проверка на админа
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator'] or message.from_user.id =='5194033781':
            bot.send_message(message.chat.id,f"report data: {report_data}")
            logger.debug(f"report data: {report_data}")
        else:
            bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет','такие данные не для тебя'][random.randint(0,4)])
    except Exception as e:
        bot.send_message(admin_grops,f"error >> {e} ")
        logger.error(f"error >> {e}")
# очистка консоли /cler 
@bot.message_handler(commands=['cls','clear'])
def send_help(message):
    #проверка на админа
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator'] or message.from_user.id =='5194033781': 
            bot.send_message(admin_grops,f"экран очищен, очистил : @{message.from_user.username}")
            os.system('clear')
            logger.debug(f"экран очищен очистил:  @{message.from_user.username}")
    else:
        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])

# Команда /monitor    
@bot.message_handler(commands=['monitor','монитор'])
def monitor_command(message):
    if message.date - time.time() <= 60:
        cpu_percent, ram_percent, disk_percent, response_time = monitor_resources()
        bot.reply_to(message, f"CPU: {cpu_percent}%\nRAM: {ram_percent}%\nDisk: {disk_percent}%\nPing: {response_time}")

# Команда /test 
@bot.message_handler(commands=['test'])
def monitor_command(message):
    test=''
    test+=os.getcwd()+'\n'
    swap = psutil.swap_memory()
    if os.path.exists(os.path.join(os.getcwd(), 'asets', 'hello.gif')):
        test=test+'gif OK\n'
    else:
        test=test+'error no gif\n'
    if os.path.exists(os.path.join(os.getcwd(), 'Users_base.db')):
        test=test+'data base OK\n'
    else:
        test=test+"error no bata base \n"
    if os.path.exists(os.path.join(os.getcwd(), 'cats_message.log')):
        test=test+'messege log OK\n'
    else:
        test=test+'warning no messege log \n'
    if os.path.exists(os.path.join(os.getcwd(), 'asets' , 'Roboto_Condensed-ExtraBoldItalic.ttf')):
        test=test+'Roboto_Condensed-ExtraBoldItalic шрифт OK\n'
    else:
        test=test+'error no Roboto_Condensed-ExtraBoldItalic \n'
    if os.path.exists(os.path.join(os.getcwd(),'settings.json')):
        test=test+'cofig file OK\n'
    else:
        test=test+'error no config file \n'
                # Определяем путь к ffmpeg
    if sys.platform.startswith('win'):
        ffmpeg=os.path.join(os.getcwd(), 'asets' ,'ffmpeg-master-latest-win64-gpl-shared','bin','ffmpeg.exe') # для windows
    else:
        ffmpeg=os.path.join(os.getcwd(), 'asets' ,'ffmpeg-master-latest-linuxarm64-lgpl','bin','ffmpeg') # для Linux    
    if os.path.exists(ffmpeg):
        test=test+'ffmpeg OK\n'
    else:
        test=test+'error no ffmpeg\n'
    test=test+f"ID> {message.from_user.id}\n"
    test=test+f"ID admin grup> {admin_grops}\n"
    test=test+f"IP>{get('https://api.ipify.org').content.decode('utf8')}\n"
    cpu_percent, ram_percent, disk_percent, response_time = monitor_resources()
    bot.send_message(message.chat.id, f"CPU: {cpu_percent}%\nRAM: {ram_percent}%\nDisk: {disk_percent}%\nPing: {response_time}\nфайл подкачки: {swap.percent}% ({swap.total / 1073741824:.2f} GB)\n{test} \nadmin > {bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator']}")

# Команда /time_server
@bot.message_handler(commands=['time_server'])
def time_server_command(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    bot.send_message(message.chat.id, f"Серверное время: {current_time}")    
#команда /правило 
@bot.message_handler(commands=['правило','правила','закон','rules'])
def pravilo(message):
    if message.date - time.time()<=60:
        pass
    #    markup = types.InlineKeyboardMarkup()
    #    button1 = types.InlineKeyboardButton("правила", url='https://xhak2215.github.io/aea_rules.github.io/')
    #    markup.add(button1)
    #    bot.reply_to(message, 'правила перенесены на web страницу', reply_markup=markup)
    
# Хранение данных о репортах
report_data =  {}
report_user=[]
# Обработка ответа на сообщение с /report
@bot.message_handler(commands=['report','репорт','fufufu'])
def handle_report(message):
    n=5
    if message.reply_to_message:
        chat_id = message.chat.id#инециалезацыя всякой хрени
        reported_message_text = message.reply_to_message.text
        report_user.append(message.from_user.id)
        if chat_id not in report_data:#проверка на существования пометки chat_id
            report_data[chat_id] = {'responses': set()}
            
        report = report_data[chat_id]
        #добавляем id балбеса or нарушителя в тетрадь смерти Сталина report
        report['responses'].add(message.reply_to_message.from_user.id) 
        ban_ded=message.reply_to_message.from_user.id
        report_chat=message.chat.id
    
        message_to_report=str(report_chat).replace("-100", "")
        if len(report['responses'])>1:
            data_base(chat_id,message.reply_to_message,ps_reputation_upt=1)
        coment_message=''
        coment=message.text.replacce('/репорт','').replacce('/report','').replacce('/fufufu','').split(' ')
        if len(coment)>1:
            if len(coment[1])>2 and coment[1]!='':
                coment_message=f'| комментарий:{coment[1]}'

        if message.reply_to_message.content_type == 'sticker':
            bot.send_message(admin_grops,f"послали репорт на >> tg://user?id={message.reply_to_message.from_user.id}, @{message.reply_to_message.from_user.username} {coment_message}| https://t.me/c/{message_to_report}/{message.reply_to_message.message_id} | ↓стикер↓")
            logger.info(f"послали репорт на >>  @{message.reply_to_message.from_user.username} {coment_message}| https://t.me/c/{message_to_report}/{message.reply_to_message.message_id} стикер id > {message.reply_to_message.sticker.file_id}")
            bot.send_sticker(admin_grops, message.reply_to_message.sticker.file_id)
        else:
            bot.send_message(admin_grops,f"послали репорт на >> tg://user?id={message.reply_to_message.from_user.id}, @{message.reply_to_message.from_user.username} {coment_message}| https://t.me/c/{message_to_report}/{message.reply_to_message.message_id} | сообщение>> {reported_message_text if message.content_type == 'text' else message.content_type}")
            logger.info(f"послали репорт на >>  @{message.reply_to_message.from_user.username} {coment_message}| https://t.me/c/{message_to_report}/{message.reply_to_message.message_id} сообщение>> {reported_message_text if message.content_type == 'text' else message.content_type}")
        bot.reply_to(message,['админы посмотрят','амон уже в пути','да придет же админ и покарает нечестивцев баном','кто тут нарушает?','стоять бояться работает админ','записал ...'][random.randint(0,4)])
        # Проверяем, достаточно ли ответов для бана
        reput=data_base(message.chat.id,ban_ded)[1]
        if reput > 2:
            n=4
        elif reput < 0:
            n=6
        else:
            n=5
        if len(report['responses']) >= n:
            for i in range(len(report_user)):
                data_base(message.chat.id,report_user[i],ps_reputation_upt=-1)
#           bot.kick_chat_member(chat_id, user_to_ban, until_date=int(time.time()) + 86400)
            for i in range(len(admin_list)):
                if i >0:
                    teg+=f",{admin_list[i]}"
                else:
                    teg+=f"{admin_list[i]}"
            bot.send_message(admin_grops,f"{teg} грубый нарушитель ! >> @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_report}/{message.reply_to_message.message_id}")
            if DELET_MESSADGE:
                bot.delete_message(message.chat.id,message.message_id)
        # Удаляем данные о репорте
        del report_data[chat_id]
    else: 
        bot.reply_to(message, "Пожалуйста, ответьте командой на сообщение, нарушающее правила, чтобы сообщить о нарушении.")

def fetch_data_by_column_and_row(column_name, row_index):
    # Создаем подключение к базе данных
    connection = sqlite3.connect('Users_base.db')
    cursor = connection.cursor()
    try:
        # Выполняем запрос для получения данных из указанного столбца по индексу строки
        query = f'SELECT {column_name} FROM Users LIMIT 1 OFFSET ?'
        cursor.execute(query, (row_index,))  # Передаем индекс как кортеж
        result = cursor.fetchone()  # Получаем первую строку результата
        if result:
            return result[0]  # Возвращаем значение или None, если не найдено
        else:
            return None
    except sqlite3.Error as e:
        logger.error(f'get data base error >> {e}')
        return 'get data base error >>'+e
    
@bot.message_handler(commands=['config','настройки'])
def configfile(message):
    try:
        f=open(f'{os.getcwd()}/settings.json', 'r',encoding='utf-8', errors='replace')
        out=f.read()
        if out=='' or out==None:
            out='none'
        bot.reply_to(message,out)
        f.close()
        if  '-r' in message.text :
            try:
                with open("settings.json", "r") as json_settings:
                    settings= json.load(json_settings)
                try:
                    bambam=bool(settings['bambam'])
                    DELET_MESSADGE=bool(settings['delet_messadge'])
                    admin_grops=str(settings['admin_grops'])
                    SPAM_LIMIT=int(settings['spam_limit'])
                    SPAM_TIMEFRAME=int(settings['spam_timer'])
                    BAN_AND_MYTE_COMMAND=bool(settings['ban_and_myte_command'])
                    CONSOLE_CONTROL=bool(settings['console_control'])
                    logger.info('настройки пере инициалезированы')
                except:
                    bot.reply_to(message,'не удалось использованы настройки по умолчанию ')
                    umsettings()
                    logger.debug('error settings init')
            except:
                bot.reply_to(message,'не удалось прочитать файл настроек')
                logger.debug('error settings reload ')
    except Exception as e:
        try:
            f.close()
        except:pass
        bot.reply_to(message,f"error logs file>> {e} ")
        logger.error(f"config error >> {e}")

@bot.message_handler(commands=['data_base'])
def send_help(message):
    datas=''
    try:
        #проверка на админа
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id ==5194033781:
            connection = sqlite3.connect('Users_base.db')
            cursor = connection.cursor()
            # Получаем информацию о столбцах в таблице Users
            cursor.execute('SELECT * FROM Users')
            rows = cursor.fetchall() 
            # Печатаем информацию о столбцах
            for column in rows:
                datas += str(column)+'\n'
            connection.close()
            bot.send_message(message.chat.id,f"data base>>\n№ | chat id |r| user id|num_message|ar|data\n----------------------------------------\n{datas}")
            logger.debug(f"база данных :\n{datas}")
        else:
            bot.reply_to(message,f"ты не достоин \nты не админ")
    except Exception as e:
        bot.send_message(admin_grops,f"error >> {e} ")
        logger.error(f"error >> {e}")
        
def update_user(id, chat, reputation=None, ps_reputation=None, soob_num=None ,day_message_num=None ,reputation_time=None):
    # Создаем подключение к базе данных
    connection = sqlite3.connect('Users_base.db', timeout=10)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")

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
    
    return
    
    list
    
    0-resperens -- количество репутации
    
    1-ps_reputation_new -- количество авто репутации 
    
    2-soob_num -- количество сообщений
    
    3-time_v -- дата входа если нет то возворощяет 0
    
    3-reputation_time -- дана изменения авто репутации содержит `dict` словарь
    '''

    if ps_reputation_upt == 0:
        reputation_time=None
    else:
        reputation_time=time.time()
    try:
        resperens = 5
        # Создаем подключение к базе данных
        connection = sqlite3.connect('Users_base.db',timeout=10)
        cursor = connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")

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
        bot.send_message(admin_grops, f"data_base error>> {e}")
        return None  # Возвращаем None в случае ошибки
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
        try:
            # Обновляем базу данных
            connection = sqlite3.connect('Users_base.db', timeout=10)
            cursor = connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute('UPDATE Users SET day_message = 0')
            connection.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            if connection:
                connection.close()
        # Обновляем время последнего сброса
        try:
            with open(file_path, 'w') as json_settings:
                json.dump({"reset_time": time.time()}, json_settings)
            return True
        except IOError as e:
            print(f"File write error: {e}")
            return False
    return False
    
def status(rec):
    if rec >= 1000:
        status=["читы вырубай ! ",'как то многовато ,читы ?'][random.randint(0,1)]
    elif rec <=1:
        status=["ты плохой исправляйся 😡",'ай ай ай нарушаем','фу таким быть','а ну не нарушай ','зачем нарушал правил что ли не знаешь'][random.randint(0,4)]
    elif rec>=5:
        status=['ты хороший 😊','ты умница 👍','законопослушый так держать! ','харош'][random.randint(0,2)]
    elif rec>=10:
        status=['партия гордиться вами','благодарю за твой вклад товарищ!','ты хороший 😊','ты умница 👍'][random.randint(0,3)]
    elif rec<=0:
        status=['ну это бан','в бан тебя','ай ай ай bam bam bam ждет тебя'][random.randint(0,2)]
    elif rec==None:
        status='ошибка получения данных '
    else:
        status=["😐",'ну норм','нейтральный','не без греха'][random.randint(0,3)]
    return status

@bot.message_handler(commands=['я', 'me'])
def send_statbstic(message):
    if message.date - time.time()<=60:
        data=data_base(message.chat.id,message.from_user.id,soob_num=1)
        bot.reply_to(message, f"Твоя репутация: {data[0]} \n{status(data[0])}\nколичество сообщений: {data[2]}")

warn_data= {}
# Обработка ответа на сообщение /warn
@bot.message_handler(commands=['warn'])
def handle_warn(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id==5194033781:
        if message.reply_to_message:

            chat_id = message.chat.id#инециалезацыя всякой хрени
            warn_message = message.reply_to_message.from_user.id
            warn_message_text = message.reply_to_message.text
            message_to_warp=str(chat_id).replace("-100", "")

            reputation=data_base(message.chat.id,warn_message,1,ps_reputation_upt=2)[0]
            bot.reply_to(message,f'репутация снижена \nтекущяя репутация пользевателя:{reputation}')
            bot.send_message(admin_grops,f"репутация снижена >> tg://user?id={message.reply_to_message.from_user.id}, @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} | сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.debug(f"репутация снижена >>  @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.info(f"Пользователь @{message.from_user.username} понизил репутацию @{message.reply_to_message.from_user.username} ") 
        
        # Проверяем, достаточно ли маленькая репутация для мута
            if bambam==True:
                if reputation <= 0:
                    #Ограничиваем пользователя на 24 часа 
                    bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    until_date=timedelta(hours=24),
                    can_send_messages=False
                    )
                    bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} получил мут на 24 часа за нарушение.")
                    logger.info(f"Пользователь {message.reply_to_message.from_user.username} получил мут на 24 часа за нарушение.")        
#           bot.kick_chat_member(chat_id, user_to_ban, until_date=int(time.time()) + 86400)
                bot.send_message(admin_grops,f"грубый нарушитель ! >> tg://user?id={warn_message} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id}")
        else:
            bot.reply_to(message, "Пожалуйста, ответьте командой на сообщение, нарушающее правила, чтобы снизить репутацию") 
    else:
        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])
                    
@bot.message_handler(commands=['reput'])
def handle_warn(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id ==5194033781:
        if message.reply_to_message:
            #инециалезацыя всякой хрени 
            warn_message_text = message.reply_to_message.text
            user=message.reply_to_message.from_user.id
            warn_chat=message.chat.id
            message_to_warp=str(warn_chat).replace("-100", "")

            data=data_base(message.chat.id,user,-1,0,-2)#партия довольна вами +1 к репутации
            bot.reply_to(message,f'репутация повышена \nтекущяя репутация пользевателя:{data[0]}')
            bot.send_message(admin_grops,f"репутация повышена >> tg://user?id={message.reply_to_message.from_user.id}, @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} | сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.debug(f"репутация повышена >>  @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.info(f"Пользователь @{message.from_user.username} повысил репутацию ") 
        else: 
            bot.reply_to(message, "Пожалуйста, ответьте командой на сообщение, чтобы повысить репутацию")  
    else:
        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])
        
@bot.message_handler(commands=['info','user'])#узнать репутацию
def handle_warn(message):
#    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id ==5194033781:
    if message.reply_to_message:
        data_v=''
        i=0
        c=''
        chat_id = message.chat.id# инециалезацыя всякой хрени 
        user=message.reply_to_message.from_user.id
        #message_to_warp=str(warn_chat).replace("-100", "")
        data=data_base(chat_id,user)
        if '-all' in str(message.text).lower():
            bot.reply_to(message,f'ID:{user}\nрепутация:{data[0]}\nавто репутация:{data[1]}\nсообщение:{data[2]}\ntime:{datetime.fromtimestamp(data[3]).strftime('%Y-%m-%d %H:%M:%S')}')
            return
        if str(data[3]) != str(0):
            if data[3]>=86400:
                if round((time.time()-data[3])/86400)==1:
                    c='день назад'
                else:
                    c='дней назад' 
                i=str(round((time.time()-data[3])/86400))+ c
            elif data[3]>=3600:
                if round((time.time()-data[3])/3600)==1:
                    c='час назад'
                else:
                    c='часов назад' 
                i=str(round((time.time()-data[3])/3600))+ c
            else:
                data_v=f'\nзащел в чат {datetime.fromtimestamp(data[3]).strftime('%Y-%m-%d %H:%M:%S')} ({i})'
        bot.reply_to(message,f'текущая репутация пользователя:{data[0]}\nсообщения:{data[2]}') # \nза день:{data[4]}{data_v}
    else: 
        bot.reply_to(message, "Пожалуйста, ответьте командой на сообщение, чтобы узнать репутацию и количество сообщений")  
#    else:
#        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])

@bot.message_handler(commands=['гойда','goida'])
def handle_goida(message):
    if time.time() - message.date <= 60:
        rand=random.randint(0,4)
        if rand==0:bot.reply_to(message,'наш слон')
        elif rand==1:bot.reply_to(message,'ГООООООЛ')
        elif rand==2:bot.reply_to(message,'да будет же гойда')
        elif rand==3:bot.reply_to(message,'держи гойду')
        elif rand==4:bot.send_photo(message.chat.id,io.BytesIO(requests.get('https://soski.tv/images/thumbnails/76828318.jpg').content),reply_to_message_id=message.message_id)
        
@bot.message_handler(commands=['bambambam'])
def handle_warn(message):
    if time.time() - message.date >= 60:
        return
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id ==5194033781:
        if message.reply_to_message:
            if message.from_user.id =='5806296576':
                bot.reply_to(message,['маге не понравилось','мага покарай нарушителей мутом!'][random.randint(0,1)])
            else:
                bot.reply_to(message,["кто то похоже себя плохо вел",'ай ай ай','анука что они там тварят','что то случилось?'][random.randint(0,3)])
        else:
            if message.from_user.id =='5806296576':
                bot.reply_to(message,['мага что такое','кто то опять беспредельничяет'][random.randint(0,1)])
            else:    
                bot.reply_to(message,['что то случилось мистер админ','bam bam бум бум','глдавное не спамь!','ану ка что тут такого'][random.randint(0,3)])
    else:
        bot.reply_to(message,['что тебе нужно','кто то плохо себя вел?','главное не спамь !','боньк',][random.randint(0,3)])
# Периодическое напоминание
def send_reminder():
    chat_id = '-1002170027967'# Укажите ID чата для отправки напоминаний
    bot.send_message(chat_id, '')
# Планирование напоминаний
#schedule.every().day.at("12:00").do(send_reminder)

@bot.message_handler(commands=['ban','бан'])
def handle_warn(message):
        commad=str(message.text).lower()
        if BAN_AND_MYTE_COMMAND !=True:
            bot.reply_to(message,'отключено , для включения задайте парамитер (в settings.json) ban_and_myte_command как true')
            return
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id ==5194033781:
            if message.reply_to_message:
                if 'reason:' in commad:
                    reason=commad.split('reason:')[1]
                else :
                    bot.reply_to(message,'SyntaxError\nнет аргумента reason:\nпример:`/бан reason:причина`')
                try:
                    bot.ban_chat_member(message.chat.id,message.reply_to_message)
                    logger.info(f'ban for {message.reply_to_message.from_user.username}\nreason:{reason}')
                    bot.send_message(admin_grops,f'ban for {message.reply_to_message.from_user.username}\nreason:{reason}')
                except telebot.apihelper.ApiTelegramException:
                    bot.reply_to(message,'error>> elebot.apihelper.ApiTelegramException\nвероятно у бота недостаточно прав')
            else:bot.reply_to(message,'Пожалуйста, ответьте командой на сообщение, чтобы выдать бан')
        else:
            bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет','ты думал сможешь взять и забанить наивный'][random.randint(0,5)])

@bot.message_handler(commands=['mute','мут'])
def handle_warn(message):
        commad=str(message.text).lower()
        if BAN_AND_MYTE_COMMAND !=True:
            bot.reply_to(message,'отключено , для включения задайте парамитер (в settings.json) ban_and_myte_command как true')
            return
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id ==5194033781:
            if message.reply_to_message:
                wirning=None
                if 'reason:' in commad and 'time:'in commad:
                    finds = re.findall(r'(\breason:\b|\btime:\b)', commad, re.IGNORECASE)
                    if format(finds[0])== 'reason:':
                        arg=commad.replace("/mute", "").replace("/мут", "").split('time:')
                        timer=arg[1]
                        reason=arg[0]
                    else:
                        arg=commad.replace("/mute", "").replace("/мут", "").split('reason:')
                        timer=arg[0]
                        reason=arg[1]
                    if '.' in timer: 
                        deleu=timer.split('.')[1] 
                        num_date=int(re.sub(r'\D', '',timer.split('.')[0])) #убираем буквы и т.д
                        if deleu=='h' or deleu=='d' or deleu=='m' or deleu=='s':
                            if deleu=='h':
                                deleu=3600
                            elif deleu=='d':
                                deleu=86400
                            elif deleu=='m':
                                deleu=60
                            elif deleu=='s':
                                deleu=0
                    else:
                        wirning+=f'не корректное значение времени ({deleu}) использован аргумент по умолчанию (в часах)\nпример: `/мут reason:причина time:1.h` \n.h - часы (по умолчанию) , .d - дни , .m - минуты '
                        deleu=3600
                else:
                    error=''
                    if 'reason:' not in commad :
                        error+=' не хватает аргумента `reason:`'
                    if 'time:' not in commad :
                        if len(error)>1:
                            error+=','
                        error+=' не хватает аргумента `time:`'
                    bot.reply_to(message,f'SyntaxError\n{error}\nпример: `/мут reason:причина time:1.h` \n.h - часы (по умолчанию) , .d - дни , .m - минуты',parse_mode='MarkdownV2')
                    return
                #time=re.sub(r'.*?time:', '', time, 1)# убираем все до time:
                try:
                    bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, until_date=time.time() + num_date*deleu)
                    logger.info(f'ban for {message.reply_to_message.from_user.username}\n{reason}')
                    bot.send_message(admin_grops,f'myte for {message.reply_to_message.from_user.username}\ntime:{num_date} ({num_date*deleu}) {reason}')
                    if wirning != None:
                        bot.reply_to(message,wirning)
                except telebot.apihelper.ApiTelegramException:
                    bot.reply_to(message,'error>> elebot.apihelper.ApiTelegramException\nвероятно у бота недостаточно прав')
            else:bot.reply_to(message,'Пожалуйста, ответьте командой на сообщение, чтобы вытать мут')
        else:
            bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет','ты думал сможешь взять и замутить наивный'][random.randint(0,5)])

@bot.message_handler(commands=['cmd','console'])
def handle_warn(message):
    try:
        if CONSOLE_CONTROL:
            if str(message.chat.id)==admin_grops or message.from_user.id == 5194033781:
                if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id == 5194033781:
                    command=str(message.text).split(' ')[1]
                    if sys.platform.startswith('win'): # кросс плотформиность
                        result=subprocess.run(command , shell=True, stdout=subprocess.PIPE, text=True)
                        out=result.stdout
                    else:
                         result=subprocess.run(command , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                         out=result.stdout + result.stderr 
                    bot.reply_to(message, out if out !=None else 'None')
                else:
                    if message.date - time.time()<=60:
                        bot.reply_to(['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет','ай ай ай с терминалом играться '][random.randint(0,5)])
            else:
                if message.date - time.time()<=60:
                    bot.reply_to(message,'эта команда может быть выполнена только в группе администрации')
        else:
            if message.date - time.time()<=60:
                bot.reply_to(message,'отключено в настройках(settings.json) парамитер console_control')
    except:
        bot.reply_to(message,traceback.format_exc())
        
@bot.message_handler(commands=['t','translate'])  
def translitor(message):
    if message.reply_to_message:
        bin=str(message.reply_to_message.text).replace(' ','')
        if set(bin) == {'0', '1'} :
            bytes_list = [int(bin[i:i+8], 2) for i in range(0, len(bin), 8)]
            bot.reply_to(message,bytes(bytes_list).decode('utf-8', errors='replace'))
            return
        elif bin[0:6] == '0a2e14':
            bot.reply_to(message, bytes.fromhex(bin).decode('utf-8'))
            return
            
        translator = Translator()
        conf = translator.detect(message.reply_to_message.text)
        kont=f'Язык: {conf.lang}'
        result = translator.translate(message.reply_to_message.text, src=conf.lang, dest='ru')
        bot.reply_to(message,kont+'\n'+str(result.text))
    else:
        if ':' in message.text:
            try:
                text=str(message.text).replace('/t','').replace('/translite','').split(':')
                if text[1].lower()=="bin":
                    hex_str = binascii.hexlify(text[0].encode('utf-8')).decode()
                    binary_str = ''.join([
                    format(int(hex_str[i:i+2], 16), '08b') 
                    for i in range(0, len(hex_str), 2)
                        ])
                    bot.reply_to(message, ' '.join([binary_str[i:i+8] for i in range(0, len(binary_str), 8)]))
                    return
                elif text[1].lower()=="hex":
                    bot.reply_to(message, '0a2e14'+(text[0].encode("utf-8").hex().replace("'",'')))
                    return
                translator = Translator()
                conf = translator.detect(str(message.text))
                result = translator.translate(text[1], src=conf.lang, dest=text[0].replace(' ',''))
                bot.reply_to(message,result.text)
            except ValueError:
                bot.reply_to(message,'похоже язык не определен (примечание язык нужно указывать в сокращённой форме так: en - английский')
        

@bot.message_handler(commands=['to_text'])
def audio_to_text(message):
    mes=None
    if message.reply_to_message :
        if message.reply_to_message.voice:
            try:
                # Инициализация модели Vosk
                model_path = os.path.join(os.getcwd(), 'asets', "vosk-model-small-ru-0.22")
                if not os.path.exists(model_path):
                    logger.warning(f"Модель Vosk не найдена по пути: {model_path}")
        
                rec = KaldiRecognizer(Model(model_path), 16000)
                file_info = bot.get_file(message.reply_to_message.voice.file_id)
                ogg_data = bot.download_file(file_info.file_path)
                # Распознавание
                results = []
                data_r=asets.ffmpeg_tool.audio_conwert(ogg_data,'wav')
                if type(data_r)!='bytes':
                    logger.error(data_r)
                wav_buffer = io.BytesIO(data_r) # конвертирую в wav
                while True:
                    data = wav_buffer.read(4000)
                    if not data:
                        break
                    if rec.AcceptWaveform(data):
                        results.append(json.loads(rec.Result()))
        
                final = json.loads(rec.FinalResult())
                text = " ".join([res.get("text", "") for res in results if "text" in res] + [final.get("text", "")])
                bot.reply_to(message, f"Распознанный текст:\n{text}")
                
            except Exception as e:
                logger.error(f"Ошибка распознавания: {str(e)}\n{traceback.format_exc()}")
        elif message.reply_to_message.photo:
            pass # распознование текста на фото не реализовал(спиздил код) из за необходимости использования нескольких тяжелых библиотек   
    else:
        bot.reply_to_message(message, "Пожалуйста, ответьте командой /to_text на голосовое сообщение")
        
@bot.message_handler(commands=['download','dow'])
def download(message):
    if '-help' in message.text:
        bot.reply_to(message,
            'потдерживает скачивание голосовых сообщений,стикеров и аудио дорожек видео(звук из видео)\n'
            'придел веса файла 20 мб\n'
            "возможные форматы: <a href='https://github.com/xHak2215/admin_trlrgram_bot#format'>см. дакументацию</a>\n"
            'инструкция и примеры использования:\n'
            'скачивание стикеров: <code>/download(или же /dow) png(любой доступный формат) </code> дополнительный отрибут:<code>resize:</code> - изменяет размер изоброжения  по умолчанию 512 на 512 пример:<code>/download png resize:600,600</code>\n'
            'скачивание голосовых сообщений: <code>/download mp3 </code>\n'
            'скачивание аудио дорожек: <code>/download mp3 </code>\n'
            'скачивание фото: <code>/download png </code>'
        ,parse_mode='HTML',disable_web_page_preview=True) 
        return
    
    if message.reply_to_message:
            if message.reply_to_message.sticker or message.reply_to_message.photo :
                if len(list(str(message.text).split(' ')))<2:
                    #bot.reply_to(message,"неверное использование команды пример: /download png ")
                    #return
                    output_format='png'
                else:
                    output_format=str(message.text).split(' ')[1].lower()
                
                if message.reply_to_message.sticker:
                    sticker_id = message.reply_to_message.sticker.file_id
                    try:
                        file_info = bot.get_file(sticker_id)
                    except telebot.apihelper.ApiTelegramException:
                        bot.reply_to(message,f'файл слишком большой ')
                        return
                    if message.reply_to_message.sticker.is_animated or message.reply_to_message.sticker.is_video:
                        otv='анимированные стикеры не поддерживаться'
                        #' автор заебался реализовывать поддержку этой фигни 100 с лишнем строк кода было написано а затем удалено это ппц кокого хрена для того что бы скачать анимировный стикер нужно создовать и редактировать 3 промежуточных файла потому что видители загруженые байты кроме того что отличаються webm/tgs так еще хрен их конвертируеш без костылей в нормальное gif бл и да это сообщение редкое-' 
                        bot.reply_to(message,otv)
                        return
                    else:
                        # Нужно получить путь, где лежит файл стикера на Сервере Телеграмма
                        # формируем ссылку и "загружаем" изображение открываем  из байтов 
                        with Image.open(io.BytesIO(requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}', file_info.file_path.split('/')[1], allow_redirects=True).content)) as img:
                        # Конвертируем в RGB для форматов, которые не поддерживают прозрачность
                            if output_format in ('JPEG', 'JPG'):
                                img = img.convert('RGB')
                            
                elif message.reply_to_message.photo:# скачиваем фото
                    photo_id = message.reply_to_message.photo[-1].file_id
                    file_info = bot.get_file(photo_id)
                    img = Image.open(io.BytesIO(bot.download_file(file_info.file_path)))
                    if output_format in ('JPEG', 'JPG'):
                        img = img.convert('RGB')
        
                # Сохраняем в байтовый поток
                output_buffer = io.BytesIO()
                
                if "resize:" in message.text:
                    rise=str(message.text).split('resize:')[1]
                    # print(rise.split(',')[0],rise.split(',')[1])
                    img=img.resize((int(rise.split(',')[0]),int(rise.split(',')[1])))
                try:
                    img.save(output_buffer, format=output_format)
                except KeyError:
                    bot.reply_to(message,f'ошибка с форматом {output_format} не определен')
                    del output_buffer # очищяем дабы осбободить память
                    return
                try:
                        # Используем BytesIO как файлоподобный объект
                    with io.BytesIO(output_buffer.getvalue()) as file_stream:
                        file_stream.name = f'sticker_{datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M')}.{output_format}'
            
                     # Отправляем файл напрямую из памяти
                        bot.send_document(
                        chat_id=message.chat.id,
                        document=file_stream,
                        reply_to_message_id=message.message_id,
                        timeout=30  # Увеличиваем таймаут для больших файлов
                        )
                except Exception as e:
                    bot.reply_to(message, f"Ошибка отправки файла: {str(e)}")
                #bot.send_document(message.chat.id, output_buffer.getvalue() ,reply_to_message_id=message.message_id,visible_file_name=f'sticker_{datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M')}.{output_format}')
                del output_buffer # очищяем дабы осбободить память
                
            elif message.reply_to_message.voice:
                if len(list(str(message.text).split(' ')))<2:
                    bot.reply_to(message,"неверное использование команды пример: /download mp3 ")
                    return
                output_format=str(message.text).split(' ')[1].lower()
                if output_format in ['mp3','wav','aac','ogg','flac','wma','aiff','opus','alac','mp2']:
                    try:
                        file_info = bot.get_file(message.reply_to_message.video.file_id)
                    except telebot.apihelper.ApiTelegramException:
                        bot.reply_to(message,f'файл слишком большой ')
                        return
                    with requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}', stream=True) as r:
                        r.raise_for_status()
                        total_size = int(r.headers.get('content-length', 0))
                        chunk_size = 1024 * 1024  # 1MB chunks
                        video_data = io.BytesIO()
            
                        for chunk in r.iter_content(chunk_size=chunk_size):
                            video_data.write(chunk)
                    data=asets.ffmpeg_tool.audio_conwert(video_data,output_format)
                    if type(data) !=bytes:#если ошибка задаем пораметры по умолчанию
                        bot.reply_to(message,f'случилась ошибка>{data} приняты параметры по умолчанию')
                        data=video_data
                        output_format='ogg'
                    with io.BytesIO(data) as file_stream:
                        file_stream.name = f'voice_{datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M')}.{output_format}'
                            # Отправляем файл напрямую из памяти
                        bot.send_document(
                        chat_id=message.chat.id,
                        document=file_stream,
                        reply_to_message_id=message.message_id,
                        timeout=30  # Увеличиваем таймаут для больших файлов
                        )
                else:
                    bot.reply_to(message,'такого формата нет или он не потдерживаеться')
                    return
            elif message.reply_to_message.video:
                if len(list(str(message.text).split(' ')))<2:
                    bot.reply_to(message,"неверное использование команды пример: /download mp3 ")
                    return
                oformat=list(str(message.text).split(' '))[1].lower()
                try:
                    file_info = bot.get_file(message.reply_to_message.video.file_id)
                except telebot.apihelper.ApiTelegramException:
                    bot.reply_to(message,f'файл слишком большой ')
                    return
                with requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}', stream=True) as r:
                    r.raise_for_status()
                    total_size = int(r.headers.get('content-length', 0))
                    chunk_size = 1024 * 1024  # 1MB chunks
                    video_data = io.BytesIO()
            
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        video_data.write(chunk)
                    
                if oformat in ["ogg","mp3","wav","aac","flac","m4a","webm","ac3","wma"]:
                    data=asets.ffmpeg_tool.video_to_audio_conwert(video_data.getvalue() ,oformat)
                    if type(data) != bytes:#если ошибка задаем пораметры по умолчанию
                        bot.reply_to(message,f'случилась ошибка>{data} ')
                        return
                    try:
                        with io.BytesIO(data) as file_stream:
                            file_stream.name = f'music_{datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M')}.{oformat}'
            
                            # Отправляем файл напрямую из памяти
                            bot.send_document(
                            chat_id=message.chat.id,
                            document=file_stream,
                            reply_to_message_id=message.message_id,
                            timeout=30  # Увеличиваем таймаут для больших файлов
                            )
                    except telebot.apihelper.ApiTelegramException:
                        bot.reply_to(message,f'файл слишком большой ({len(data)} байт) ')
                        return
                else:
                    bot.reply_to(message,'такого формата нет или он не потдерживаеться')
            else:
                bot.reply_to(message,'не подлежит скачиванию')
    else:
        bot.reply_to(message,'ответе на ГС или стикер чтобы скачать')
        
@bot.message_handler(commands=['blaklist'])
def blaklist(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id ==5194033781:
        if message.reply_to_message.sticker and message.reply_to_message:
            if not os.path.exists(os.path.join(os.getcwd(), 'asets', "blacklist.json")):
                logger.warning('no file blacklist.json')
                with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'w') as f:
                    json.dump({'stiker':[1]}, f)
            with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'r') as f:
                blist = json.load(f)['stiker']
    
            sticker_id = message.reply_to_message.sticker.file_id
            if sticker_id not in blist:
                blist.append(sticker_id)
    
            with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'w') as f:
                json.dump({'stiker':blist}, f)
            bot.send_message(admin_grops,f'стикер (id:{message.reply_to_message.sticker.file_id}) добавлен в черный список')
    
        else:
            bot.reply_to(message,'ответьте этой командой на стикер что бы внести его в черный список ')
    else:
        if message.date - time.time()<=60:
            bot.reply_to(['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет','нэт'][random.randint(0,5)])
    
@bot.message_handler(commands=['unblaklist'])
def unblaklist(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id ==5194033781:
        if message.reply_to_message.sticker and message.reply_to_message:
            if not os.path.exists(os.path.join(os.getcwd(), 'asets', "blacklist.json")):
                logger.warning('no file blacklist.json')
                with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'w') as f:
                    json.dump([], f)
            with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'r') as f:
                blist = json.load(f)['stiker']
    
            blist=list(blist).remove(message.reply_to_message.sticker.file_id)# удаление стикера из списка 

            with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'w') as f:
                if len(blist)<1:
                    blist=[0]
                json.dump({'stiker':blist}, f)
            bot.send_message(admin_grops,f'стикер (id:{message.reply_to_message.sticker.file_id}) убран из черного списка')
        else:
            bot.reply_to(message,'ответьте этой командой на стикер что бы убрать его из черного списка')
    else:
        if message.date - time.time()<=60:
            bot.reply_to(['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет','нэт'][random.randint(0,5)])
            
@bot.message_handler(commands=['message_info'])
def unblaklist(message):
    if message.reply_to_message:
        out_message=' '
        out_message+=f'тип: {message.reply_to_message.content_type}\n'
        out_message+=f'message id:{message.message_id}\n'
        if str(message.reply_to_message.content_type) in ['video','photo','animation','sticker']:
            if message.reply_to_message.sticker: media_id = message.reply_to_message.sticker.file_id
            elif message.reply_to_message.video: media_id = message.reply_to_message.video.file_id
            elif message.reply_to_message.photo:
                media_id = message.reply_to_message.photo[-1].file_id
            elif message.reply_to_message.animation: media_id = message.reply_to_message.animation.file_id
            if 'media_id' in locals():
                file_info = bot.get_file(media_id)
                out_message+=f'ulr:https://api.telegram.org/file/bot{bot.token}/{file_info.file_path} \nвес: {round(len(requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}').content),2)} байт\n'
        if message.reply_to_message.sticker: out_message+=f'sticker ID: {message.reply_to_message.sticker.file_id}\nemoji:{message.reply_to_message.sticker.emoji}\n'
        #if message.reply_to_message.video:
            #media_id = message.reply_to_message.video.file_id
            #file_info = bot.get_file(media_id)
            #print(requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}', file_info.file_path.split('/')[1], allow_redirects=True).content)
            #out_message+=f'meta data:{str(requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}', file_info.file_path.split('/')[1], allow_redirects=True).content)}\n'
        elif message.reply_to_message.photo:
            media_id = message.reply_to_message.photo[-1].file_id
            file_info = bot.get_file(media_id)
            with Image.open(io.BytesIO(requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}', file_info.file_path.split('/')[1], allow_redirects=True).content)) as img:
                out_message+=f'meta data (exif):{img.getexif()}\n'
            out_message+=f'width(высота): {message.reply_to_message.photo[-1].width}\n'
            out_message+=f'height(ширена): {message.reply_to_message.photo[-1].height}\n'
        bot.reply_to(message,out_message)
        
class DeleteData:
    def __init__(self):
        self.message_l = []
        self.chat_id = None
# Глобальный экземпляр для хранения данных
delete_data = DeleteData()

def nacase(message, delete_message=None):
    try:
        user_messages[message.from_user.id] = []
        the_message = str(message.chat.id).replace("-100", "")
        
        if bool(bambam): 
            # Ограничиваем пользователя на 24 часа
            bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                until_date=int(time.time()) + 86400, 
                can_send_messages=False
            )
            data_base(message.chat.id, message.from_user.id, ps_reputation_upt=3)
            bot.send_message(
                message.chat.id, 
                f"Пользователью @{message.from_user.username} выдан мут на 1 день."
            )
        
        # Формируем сообщение для админов
        admin_msg = (
            f'Обнаружен спам от пользователя >> @{message.from_user.username}\n'
            f'Сообщение: {message.text if message.content_type == "text" else message.content_type}'
            f'|https://t.me/c/{the_message}/{message.message_id}'
        )
        
        if DELET_MESSADGE and delete_message:
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(
                "Удалить спам", 
                callback_data=f"delete_spam_{message.chat.id}"
            )
            markup.add(button)
            
            # Сохраняем данные для удаления
            delete_data.message_l = delete_message
            delete_data.chat_id = message.chat.id
            bot.send_message(admin_grops, admin_msg, reply_markup=markup)
        else:
            bot.send_message(admin_grops, admin_msg)
        
        logger.info(f'Обнаружен спам от пользователя >> @{message.from_user.username}, id: {message.from_user.id}')
        
    except telebot.apihelper.ApiTelegramException as e:
        bot.send_message(admin_grops, f'{str(e)}\nВероятно у бота недостаточно прав')
        logger.error(f'{str(e)}\nВероятно у бота недостаточно прав')
    except Exception as e:
        bot.send_message(admin_grops, f"Неожиданная ошибка: {str(e)}")
        logger.error(f"Неожиданная ошибка: {str(e)}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_spam_'))
def handle_spam_deletion(call):
    try:
        # Проверка прав администратора
        if (call.from_user.id not in [5194033781] and bot.get_chat_member(call.message.chat.id, call.from_user.id).status not in ['creator', 'administrator']):
            bot.answer_callback_query(
                call.id,
                text=random.choice(['Ты не администратор!','Только админы вершат правосудие','Ты не админ','Неа, тебе нельзя','Нет']),
                show_alert=False
            )
            return
        # Проверка наличия сообщений для удаления
        if not hasattr(delete_data, 'message_l') or not delete_data.message_l:
            bot.answer_callback_query(call.id, "Нет сообщений для удаления")
            return
        # Удаление сообщений
        deleted_count = 0
        for msg_id in delete_data.message_l:
            try:
                bot.delete_message(delete_data.chat_id, msg_id)
                deleted_count += 1
            except:
                continue
        # Ответ пользователю
        bot.answer_callback_query(call.id, f"Успешно удалено {deleted_count}/{len(delete_data.message_l)} сообщений")
    except Exception as e:
        bot.send_message(admin_grops,f"Ошибка при удалении: {str(e)}")
        logger.error(f"Ошибка в handle_spam_deletion: {str(e)}")
        
@bot.message_handler(commands=['ping'])
def ping_command(message):
    if '-help' in message.text:
        bot.reply_to(message, 'аргументы: /ping ссылка для тестирования по умолчанию https://ya.ru ,количество повторов замера задержки , режим расчета True - вычисление средни статисчической задержки из всех попыток. по умолчанию (не указывая значение) отоброжение зажержки каждой попытки')
    data=str(message.text).split(' ')
    if len(data)>1:
        command=data[1]
    else:
        url='https://ya.ru'
        start_time = time.time()
        response=requests.get(url)
        if response.status_code==200:
            scode= ''
        else:
            scode=f'\nerror conect\nstatus code {response.status_code}'
        p_time=time.time() - start_time
        bot.reply_to(message,'ping:'+p_time+scode)
        return
    parm=command.split(',')
    regim=False
    if len(parm) >= 2:
        povt = int(parm[1])
    else:
        povt = 1
    if len(parm) >= 3:
        regim=parm[2]
    if bool(regim):
        p_time=0
    else:
        p_time=[]
    for i in range(povt):
        start_time = time.time()
        response=requests.get(parm[0])
        if response.status_code==200:
            scode= ''
        else:
            scode=f'\nerror conect\nstatus code {response.status_code}'
        if bool(regim):
            p_time+=time.time() - start_time
        else:
            p_time.append(time.time() - start_time)
    if bool(regim):
        bot.reply_to(message,f'ping:{round(p_time/povt,4)}s{scode}')
    else:
        out=''
        for i in range((len(p_time))):
            out+=f'[{i}] ping: {round(p_time[i],5)}s\n' 
        bot.reply_to(message,out+scode)
        
        
user_messages = {}#инициализация словарей и тп
user_text = {}
message_text=[]
#SPAM_LIMIT = 8 # Максимальное количество сообщений
#SPAM_TIMEFRAME = 4  # Время в секундах для отслеживания спама
s_level=0
tekst_m=[]
delete_message=[]
        
# Функция для обработки сообщений
def anti_spam(message):
    #инициализация хрени всякой     
    user_id = message.from_user.id
    current_time = time.time()
    tekst_m.append({message.text:message.message_id})
    user_text[user_id] = tekst_m  # Сохраняем текст сообщения и id
    keys_to_delete=[]
    
    data_base(message.chat.id,message.from_user.id,soob_num=1)# добовляем 1 сообщение 
   
    # Удаление старых временных меток
    if user_id not in user_messages:
        user_messages[user_id] = []
    user_messages[user_id] = [
        [ts, msg_id] 
        for [ts, msg_id] in user_messages[user_id] 
        if current_time - ts < SPAM_TIMEFRAME
    ]
    
    # Добавление текущего временного штампа
    user_messages[user_id].append([current_time, message.message_id])
    
    emoji=''
    if message.content_type=='sticker':
        emoji=f'( {message.sticker.emoji} )'
    logs = f"chat>>{message.chat.id} user >> tg://user?id={message.from_user.id}, @{message.from_user.username} | сообщение >>\n{message.text if message.content_type == 'text' else message.content_type} {emoji}"
    print("————")
    logger.debug(logs)
   # Проверка на спам
    if len(user_messages[user_id]) > SPAM_LIMIT:
        for i in user_messages[user_id]:
            delete_message.append(i[1])
        nacase(message,delete_message)
        #bot.delete_message(message.chat.id,message.message_id)
        return
    if len(list(user_text.keys()))>0 and user_text[list(user_text.keys())[0]] != None and  message.text:
        paket_num=4
        sr_d,slova=0,[]
        keys_to_delete=[]
        list_mess=[]
        for i in range(len(user_text.keys())):
            mess=list(user_text[list(user_text.keys())[i]])
            for temp_list_mess in list(user_text[list(user_text.keys())[i]]):
                list_mess.append(list(temp_list_mess.keys())[0])# достаю текст сообщения и добовляю list_mess
            povtor_messade_shet=0
            k=0
            for a in range(len(list_mess)):
                k=a-1
                if k<len(list_mess) or len(list_mess)>k:
                    k=0
                if str(list_mess[k]).lower() == str(list_mess[a]).lower():
                    povtor_messade_shet=povtor_messade_shet+povtor_messade_shet
                if povtor_messade_shet>=SPAM_LIMIT:
                    keys_to_delete.append(list(user_text.keys())[i])
                    nacase(message,[message.message.id])
                s_level=0
                list_povt_slov=[]
                if list_mess[a]!=None:
                    text_s=str(list_mess[a])
                    if str(text_s)==list_mess[0] and len(list_mess)>=1:
                        s_level+=1
                    if len(text_s)>=300:
                        s_level+=1
                    if list_mess.count(" ")<=round(len(text_s)/10):# подсчет пробелов
                        s_level+=1
                    if len(text_s)>=20+SPAM_LIMIT:
                        slova=list(str(text_s).split(' '))
                        for s in range(len(slova)):
                            slova.append(slova[s].split(',')[0])
                            sr_d=+len(slova[s])
                        if  len(slova) !=0 and sr_d !=0 and len(slova)>len(text_s)-sr_d/len(slova):
                            s_level+=sr_d/len(slova)
                cours=0
                for l in range(round(len(str(list_mess[a]))/paket_num)):
                    text=''
                    text = str(list_mess[a])[cours:cours + paket_num]
                    list_povt_slov.append(text)
                    cours += paket_num
                bambamSpamerBlat=0
                for b in range(len(list_povt_slov)):
                    if list_povt_slov[b]==list_povt_slov[0]:
                        bambamSpamerBlat=bambamSpamerBlat+1
                if bambamSpamerBlat>SPAM_LIMIT:
                    keys_to_delete.append(list(user_text.keys())[i])
                    nacase(message,[message.message.id])
        #print(list_povt_slov)# debug
        #print(list(user_text.keys())[i])
        #print(s_level)
            if s_level>=len(list_povt_slov) and len(list_povt_slov)>=5:
                keys_to_delete.append(list(user_text.keys())[i])
                print(mess[list(user_text.keys())[i]])
                nacase(message,[message.message.id])
    # Удаляем ключи после завершения итерации
    for key in range(len(keys_to_delete)):
        if key != None:
            del user_text[keys_to_delete[key]]
    
text={}
warn=0
def anti_spam_forward(message,text=text,warn=warn):
    text[message.from_user.id] = str(message.text).lower().replace(' ','')
    counts = Counter(text.values())
    warn = sum(v-1 for v in counts.values())  # Считаем все дубликаты
    if warn > SPAM_LIMIT:
        nacase(message)
        text={}
    if time.time()-message.date>=30:
        text={}

@bot.message_handler(content_types=['text','sticker'])
def message_handler(message):
    if message.sticker:
        if not os.path.exists(os.path.join(os.getcwd(), 'asets', "blacklist.json")):
            logger.warning('no file blacklist.json')
            with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'w') as f:
                json.dump([], f)
        with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'r') as f:
            blist = json.load(f)['stiker']
        if message.sticker.file_id in blist:
            if bool(DELET_MESSADGE):
                try:
                    bot.delete_message(message.chat.id,message.message_id)
                    bot.send_message(admin_grops,f'запрещеный стикер от @{message.from_user.username} удален')
                except telebot.apihelper.ApiTelegramException:
                    bot.reply_to(message,'error>> elebot.apihelper.ApiTelegramException\nвероятно у бота недостаточно прав')
    teg=''
    commad=str(message.text).lower()
    if "[help]" in commad or "[Help]" in commad:     
        id_help_hat=str(message.chat.id).replace("-100", "")
        for i in range(len(admin_list)):
            if i >0:
                teg+=f",{admin_list[i]}"
            else:
                teg+=f"{admin_list[i]}"
        bot.send_message(admin_grops,  f"{teg} есть вопрос от @{message.from_user.username} \nвот он: https://t.me/c/{id_help_hat}/{message.message_id}")# это не читабельное гавно но оно работает
    if commad=='!я' and message.reply_to_message != True:
        send_statbstic(message)
        
    if time.time() - message.date >= SPAM_TIMEFRAME:
        data_base(message.chat.id,message.from_user.id,soob_num=1)# для того что бы все сообщения подсчитывались
        return
    elif message.forward_from:
        anti_spam_forward(message)
    else:
        anti_spam(message)
        if AUTO_TRANSLETE['Activate']:
            translator = Translator()
            conf = translator.detect(str(message.text))
            if conf.lang != AUTO_TRANSLETE['laung']:
                result = translator.translate(str(message.text), src=conf.lang, dest=AUTO_TRANSLETE['laung'])
                bot.reply_to(message,result.text)

@bot.message_handler(content_types=['video','photo','animation'])
def message_handler(message):
    if time.time() - message.date >= SPAM_TIMEFRAME or message.media_group_id != None:
        return
    else:
        anti_spam(message)
@bot.message_handler(content_types=['voice'])
def message_voice(message):
    if time.time() - message.date >= SPAM_TIMEFRAME:
        data_base(message.chat.id,message.from_user.id,soob_num=1)# для того что бы все сообщения подсчитывались
        return
    elif message.forward_from:
        anti_spam_forward(message)
        if message.voice.duration>=300:
            bot.reply_to(message,'чет как то многовато')
        elif message.voice.duration>=1800:
            bot.reply_to(message,'скока бл ...ужас')
    else:
        anti_spam(message)
        if message.voice.duration>=300:
            bot.reply_to(message,'чет как то многовато')
        elif message.voice.duration>=1800:
            bot.reply_to(message,'скока бл ...ужас')
# Обработчик всех остальных типов сообщений
@bot.message_handler(func=lambda message: True)
def other_message_handler(message):
    if time.time() - message.date >= SPAM_TIMEFRAME or message.forward_date and message.forward_from and message.forward_from_chat:
        return
    anti_spam(message)

#новый юзер 
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        logger.info(f'new member in chat | user name> {message.from_user.username}')
        data_base(message.chat.id,new_member.id,time_v=time.time())
        if message.date - time.time()<=300:
            try:
                input_gif_path = os.path.join(os.getcwd(),'asets','hello.gif')
                output_gif_path = 'output.gif'
                # Открываем изображение
                gif = Image.open(input_gif_path)
                # Создаем список для хранения кадров с текстом
                frames_with_text = []
                # Настройка шрифта (по умолчанию, если шрифт не найден, будет использован шрифт по умолчанию)
                try:
                    font = ImageFont.truetype(os.path.join(os.getcwd(),'asets','Roboto_Condensed-ExtraBoldItalic.ttf'), 35)
                except IOError:
                    font = ImageFont.load_default(size=35)
                # Добавляем текст на каждый кадр
                for frame in range(gif.n_frames):
                    gif.seek(frame)
                    # Копируем текущий кадр
                    new_frame = gif.copy()
                #    Преобразуем в rgba 
                    new_frame = new_frame.convert('RGBA')
                    draw = ImageDraw.Draw(new_frame)
                    # Определяем текст и его позицию
                    usernameh=message.from_user.first_name
                    ot=26-len(usernameh)
                    otstup=' '*ot
                    text = f"добро пожаловать в чат  \n{otstup}{usernameh}" 
                    text_position =(60, 300) # Позиция (x, y) для текста        
                    # Добавляем текст на кадр
                    draw.text(text_position, text, font=font, fill=(21,96,189))  # Цвет текста задан в формате RGB
                    frames_with_text.append(new_frame)# Добавляем новый кадр в список
                    # Сохраняем новый GIF с текстом
                frames_with_text[0].save(output_gif_path, save_all=True, append_images=frames_with_text[1:], loop=0)
                try:
                    with open('output.gif', 'rb') as gif_file:
                        bot.send_animation(chat_id=message.chat.id, animation=gif_file, reply_to_message_id=message.message_id)
                    os.remove('output.gif') 
                except Exception as e:
                    bot.send_message(message.chat.id,f'упс ошибка\n error>>{e} \n@HITHELL чини!')
            except Exception as e:
                logger.error(f'error hello message >>{e}')
                username = '@'+new_member.username if new_member.username else new_member.first_name 
                welcome_message = [f"Привет, {username}! Добро пожаловать в наш чат!  /help для справки",f"<s>новенький скинь ножки</s>  Привет, @{username}! Добро пожаловать в наш чат!  /help для справки"][random.randint(0,1)]
                bot.reply_to(message , welcome_message, parse_mode="HTML")
# Основной цикл
def main():
    try:
        print("\033[32m{}\033[0m".format('нет ошибок :3 '))
        while True:
            try:
                try:
                    bot.polling(none_stop=True)
                    schedule.run_pending()
                    # Запускаем в отдельном потоке при старте бота
                    #scheduler_thread = threading.Thread(target=update_user)
                    #scheduler_thread.daemon = True
                    #scheduler_thread.start()
                except requests.exceptions.ReadTimeout:
                    print("time out")
            except Exception as e:
                logger.error(f"Ошибка: {e} \n-----------------------------\n {traceback.format_exc()}")
                time.sleep(3)
    except Exception as e:
        bot.send_message(admin_grops,f'ошибка при старте:\n{e}\n-----------------------\n{traceback.format_exc()}')
if __name__ == '__main__':
    main()
    
    
