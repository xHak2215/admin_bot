import os
import os.path
import json
import re
import sys
import time
import random
from datetime import timedelta, datetime
import traceback
from collections import Counter
import threading
import io
import binascii
import gc
from dataclasses import dataclass
import asyncio
import tempfile
import numpy as np


import asets.ffmpeg_tool
import asets.dictt
from asets.wiki_api_lib import wiki
from asets.data_bese import data_base, team_data_bese, tu_base, tu_base_balance

try:
    import vosk
    from vosk import Model, KaldiRecognizer
    import telebot  
    from collections import defaultdict
    import psutil
    #import schedule
    import requests
    import subprocess
    from loguru import logger
    import sqlite3
    from PIL import Image, ImageDraw, ImageFont
    import deep_translator
    from deep_translator import GoogleTranslator
    from moviepy import ImageSequenceClip
    import ahocorasick
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
            print('\33[31m error install (что то пошло не так )')
    exit(1)

if not os.path.exists(os.path.join(os.getcwd(), 'asets')):
    os.mkdir('asets')

try:
    with open("TOKEN", "r") as t:
        TOKEN=t.readlines()[0].replace(' ','').replace('\n','')
except FileNotFoundError:
    print('\33[31m error no file TOKEN ,the file auto creat please write you token to file TOKEN \33[0m')
    with open(os.path.join(os.getcwd(), 'TOKEN'), 'w') as f:
        f.write('please write you token')
    sys.exit(1)
    

settings={'bambam': False, 'delet_messadge': False, 'admin_grops': '-1002284704738', 'spam_limit': 10, 'spam_timer': 4, 'ban_and_myte_command': True, 'console_control': True, 'auto_translete': {'laung': 'ru', 'Activate': False}, 'admin_list': ['HITHELL', 'mggxst']}

try:
    with open("settings.json", "r") as json_settings:
        settings = json.load(json_settings)
except:
    logger.debug('error settings import')
    with open("settings.json", "w") as json_settings:
        json.dump({'bambam': False, 'delet_messadge': True, 'admin_grops': '-1002284704738', 'spam_limit': 10, 'spam_timer': 4, 'ban_and_myte_command': True, 'console_control': True, 'auto_translete': {'laung': 'ru', 'Activate': False}, 'admin_list': ['HITHELL', 'mggxst']} ,json_settings)


BAMBAM=bool(settings['bambam'])
DELET_MESSADGE=bool(settings['delet_messadge'])
admin_grops=str(settings['admin_grops'])
SPAM_LIMIT=int(settings['spam_limit'])
SPAM_TIMEFRAME=int(settings['spam_timer'])
BAN_AND_MYTE_COMMAND=bool(settings['ban_and_myte_command'])
CONSOLE_CONTROL=bool(settings['console_control'])
AUTO_TRANSLETE=dict(settings['auto_translete'])
admin_list=list(settings['admin_list'])


help_user = '<code>/report</code> — забань дебила в чате\n\n<code>/я</code> — узнать свою репутацию и количество сообщений\n\n<code>/info</code> — узнать информацию о пользователе\n\n<code>/translite</code> (сокращено <code>/t</code>) — перевод сообщения на русский перевод своего сообщения на другой язык:<code>/t любой текст:eg</code> поддерживаться bin и hex кодировки\n\n<code>/download</code> (сокращено <code>/dow</code>) — скачивание стикеров,ГС и аудио дорожек видео при скачивании можно изменить формат пример: <code>/download png</code> для дополнительный инструкций введите <code>/download -help</code>\n\n<code>/to_text</code> — перевод ГС в текст\n\n<code>/serh</code> - поиск статей на википедии пример:<code>/serh запрос</code>\n\n<code>/team</code> - позволяет создавать кланы/команды; <code>/team -h</code> для инструкции по использованию (бета)\n\n<code>/swearing_top</code> - топ матершинеков чата\n\n<code>/gif_search</code> - посик gif по запросу, пример:<code>/gif_search котик</code>\n\nЕсли есть вопросы задайте его добавив в сообщение <code>[help]</code> и наши хелперы по возможности помогут вам \n\n<code>/admin_command</code> команды администраторов\n<a href="https://github.com/xHak2215/admin_bot#doc_commad" a>расширенная документация команд</a>' 
admin_command = '<code>/monitor</code> — выводит показатели сервера; \n<code>/warn</code> — понижение репутации на 1; \n<code>/reput</code> — повышение репутации на 1; \n<code>/data_base</code> — выводит базу данных, возможен поиск конкретного пользователя пример: <code>/data_base 5194033781</code>; \n<code>/info</code> — узнать репутацию пользователя;\n <code>/blaklist</code> — добавляет стикер в черный список; \n<code>/unblaklist</code> — убирает стикер из черного списка; \n<code>/log</code> - получить лог файл; \n<code>/backup_log</code> - создание бекапа текущего лог файла; \n<code>/null_log</code> - очищение текущего лог файла; \n<code> /mute</code> - мут пользователя, пример: <code>/мут 1 h \n *причина*</code>\nh - обозначает часы, так же можно указать d - дни и m - минуты; \n<code>/ban</code>  - бан пользователя, пример:<code>/бан\n*причина*</code>'

#/creat - позволяет создавать скрипты является простым "командным языком программирования" (бета) подробнее:<a href="https://github.com/xHak2215/admin_bot#creat_program_info">см. дакументацию</a>\n\n

logse="nan"
i=0
log_file_name="cats_message.log"
random.seed(round(time.time())+int(round(psutil.virtual_memory().percent)))#создание уникального сида
vosk_model_path = os.path.join(os.getcwd(), 'asets', "vosk-model-small-ru-0.22")

gc.enable()
gc.set_debug(2)

class Blak_stiket_list:
    """
    **хранит запрещенные стикеры**

    :param: None
    """
    def __init__(self,blist=[0]):
        self.blist=blist
    
    def add(self, sticker_id):
        """Добавляет стикер в черный список, если его там нет."""
        if sticker_id not in self.blist:
            self.blist.append(sticker_id)

    def removes(self, sticker_id):
        """Удаляет стикер из черного списка, если он там есть."""
        if sticker_id in self.blist:
            self.blist.remove(sticker_id)

    def slen(self):
        """Возвращает количество запрещенных стикеров."""
        return len(self.blist)-1

bklist=Blak_stiket_list()

def get_telegram_api()->dict:
    """
    ## return dict
    ### key dict: 
    - ping :get ping type:float | None
    - status :status code type:int | None
    - respone :respone telegram api (getMe) type:dict | None
    - error :errors no errors to None type:str | None
    """
    timer=time.time()
    try:
        respone=requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe",timeout=20)
    except Exception as e:
        return {"ping":None,"status":None,"respone":None,"error":e}
    ping=time.time()-timer
    return {"ping":ping,"status":respone.status_code,"respone":json.loads(respone.content),"error":None}

if not os.path.exists(os.path.join(os.getcwd(), 'asets', "blacklist.json")):
    logger.warning('no file blacklist.json')
    with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'w') as f:
            json.dump({'stiker':[0]}, f)
with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'r') as f:
    try:
        bklist.add(json.load(f)['stiker'])
    except json.decoder.JSONDecodeError: 
        with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'w') as f:
            json.dump({'stiker':[0]}, f)

# Инициализация логирования
logger.add(log_file_name, level="TRACE", encoding='utf-8', rotation="500 MB")

bot = telebot.TeleBot(TOKEN ,num_threads=5)

#apihelper.MAX_THREADS = 5  # Ограничиваем количество потоков
#updater = Updater(token=TOKEN)
#dispatcher = updater.dispatcher
warn=0
print('\33[0m')
print('\n'+os.getcwd())

if os.path.exists(os.path.join(os.getcwd(), 'asets' ,'hello.gif')):
    print('gif           \33[32mOK\33[0m')
else:
    warn=warn+1
    print('\33[31error no hello.gif\33[0m')
if os.path.exists(os.path.join(os.getcwd(), 'asets' ,'blacklist.json')):pass
else:
    warn=warn+1
if os.path.exists(os.path.join(os.getcwd(), 'settings.json')):
    print('settings.json \33[32mOK\33[0m')
else:
    warn=warn+1
    print('\33[31error no settings.json\33[0m')
if os.path.exists(os.path.join(os.getcwd(), 'requirements.txt')) != True:
    warn=warn+1
if os.path.exists(os.path.join(os.getcwd(), 'Users_base.db')):
    print('data base     \33[32mOk\33[0m')
else:
    warn=warn+1
    print("\33[31merror no bata base\33[0m")
if warn >=3:
    bot.send_message(admin_grops, f"обнаружены не критичные ошибки возможны неполадки\nwarn level:{warn}")

date = datetime.now().strftime("%H:%M")

#bot.send_message(admin_grops, f"бот запущен ")
logger.info("бот запущен")
    
# Функция для мониторинга ресурсов
def monitor_resources():
    response_time,response_time,cpu_percent,ram_percent,disk_percent=0,0,0,0,0
    popitki=5
    popitka1=0
    #пинг в среднем 5 (можно изменять в popitki )попыток
    for i in range(popitki):
        start_time = time.time()
        response=requests.get('https://core.telegram.org/')
        if response.status_code==200:
            scode= ''
            pass
        else:
            scode=f" status code {response.status_code}"
        if i == 1:
            popitka1= time.time() - start_time
        response_time+= time.time() - start_time
        cpu_percent += float(psutil.cpu_percent())
        ram_percent +=float(psutil.virtual_memory().percent)
        if sys.platform.startswith('win'):
            disk_percent +=float(psutil.disk_usage('C:/').percent)
        else:
            disk_percent +=float(psutil.disk_usage('/').percent)
    shutka=' '
    if round(cpu_percent/popitki)==100:
        shutka='\nпроцессор шя рванет 🤯'
    print(f"CPU: {round(cpu_percent/popitki)}%,\nRAM: {round(ram_percent/popitki)}%,\nDisk: {round(disk_percent/popitki)}%,\nPing: {popitka1} \n{shutka}")
    return round(cpu_percent/popitki,1), round(ram_percent/popitki,1), round(disk_percent/popitki,1), str(str(round(response_time/popitki,3))+'s'+scode+shutka),round(popitka1,3)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type != 'private' and message.date - time.time() <= 60:
        bot.reply_to(message, 'приветствую пользователь. ознакомитесь с командами бота с помощью команды /help\n<a href="https://github.com/xHak2215/admin_bot"a>Github бота</a>',parse_mode='HTML',disable_web_page_preview=True)

# Команда /help
@bot.message_handler(commands=['help','помощь','sos'])
def send_help(message):
    if message.date - time.time() <= 60:
        bot.reply_to(message, help_user ,parse_mode='HTML',disable_web_page_preview=True)

@bot.message_handler(commands=['admin_command'])
def send_admin_help(message):
    if message.date - time.time() <= 60:
        bot.reply_to(message, admin_command ,parse_mode='HTML',disable_web_page_preview=True)
    
# Команда /log
@bot.message_handler(commands=['log'])
def send_log(message):
    try:
        data=data_base(message.chat.id, message.from_user.id)
        if data and data[1]<15 and data[0]>=3 or bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator'] or message.from_user.id == 5194033781:
            bot.send_document(message.chat.id,reply_to_message_id=message.message_id,document=open(log_file_name, 'r',encoding='utf-8', errors='replace'))

    except Exception as e:
        bot.send_message(admin_grops,f"error logs file>> {e} ")
        logger.error(f"log error >> {e}")
        
#очищение логов /null_log
@bot.message_handler(commands=['null_log','clear_log'])
def null_log(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator'] or message.from_user.id == 5194033781:
        if str(message.chat.id)==str(admin_grops) or message.from_user.id == 5194033781:
            file = open(log_file_name, "w")
            # Изменяем содержимое файла
            file.write("log null\n")
            # Закрываем файл
            file.close()
            bot.send_message(admin_grops, f"логи очищены очистил : @{message.from_user.username}")
            logger.info(f"логи очищены, очистил:  @{message.from_user.username}")
        else:
            bot.reply_to(message,'команда доступна только из группы администрации')
    else:
        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])

# /backup_log
@bot.message_handler(commands=['backup_log'])
def backup_log(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator'] or message.from_user.id ==5194033781:
        try:
        #проверка на админа
            if str(message.chat.id)==str(admin_grops) or message.from_user.id == 5194033781:
                if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator'] or message.from_user.id == 5194033781:
                    if os.path.isdir("backup_log"):
                        if os.path.isfile(log_file_name):
                            root_dict=os.getcwd()
                            try:
                                log=open(log_file_name,'r')
                                os.chdir(os.path.join(root_dict,"backup_log"))
                                open(f"cats_message({datetime.now()}).log",'w+').write(log.read())
                                bot.send_message(admin_grops,f"бекап логов сделан инициатор: @{message.from_user.username}")
                            except Exception as e:logger.error(f"{e}\n{traceback.format_exc()}")
                            finally:
                                os.chdir(root_dict)
                        else:
                            bot.reply_to(message,"файл логов еще не создан копировать то и не чего")
                    else:
                        os.mkdir("backup_log")
                else:
                    bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])
            else:
                bot.reply_to(message,'команда доступна только из группы администрации')
        except Exception as e:
            bot.send_message(admin_grops,f"error logs file>> {e} ")
            logger.error(f"clear log  error >> {e}")
    else:
        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])
        
#report data список с кол.во. репортами /report_data 
@bot.message_handler(commands=['report_data'])
def send_report_data(message):
    try:
        #проверка на админа
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator'] or message.from_user.id ==5194033781:
            bot.send_message(message.chat.id,f"report data: {report_data}")
            logger.debug(f"report data: {report_data}")
        else:
            bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет','такие данные не для тебя'][random.randint(0,4)])
    except Exception as e:
        bot.send_message(admin_grops,f"error >> {e} ")
        logger.error(f"error >> {e}")

# очистка консоли /cler 
@bot.message_handler(commands=['cls','clear'])
def clear_console(message):
    #проверка на админа
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator'] or message.from_user.id ==5194033781: 
            bot.send_message(admin_grops,f"экран очищен, очистил : @{message.from_user.username}")
            os.system('clear')
            logger.info(f"экран очищен очистил:  @{message.from_user.username}")
    else:
        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])

# Команда /monitor    
@bot.message_handler(commands=['monitor','монитор'])
def monitor_command(message):
    if message.date - time.time() <= 60:
        cpu_percent, ram_percent, disk_percent, response_time ,p = monitor_resources()
        bot.reply_to(message, f"CPU: {cpu_percent}%\nRAM: {ram_percent}%\nDisk: {disk_percent}%\nPing: {response_time}")

# Команда /test 
@bot.message_handler(commands=['test'])
def monitor_test_command(message):
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
    if os.path.exists(os.path.join(os.getcwd(), log_file_name)):
        test=test+'messege log OK\n'
    else:
        test=test+'warning no messege log \n'
    if os.path.exists(os.path.join(os.getcwd(), 'asets' , 'Roboto-VariableFont_wdth,wght.ttf')):
        test=test+'Roboto-VariableFont_wdth,wght.ttf шрифт OK\n'
    else:
        test=test+'error no Roboto-VariableFont_wdth,wght.ttf\n'
    if os.path.exists(os.path.join(os.getcwd(), 'settings.json')):
        test=test+'cofig file OK\n'
    else:
        test=test+'error no config file \n'
    buff=''
    ffpg=asets.ffmpeg_tool.test_ffmpeg()
    if type(ffpg)==str:
        buff =f"(error start:{ffpg})"
    else:
        if ffpg:
            test=test+'ffmpeg OK\n\n'
        else:
            test=test+f"error no ffmpeg {buff}\n\n"
    test=test+f"ID> {message.from_user.id}\n"
    test=test+f"ID admin grup> {admin_grops}\n"
    test=test+f"IP>{requests.get('https://api.ipify.org').content.decode('utf8')}\n"

    if '-all' in message.text.lower():
        api_data=get_telegram_api()
        test=test+f"\napi data\nping:{api_data["ping"]}\nstatus code:{api_data["status"]}\nbot info: {str(api_data["respone"])}\n"

    cpu_percent, ram_percent, disk_percent, response_time, ping1 = monitor_resources()
    bot.send_message(message.chat.id, f"CPU: {cpu_percent}%\nRAM: {ram_percent}%\nDisk: {disk_percent}%\nPing: {response_time}\n∟{ping1}\nфайл подкачки: {swap.percent}% ({swap.total / 1073741824:.2f} GB)\nadmin > {bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator']}\n\n{test}")

# Команда /time_server
@bot.message_handler(commands=['time_server'])
def time_server_command(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    bot.send_message(message.chat.id, f"Серверное время: {current_time}")    
    
#команда /правило 
"""
@bot.message_handler(commands=['правило','правила','закон','rules'])
def send_rules(message):
    if message.date - time.time()<=60:
        try:
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton("правила", url='https://xhak2215.github.io/aea_rules.github.io/')
            markup.add(button1)
            msg=bot.reply_to(message, 'правила перенесены на web страницу\n(будет удалено через 15)', reply_markup=markup)
            for tim in range(1,15):
                bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg.message_id,
                text=f"правила перенесены на web страницу\n(будет удалено через {15-tim})",
                reply_markup=markup
                )
                time.sleep(1)
        finally:
            bot.delete_message(message.chat.id, msg.message_id)
    """   
            

# Хранение данных о репортах
report_data = {}
anti_spam_reports_list={}
report_user = []
# Обработка ответа на сообщение с /report
@bot.message_handler(commands=['report','репорт','fufufu'])
def handle_report(message):
    if message.reply_to_message:
        
        chat_id = message.chat.id#инециалезацыя всякой хрени
        reported_message_text = message.reply_to_message.text
        reporters_user_id = message.from_user.id
        report_user.append(message.from_user.id)
        ban_ded = message.reply_to_message.from_user.id

        if chat_id not in report_data:#проверка на существования пометки chat_id
            report_data[chat_id] = {'responses': set()}

        r_time=time.time()
        # Удаление старых временных меток
        if reporters_user_id not in anti_spam_reports_list:
            anti_spam_reports_list[reporters_user_id] = []
        anti_spam_reports_list[reporters_user_id] = [
            [ts, msg_id] 
            for [ts, msg_id] in anti_spam_reports_list[reporters_user_id] 
            if r_time - ts < 8
        ]
        
        # Добавление текущего временного штампа
        anti_spam_reports_list[reporters_user_id].append([r_time, message.message_id])
        # Проверка на спам
        if len(anti_spam_reports_list[reporters_user_id]) >= 4:
            bot.delete_message(message.chat.id, message.message_id)
            return
            
        report = report_data[chat_id]
        #добавляем id нарушителя в тетрадь смерти Сталина report
        report['responses'].add(ban_ded) 

        user_data = data_base(chat_id, ban_ded)

        message_to_report=str(chat_id).replace("-100", "")
        if len(report['responses'])>1:
            data_base(chat_id, ban_ded, {"auto_reputation":user_data[7]+1})

        # коментарий к репорту
        coment_message=''
        coment=str(message.text).replace('/репорт','').replace('/report','').replace('/fufufu','').split(' ',1)
        if len(coment)>1 and len(coment[1])>2 and coment[1]!='' and coment[1]!=' ':
            coment_message=f"\nкомментарий:{coment[1]} |\n"

        if message.reply_to_message.content_type == 'sticker':
            bot.send_message(admin_grops,f"послали репорт на >> tg://user?id={ban_ded}, @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_report}/{message.reply_to_message.message_id} |{coment_message} ↓стикер↓")
            logger.info(f"послали репорт на >>  @{message.reply_to_message.from_user.username} {coment_message}| https://t.me/c/{message_to_report}/{message.reply_to_message.message_id} стикер id > {message.reply_to_message.sticker.file_id}")
            bot.send_sticker(admin_grops, message.reply_to_message.sticker.file_id)
        else:
            if message.content_type == 'text':
                content=reported_message_text
            else: content=message.content_type
            bot.send_message(admin_grops,f"послали репорт на >> tg://user?id={message.reply_to_message.from_user.id}, @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_report}/{message.reply_to_message.message_id} |{coment_message} сообщение>> {content}")
            logger.info(f"послали репорт на >>  @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_report}/{message.reply_to_message.message_id} |{coment_message} сообщение>> {content}")
 
        bot.reply_to(message,['админы посмотрят','амон уже в пути','да придет же админ и покарает нечестивцев баном','кто тут нарушает?','стоять бояться работает админ','записал ...','щя кто нибуть глянет','щя админ глянет...','записал в лог...','SWAT уже выехал'][random.randint(0,9)])
        # Проверяем, достаточно ли ответов для бана
        reput = user_data[7]
        if reput > 2: n = 4
        elif reput < 0: n = 6
        else: n = 5

        if len(report['responses']) >= n:
            for i in range(len(report_user)):
                reputa=data_base(message.chat.id, report_user[i])[7]
                data_base(message.chat.id, report_user[i], {"auto_reputation":reputa-1})
            teg=''
            if admin_list:
                for i in range(len(admin_list)):
                    if i >0:
                        teg+=f", @{admin_list[i]}"
                    else:
                        teg+=f"@{admin_list[i]}"

            mer=bot.send_message(admin_grops,f"{teg} грубый нарушитель ! >> @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_report}/{message.reply_to_message.message_id}")
            if DELET_MESSADGE:
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                except telebot.apihelper.ApiTelegramException as e:
                    bot.reply_to(mer, f"не удлось удалить сообщения вероятно у бота не достаточно прав\nerror:{e}")
                # Удаляем данные о репорте
                del report_data[chat_id]
    else:
        if time.time()-message.date <= 60:
            bot.reply_to(message, "Пожалуйста, ответьте командой на сообщение, нарушающее правила, чтобы сообщить о нарушении.")
    
@bot.message_handler(commands=['config','настройки'])
def configfile(message):
    global settings, BAMBAM, DELET_MESSADGE, admin_grops, SPAM_LIMIT, SPAM_TIMEFRAME, BAN_AND_MYTE_COMMAND, CONSOLE_CONTROL, AUTO_TRANSLETE, admin_list
    try:
        if  '-r' in message.text:
            try:
                with open("settings.json", "r") as json_settings:
                    settings=json.load(json_settings)
                BAMBAM=bool(settings['bambam'])
                DELET_MESSADGE=bool(settings['delet_messadge'])
                admin_grops=str(settings['admin_grops'])
                SPAM_LIMIT=int(settings['spam_limit'])
                SPAM_TIMEFRAME=int(settings['spam_timer'])
                BAN_AND_MYTE_COMMAND=bool(settings['ban_and_myte_command'])
                CONSOLE_CONTROL=bool(settings['console_control'])
                AUTO_TRANSLETE=dict(settings['auto_translete'])
                admin_list=list(settings['admin_list'])
                logger.info('настройки пере инициалезированы')
            except Exception as e:
                bot.reply_to(message, f"не удалось обновить настройки\nошибка")
                logger.debug('error settings init')
                
        bot.reply_to(message, str(settings))
    except Exception as e:
        bot.reply_to(message,f"error logs file>> {e} ")
        logger.error(f"config error >> {e}\n{traceback.format_exc()}")

@bot.message_handler(commands=['data_base'])
def send_data_base(message):
    # проверка на админа
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id == 5194033781:
        connection = sqlite3.connect('Users_base.db')
        cursor = connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL")
        try:
            arg=message.text.split(' ',1)
            
            errors=''
            datas,info='',''
            if len(arg)<2:
                # Получаем информацию о столбцах в таблице Users
                cursor.execute('SELECT * FROM Users')
                rows = cursor.fetchall() 
                cursor.execute('PRAGMA table_info(Users);')
                data = cursor.fetchall() 
                # Печатаем информацию о столбцах
                for column in rows:
                    datas += str(column)+'\n'
                for i in data:
                    info+=' '+str(list(i)[1])
                connection.close()
            else:
                try:
                    arg_id=int(re.sub(r'[^0-9]', '', str(arg[1]).replace(' ','')))
                except ValueError as e:
                    bot.reply_to(message,f"неверный аргумент({arg[1]}) пример: /data_base <id>")
                    return
                cursor.execute('SELECT * FROM Users WHERE warn_user_id = ? AND chat_id = ?', (arg_id,message.chat.id))
                result = cursor.fetchone()
                datas=str(result).replace(')','').replace('(','')
                cursor.execute('PRAGMA table_info(Users);')
                data = cursor.fetchall() 
                for i in data:
                    info+=' '+str(list(i)[1])
            if datas != None and info != None:
                if len(datas)>500:
                    datas=datas[:490]+"..."
                    errors+="база данных слишком большая для вывода,сокращена до приемлемого объема\n"
                bot.reply_to(message,f"data base>>\n{errors}{info}\n----------------------------------------------------------\n{datas}")
                print(f"база данных :\n{datas}")
            else:
                bot.reply_to(message,"данные не были найдены")
        except Exception as e:
            bot.send_message(admin_grops,f"error send_data_base >> {e} ")
            logger.error(f"error send_data_base >> {e}\n{traceback.format_exc()}")
        finally:
            connection.close()
    else:
        bot.reply_to(message,['ты не администратор!','тебе такое смотреть не дам','ты не админ','не а тебе нельзя','нет','нэт'][random.randint(0,5)])


def status(rec):
    emjges=['❤️','👍','😍','😊'][random.randint(0, 3)]
    if rec >= 1000:
        status=["читы вырубай ! ","как то многовато ,читы ?","уважаемо уважаемо","уважаемый человек"][random.randint(0,3)]
    elif rec <=1:
        status=["ты плохой исправляйся 😡",'ай ай ай нарушаем','фу таким быть','а ну не нарушай ','зачем нарушал, правил что ли не знаешь'][random.randint(0,4)]
    elif rec>=5:
        status=[f'ты хороший {emjges}',f'ты умница {emjges}','законопослушый так держать! ','харош', 'хорошо! продолжай в том же духе'][random.randint(0,2)]
    elif rec>=10:
        status=['партия гордиться вами','ты молодец товарищ!',f'ты хороший {emjges}',f'ты умница {emjges}', f'ты очень хорошоый !'][random.randint(0,3)]
    elif rec<=0:
        status=['ну это бан','в бан тебя','ай ай ай bam bam bam ждет тебя'][random.randint(0,2)]
    elif rec==None:
        status='ошибка получения данных '
    else:
        status=["😐",'ну норм','нейтральный','не без греха'][random.randint(0,3)]
    return status

@bot.message_handler(commands=['я', 'me', 'Я'])
def send_statbstic(message):
    if time.time()-message.date <= 80:
        m = data_base(message.chat.id, message.from_user.id)[5]
        data = data_base(message.chat.id, message.from_user.id, {"num_message":m+1})
        bot.reply_to(message, f"Твоя репутация: {data[3]} \n{status(data[3])}\nколичество сообщений: {data[5]}")

warn_data = {}
# Обработка ответа на сообщение /warn
@bot.message_handler(commands=['warn', 'варн', 'предупреждение'])
def handle_warn(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id==5194033781:
        if message.reply_to_message:

            chat_id = message.chat.id#инециалезацыя всякой хрени
            warn_message = message.reply_to_message.from_user.id
            warn_message_text = message.reply_to_message.text
            message_to_warp=str(chat_id).replace("-100", "")
            
            reputation=data_base(message.chat.id,warn_message)[3]-1
            data_base(message.chat.id,warn_message,{"reputation":reputation})

            bot.reply_to(message,f'репутация снижена \nтекущяя репутация пользевателя:{reputation}')
            bot.send_message(admin_grops,f"репутация снижена >> tg://user?id={message.reply_to_message.from_user.id}, @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} | сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.debug(f"репутация снижена >>  @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.info(f"Пользователь @{message.from_user.username} понизил репутацию @{message.reply_to_message.from_user.username} ") 
        
            # Проверяем, достаточно ли маленькая репутация для мута
            if BAMBAM and reputation <= 0:
                # Ограничиваем пользователя на 24 часа 
                try:
                    bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    until_date=timedelta(hours=24.0),
                    can_send_messages=False
                    )
                    bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} получил мут на 24 часа за нарушение.")
                    logger.info(f"Пользователь {message.reply_to_message.from_user.username} получил мут на 24 часа за нарушение.")    
                except Exception as e:
                    bot.send_message(admin_grops,f"ошибка при выдаче мута:{e}")
                    logger.error(f"{e}")    
                    return    
                #  bot.kick_chat_member(chat_id, user_to_ban, until_date=int(time.time()) + 86400)
                bot.send_message(admin_grops, f"грубый нарушитель ! >> tg://user?id={warn_message} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id}")
        else:
            bot.reply_to(message, "Пожалуйста, ответьте командой на сообщение, нарушающее правила, чтобы снизить репутацию") 
    else:
        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])
                    
@bot.message_handler(commands=['reput', 'репут', 'репутация'])
def handle_reput(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id ==5194033781:
        if message.reply_to_message:
            #инециалезацыя всякой хрени 
            warn_message_text = message.reply_to_message.text
            user=message.reply_to_message.from_user.id
            warn_chat=message.chat.id
            message_to_warp=str(warn_chat).replace("-100", "")

            data=data_base(message.chat.id, user)#партия довольна вами +1 репутации
            data_base(message.chat.id, user, {"reputation": data[3]+1})

            bot.reply_to(message,f'репутация повышена \nтекущяя репутация пользевателя:{data[3]}')
            bot.send_message(admin_grops,f"репутация повышена >> tg://user?id={message.reply_to_message.from_user.id}, @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} | сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.debug(f"репутация повышена >>  @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.info(f"Пользователь @{message.from_user.username} повысил репутацию ") 
        else: 
            bot.reply_to(message, "Пожалуйста, ответьте командой на сообщение, чтобы повысить репутацию")  
    else:
        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])
        
@bot.message_handler(commands=['info','user','кто'])#узнать репутацию
def handle_info(message):
#    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id ==5194033781:
    if message.reply_to_message:
        data_v=''
        i=0
        c=''
        chat_id = message.chat.id
        user=message.reply_to_message.from_user.id

        data=data_base(chat_id, user)
        if '-all' in str(message.text).lower():
            if str(data[9])==str(0):
                date=0
            else:
                date=datetime.fromtimestamp(data[9]).strftime(r"%Y-%m-%d %H:%M:%S")
            bot.reply_to(message,f"ID:{user}\nрепутация:{data[3]}\nавто репутация:{data[7]}\nсообщения:{data[5]}\ntime:{date}")
            return
        
        if str(data[9]) and str(data[9]) != str(0):
            if data[3]>=86400:
                if round((time.time()-data[9])/86400) == 1:
                    c='день назад'
                else:
                    c='дней назад' 
                i=str(round((time.time()-data[9])/86400)) + c
            elif data[3]>=3600:
                if round((time.time()-data[9])/3600) == 1:
                    c='час назад'
                else:
                    c='часов назад' 
                i=str(round((time.time()-data[9])/3600)) + c
            data_v=f"\nзащел в чат: {datetime.fromtimestamp(data[9]).strftime(r"%Y-%m-%d %H:%M:%S")} ({i})"

        if time.time()-message.date <=65:
            bot.reply_to(message,f"репутация пользователя:{data[9]}\nсообщения:{data[5]}{data_v}") # \nза день:{data[6]}{data_v}
    else: 
        if time.time()-message.date <=65:
            bot.reply_to(message, "Пожалуйста, ответьте командой на сообщение, чтобы узнать репутацию и количество сообщений")  
#    else:
#        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])

@bot.message_handler(commands=['гойда','goida'])
def handle_goida(message):
    if time.time() - message.date <= 60:
        rand=random.randint(0, 7)
        if rand==0:bot.reply_to(message, 'наш слон')
        elif rand==1:bot.reply_to(message, 'ГООООООЛ')
        elif rand==2:bot.reply_to(message, 'да будет же гойда')
        elif rand==3:bot.reply_to(message, 'держи гойду')
        elif rand==4:bot.reply_to(message, 'ZOV гойда ZOV')
        elif rand==5:bot.send_video(message.chat.id,io.BytesIO(requests.get(r'https://github.com/xHak2215/arhive-host-file/raw/refs/heads/main/goida-%D0%B3%D0%BE%D0%B9%D0%B4%D0%B0.mp4').content),reply_to_message_id=message.message_id)
        elif rand==6:bot.send_video(message.chat.id,io.BytesIO(requests.get(r'https://github.com/xHak2215/arhive-host-file/raw/refs/heads/main/%D1%81%D1%83%D0%BF%D0%B5%D1%80_%D0%B3%D0%BE%D0%B9%D0%B4%D0%B0.mp4').content),reply_to_message_id=message.message_id)
        elif rand==7:bot.send_video(message.chat.id,io.BytesIO(requests.get(r'https://github.com/xHak2215/arhive-host-file/blob/main/%D0%BE%D1%85%D0%BB%D0%BE%D0%B1%D1%8B%D1%81%D1%82%D0%B8%D0%BD-%D0%B3%D0%BE%D0%B9%D0%B4%D0%B0-%D0%B3%D0%BE%D0%B9%D0%B4%D0%B0-%D0%BA%D1%80%D0%B8%D1%87%D0%B8%D1%82.gif?raw=true').content),reply_to_message_id=message.message_id)

        
@bot.message_handler(commands=['bambambam'])
def bambam(message):
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
                bot.reply_to(message,['мага что такое?','кто то опять беспредельничяет'][random.randint(0,1)])
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
def handle_ban_command(message):
    if not BAN_AND_MYTE_COMMAND:
        bot.reply_to(message,'отключено , для включения задайте парамитер (в settings.json) ban_and_myte_command как true')
        return
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id == 5194033781:
        if message.reply_to_message:
            if '\n' in message.text:
                reason = message.text.split("\n",1)[1]
            else:
                bot.reply_to(message,"вы не указали причину ! пример команды\n/ban\n<причина>")
                return
            try:
                bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                logger.info(f"ban for {message.reply_to_message.from_user.username} id:{message.reply_to_message.from_user.id}\nreason:{reason}")
                bot.send_message(admin_grops,f'ban for {message.reply_to_message.from_user.username}\nreason:{reason}')
            except telebot.apihelper.ApiTelegramException as e:
                bot.reply_to(message,f'error>> {e}\nвероятно у бота недостаточно прав')
                logger.error(f"{e}\n{traceback.format_exc()}")

        else:
            bot.reply_to(message, "ответье на сообщение человека которого хотите забанить ")
    else:
        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет','ты думал сможешь взять и забанить наивный'][random.randint(0,5)])

@bot.message_handler(commands=['mute','мут'])
def handle_mute_command(message):
        if ' ' not in message.text:
            bot.reply_to(message,"не правельный синтакисис команды")
        commad=message.text.split(' ',1)[1]
        if not BAN_AND_MYTE_COMMAND:
            bot.reply_to(message,'отключено, для включения задайте парамитер (в settings.json) ban_and_myte_command как true')
            return
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id == 5194033781:
            if message.reply_to_message:
                cont = commad.split("\n")[0].lower()
                reason = commad.split("\n", 1)[1]
                
                deleua = cont.split(" ")[1]
                timer = int(cont.split(" ")[0])

                if deleua=='h' or deleua=='hour' or deleua=='hours' or deleua=='час' or deleua=='часы':
                    deleu=3600

                elif deleua=='d' or deleua=='day' or deleua=='days' or  deleua=='день' or deleua=='дни':
                    deleu=86400

                elif deleua=='m' or deleua=='minute' or deleua=='минута' or deleua=='минуты':
                    deleu=60
                
                elif deleua=='неделя' or deleua=='weeks' or deleua=='week':
                    deleu=604800

                elif deleua=='месяц' or deleua=='месяцы' or deleua=='month' or deleua=='months':
                    deleu=2592000

                elif deleua=='s' or deleua=='second' or deleua=='секунды' or deleua=='секунда':
                    deleu=0
                else:
                    bot.reply_to(message,f"не корректное значение времени {deleua} использован аргумент по умолчанию (в часах)\nпример: /мут time:1 h \nпричина  \nh - часы (по умолчанию), d - дни, m - минуты ")
                    return
                
                user = message.reply_to_message

                try:
                    bot.restrict_chat_member(message.chat.id, user.from_user.id, until_date=(message.date + timer*deleu))
                    logger.info(f"mute for {user.from_user.username} id:{user.from_user.id} time:{timer}{deleua} reason:{reason}")
                    bot.send_message(admin_grops,f"mute for {user.from_user.id}\ntime:{timer}{deleua} ({timer*deleu}s.) {reason}")
                except telebot.apihelper.ApiTelegramException as e:
                    bot.reply_to(message,f'error>> {e}\nвероятно у бота недостаточно прав')
                    logger.error(f"{e}\n{traceback.format_exc()}")
        else:
            bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет','ты думал сможешь взять и замутить наивный'][random.randint(0,5)])


@bot.message_handler(commands=['cmd','console'])
def handle_command(message):
    try:
        if CONSOLE_CONTROL:
            if str(message.chat.id)==str(admin_grops) or message.from_user.id == 5194033781:
                if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id == 5194033781:
                    command=str(message.text).split(' ',1)[1]
                    if sys.platform.startswith('win'): # кросс плотформиность
                        result=subprocess.run(command , shell=True, stdout=subprocess.PIPE, text=True)
                        out=result.stdout
                    else:
                         result=subprocess.run(command , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                         out=result.stdout + result.stderr 
                    bot.reply_to(message, out if out !=None else 'None')
                else:
                    if message.date - time.time()<=60:
                        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет','ай ай ай с терминалом играться '][random.randint(0,5)])
            else:
                if message.date - time.time()<=60:
                    bot.reply_to(message,'эта команда может быть выполнена только в группе администрации')
        else:
            if message.date - time.time()<=60:
                bot.reply_to(message,'отключено в настройках(settings.json) парамитер console_control')
    except:
        bot.reply_to(message,traceback.format_exc())

def scan_hex_in_text(text:str)->bool:
    for i in text:
        if i not in ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']:
            return False
    return True

@bot.message_handler(commands=['t','translate','перевод'])  
def translitor(message):
    if message.reply_to_message:
        if not message.reply_to_message.text:
            bot.reply_to(message,["я могу переводить только текст!", "это не текст, я такое не переведу"][random.randint(0,1)])
            return
        bins=str(message.reply_to_message.text).replace(' ','').lower()
        if set(bins) == {'0', '1'} :
            bytes_list = [int(bins[i:i+8], 2) for i in range(0, len(bins), 8)]
            bot.reply_to(message,bytes(bytes_list).decode('utf-8', errors='replace'))
            return
        elif bins[0:4] == '202e' or scan_hex_in_text(bins):
            bot.reply_to(message, bytes.fromhex(bins).decode('utf-8', errors='replace'))
            return
        elif len(message.text.split(' ')) > 1:
            if str(message.text.split(' ')[1].replace(' ','')) == 'translit' or str(message.text.split(' ')[1]).replace(' ','') == 'транслит':
                bot.reply_to(message, ''.join(str(asets.dictt.translit_eng.get(c, c) for c in message.reply_to_message.text)))
                return
            
        translated = GoogleTranslator(source='auto', target='ru').translate(message.reply_to_message.text)
        bot.reply_to(message, f"перевод:\n{translated}")
    else:
        if ':' in message.text:
            text=str(message.text).replace('/t','').replace('/translate','').replace('перевод', '').split(':')
            if text[1].lower()=="bin":
                hex_str = binascii.hexlify(text[0].encode('utf-8')).decode()
                binary_str = ''.join([
                format(int(hex_str[i:i+2], 16), '08b')for i in range(0, len(hex_str), 2)])
                bot.reply_to(message, ' '.join([binary_str[i:i+8] for i in range(0, len(binary_str), 8)]))
                return
            
            elif text[1].lower()=="hex":
                bot.reply_to(message, '202e'+(text[0].encode("utf-8").hex().replace("'",'')))
                return
            
            elif text[1].lower()=="translit" or text[1].lower()=="транслит":
                bot.reply_to(message,str(''.join(asets.dictt.translit_ru.get(c, c) for c in text[0])))

            else:
                try:
                    translated = GoogleTranslator(source='auto', target=text[1].replace(' ','')).translate(text[0])
                    bot.reply_to(message, f"перевод:\n{translated}")
                except deep_translator.exceptions.LanguageNotSupportedException:
                    bot.reply_to(message, "похоже язык не определен (примечание язык нужно указывать в сокращённой форме)",parse_mode='HTML',disable_web_page_preview=True)
        else:
            bot.reply_to(message, "нет арументов или они ошибочны")
        

vosk.SetLogLevel(-1) # отключение логов
rec = KaldiRecognizer(Model(vosk_model_path), 16000) # эксмпляр модели 


@bot.message_handler(commands=['to_text','в_текст'])
def audio_to_text(message):
    if message.reply_to_message:
        if message.reply_to_message.voice:
            if not os.path.exists(vosk_model_path):
                logger.warning(f"Модель Vosk не найдена по пути: {vosk_model_path}")
                bot.reply_to(message,f'модель {vosk_model_path} не найдена сообщите разработчику/хосту о проблеме')
                return
            else:
                msg=bot.reply_to(message,['выполняется','идет расшифровка','приодеться немного подождать...','Loading','загрузка'][random.randint(0,4)])
            try:
                timers=time.time()

                file_info = bot.get_file(message.reply_to_message.voice.file_id)
                if file_info:
                    ogg_data = bot.download_file(file_info.file_path)
                else:
                    logger.error(f"no data file_info ({file_info})")
                    if msg:
                        bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=msg.message_id,
                        text=f"случилась ошибка :("
                        )
                    else:
                        bot.reply_to(message, f"случилась ошибка :(")
                    return

                # Распознавание
                results = []
                data_r=asets.ffmpeg_tool.audio_conwert(ogg_data,'wav') # конвертирую в wav
                if not data_r is bytes:
                    logger.error(data_r)
                    bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=msg.message_id,
                    text=f"случилась ошибка :(\n{data_r}"
                    )
                    return
                wav_buffer = io.BytesIO(data_r)
                while True:
                    data = wav_buffer.read(4000)
                    if not data:
                        break
                    if rec.AcceptWaveform(data):
                        results.append(json.loads(rec.Result()))
                final = json.loads(rec.FinalResult())
                text = str(" ".join([res.get("text", "") for res in results if "text" in res] + [final.get("text", "")]))
                try:
                    bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=msg.message_id,
                    text=f"текст:\n{text[:4050]}\n\nвремя исполнения:{time.time()-timers:.2f}")
                except:bot.reply_to(message,f"текст:\n{text[:4050]}\n\nвремя исполнения:{time.time()-timers:.2f}с.")
                
            except Exception as e:
                logger.error(f"Ошибка распознавания: {str(e)}\n{traceback.format_exc()}")
                if msg:
                    bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=msg.message_id,
                    text=f"случилась ошибка :(\n{e}"
                    )
        else:
            bot.reply_to(message, "это не ГС; Пожалуйста, ответьте командой на голосовое сообщение чтобы распознать текст в нем")
        #elif message.reply_to_message.photo:
        #    pass # распознование текста на фото не реализовал(спиздил код) из за необходимости использования нескольких тяжелых библиотек   
    else:
        bot.reply_to(message, "Пожалуйста, ответьте командой на голосовое сообщение чтобы распознать текст в нем")
        
@bot.message_handler(commands=['download','dow'])
def download(message):
    if '-help' in message.text or '-h' in message.text:
        bot.reply_to(message,
            'потдерживает скачивание голосовых сообщений,стикеров и аудио дорожек видео(звук из видео)\n'
            'придел веса файла 20 мб\n'
            "возможные форматы: <a href='https://github.com/xHak2215/admin_bot#format'>см. дакументацию</a>\n"
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
                        with Image.open(io.BytesIO(requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}', str(file_info.file_path).split('/')[1], allow_redirects=True).content)) as img:
                        # Конвертируем в RGB для форматов, которые не поддерживают прозрачность
                            if output_format in ('JPEG', 'JPG'):
                                img = img.convert('RGB')
                            
                elif message.reply_to_message.photo:# скачиваем фото
                    photo_id = message.reply_to_message.photo[-1].file_id
                    file_info = bot.get_file(photo_id)
                    img = Image.open(io.BytesIO(bot.download_file(file_info.file_path)))
                    if output_format in ('JPEG', 'JPG'):
                        img = img.convert('RGB')
                else:
                    bot.reply_to(message, "не потдерживаеться")
                    return
        
                # Сохраняем в байтовый поток
                output_buffer = io.BytesIO()
                
                if "resize:" in message.text:
                    rise=str(message.text).split('resize:')[1]
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
                        file_stream.name = f'sticker_{datetime.fromtimestamp(time.time()).strftime(r"%Y-%m-%d %H:%M")}.{output_format}'
            
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
                        file_info = bot.get_file(message.reply_to_message.voice.file_id)
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
                    data=asets.ffmpeg_tool.audio_conwert(video_data.getvalue(),output_format)
                    if not data is bytes:#если ошибка задаем пораметры по умолчанию
                        bot.reply_to(message,f'случилась ошибка>{data} приняты параметры по умолчанию')
                        data=video_data
                        output_format='ogg'
                        return
                    with io.BytesIO(data) as file_stream:
                        file_stream.name = f'voice_{datetime.fromtimestamp(time.time()).strftime(r"%Y-%m-%d %H:%M")}.{output_format}'
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
                            file_stream.name = f'music_{datetime.fromtimestamp(time.time()).strftime(r"%Y-%m-%d %H:%M")}.{oformat}'
            
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
        if message.reply_to_message and message.reply_to_message.sticker:
            if not os.path.exists(os.path.join(os.getcwd(), 'asets', "blacklist.json")):
                logger.warning('no file blacklist.json')
                with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'w') as f:
                    json.dump({'stiker':[0]}, f)
            with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'r') as f:
                bklist.blist = json.load(f)['stiker']
    
            bklist.add(message.reply_to_message.sticker.file_id)
    
            with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'w') as f:
                json.dump({'stiker':bklist.blist}, f)
            bot.send_message(admin_grops,f'@{message.from_user.username} добавил стикер (id:{message.reply_to_message.sticker.file_id}) в черный список')
        else:
            if len(message.text.split(' '))>1:
                if message.text.split(' ')[1].lower() =='-info':
                    bot.reply_to(message,f"количество заблокированых стикеров:{bklist.slen()}")
                    return
            bot.reply_to(message,'ответьте этой командой на стикер что бы внести его в черный список ')
    else:
        if message.date - time.time()<=60:
            bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет','нэт'][random.randint(0,5)])
    
@bot.message_handler(commands=['unblaklist'])
def unblaklist(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id ==5194033781:
        if message.reply_to_message and message.reply_to_message.sticker:
            if not os.path.exists(os.path.join(os.getcwd(), 'asets', "blacklist.json")):
                logger.warning('no file blacklist.json')
                with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'w') as f:
                    json.dump([0], f)
            with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'r') as f:
                bklist.blist = json.load(f)['stiker']
            file_id = str(message.reply_to_message.sticker.file_id)
            if file_id in bklist.blist :
                bklist.removes(file_id) # удаление стикера из списка
            else:
                bot.reply_to(message,['такого стикера в списке нет','стикера и так нет в списке','такого не нашел такого не знаю'][random.randint(0,1)])
                return
            with open(os.path.join(os.getcwd(), 'asets', "blacklist.json"), 'w') as f:
                if len(list(bklist.blist))<1:
                    bklist.add([0])
                json.dump({'stiker':bklist.blist}, f)
            bot.send_message(admin_grops,f'@{message.from_user.username} убрал стикер (id:{message.reply_to_message.sticker.file_id}) из черного списка')
        else:
            bot.reply_to(message,'ответьте этой командой на стикер что бы убрать его из черного списка')
    else:
        if message.date - time.time()<=60:
            bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет','нэт','Для этого нужно быть админом'][random.randint(0,5)])

@bot.message_handler(commands=['message_info'])
def send_message_info(message):
    if message.reply_to_message:
        out_message=' '
        out_message+=f'тип: {message.reply_to_message.content_type}\n'
        out_message+=f'message id:{message.message_id}\n'
        if str(message.reply_to_message.content_type) in ['video','photo','animation','sticker']:
            if message.reply_to_message.sticker: media_id = message.reply_to_message.sticker.file_id
            elif message.reply_to_message.video: media_id = message.reply_to_message.video.file_id
            elif message.reply_to_message.photo: media_id = message.reply_to_message.photo[-1].file_id
            elif message.reply_to_message.animation: media_id = message.reply_to_message.animation.file_id
            file_info = bot.get_file(media_id)
            out_message+=f"ulr:https://api.telegram.org/file/bot{bot.token}/{file_info.file_path} \nвес: {round(len(requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}').content),2)} байт\n"
        if message.reply_to_message.sticker: out_message+=f'sticker ID: {message.reply_to_message.sticker.file_id}\nemoji:{message.reply_to_message.sticker.emoji}\n'
        #if message.reply_to_message.video:
            #media_id = message.reply_to_message.video.file_id
            #file_info = bot.get_file(media_id)
            #print(requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}', file_info.file_path.split('/')[1], allow_redirects=True).content)
            #out_message+=f'meta data:{str(requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}', file_info.file_path.split('/')[1], allow_redirects=True).content)}\n'
        elif message.reply_to_message.photo:
            media_id = message.reply_to_message.photo[-1].file_id
            file_info = bot.get_file(media_id)
            with Image.open(io.BytesIO(requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}', str(file_info.file_path).split('/')[1], allow_redirects=True).content)) as img:
                out_message+=f'meta data (exif):{img.getexif()}\n'
            out_message+=f'width(высота): {message.reply_to_message.photo[-1].width}\n'
            out_message+=f'height(ширена): {message.reply_to_message.photo[-1].height}\n'
        bot.reply_to(message,out_message)

@bot.message_handler(commands=['gif_search', 'поиск_gif', 'Поиск_gif', 'search_gif'])
def gif_search(message):
    if len(message.text.split(' '))<=1:
        bot.reply_to(message, "не хватает аргумента, пример:<code>/gif_search котик</code>",parse_mode='HTML')
        return
    promt=message.text.split(' ',1)[1]
    tokin='FfeiGAnJZhno9w7M6OCwaTguVJ0ePmQv' # я дарю вам этот токен но он бесплатный и вы можете создать свой 

    data=requests.get("https://api.giphy.com/v1/gifs/search",params={'api_key':tokin,
                                                                'q':promt, 'limit':10})
    list_gif=data.json()['data']
    if data.json()['meta']['status']==200:
        if len(list_gif)>=1:
            gif=list_gif[random.randint(0, len(list_gif)-1)]['images']['original']['url']

            gif_data=requests.get(gif).content

            bot.send_video(message.chat.id, gif_data, reply_to_message_id = message.id)
        else:
            bot.reply_to(message, ["похоже такой GIF нет", "я не нашел такую GIF", "похоже такого нету", "ничего не нашлось, увы", "ничего не нашлось =[", "ничего не нашлось :("][random.randint(0,5)])
            return
    else:
        bot.reply_to(message, f"случилась какая то ошибка =[\nмета данные:{data.json()['meta']}")
        return

@dataclass
class DeleteData:
    message_l = []
    chat_id = 0

# Глобальный экземпляр для хранения данных
delete_data = DeleteData()

def nacase(message, delete_message=None):
    try:
        user_messages[message.from_user.id] = []
        the_message = str(message.chat.id).replace("-100", "")
        
        if bool(BAMBAM): 
            # Ограничиваем пользователя на 24 часа
            try:
                bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    until_date=int(time.time()) + 86400, 
                    can_send_messages=False
                )
            except telebot.apihelper.ApiTelegramException as e:
                bot.send_message(admin_grops, f'{str(e)}\nВероятно у бота недостаточно прав')
                logger.error(f'{str(e)}\nВероятно у бота недостаточно прав')

            auto_reputation=data_base(message.chat.id, message.from_user.id)[7]
            data_base(message.chat.id, message.from_user.id, {"auto_reputation":auto_reputation})

            bot.send_message(
                message.chat.id, 
                f"Пользователью @{message.from_user.username} выдан мут на 1 день."
            )

        text = str(message.text if message.content_type == "text" else message.content_type)[:120]
        # Формируем сообщение для админов
        admin_msg = (
            f'Обнаружен спам от пользователя >> @{message.from_user.username}\n'
            f'Сообщение: {text}'
            f'|https://t.me/c/{the_message}/{message.message_id}'
        )
        
        if DELET_MESSADGE and delete_message:
            markup = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton(
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

        if message.from_user.username:
            us=f" @{message.from_user.username},"
        else:
            us=''
        
        logger.info(f'Обнаружен спам от пользователя >>{us} id: {message.from_user.id} message:https://t.me/c/{the_message}/{message.message_id}')
        
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {str(e)}\n{traceback.format_exc()}")

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
        i=0
        for msg_id in delete_data.message_l:
            try:
                bot.delete_message(delete_data.chat_id, msg_id)
                deleted_count += 1
            except telebot.apihelper.ApiTelegramException as e:
                if i<=2:
                    bot.send_message(admin_grops, f"случилась ошибка при попытке удаления сообщений\n{str(e)}\nвероятно у бота недостаточно прав")
                i=i+1
            except:continue

        # Ответ пользователю
        bot.answer_callback_query(call.id, f"Успешно удалено {deleted_count}/{len(delete_data.message_l)} сообщений")
        logger.info(f"Успешно удалено {deleted_count}/{len(delete_data.message_l)} сообщений. инициатор: @{call.from_user.username}")
    except Exception as e:
        bot.send_message(admin_grops,f"Ошибка при удалении: {str(e)}")
        logger.error(f"Ошибка в handle_spam_deletion: {str(e)}\n{traceback.format_exc()}")

@bot.message_handler(commands=['ping','пинг'])
def ping_command(message):
    if '-help' in message.text or '-h' in message.text:
        bot.reply_to(message, 'аргументы: /ping (ссылка для тестирования по умолчанию https://ya.ru) (количество повторов измерения)  (режим расчета).\nрежимы расчета: 1 - вычисление средни статистической задержки из всех попыток. по умолчанию (не указывая значение) 2 - отображение задержки каждой попытки\nпример:<code>/ping example.com 5 1</code>',parse_mode='HTML',disable_web_page_preview=True)
        return
    data=message.text.split(' ',1)
    test_time=[]

    if len(data)>1:
        command=data[1].split(' ')

        if "http://" in command[0].replace(' ','') or "https://" in command[0].replace(' ',''):
            url=command[0].replace(' ','')
        else:
            url=f"https://{command[0].replace(' ','')}"

        for _ in range(int(command[1].replace(' ',''))):
            try:
                timer=time.monotonic()
                response=requests.get(url, timeout=20)
                test_time.append(time.monotonic() - timer)
            except requests.exceptions.ReadTimeout:
                bot.reply_to(message,'превышена задержка (20s) возможно сайт недоступен')
                return
            
        if command[2].replace(' ','') == '1':
            num=0
            for i in test_time: num=+i
            ping = round(num / len(test_time), 4)

            bot.reply_to(message, f"ping: {ping}")

        if command[2].replace(' ','') == '2':
            ping=''
            for i in range(len(test_time)): ping+=f"{i} ping: {round(test_time[i], 3)}\n"

            bot.reply_to(message, ping)

    else:
        url='https://ya.ru'
        start_time = time.time()
        try:
            response=requests.get(url, timeout=20)
        except requests.exceptions.ReadTimeout:
            bot.reply_to(message,'превышена задержка (20s) возможно сайт недоступен')
            return
        if response.status_code==200:
            scode= ''
        else:
            scode=f'\nerror conect\nstatus code {response.status_code}'
        p_time=time.time() - start_time
        bot.reply_to(message, f"ping:{p_time} {scode}")
        return


@dataclass
class SearhData:
    title_and_url=[]
    wiki_api_out=[]
    message_id=-1
    chat_id=0

wiki_api=wiki()
data_wiki_serh=SearhData()

@bot.message_handler(commands=['serh','поиск','searh'])
def searh_network(message): 
    if '-ping' in message.text:
        ping=wiki_api.wiki_ping()
        if ping['error']!=None:
            bot.reply_to(message,f"превышена задержка (20s) возможно ресурс недоступен\nstatus code:{ping['error']}")
            return
        bot.reply_to(message,f'ping to wikipedia.org>{ping['time_out']}',parse_mode='HTML',disable_web_page_preview=True)
        return
    if len(message.text.split(' ',1))>1:
        promt=message.text.split(' ',1)[1]
    else:
        bot.reply_to(message,"вы не указали  аргумент")
        return
    
    e_mess=bot.reply_to(message,"поиск...")
    try:
        out_wiki=wiki_api.search_query(promt)
    except Exception as e:
        logger.error(f"{e}\n{traceback.format_exc()}")
        wiki_api.time_out_edit(40)
        try:
            out_wiki=wiki_api.search_query(promt)
        except Exception as e:
            logger.error(f"{e}\n{traceback.format_exc()}")
            bot.edit_message_text(f"случилась ошибка",
            data_wiki_serh.chat_id,
            e_mess.id)
            return
        finally:wiki_api.time_out_edit(20)

    if out_wiki == None:
        bot.edit_message_text("не удалось найти, возможно проблемы настороне сервера",
            data_wiki_serh.chat_id,
            e_mess.id)
        return
    data_wiki_serh.wiki_api_out=out_wiki

    l=[]
    for i in out_wiki:
        l.append(i['page'])
    data_wiki_serh.title_and_url = l
    data_wiki_serh.chat_id = message.chat.id

    markup = telebot.types.InlineKeyboardMarkup()
    for i in range(len(l)):
        button = telebot.types.InlineKeyboardButton(
            l[i], 
            callback_data=f"title_wiki_resurse_{e_mess.id}_{i}"
            )
        markup.add(button)
    if len(l)<=0:
        bot.edit_message_text(['упс ничего не найдено','я ничего не нашел','я ничего не смог найти','не найдено попробуйте переформулировать запрос' ][random.randint(0,3)],
                              data_wiki_serh.chat_id,
                              e_mess.id
                              )
    else:
        data_wiki_serh.message_id = bot.edit_message_text("выберите наиболее подходящую статью",
                              data_wiki_serh.chat_id,
                              e_mess.id,
                              reply_markup=markup
                              ).id


@bot.callback_query_handler(func=lambda call:call.data.startswith('title_wiki_resurse_'))
def handle_wiki_searh(call):
    for title in data_wiki_serh.title_and_url:
        if title == data_wiki_serh.title_and_url[int(call.data.split('_')[-1])]:
            bot.answer_callback_query(call.id, "выполняю")
            page=wiki_api.title_to_page(title)
            link=''
            
            if page == '' or page == None:
                page=['упс ничего не найдено','я ничего не нашел','я ничего не смог найти','не найдено попробуйте переформулировать запрос' ][random.randint(0,3)]
            else:
                if len(page)>=2000:
                    for i in data_wiki_serh.wiki_api_out:
                        if i['page'] == title:
                            link=i['link']
                    page=page[:2000]+'...'+f"\nстатья:{link}"
            bot.answer_callback_query(call.id)
            bot.edit_message_text(
            chat_id=data_wiki_serh.chat_id,
            message_id=call.data.split('_')[-2],
            text=page
            ,parse_mode='HTML',disable_web_page_preview=True
            )

def ext_arg_scob(arg:str)-> str|list:
    if '{' not in arg:
        return arg
    bufer=[]
    for con in arg.split('{'):
        if '}' in con:
            bufer.append(con.split('}')[0])
    return bufer

def evaluate_condition(condition:str):
    """## функция исполнения логических и математических операций 
    Args:
        condition (_str_): логическое или маткематическое вырожение
    Returns:
        bool or int
    """
    b,a,op='','',''
    for ops in ["+","-","*","/","**","%",'==','!=','<','<=','>','>=']:
        if ops in condition:
            data=str(condition).split(ops,1)
            op=ops
            a=data[0]
            b=data[1]
            break
    try:
        try:
            a = int(a)
        except ValueError:    
            a = float(a)
    except ValueError:
        a = str(a)
    try:
        try:
            b = int(b)
        except ValueError:       
            b = float(b)
    except ValueError:
        b = str(b)
        
    if op == "+": return a + b
    elif op == "-": return a - b
    elif op == "*": return a * b
    elif op == "/":
        if a == 0:
            return "-0"
        return a / b
    elif op == "**": return a ** b
    elif op == "%": return a % b
    elif op == '==': return a == b
    elif op == '!=': return a != b
    elif op == '<': return a < b
    elif op == '<=': return a <= b
    elif op == '>': return a > b
    elif op == '>=': return a >= b
    else:return None

def r_value(vare:str,value)->str:
    """
    ### заменяет переменную в скобках(таких:`{}`) на содержимое этой самой пременной

    :param1: строка в которой должны быть заменены переменные  

    :param2: словарь с переменными

    :return: та же строка на переменные заменены на их содержимое  
    """
    if '{' in vare and '}' in vare:
        vars=ext_arg_scob(vare)
        for var in vars:
            if var in list(value.keys()):
                vare=vare.replace('{'+str(var)+'}',str(value[var]))
    return vare

@bot.message_handler(commands=['creat'])
def create_logic(message):
    send_bufer=[]
    if message.reply_to_message:
        reply_to=message.reply_to_message.text if message.reply_to_message.text != None else '$none'  
        username=message.reply_to_message.from_user.username if message.reply_to_message.from_user.username != None else '$none'   
    else:
        reply_to='$none'
        username='$none'
    value={"$pi":3.1415926535, "$reply_to":reply_to, "$username":username}
    program_line=[]
    line=0
    program=message.text.split('creat',1)[1].replace('/creat','')
    program_line=str(program).split('\n')
    kav_serh_pattern = re.compile(r'\"[^\"]+\"')
    while True:
        if line>len(program_line):
            break
        if line >300:break
        try:
            command=program_line[line]
        except IndexError:
            break

        if command.startswith('send'):
            if '"' in command: 
                arg=kav_serh_pattern.search(command)
                if arg == None:
                    bot.reply_to(message,f"{command}]\n     {'^'*len(command)}\nerror incorret arg \nline:{line}")
                    return
                else:arg=arg.group()[1:-1]
            else:
                if ' ' in command:
                    if command.split(' ',1)[1] in list(value.keys()):
                        send_bufer.append(value[command.split(' ',1)[1]])
                        return
                bot.reply_to(message,f"{command}]\n     {'^'*len(command)}\nerror incorret arg \nline:{line}")
                return
            if '{' in arg and '}' in arg:
                vars=ext_arg_scob(arg)
                for var in vars:
                    if var in list(value.keys()):
                        arg=arg.replace('{'+str(var)+'}',str(value[var]))
            send_bufer.append(arg)

        elif command.startswith('var'):
            try:
                data=command.split(' ',1)[1]
                arg=data.split('=',1)[1]
            except:
                bot.reply_to(message,f"{command}]\n     {'^'*len(command)}\nerror incorret arg \nline:{line}")
                return
            if '{' in arg and '}' in arg:
                vars=ext_arg_scob(arg)
                for var in vars:
                    if var in list(value.keys()):
                        arg=arg.replace('{'+str(var)+'}',str(value[var]))
            value[data.split('=')[0].replace(' ','')]=arg

        elif command.startswith('value'):
            send_bufer.append(str(value))

        elif command.replace(' ','')[:1]=='#':pass
        
        elif command.startswith('calc'):
            try:
                args=command.split(' ',1)[1]
                val=args.split('=',1)[0]
            except IndexError:
                bot.reply_to(message,f"{command}     \n{'^'*len(command)}\nerror no args \nline:{line}")
                return
            arg=str(args.split('=',1)[1]).replace(' ','')
            arg=r_value(arg,value)
            if "or" in arg.lower() or "and" in arg.lower() or "not" in arg.lower():
                expr = str(arg).replace(" ", "").lower()
                # Обрабатываем логическое NOT
                if expr.startswith("not"):
                    arg = evaluate_condition(expr[3:])
                    out= not arg

                # Обрабатываем OR и AND (разделяем по операторам)
                for op in ["or", "and"]:
                    if op in expr:
                        parts = expr.split(op)
                        if len(parts) == 2:
                            left = evaluate_condition(parts[0])
                            right = evaluate_condition(parts[1])
                            out= left or right if op == "or" else left and right
            else:
                out=evaluate_condition(arg)
            if out!=None:
                if out != '-0':
                    value[val]=str(out)
                else:
                    bot.reply_to(message,f"{command}\n{'^'*len(command)}\nerror division by zero \nline:{line}")
                    return
            else:
                bot.reply_to(message,f'{command}\n{'^'*len(command)}\nне коректное условие \nстрока:{line}')
                return
                
        elif command.startswith('.end'):break
        elif command.startswith('program'):
            value['$program_name']=r_value(command,value).split(' ',1)[1]
        
        elif command.startswith('random'):
            try:
                cont=command.split(' ',1)[1]
            except IndexError:
                bot.reply_to(message,f"{command}\n{'^'*len(command)}\nerror no args \nline:{line}")
                return
            
            if '{' in cont and '}' in cont:
                vars=ext_arg_scob(cont)
                for var in vars:
                    if var in list(value.keys()):
                        cont=cont.replace('{'+str(var)+'}',str(value[var]))
            if '=' in cont and '-' in cont:
                arg=cont.split('=',1)[1]
                a=arg.split('-',1)[0]
                b=arg.split('-',1)[1]
                v=cont.split('=',1)[0]
            else:
                bot.reply_to(message,f"{command}\n{'^'*len(command)}\nerror no args or invalid args\nline:{line}")
                return
            try:
                a,b=int(a),int(b)
            except ValueError:
                bot.reply_to(message,f"{command}\n{'^'*len(command)}\nerror invalid literal for num \nline:{line}")
                return
            if a==b+1:
                value[v]=a
            else:
                value[v]=random.randint(a,b)
            #    bot.reply_to(message,f"{command}\n{'^'*len(command)}\nerror not correct arg \n(random {v}=start num-stop num) \nline:{line}")
            #    return
        elif command.startswith('log'):
            logger.info(f"/creat log> line:{line} message:{command.split(' ',1)[1]}")

        elif command.startswith('if'):
            try:
                arg=command.split(' ',1)[1].split(':',1)[0]
            except IndexError:
                bot.reply_to(message,f"{command}\n   {'^'*len(command)}\nerror no args \nline:{line}")
                return
            out=None
            if '{' in arg and '}' in arg:
                vars=ext_arg_scob(arg)
                for var in vars:
                    if var in list(value.keys()):
                        arg=arg.replace('{'+str(var)+'}',str(value[var]))
            if "or" in arg.lower() or "and" in arg.lower() or "not" in arg.lower():
                expr = str(arg).replace(" ", "").lower()
                # Обрабатываем логическое NOT
                if expr.startswith("not"):
                    arg = evaluate_condition(expr[3:])
                    out= not arg
                
                # Обрабатываем OR и AND (разделяем по операторам)
                for op in ["or", "and"]:
                    if op in expr:
                        parts = expr.split(op)
                        if len(parts) == 2:
                            left = evaluate_condition(parts[0])
                            right = evaluate_condition(parts[1])
                            out= left or right if op == "or" else left and right
                        else:out=None
                    else:out=None
            else:
                out=evaluate_condition(arg)
            if out is None:
                bot.reply_to(message,f'{command}\n{'^'*len(command)}\nне коректное условие \nстрока:{line}')
                return
            if out == '-0':
                bot.reply_to(message,f"{command}\n{'^'*len(command)}\nerror division by zero \nline:{line}")
                return
            if out == 'True' or out:
                new_code = command.split(':', 1)[1]
                ine=1
                if '&' in command:
                    #kav_serh_pattern.search(new_code)
                    i=list(new_code.split('&'))#это кастыль но оно вроде как работает
                    for nc in i:
                        program_line.insert(line+ine,nc)
                        ine=ine+1
                else:
                    program_line.insert(line+ine,new_code)
                    ine=ine+1
                    
        elif command.startswith('for'): # for i in 5: ...
            try:
                arg=command.split(' ',1)[1].split(':',1)[0]
            except IndexError:
                bot.reply_to(message,f"{command}\n{'^'*len(command)}\nerror no args \nline:{line}")
                return
            if "{" in arg and "}" in arg:
                vars=ext_arg_scob(arg)
                for var in vars:
                    if var in list(value.keys()):
                        arg=arg.replace('{'+str(var)+'}',str(value[var]))
            new_code = command.split(':', 1)[1]

            match = re.search(r"(.*)\bin\b(.*)", arg)
            if match:
                var = match.group(1).strip()  
                num = match.group(2).strip() 
            else:
                bot.reply_to(message,f"{command}\n{'^'*len(command)}\nerror no args (Incorrect arguments) \n{command}\n{"   "+"^"*len(arg)} \nline:{line}")
                return
            try:
                num=int(num)
            except ValueError:
                bot.reply_to(message,f"{command}\n{'^'*len(command)}\nerror invalid literal for num \nline:{line}")
                return
            ine=1
            for i in range(num):
                value[var]=i
                new_code_v=new_code
                if '{' in new_code and '}' in new_code:
                    vars=ext_arg_scob(new_code)
                    for var in vars:
                        if var in list(value.keys()):
                            new_code_v=new_code.replace('{'+str(var)+'}',str(value[var]))
                if ';' in new_code_v:
                    i=new_code_v.split(';')
                    for nc in i:
                        program_line.insert(line+ine,nc)
                        ine=ine+1
                else:
                    program_line.insert(line+ine,new_code_v)
                    ine=ine+1
            
        elif command.startswith('timeout'):
            try:
                arg=command.split(' ',1)[1]
                if '{' in arg and '}' in arg:
                    vars=ext_arg_scob(arg)
                    for var in vars:
                        if var in list(value.keys()):
                            arg=arg.replace('{'+str(var)+'}',str(value[var]))
            except IndexError:
                bot.reply_to(message,f"{command}\n{'^'*len(command)}\nerror no args (Incorrect arguments) \nline:{line}")
                return
            time.sleep(int(arg))
            
        elif command.startswith('len'):
            if '{' in command and '}' in command:
                vars=ext_arg_scob(command)
                for var in vars:
                    if var in list(value.keys()):
                        command=command.replace('{'+str(var)+'}',str(value[var]))
            arg=command.split(' ',1)[1]
            value[arg.split('=',1)[0]]=len(arg.split('=',1)[1])
            
        elif command.startswith('list'):
            if '{' in command and '}' in command:
                vars=ext_arg_scob(command)
                for var in vars:
                    if var in list(value.keys()):
                        command=command.replace('{'+str(var)+'}',str(value[var]))
            try:
                arg=command.split(' ',1)[1]
                num_list=arg.split('[',1)[1].split(']',1)[0]
                lis=arg.split('=',1)[1].split('[',1)[0]
                var=arg.split('=',1)[0]
                content=arg.split('=',2)#находим аргумент присваивания элемента
                if len(content)>2:
                    content=str(content[2])#если есть то вытягиваем его из списка
            except IndexError:
                bot.reply_to(message,f"{command}\n{'^'*len(command)}\nsyntax error (Incorrect arguments) \nline:{line}")
                return
            try:
                num_list=int(num_list)
            except ValueError:
                bot.reply_to(message,f"{command}\n{'^'*len(command)}\nerror ({num_list}) invalid literal for num \nline:{line}")
                return
            if ',' in arg:
                try:
                    lis_temp=lis.split(',')
                    if not content is list:# если аргумент есть и его вытянули из списка то присваемаем его 
                        lis_temp[num_list]=content
                        value[var] = lis_temp[num_list]
                    else:
                        value[var] = lis_temp[num_list]
                except IndexError:
                    bot.reply_to(message,f"error {command}\n{'^'*len(command)}\nlist index out of range\nline:{line}")
                    return
        
        elif command.startswith("replace"):# replace a={input_text}:old_symdol,new_symdol
            command=r_value(command,value)
            try:
                arg=command.split(" ",1)[1]
                var=arg.split("=",1)[0]
                data=arg.split("=",1)[1]
                text=data.split(":",1)[0]
                new_old_texts=data.split(":")[1]
                if len(new_old_texts.split(",",1))<=1:
                    bot.reply_to(message,f"{command}\n{'^'*len(command)}\nincorrect arguments \n{new_old_texts}\n{"^"*len(new_old_texts)}\nline:{line}")
                    return
            except IndexError:
                bot.reply_to(message,f"{command}\n{'^'*len(command)}\nsyntax error (Incorrect arguments) \nline:{line}")
                return
            try:
                value[var]=text.replace(new_old_texts.split(",")[0],new_old_texts.split(",")[1])
            except Exception as e:bot.reply_to(message,f"error {e}")

        elif command.startswith(' ') or command.startswith(''):pass
        else:
            bot.reply_to(message,f"{command}\n{'^'*len(command)}\nsyntax error no command \nline:{line}")
            return
        line=line+1
    for send_text in send_bufer:
        if len(send_bufer) >=20:
            bot.reply_to(message, f"провощено количество отправляемых сообщений {len(send_bufer)}/30")
            return
        else:
            try:
                if len(send_text)<=600:
                    bot.send_message(message.chat.id, str(send_text), parse_mode='HTML')
                else:bot.reply_to(message,f"привышена максимальная длина сообщения 600/{len(send_text)}")
            except telebot.apihelper.ApiTelegramException as e:
                bot.reply_to(message,f"error: {e}\nA request to the Telegram API was unsuccessful\nline:{line}")
            except Exception as e:
                bot.reply_to(message,f"{e}\nline:{line}")

bese=team_data_bese()

@bot.message_handler(commands=['team','каманда','клан'])  
def team(message):
    if ' ' not in message.text:
        bot.reply_to(message,"нет параметров! <code>/team -help</code> для справки",parse_mode='HTML')
        return 
    if "-help" in message.text.lower() or "-h" in message.text.lower():
        bot.reply_to(message,
        """
<code>/team создать имя_команды </code> - имя должно быть не более 70 символов и быть без пробелов все пробелы автамтически убераються;
<code>/team пригласить в имя_команды </code> - ответе на сообщения того человека которого хотите пригласить в команду;
<code>/team инфо имя_команды </code> - информация о команде а именно время создания, участники,создатель команды;
<code>/team сбор имя_команды </code> - тегает всех учасиков команды';
<code>/team покинуть имя_команды </code> - удаляет вас из команды если вы не ее создатель;
<code>/team удалить имя_команды </code> - позволяет создателю команды удалить ее; 
        """
        ,parse_mode='HTML') 
        return

    command=str(message.text.split(' ',1)[1])
    if 'создать' in command: 
        if ' ' not in command:
            bot.reply_to(message,"нет аргумента")
            return 
        name=command.split('создать',1)[1].replace(' ','')
        colonium=bese.data_bese_colonium()
        if not colonium:
            colonium=[]
        if name in [i[0] for i in colonium]:
            bot.reply_to(message,"такая команда уже есть!\nпридумай другое название")
            return
        if len(name)<71:
            bese.team_bese_init(message.chat.id, name,
                        users=[{"username":message.from_user.username, "frist_name":message.from_user.first_name, "id":message.from_user.id, "in_time":message.date, "status":"creator" }],
                        team_info={"creat_time":message.date, "creator_id":message.from_user.id, "creator_user_name":message.from_user.username}
                        )
            bot.reply_to(message,f"команда '{name}' создана")

        else:bot.reply_to(message,"такое название не подходит!")

    elif 'инфо' in command:
        if ' ' not in command:
            bot.reply_to(message,"нет аргумента")
            return 
        name=command.split('инфо', 1)[1].replace(' ','')
        messages=''
        data=bese.data_seah(message.chat.id, name)
        if data:
            messages+=f"название: {data[2]}\n"
            messages+=f"дата создания: {datetime.fromtimestamp(int(json.loads(data[4])['creat_time'])).strftime(r"%Y-%m-%d-%H.%M.%S")}\n"
            messages+=f"создатель: {json.loads(data[4])['creator_user_name']}\n"
            messages+=f"учасники:\n"
            for uname in json.loads(data[3]):
                us=''
                if uname["username"]:
                    us=uname["username"]
                else:
                    us=f"<a href='tg://user?id={uname["id"]}'>{uname["frist_name"]}</a>"
                messages+=f"{us}\n"

            bot.reply_to(message, messages ,parse_mode='HTML')

        else:
            bot.reply_to(message,f"не коректный ответ от БД ({data})")

    elif 'сбор' in command:
        if ' ' not in command:
            bot.reply_to(message,"нет аргумента")
            return 
        name=command.split('сбор', 1)[1].replace(' ','')
        messages=''
        data=bese.data_seah(message.chat.id, name)
        if data:
            for uname in json.loads(data[3]):
                us=''
                if uname["username"]:
                    us="@"+uname["username"]
                else:
                    us=f"<a href='tg://user?id={uname["id"]}'>{uname["frist_name"]}</a>"
                messages+=f"{us}\n"
            bot.reply_to(message, messages ,parse_mode='HTML')

        else:
            bot.reply_to(message,f"такой команды нет, создайте ее! <code>/team создать {name}</code>" ,parse_mode='HTML')
            return
    
    elif 'пригласить' in command: # /team пригласить в team_name 
        if message.reply_to_message:
            un=message.reply_to_message.from_user.username
            id=message.reply_to_message.from_user.id
            if ' ' not in command or 'в' not in command:
                bot.reply_to(message,"нет аргумента")
                return 
            team_name=command.split('в',1)[1].replace(' ','')

            if team_name in [i[0] for i in bese.data_bese_colonium()]:
                team_data=bese.data_seah(message.chat.id, team_name)
                if team_data:
                    for i in json.loads(team_data[3]):
                        if str(i['id'])==str(id):
                            bot.reply_to(message, "этот пользователь уже есть в команде ")
                            return
                
                    markup = telebot.types.InlineKeyboardMarkup()
                    
                    markup.add(telebot.types.InlineKeyboardButton(
                    "✅ принять",
                    callback_data=f"teamGetSiginYes_{id}_{team_name}"))

                    markup.add(telebot.types.InlineKeyboardButton(
                    "❌ отказаться",
                    callback_data=f"teamGetSiginNo_{id}_{team_name}"))

                    bot.send_message(message.chat.id,f"<a href='tg://user?id={id}'>{message.reply_to_message.from_user.first_name}</a>\nвас прегласили в команду {team_name}!"
                        ,parse_mode='HTML',disable_web_page_preview=True,reply_markup=markup)
                else:
                    bot.reply_to(message,f"такой команды нет, создайте ее! <code>/team создать {team_name}</code>",parse_mode='HTML')
                    return
            else:
                bot.reply_to(message,f"такой команды нет, создайте ее! <code>/team создать {team_name}</code>",parse_mode='HTML')
                return
        else: bot.reply_to(message,"ответе на сообщение человека которого нужно пригласить")

    elif 'покинуть' in command:
        if ' ' not in command:
            bot.reply_to(message,"нет аргумента")
            return 
        name=command.split(' ',1)[1].replace(' ','')
        un=message.from_user.username
        id=message.from_user.id

        team_data=bese.data_seah(message.chat.id, name)
        if team_data:
            users=json.loads(team_data[3])
            new=[]
            for u in users:
                if u['id'] != id or u['status'] == "creator":
                    new.append(u)
                else:
                    continue
            bese.upades(name, message.chat.id, new, None)
            bot.reply_to(message,f"вы покинули {name}")
        else:
            bot.reply_to(message, "такой команды нет")

    elif 'удалить' in command:
        if ' ' not in command:
            bot.reply_to(message,"нет аргумента")
            return 
        name=command.split(' ',1)[1].replace(' ','')
        id=message.from_user.id
        team_data=bese.data_seah(message.chat.id, name)
        if team_data:
            users=json.loads(team_data[3])
            new=[]
            for user in users:
                if str(user['id']) == str(id):
                    if user['status'] == "creator":
                        r=bese.delete_team(name, message.chat.id)
                        if r:
                            bot.reply_to(message, "команда удалена")
                        else:
                            bot.reply_to(message,"не удалось удалить комнду вероятно ошибка БД, извените")
                    else:
                        bot.reply_to(message,"нет прав удаление команды доступно только ее создателям")
                else:
                    bot.reply_to(message,"нет прав удаление команды доступно только ее создателям")
    else:
        bot.reply_to(message, "нет параметров или они не корректны")

@bot.callback_query_handler(func=lambda call:call.data.startswith('teamGetSiginYes_'))
def handle_team_buttony(call):
    cd=call.data.split('_',1)[1]
    if int(cd.split('_')[0]) != call.from_user.id:
        bot.answer_callback_query(call.id, "это не для тебя.")
        return
    team_name=cd.split('_',1)[1]
    data=bese.data_seah(call.message.chat.id, team_name)
    if data:
        new_user=json.loads(data[3])
        new_user.append({"username":call.from_user.username, "frist_name":call.from_user.first_name, "id":call.from_user.id, "in_time":time.time(), "status":"user"})
        bese.upades(team_name, call.message.chat.id, new_user, None)
        bot.answer_callback_query(call.id)
        bot.answer_callback_query(call.id, f"вы в команде {team_name} !")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        logger.debug(f"нет данных из БД :(\n{data}")


@bot.callback_query_handler(func=lambda call:call.data.startswith('teamGetSiginNo_'))
def handle_team_buttonn(call):
    bot.answer_callback_query(call.id)
    bot.answer_callback_query(call.id, "ну ладно не хочешь как хочешь")
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.message_handler(commands=['swearing_top','матершитники','топ_матерящехся','матерщинники'])
def swearing_top(message):
    base=tu_base_balance()

    if len(base)<=0:
        bot.reply_to(message, "тут пока некого нет...")

    num_list=[]
    users_list={}

    for user in base:
        num_list.append(user[4])
        users_list[user[4]] = user[3]
    
    relust_text=''
    modif=''
    top=sorted(num_list)
    top_index=0
    for i in top:
        if top_index == 0:
            modif=["главный матершиник", "главный любитель бранных слов", ""][random.randint(0,2)] 
        if users_list[i] is None:
            users_list[i] = 0
        relust_text+=f"{top_index} {users_list[i]} {i} {modif}\n"
        top_index+=1

    bot.reply_to(message, relust_text)


def log_messages(message):
    emoji=''
    if message.content_type=='sticker':
        emoji=f"( {message.sticker.emoji} )"
    reply_to=''
    if message.reply_to_message:
        cont=f"{message.reply_to_message.text if message.reply_to_message.content_type == 'text' else message.reply_to_message.content_type} {f"( {message.reply_to_message.sticker.emoji} )" if message.reply_to_message.content_type=='sticker' else ''}"
        if len(cont)>25:reply_to='\nReply to: '+cont[:25]+'...'
        else:reply_to='\nReply to: '+cont

    if message.from_user.username != None:user_n='@'+message.from_user.username
    else:user_n=str(message.from_user.first_name)
    logs = f"chat>> {message.chat.id} user>> {user_n} id>> {message.from_user.id} {reply_to}| сообщение >>\n{str(message.text if message.content_type == 'text' else message.content_type)} {emoji}"
    logger.info(logs)
    print("————")


user_messages = {}#инициализация слова+рей и тп
user_text = {}
message_text = []
#SPAM_LIMIT = 8 # Максимальное количество сообщений
#SPAM_TIMEFRAME = 4  # Время в секундах для отслеживания спама
s_level = 0
tekst_m = []
delete_message = []

# Функция для обработки сообщений
def anti_spam(message, auto_repytation=0):
    global user_messages
    global user_text
    global message_text
    #инициализация хрени всякой     
    user_id = message.from_user.id
    current_time = time.time()
    tekst_m.append({message.text:message.message_id})
    user_text[user_id] = tekst_m  # Сохраняем текст сообщения и id
    keys_to_delete=[]
   
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
    
    # Проверка на спам
    if len(user_messages[user_id]) > SPAM_LIMIT:
        for i in user_messages[user_id]:
            delete_message.append(i[1])
        nacase(message,delete_message)
        user_text.clear()
        user_messages.clear()
        #bot.delete_message(message.chat.id,message.message_id)
        return

    if len(list(user_text.keys()))>0 and user_text[list(user_text.keys())[0]] != None and  message.text:
        try:
            user_id=message.from_user.id
            paket_num=4
            sr_d,slova=0,[]
            keys_to_delete=[]
            list_mess=[]
            for i in range(0, len(user_text.keys())-1):
                #mess=list(user_text[list(user_text.keys())[i]])
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
                        keys_to_delete.append(user_id)
                        nacase(message, [message.message_id])
                        break
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
                    BAMBAMSpamerBlat=0
                    for b in range(len(list_povt_slov)):
                        if list_povt_slov[b]==list_povt_slov[0]:
                            BAMBAMSpamerBlat=BAMBAMSpamerBlat+1
                    if BAMBAMSpamerBlat>SPAM_LIMIT:
                        keys_to_delete.append(user_id)
                        nacase(message,[message.message_id])
                        user_messages.clear()
                        break
            #print(list_povt_slov)# debug
            #print(list(user_text.keys())[i])
            #print(s_level)
                if s_level>=len(list_povt_slov) and len(list_povt_slov)>=5:
                    keys_to_delete.append(user_id)
                    nacase(message,[message.message_id])
                    user_messages.clear()

            # Удаляем ключи после завершения итерации
            for key in range(len(keys_to_delete)):
                try:
                    if key != None:
                        del user_text[keys_to_delete[key]]
                except Exception as e: 
                    logger.error(e)
                    continue
            tekst_m.clear() # возможно надо переделать эту строку но мне лень может поже
        except Exception as e:
            logger.error(f"Ошибка: {e} \n-----------------------------\n {traceback.format_exc()}")  
        finally: 
            tekst_m.clear() 
            user_text.clear()

text={}
warn=0
def anti_spam_forward(message, text=text, warn=warn):
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
    log_messages(message)
    data=data_base(message.chat.id, message.from_user.id)
    data_base(message.chat.id, message.from_user.id, {"num_message":data[5]+1})# добовляем 1 сообщение

    if message.sticker and message.sticker.file_id in bklist.blist:
        if bool(DELET_MESSADGE):
            try:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(admin_grops,f'запрещеный стикер от @{message.from_user.username} удален')
            except telebot.apihelper.ApiTelegramException as e:
                bot.send_message(admin_grops,f'error>>{e}\nвероятно у бота недостаточно прав')
    
    commad=str(message.text).lower()
    if "[help]" in commad or "[Help]" in commad:
        id_help_hat=str(message.chat.id).replace("-100", "")
        if time.time()-message.date<=86400: 
            teg=''
            mess_text=''

            if admin_list:
                for i in range(len(admin_list)):
                    if i > 0:
                        teg+=f",@{admin_list[i]}"
                    else:
                        teg+=f"@{admin_list[i]}"

            if len(message.text)>150:
                mess_text=message.text[:150]+"..." #сокрощяем если текст сильно длинный
            else:mess_text=message.text
            bot.send_message(admin_grops, f"{teg} есть вопрос от @{message.from_user.username} \nвот он:{mess_text}\n | https://t.me/c/{id_help_hat}/{message.message_id}")
        
    if time.time() - message.date >= SPAM_TIMEFRAME:
        return
    
    elif message.forward_from:
        anti_spam_forward(message)
    else:
        anti_spam(message, data[7])
        if AUTO_TRANSLETE['Activate'] and message.text:
            translated = GoogleTranslator(source='auto', target=AUTO_TRANSLETE['laung']).translate(message.text)
            bot.reply_to(message, f"перевод:\n{translated}")

    with open(os.path.join(os.getcwd(), "asets", "mats.json"), 'r') as f:
        swears_list=json.load(f)["swears"] 
    text=str(message.text).replace(' ','').lower()

    A = ahocorasick.Automaton()
    for i, k in enumerate(swears_list):
        A.add_word(k, (i, k))
    A.make_automaton()

    cnt = Counter()
    for end_idx, found in A.iter(text.lower()):
        cnt[found] += 1
    d=dict(cnt)
    num_swears=0

    for key in list(d.keys()):
        num_swears+=d[key]

    if message.from_user.username:
        user_n=message.from_user.username
    else:
        user_n=message.from_user.first_name

    if num_swears>0:
        swears=tu_base(message.from_user.id, message.chat.id, user_n, None)
        if swears:
            if swears[0][4]:
                tu_base(message.from_user.id, message.chat.id, user_n, {"swears":swears[0][4]+num_swears})
            else:
                tu_base(message.from_user.id, message.chat.id, user_n, {"swears":1})

@bot.message_handler(content_types=['video','photo','animation'])
def message_handler_anim(message):
    log_messages(message)
    data=data_base(message.chat.id, message.from_user.id)
    data_base(message.chat.id, message.from_user.id, {"num_message":data[5]+1})# добовляем 1 сообщение
    if time.time() - message.date >= SPAM_TIMEFRAME or message.media_group_id != None:
        return
    else:
        anti_spam(message, data[7])

@bot.message_handler(content_types=['voice'])
def message_voice(message):
    log_messages(message)
    data=data_base(message.chat.id, message.from_user.id)
    data_base(message.chat.id, message.from_user.id, {"num_message":data[5]+1})# добовляем 1 сообщение

    if time.time() - message.date >= SPAM_TIMEFRAME:
        return
    elif message.forward_from:
        anti_spam_forward(message)
    
    else:
        anti_spam(message, data[7])
    #    if message.voice.duration>=1800 and time.time()-message.date>=60:
    #        bot.reply_to(message,'скока бл ...ужас')

# Обработчик всех остальных типов сообщений
@bot.message_handler(func=lambda message: True)
def other_message_handler(message):
    log_messages(message)
    data=data_base(message.chat.id, message.from_user.id)
    data_base(message.chat.id, message.from_user.id, {"num_message":data[5]+1})# добовляем 1 сообщение

    if time.time() - message.date >= SPAM_TIMEFRAME or message.forward_date and message.forward_from and message.forward_from_chat:
        return
    anti_spam(message, data[7])

#новый юзер 
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        logger.info(f"new member in chat | user name> @{message.from_user.username}")
        data_base(message.chat.id, new_member.id, {"vhod_data": message.date})
        if time.time() - message.date <= 350:
            try:
                input_gif_path = os.path.join(os.getcwd(), 'asets', 'hello.gif')

                gif = Image.open(input_gif_path)
                frames_with_text = []

                # шрифт: пробуем ваш файл, если нет — дефолтный
                if os.path.exists(os.path.join(os.getcwd(), 'asets', 'Roboto-VariableFont_wdth,wght.ttf')):
                    font_path = os.path.join(os.getcwd(), 'asets', 'Roboto-VariableFont_wdth,wght.ttf')
                    font = ImageFont.truetype(font_path, 43)
                else:
                    font = ImageFont.load_default()

                for frame_index in range(getattr(gif, "n_frames", 1)):
                    gif.seek(frame_index)
                    frame = gif.convert("RGBA")

                    draw = ImageDraw.Draw(frame)
                    if message.from_user.first_name:
                        usernameh = message.from_user.first_name
                        if message.from_user.last_name:
                            usernameh+=f" {message.from_user.last_name[0:30]}"
                    else:
                        usernameh = message.from_user.username

                    otstup = ' ' * (23 - len(usernameh))
                    text = f"добро пожаловать\n {otstup}{usernameh}"
                    text_position = (85, 300)
                    # рисуем текст (RGBA)
                    draw.text(text_position, text, font=font, fill=(21, 96, 189, 255))

                    # Конвертируем обратно в "P" palette для корректного GIF
                    out_frame = frame.convert("P", palette=Image.ADAPTIVE, colors=128)
                    frames_with_text.append(out_frame)
                #этот код был спижен
                duration_ms = getattr(gif, "info", {}).get("duration", None)
                if duration_ms:
                    fps = max(1, int(round(1000.0 / duration_ms)))
                else:
                    fps = 20

                # Ограничим fps по количеству кадров и длительности чтобы избежать экстремов
                num_frames = len(frames_with_text)
                if num_frames > fps * 10:  # если очень много кадров, увеличим шаг
                    step = max(1, num_frames // (fps * 10))
                    frames_with_text = frames_with_text[::step]
                    num_frames = len(frames_with_text)

                # Подготовка numpy-кадров (RGB) напрямую из PIL
                frames_np = [np.array(im.convert("RGB")) for im in frames_with_text]

                # динамическое определение пути
                tmpdir = tempfile.mkdtemp(prefix="welcome_vid_")
                out_mp4 = os.path.join(tmpdir, "welcome.mp4")

                clip = None
                try:
                    clip = ImageSequenceClip(frames_np, fps=fps)

                    # Подбор параметров кодека: используем crf 23 (баланс) если файл большой, иначе 20
                    # Рассчитаем примерный целевой CRF по исходному количеству пикселей/кадра:
                    w, h = frames_np[0].shape[1], frames_np[0].shape[0]
                    px = w * h
                    # простая эвристика: чем больше пикселей, тем чуть выше CRF (больше сжатие)
                    crf = 23
                    if px < 320*240:
                        crf = 20
                    elif px > 1280*720:
                        crf = 25

                    # Запись файла (moviepy использует ffmpeg)
                    clip.write_videofile(
                        out_mp4,
                        codec="libx264",
                        ffmpeg_params=["-pix_fmt", "yuv420p", "-crf", str(crf)],
                        preset="medium"
                    )
                    #коец спиженого кода
                    # Отправляем как video
                    with open(out_mp4, "rb") as vf:
                        bot.send_video(message.chat.id, vf, reply_to_message_id=message.message_id, timeout=60)

                finally:
                    if clip is not None:
                        try:
                            clip.close()
                        except Exception:
                            pass
                    try:
                        for fn in os.listdir(tmpdir):
                            os.remove(os.path.join(tmpdir, fn))
                        os.rmdir(tmpdir)
                    except Exception as e:
                        logger.error(f"{e}\n{traceback.format_exc()}")
            except Exception as e:
                logger.error(f"error send hello message >>{e}\n{traceback.format_exc()}")
                username = '@' + new_member.username if new_member.username else new_member.first_name
                welcome_message = [f"Привет, {username}! Добро пожаловать в наш чат!  /help для справки", f"<s>новенький скинь ножки</s>  Привет, {username}! Добро пожаловать в наш чат!  /help для справки", f"привецтвую, {username}! Добро пожаловать в наш чат!  /help для справки"][random.randint(0, 2)]
                bot.reply_to(message, welcome_message, parse_mode="HTML")


@bot.message_handler(content_types=['left_chat_member'])
def exit_chat_member(message):
    logger.info(f"left chat member | user name> @{message.from_user.username} |ib> {message.from_user.id}")
    #bot.reply_to(message,['пока пока','пока, я буду скучать'][random.randint(0,1)])

# Основной цикл
def main():
    get_num=0
    try:
        print("\033[32mнет ошибок :3\033[0m")
        while True:
            try:
                try:
                    get_num=+1
                    bot.polling(none_stop=True,timeout=30,long_polling_timeout=30,interval=1)
                    #schedule.run_pending()
                    if get_num >=100:
                        get_num=0
                        time.sleep(1)
                    # Запускаем в отдельном потоке при старте бота
                    #scheduler_thread = threading.Thread(target=update_user)
                    #scheduler_thread.daemon = True
                    #scheduler_thread.start()
                except requests.exceptions.ReadTimeout as e:
                    logger.error(f"time out ({e})")
                except requests.exceptions.ConnectionError as e:
                    logger.error(f"Error Connection ({e})\n{traceback.format_exc()}")
            except Exception as e:
                logger.error(f"Ошибка: {e} \n-----------------------------\n{traceback.format_exc()}")
                time.sleep(3)
    except Exception as e:
        bot.send_message(admin_grops,f'ошибка при старте:\n{e}\n-----------------------\n{traceback.format_exc()}')
if __name__ == '__main__':
    main()
