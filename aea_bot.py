import telebot
from telebot import types
from datetime import timedelta
from collections import defaultdict
import traceback
import time
import psutil
import schedule
from datetime import datetime
import requests
import os
from loguru import logger
import sqlite3
import random
from PIL import Image, ImageDraw, ImageFont
import os.path
import json
import re
import sys
TOKEN = "tokin" 

def umsettings():
    bambam=False
    delet_messadge=False
    admin_grops="-1002284704738"
    SPAM_LIMIT = 10 # Максимальное количество сообщений
    SPAM_TIMEFRAME = 4  # Время в секундах для отслеживания спама
    BAN_AND_MYTE_COMMAND= True


try:
    with open("settings.json", "r") as json_settings:
        settings= json.load(json_settings)
except:
    umsettings()
help_user = '/report - забань дебила в чате \nчтобы получить список правил \n/правило \n Если есть вопросы задайте его добвавив в сообщение [help] и наши хелперы по возмодности помогут вам \n/admin_command команды администраторов  ' 
message_reminder = 'Не забывайте про команду /report для сообщений о нарушении правил.'
PRAVILO='''
Правила:\n

1. Запрещен расизм, нацизм, ЛГБТ, выдвежение полит взглядов и прочие распространения подобных движений (бан - мут)  \n

2. 18+ контент в любом виде, или же приближенный (мут) \n

2.2 Эротика разрешена только если:\nне видно нижнего белья, выпирающих сосков и не обнажены части тела такие как ( скажу не очень красиво: жопа, сиськи, половые органы,  ноги выши половины ляжки, торс ниже пупа, спина ниже копчика,), так же отсутствуют прикосновения в половы органам (любые) и груди.
Подобные критерии оносятся и к неодушевлённым предметам (любым). Так же запрещены непристойные позы, так же позы с акцентом на выше перечисленное.
3. Оскорбления/Ссоры (мут) \n

4. Любой прямой или косвенный вред группе (бан) \n

5. Реклама в любом виде(мут) \n

6. Попытки обойти правила в связи с отсутствием некоторых косвенно запрещённых пунктов (бан) \n

Так же:\n

1. Администрация/Модерация имеет право выдавать пользователям warn/mute/ban операясь на свое усмотрение и ориентируясь на правила. \n

2. Минимальная мера наказания - снижение репутации посредством выдачи команды "/warn"\n

3. Пункт 1 правил включает абсолютно любые взгляды, во избежании поиска лазеек в своде правил.\n
4. Наказание выданное администрацией может быть оспорено только глав.админом.\n\n

(Правила в дальнейшем будут пересмотренны и дополненны)

'''
logse="nan"
i=0
admin_list=['@HITHELL','@mggxst']

# Инициализация логирования
logger.add("cats_message.log", level="TRACE", encoding='utf-8', rotation="500 MB")
try:
    bambam=settings['bambam']
    delet_messadge=settings['delet_messadge']
    admin_grops=settings['admin_grops']
    SPAM_LIMIT=settings['spam_limit']
    SPAM_TIMEFRAME=settings['spam_timer']
    BAN_AND_MYTE_COMMAND=settings['ban_and_myte_command']
except:
    umsettings()
    logger.debug('error settings init')
admin_groups=admin_grops

bot = telebot.TeleBot(TOKEN)
#updater = Updater(token=TOKEN)
#dispatcher = updater.dispatcher
#os.chdir(os.getcwd())
print(os.getcwd())
if os.path.exists('hello.gif'):
    print('gif OK')
else:
    print('error not gif ')
if os.path.exists('Users_base.db'):
    print('data base ok')
else:
    print("error not bata base ")

now = datetime.now()
current_time = now.strftime("%H:%M")
bot.send_message(admin_grops, f"бот запущен \ntime>> {current_time}")
logger.info("бот запущен")
    
# Функция для мониторинга ресурсов
def monitor_resources():
    response_time,response_time,cpu_percent,ram_percent,disk_percent=0,0,0,0,0
    popitki=5
    #пинг в среднем 5 (можно изменять в popitki )попыток
    for  i in range(popitki):
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
@bot.message_handler(commands=['help','помощь'])
def send_help(message):
    bot.send_message(message.chat.id, help_user)
    
# Команда /log
@bot.message_handler(commands=['log'])
def send_help(message):
    try:
        bot.send_document(admin_grops,document=open('cats_message.log', 'r',encoding='utf-8', errors='replace'))
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
    cpu_percent, ram_percent, disk_percent, response_time = monitor_resources()
    bot.reply_to(message, f"CPU: {cpu_percent}%\nRAM: {ram_percent}%\nDisk: {disk_percent}%\nPing: {response_time}")

# Команда /test 
@bot.message_handler(commands=['test'])
def monitor_command(message):
    test='none'
    test+=os.getcwd()+'\n'
    if os.path.exists(f'{os.getcwd()}/hello.gif'):
        test=test+'gif OK\n'
    else:
        test=test+'error not gif\n'
    if os.path.exists(f'{os.getcwd()}/Users_base.db'):
        test=test+'data base OK\n'
    else:
        test=test+"error not bata base \n"
    if os.path.exists(f'{os.getcwd()}/cats_message.log'):
        test=test+'messege log OK\n'
    else:
        test=test+'warning not messege log \n'
    if os.path.exists(f'{os.getcwd()}/Bounded-Black.ttf'):
        test=test+'Bounded-Black шрифт OK\n'
    else:
        test=test+'error not Bounded-Black \n'
    if os.path.exists(f'{os.getcwd()}/settings.json'):
        test=test+'cofig file OK\n'
    else:
        test=test+'error not config file \n'
    test=test+f"ID> {message.from_user.id}\n"
    test=test+f"ID admin grup> {admin_grops}\n"
    cpu_percent, ram_percent, disk_percent, response_time = monitor_resources()
    bot.send_message(message.chat.id, f"CPU: {cpu_percent}%\nRAM: {ram_percent}%\nDisk: {disk_percent}%\nPing: {response_time} \n{test} \nadmin > {bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator']}")

# Команда /time_server
@bot.message_handler(commands=['time_server'])
def time_server_command(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    bot.send_message(message.chat.id, f"Серверное время: {current_time}")    
#команда /правило 
@bot.message_handler(commands=['правило','правила','закон','specification'])
def pravilo(message):
    bot.send_message(message.chat.id,PRAVILO)
# Хранение данных о репортах
report_data =  {}
report_user=[]
# Обработка ответа на сообщение с /report
@bot.message_handler(commands=['report','репорт','fufufu'])
def handle_report(message):
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
        ps_reputation(message.reply_to_message.from_user.id,message,0,1)
        
        bot.send_message(admin_grops,f"послали репорт на >> tg://user?id={message.reply_to_message.from_user.id}, @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_report}/{message.reply_to_message.message_id} | сообщение>> {reported_message_text if message.content_type == 'text' else message.content_type}")
        logger.debug(f"послали репорт на >>  @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_report}/{message.reply_to_message.message_id} сообщение>> {reported_message_text if message.content_type == 'text' else message.content_type}")
        logger.info(f"Пользователь @{message.from_user.username} сообщил о нарушении.")
        bot.reply_to(message,['админы посмотрят','амон уже в пути','да придет же админ и покарает нечестивцев баном','кто тут нарушает?','стоять бояться работает админ'][random.randint(0,4)])
        # Проверяем, достаточно ли ответов для бана
        if len(report['responses']) >= 5:
            for i in range(len(report_user)):
                ps_reputation(report_user[i],message,0,-1)
#           bot.kick_chat_member(chat_id, user_to_ban, until_date=int(time.time()) + 86400)
            for i in range(len(admin_list)):
                if i >0:
                    teg+=f",{admin_list[i]}"
                else:
                    teg+=f"{admin_list[i]}"
            bot.send_message(admin_grops,f"{teg} грубый нарушитель ! >> tg://user?id={ban_ded} | https://t.me/c/{message_to_report}/{message.reply_to_message.message_id}")
            if delet_messadge:
                bot.delete_message(message.chat.id,message.message_id)
            #bot.send_message(admin_grops, f"Пользователь {message.reply_to_message.from_user.username} получил бан на 24 часа за нарушение.")
            #logger.debug(f"Пользователь {message.reply_to_message.from_user.username} получил бан на 24 часа за нарушение.")        
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
        print(out)
        if out=='' or out==None:
            out='none'
        bot.reply_to(message,out)
        f.close()
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
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id =='5194033781':
            connection = sqlite3.connect('Users_base.db')
            cursor = connection.cursor()
            # Получаем информацию о столбцах в таблице Users
            cursor.execute('SELECT * FROM Users')
            rows = cursor.fetchall() 
            # Печатаем информацию о столбцах
            for column in rows:
                datas += str(column)+'\n'
            connection.close()
            bot.send_message(message.chat.id,f"data base>>\n№ | chat id |r| user id|\n----------------------------------------\n{datas}")
            logger.debug(f"база данных :\n{datas}")
        else:
            bot.reply_to(message,f"ты не достоин \nты не админ")
    except Exception as e:
        bot.send_message(admin_grops,f"error >> {e} ")
        logger.error(f"error >> {e}")
        
def status(rec):
    if rec >= 1000:
        status=["читы вырубай ! ",'как то многовато ,читы ?'][random.randint(0,1)]
    elif rec <=1:
        status=["ты плохой исправляйся 😡",'ай ай ай нарушаем','фу таким быть','а ну не нарушай ','правил что ли не знаешь \nтак прочти - /правило'][random.randint(0,4)]
    elif rec>=5:
        status=['ты хороший 😊','ты умница 👍','законопослушый так держать! ','харош'][random.randint(0,2)]
    elif rec<=0:
        status=['ну это бан','в бан тебя'][random.randint(0,1)]
    elif rec==None:
        status='ошибка получения данных '
    else:
        status=["😐",'ну норм','нейтральный','не без греха'][random.randint(0,3)]
    return status


@bot.message_handler(commands=['я', 'me'])
def send_statbstic(message):
    current_reputation=data_base(message.chat.id,message.from_user.id,message,0)
    mess=ps_reputation(message.from_user.id,message,0,0)[1]
    bot.reply_to(message, f"Твоя репутация: {current_reputation} \n{status(current_reputation)}\nколичество сообщений: {mess}")


def update_user(user_id, chat, db, reputation=None):
    # Создаем подключение к базе данных
    connection = sqlite3.connect(db,timeout=10)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")

    # Формируем запрос для обновления
    query = "UPDATE Users SET "
    params = []
    
    if reputation is not None:
        query += "reputation = ?"
        params.append(reputation)
    
    # Проверяем, были ли добавлены параметры
    if params:  # Если есть параметры, добавляем WHERE
        query += " WHERE warn_user_id = ? AND chat_id = ?"
        params.append(user_id)  # Исправлено: добавляем только user_id
        params.append(chat)  # Исправлено: добавляем chat
        cursor.execute(query, params)  # Выполняем запрос
        connection.commit()  # Сохраняем изменения
    else:
        connection.close()
        logger.warning("Нет параметров для обновления.")
        return None
    
    # Закрываем соединение
    connection.close()

def data_base(chat_id, warn_user_id, message, nfkaz) -> int:
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
            warn_user_id INTEGER NOT NULL
        )
        ''')
        
        # Создаем индекс (если он еще не существует)
        cursor.execute('CREATE INDEX IF NOT EXISTS warn_user_id_index ON Users (warn_user_id)')
        
        # Проверяем, существует ли пользователь с данным warn_user_id
        cursor.execute('SELECT * FROM Users WHERE warn_user_id = ?', (warn_user_id,))
        result = cursor.fetchone()
        print('result>>', result) 
        
        if result is not None:
            # Извлекаем репутацию из результата
            current_reputation = result[2]  # Предполагаем, что репутация находится в третьем столбце
            chat = result[1]  # id чата

            if chat == message.chat.id:
                new_reputation = current_reputation - nfkaz
                # Обновляем репутацию пользователя
                update_user(warn_user_id, chat, 'Users_base.db', new_reputation)  # Передаем id пользователя для обновления
                connection.commit()
                connection.close()
                return new_reputation
            else:
                resperens = 5 - nfkaz
                cursor.execute('INSERT INTO Users (chat_id, reputation, warn_user_id) VALUES (?, ?, ?)', (chat_id, resperens, warn_user_id))
                connection.commit()
                connection.close()
                return resperens
        else:
            # Если пользователь не найден, добавляем его
            resperens = 5 - nfkaz
            cursor.execute('INSERT INTO Users (chat_id, reputation, warn_user_id) VALUES (?, ?, ?)', (chat_id, resperens, warn_user_id))
            connection.commit()
            connection.close()
            return resperens

    except Exception as e:
        logger.error(f'Ошибка в операции с базой данных: {e}')
        connection.close()
        return None  # Возвращаем None в случае ошибки

    finally:
        # Закрываем соединение
        connection.close()

def ps_reputation(warn_user_id,message,soob_num,g)->int: 
    try:
        resperens=0
        # Создаем подключение к базе данных
        connection = sqlite3.connect('ps_reputation_base.db',timeout=10)
        cursor = connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")

        
        # Создаем таблицу (если она еще не существует)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY, 
            chat_id INTEGER NOT NULL,
            reputation INTEGER NOT NULL,
            warn_user_id INTEGER NOT NULL,
            num_message INTEGER NOT NULL
        )
        ''')
        # Создаем индекс (если он еще не существует)
        cursor.execute('CREATE INDEX IF NOT EXISTS warn_user_id_index ON Users (warn_user_id)')
        # Проверяем, существует ли пользователь с данным warn_user_id
        cursor.execute('SELECT * FROM Users WHERE warn_user_id = ?', (warn_user_id,))
        result = cursor.fetchone()
        if result is not None :
            # Извлекаем репутацию из результата
            current_reputation = result[2]  #  репутация находится в третьем столбце
            chat = result[1]  # id чата
            text=result[4]

            if text is None:
                text=1
            if current_reputation is None:
                current_reputation=0
            
            if chat==message.chat.id:
                new_reputation = current_reputation+g
                # Формируем запрос для обновления
                query = "UPDATE Users SET "
                params = []
    
                if new_reputation is not None:
                    query += "reputation = ?,"
                    params.append(new_reputation)
                if new_reputation is not None:
                    query += "num_message = ?"
                    params.append(soob_num+text)
                # Проверяем, были ли добавлены параметры
                if params:  # Если есть параметры, добавляем WHERE
                    query += " WHERE warn_user_id = ? AND chat_id = ? "
                    params.append(message.from_user.id)  
                    params.append(chat)
                    cursor.execute(query, params)  # Выполняем запрос
                connection.commit()
                connection.close()
            else:
                cursor.execute('INSERT INTO Users (chat_id, reputation, warn_user_id ,num_message) VALUES (?, ?, ?, ?)', (message.chat.id, resperens, warn_user_id, soob_num))
#               bot.reply_to(message, f'Рейтинг понижен до {new_reputation}')
                connection.commit()
                connection.close()
            return [g,int(text+soob_num)]
        else:
            cursor.execute('INSERT INTO Users (chat_id, reputation, warn_user_id ,num_message) VALUES (?, ?, ?, ?)', (message.chat.id, resperens, warn_user_id,1))
            connection.commit()
            connection.close()
            return [g,1]

    except Exception as e:
        connection.close()
        logger.error(f'Ошибка в операции с базой данных: {e}')
        bot.send_message(admin_grops, f"psr error>> {e}")
    finally:
        # Закрываем соединение
        connection.close()   
        
warn_data= {}
# Обработка ответа на сообщение /warn
@bot.message_handler(commands=['warn'])
def handle_warn(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id =='5194033781':
        if message.reply_to_message:

            chat_id = message.chat.id#инециалезацыя всякой хрени
            warn_message_text = message.reply_to_message.text

            if chat_id not in warn_data:#проверка на существования пометки chat_id
                warn_data[chat_id] = {'responses': set()}
            
            reputation = warn_data[chat_id]
            #добавляем id балбеса партия не давольна вами -1 соцыальный рейтинг -1 кошка жена 
            reputation['responses'].add(message.reply_to_message.from_user.id)
            ban_ded=message.reply_to_message.from_user.id
            warn_chat=message.chat.id
        
            message_to_warp=str(warn_chat).replace("-100", "")

            reputation=data_base(chat_id,ban_ded,message,1)
            ps_reputation(ban_ded,message,0,2)
            bot.reply_to(message,f'репутация снижена \nтекущяя репутация пользевателя:{reputation}')
            bot.send_message(admin_grops,f"репутация снижена >> tg://user?id={message.reply_to_message.from_user.id}, @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} | сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.debug(f"репутация снижена >>  @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.info(f"Пользователь @{message.from_user.username} понизил репутацию ") 
        
        # Проверяем, достаточно ли ответов для мута
            if reputation <= 0:
                if bambam==True:
                    #Ограничиваем пользователя на 24 часа 
                    bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    until_date=timedelta(hours=24),
                    can_send_messages=False
                    )
                    bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} получил бан на 24 часа за нарушение.")
                    logger.debug(f"Пользователь {message.reply_to_message.from_user.username} получил бан на 24 часа за нарушение.")        
#           bot.kick_chat_member(chat_id, user_to_ban, until_date=int(time.time()) + 86400)
                bot.send_message(admin_grops,f"грубый нарушитель ! >> tg://user?id={ban_ded} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id}")
 
        else:
            bot.reply_to(message, "Пожалуйста, ответьте командой на сообщение, нарушающее правила, чтобы снизить репутацию") 
    else:
        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])
                    

@bot.message_handler(commands=['reput'])
def handle_warn(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id =='5194033781':
        if message.reply_to_message:

            chat_id = message.chat.id#инециалезацыя всякой хрени 
            warn_message_text = message.reply_to_message.text
            user=message.reply_to_message.from_user.id
            warn_chat=message.chat.id
            message_to_warp=str(warn_chat).replace("-100", "")

            reputation=data_base(chat_id,user,message,-1)#партия довольна вами +1 к репутации
            ps_reputation(user,message,0,-2)
            bot.reply_to(message,f'репутация повышена \nтекущяя репутация пользевателя:{reputation}')
            bot.send_message(admin_grops,f"репутация повышена >> tg://user?id={message.reply_to_message.from_user.id}, @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} | сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.debug(f"репутация повышена >>  @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.info(f"Пользователь @{message.from_user.username} повысил репутацию ") 
        else: 
            bot.reply_to(message, "Пожалуйста, ответьте командой на сообщение, чтобы повысить репутацию")  
    else:
        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])
        
@bot.message_handler(commands=['info','user'])#узнать репутацию
def handle_warn(message):
#    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id =='5194033781':
    if message.reply_to_message:

        chat_id = message.chat.id#инециалезацыя всякой хрени 
        #warn_message_text = message.reply_to_message.text
        ban_ded=message.reply_to_message.from_user.id
        #warn_chat=message.chat.id
        #message_to_warp=str(warn_chat).replace("-100", "")
        reputation=data_base(chat_id,ban_ded,message,0)
        bot.reply_to(message,f'текущая репутация пользователя:{reputation}')
    else: 
        bot.reply_to(message, "Пожалуйста, ответьте командой на сообщение, чтобы узнать репутацию")  
#    else:
#        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])
        
    
@bot.message_handler(commands=['admin_command'])
def handle_warn(message):
    bot.reply_to(message,'/monitor - показатели сервера \n/warn - понижение репутации на 1\n/reput - повышение репутации на 1\n/data_base - вся база данных\n/info - узнать репутацию пользователя\n/ban - отпровляет в бан пример: `/бан reason:по рофлу`\n/мут - отпровляет в мут `/мут reason:причина time:1.h` .h - часы (по умолчанию) , .d - дни , .m - минуты')


@bot.message_handler(commands=['52'])
def handle_warn(message):
    bot.reply_to(message,'52')

@bot.message_handler(commands=['гойда','goida'])
def handle_warn(message):
    bot.reply_to(message,['наш слон','ГООООООЛ'][random.randint(0,1)])

@bot.message_handler(commands=['bambambam'])
def handle_warn(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id =='5194033781':
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
        bot.reply_to(message,['что тебе нужно','кто то плохо себя вел?','главное не спамь !','боньк','спам == вычисление по IP и марсельное унижение'] [random.randint(0,4)])
# Периодическое напоминание
def send_reminder():
    chat_id = '-1002170027967'# Укажите ID чата для отправки напоминаний
    bot.send_message(chat_id, message_reminder)

# Планирование напоминаний
#schedule.every().day.at("12:00").do(send_reminder)

def nacase(message):
    try:
        user_messages[message.from_user.id] = []
        if bool(bambam):
            try:
                 #Ограничиваем пользователя на 24 часа 
                bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                until_date=timedelta(hours=24),
                can_send_messages=False
                )
                reputation=data_base(message.chat_id,message.from_user.id,message,3)
                bot.send_message(message.chat.id, f"Пользователь {message.from_user.id} замучен на 1 день.\n рапутация снижена:{reputation}" )
            except Exception as e:
                bot.send_message(admin_grops,f"error >> {e}")
                logger.error(e)
            if bool(delet_messadge):
                bot.delete_message(message.chat.id,message.message_id)
        id_spam_message=str(message.chat.id).replace("-100", "")
        logger.info(f'Обнаружен спам от пользователя >> tg://user?id={message.from_user.id}')
        bot.send_message(admin_groups, f'Обнаружен спам от пользователя >> tg://user?id={message.from_user.id}, @{message.from_user.username} | сообщение: {message.text if message.content_type == "text" else "Не текстовое сообщение"} \n|https://t.me/c/{id_spam_message}/{message.message_id}')
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

user_messages = {}#инициализация словарей и тп
user_text = {}
message_text=[]
#SPAM_LIMIT = 8 # Максимальное количество сообщений
#SPAM_TIMEFRAME = 4  # Время в секундах для отслеживания спама
s_level=0
tekst_m=[]
        

# Функция для обработки сообщений
def anti_spam(message):
    #инициализация хрени всякой 
    user_id = message.from_user.id
    current_time = time.time()
    user_text[user_id] = tekst_m.append(message.text)  # Сохраняем текст сообщения и id
   
    # Удаление старых временных меток
    if user_id not in user_messages:
        user_messages[user_id] = []
    user_messages[user_id] = [timestamp for timestamp in user_messages[user_id] if current_time - timestamp < SPAM_TIMEFRAME]

    # Добавление текущего временного штампа
    user_messages[user_id].append(current_time)
   # Проверка на спам
    if len(user_messages[user_id]) > SPAM_LIMIT:
        nacase(message)
        #bot.delete_message(message.chat.id,message.message_id)
        return
    user_messages = {}#инициализация словарей и тп
user_text = {}
message_text=[]
#SPAM_LIMIT = 8 # Максимальное количество сообщений
#SPAM_TIMEFRAME = 4  # Время в секундах для отслеживания спама
tekst_m=[]
        
# Функция для обработки сообщений
def anti_spam(message):
    #инициализация хрени всякой     
    user_id = message.from_user.id
    current_time = time.time()
    tekst_m.append(message.text)
    user_text[user_id] = tekst_m  # Сохраняем текст сообщения и id
    keys_to_delete=[]
   
    # Удаление старых временных меток
    if user_id not in user_messages:
        user_messages[user_id] = []
    user_messages[user_id] = [timestamp for timestamp in user_messages[user_id] if current_time - timestamp < SPAM_TIMEFRAME]

    # Добавление текущего временного штампа
    user_messages[user_id].append(current_time)
    
    logs = f"chat>>{message.chat.id} user >> tg://user?id={message.from_user.id}, @{message.from_user.username} | сообщение >>\n{message.text if message.content_type == 'text' else message.content_type}"
    print("————")
    logger.debug(logs)
   # Проверка на спам
    if len(user_messages[user_id]) > SPAM_LIMIT:
        nacase(message)
        #bot.delete_message(message.chat.id,message.message_id)
        return
    if len(list(user_text.keys()))>0 and user_text[list(user_text.keys())[0]] != None and  message.content_type == 'text':
        paket_num=4
        sr_d,slova=0,[]
        keys_to_delete=[]
        for i in range(len(user_text.keys())):
            list_mess=list(user_text[list(user_text.keys())[i]])
            for a in range(len(list_mess)):
                s_level=0
                list_povt_slov=[]
                if list_mess[a]!=None:
                    text_s=str(list_mess[a])
                    if str(text_s).count('@')>=10:
                        s_level+=1
                    if str(text_s)==list_mess[0] and len(list_mess)>=1:
                        s_level+=1
                    if len(text_s)>=300:
                        s_level+=1
                    if list_mess.count(" ")<=round(len(text_s)/10):# подсчет пробелов
                        s_level+=1
                    if len(text_s)>=10:
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
                for b in range(len(list_povt_slov)):
                    if list_povt_slov[b]==list_povt_slov[0]:
                        s_level=s_level+1
        #print(list_povt_slov)
        #print(list(user_text.keys())[i])
        #print(s_level)# debug
            if s_level>=len(list_povt_slov) and len(list_povt_slov)>=5:
                keys_to_delete.append(list(user_text.keys())[i])
                nacase(message)
    # Удаляем ключи после завершения итерации
    for key in range(len(keys_to_delete)):
        if key != None:
            del user_text[keys_to_delete[key]]
    #print(datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S')) вывот дату на будующее
@bot.message_handler(content_types=['text', 'sticker'])
def message_handler(message):
    teg=''
    ps_reputation(message.from_user.id,message,1,0)
    commad=str(message.text).lower()
    if "[help]" in commad or "[Help]" in commad:     
        id_help_hat=str(message.chat.id).replace("-100", "")
        for i in range(len(admin_list)):
            if i >0:
                teg+=f",{admin_list[i]}"
            else:
                teg+=f"{admin_list[i]}"
        bot.send_message(admin_groups,  f"{teg} есть вопрос от @{message.from_user.username} \nвот он: https://t.me/c/{id_help_hat}/{message.message_id}")# это не читабельное гавно но оно работает
    if commad=='!правила' or commad=='!правило' and message.reply_to_message != True:
        bot.reply_to(message,'')
    if commad=='!я' and message.reply_to_message != True:
        send_statbstic(message)
    if commad.startswith('/ban') or commad.startswith('/бан'):
        if BAN_AND_MYTE_COMMAND !=True:
            bot.reply_to(message,'отключено , для включения задайте парамитер (в settings.json) ban_and_myte_command как true')
            return
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id =='5194033781':
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
                    bot.reply_to(message,'error>> elebot.apihelper.ApiTelegramException\nвероятно у бота недостаточно прав  ')
            else:bot.reply_to(message,'Пожалуйста, ответьте командой на сообщение, чтобы выдать бан')
        else:
            bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет','ты думал сможешь взять и забанить наивный'][random.randint(0,5)])
    if commad.startswith('/mute') or commad.startswith('/мут'):
        if BAN_AND_MYTE_COMMAND !=True:
            bot.reply_to(message,'отключено , для включения задайте парамитер (в settings.json) ban_and_myte_command как true')
            return
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id =='5194033781':
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
                        num_date=int(re.sub('\D', '',timer.split('.')[0])) #убираем буквы и т.д
                        if deleu=='h' or deleu=='d' or deleu=='m':
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
                    bot.reply_to(message,f'SyntaxError\n{error}\nпример: `/мут reason:причина time:1.h` \n.h - часы (по умолчанию) , .d - дни , .m - минуты  ')
                    return
                #time=re.sub(r'.*?time:', '', time, 1)# убираем все до time:
                try:
                    bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, until_date=time.time() + num_date*deleu)
                    logger.info(f'ban for {message.reply_to_message.from_user.username}\n{reason}')
                    bot.send_message(admin_grops,f'myte for {message.reply_to_message.from_user.username}\ntime:{num_date} ({num_date*deleu}) {reason}')
                    if wirning != None:
                        bot.reply_to(message,wirning)
                except telebot.apihelper.ApiTelegramException:
                    bot.reply_to(message,'error>> elebot.apihelper.ApiTelegramException\nвероятно у бота недостаточно прав  ')
            else:bot.reply_to(message,'Пожалуйста, ответьте командой на сообщение, чтобы вытать мут')
        else:
            bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет','ты думал сможешь взять и замутить наивный'][random.randint(0,5)])

    if time.time() - message.date >= 2:
        pass
    else:
        if message.forward_from == None:
            anti_spam(message)

@bot.message_handler(content_types=['video','photo','animation'])
def message_handler(message):
    if time.time() - message.date >= 2 or message.media_group_id != None:
        return
    else:
        anti_spam(message)
# Обработчик всех остальных типов сообщений
@bot.message_handler(func=lambda message: True)
def other_message_handler(message):
    print(message.media_group_id)
    if time.time() - message.date >= 2 or message.media_group_id:
        return
    anti_spam(message)

#новый юзер 
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        logger.info(f'new member in chat | user name> {message.from_user.username}')
        # Открываем исходный GIF
        try:
            input_gif_path = f'{os.getcwd()}/hello.gif'
            output_gif_path = 'output.gif'
            # Открываем изображение
            gif = Image.open(input_gif_path)
            # Создаем список для хранения кадров с текстом
            frames_with_text = []
            # Настройка шрифта (по умолчанию, если шрифт не найден, будет использован шрифт по умолчанию)
            try:
                font = ImageFont.truetype(f"{os.getcwd()}/Bounded-Black.ttf", 35) 
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
                draw.text(text_position, text, font=font, fill=(65, 105, 225))  # Цвет текста задан в формате RGB
                # Добавляем новый кадр в список
                frames_with_text.append(new_frame)
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
            username = new_member.username if new_member.username else "пользователь"
            welcome_message = [f"Привет, @{username}! Добро пожаловать в наш чат! \n/help для справки",f"новенький скинь ножки \nой не тот текст \nПривет, @{username}! Добро пожаловать в наш чат! \n/help для справки"][random.randint(0,1)]
            bot.reply_to(message , welcome_message)
# Основной цикл
def main():
    try:
        print("\033[32m{}\033[0m".format('нет ошибок :3 '))
        while True:
            try:
                try:
                    bot.polling(none_stop=True)
                    schedule.run_pending()
                except requests.exceptions.ReadTimeout:
                    print("time out")
            except Exception as e:
                logger.error(f"Ошибка: {e} , {traceback.format_exc()}")
                time.sleep(3)
    except Exception as e:
        bot.send_message(admin_grops,'ошибка при старте\n'+e)
if __name__ == '__main__':
    main()
    
    
