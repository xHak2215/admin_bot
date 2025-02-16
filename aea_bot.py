import telebot
from telebot import types
from datetime import timedelta
from collections import defaultdict
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
TOKEN = " tokin "  

help_user = '/report - забань дебила в чате \nчтобы получить список правил \n/правило \n Если есть вопросы задайте его добвавив в сообщение [help] и наши хелперы по возмодности помогут вам \n/admin_command команды администраторов  ' 
message_reminder = 'Не забывайте про команду /report для сообщений о нарушении правил.'
logse="nan"
is_bot_active = False
i=0

admin_grops="-1002284704738"
admin_groups=admin_grops

bot = telebot.TeleBot(TOKEN)
#updater = Updater(token=TOKEN)
#dispatcher = updater.dispatcher
os.chdir('/home/pc/Рабочий стол/aea_bot')
print(os.getcwd())
if os.path.exists('hello.gif'):
    print('gif OK')
else:
    print('error not gif ')
if os.path.exists('Users_base.db'):
    print('data base ok')
else:
    print("error not bata base ")

#print(__name__)
now = datetime.now()
current_time = now.strftime("%H:%M")
bot.send_message(admin_grops, f"бот запущен \ntime>> {current_time}")
logger.info("бот запущен")
try:
    if e !='1':
         #bot.send_message(message.chat.id,'Увы, случилась ошибка>> \n' + str(e))
         pass
except :
    print("\033[32m{}\033[0m".format('нет ошибок :3 '))
    

# Функция для пинга
def ping():
    start_time = time.time()
    response = requests.get('https://core.telegram.org/')
    response_time = time.time() - start_time
    print('Ping:', response_time)
    return response_time

# Функция для мониторинга ресурсов
def monitor_resources():
    print('Monitoring resources...')
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    response_time = ping()
    shutka=' '
    if cpu_percent==100.0:
        shutka='процессор шя рванет 🤯'
    print(f"CPU: {cpu_percent}%,\nRAM: {ram_percent}%,\nDisk: {disk_percent}%,\nPing: {response_time} \n{shutka}")
    return cpu_percent, ram_percent, disk_percent, response_time

# Команда /help
@bot.message_handler(commands=['help'])
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
            if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator']:
                bot.send_message(admin_grops,f"логи очищены очистил : @{message.from_user.username}")
                file = open('cats_message.log', "w")
                # Изменяем содержимое файла
                file.write("log null")
                # Закрываем файл
                file.close()
                logger.debug(f"логи очищены, очистил:  @{message.from_user.username}")
            else:
                bot.reply_to(message.chat.id,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])
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
            bot.reply_to(message.chat.id,f"ты не достоин \nты не админ")
    except Exception as e:
        bot.send_message(admin_grops,f"error >> {e} ")
        logger.error(f"error >> {e}")
# очистка консоли /cler 
@bot.message_handler(commands=['cler'])
def send_help(message):
    #проверка на админа
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator'] or message.from_user.id =='5194033781':
            bot.send_message(admin_grops,f"экран очищен, очистил : @{message.from_user.username}")
            os.system('clear')
            logger.debug(f"экран очищен очистил:  @{message.from_user.username}")
    else:
        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])

# Команда /monitor    
@bot.message_handler(commands=['monitor'])
def monitor_command(message):
    cpu_percent, ram_percent, disk_percent, response_time = monitor_resources()
    bot.send_message(message.chat.id, f"CPU: {cpu_percent}%\nRAM: {ram_percent}%\nDisk: {disk_percent}%\nPing: {response_time:.2f}s")

# Команда /time_server
@bot.message_handler(commands=['time_server'])
def time_server_command(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    bot.send_message(message.chat.id, f"Серверное время: {current_time}")    
#команда /правило 
@bot.message_handler(commands=['правило','Правила','закон'])
def time_server_command(message):
    bot.send_message(message.chat.id, f"Правила группы\nЗапрещается:\n\nРасизм,нацизм,продвижение экстремизма в любой форме(например ЛГБТ),выведение своих полит. взглядов,зоофилия, 18+ контент, жестокие сцены (любые), оскорбление администрации (с учетом что она вас не провоцировала), оскорбление и ущемление пола нации и т.д, оскорбления, многочисленные упоминания и восхваления полит и просто преступников, спам (особенно командами), вред группе(любой), любое уклонение от правил и поиск лазеек в них. \nЭто карается снижением репутации, после мутом, после вечной блокировкой блокировкой в группе")

# Хранение данных о репортах
report_data =  {}
# Обработка ответа на сообщение с /report
@bot.message_handler(commands=['report','репорт','fufufu'])
def handle_report(message):
    if message.reply_to_message:
        chat_id = message.chat.id#инециалезацыя всякой хрени
        reported_message_text = message.reply_to_message.text

        if chat_id not in report_data:#проверка на существования пометки chat_id
            report_data[chat_id] = {'responses': set()}
            
        report = report_data[chat_id]
        #добавляем id балбеса or нарушителя в тетрадь смерти Сталина report
        report['responses'].add(message.reply_to_message.from_user.id) 
        ban_ded=message.reply_to_message.from_user.id
        report_chat=message.chat.id
        
        message_to_report=str(report_chat).replace("-100", "")
         
        bot.send_message(admin_grops,f"послали репорт на >> tg://user?id={message.reply_to_message.from_user.id}, @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_report}/{message.reply_to_message.message_id} | сообщение>> {reported_message_text if message.content_type == 'text' else message.content_type}")
        logger.debug(f"послали репорт на >>  @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_report}/{message.reply_to_message.message_id} сообщение>> {reported_message_text if message.content_type == 'text' else message.content_type}")
        logger.info(f"Пользователь @{message.from_user.username} сообщил о нарушении.")
        bot.reply_to(message,['админы посмотрят','амон уже в пути','да придет же админ и покарает нечестивцев баном','кто тут нарушает?','стоять бояться работает админ'][random.randint(0,4)])
        # Проверяем, достаточно ли ответов для бана
        if len(report['responses']) >= 5:
#           bot.kick_chat_member(chat_id, user_to_ban, until_date=int(time.time()) + 86400)
            bot.send_message(admin_grops,f"грубый нарушитель ! >> tg://user?id={ban_ded} | https://t.me/c/{message_to_report}/{message.reply_to_message.message_id}")
 

            #bot.send_message(admin_grops, f"Пользователь {message.reply_to_message.from_user.username} получил бан на 24 часа за нарушение.")
            #logger.debug(f"Пользователь {message.reply_to_message.from_user.username} получил бан на 24 часа за нарушение.")        

        # Удаляем данные о репорте
        del report_data[chat_id]
    else:
       #print(f'{report_data=}')
       #chat_id = message.chat.id
       #report_data[chat_id]['message_id'] = message.message_id
       #report_data[chat_id]['responses']  =report_data[chat_id]['responses'] + 1   
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
        return 'get data base error >>',{e}

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
        status=["читы вырубай ! ",'как то многовато ,читы ? '][random.randint(0,1)]
    elif rec <=1:
        status=["ты плохой исправляйся 😡",'ай ай ай нарушаем'][random.randint(0,1)]
    elif rec>=5:
        status=['ты хороший 😊','ты молодец 👍','законопослушый так держать! '][random.randint(0,2)]
        
    else:
        status=["😐",'ну норм','нейтральный','не без гриха'][random.randint(0,3)]
    return status
import sqlite3
import logging

@bot.message_handler(commands=['я', 'me'])
def send_statbstic(message):
    try:
        with sqlite3.connect('Users_base.db') as connection:
            cursor = connection.cursor()

            # Создаем таблицу, если она не существует
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL,
                reputation INTEGER NOT NULL,
                warn_user_id INTEGER NOT NULL
            )
            ''')

            # Создаем индекс, если он еще не существует
            cursor.execute('CREATE INDEX IF NOT EXISTS warn_user_id_index ON Users (warn_user_id)')

            user_id = message.from_user.id
            
            # Проверяем, существует ли пользователь с данным warn_user_id
            cursor.execute('SELECT * FROM Users WHERE warn_user_id = ?', (user_id,))
            result = cursor.fetchone()

            if result is not None:
                # Извлекаем репутацию из результата
                current_reputation = result[2]  # Предполагаем, что репутация находится в третьем столбце
                bot.reply_to(message, f"Твоя репутация: {current_reputation} \n{status(current_reputation)}")
            else:
                # Пользователь не существует, добавляем его с начальной репутацией
                cursor.execute("INSERT INTO Users (chat_id, reputation, warn_user_id) VALUES (?, ?, ?)",
                               (message.chat.id, 5, user_id))
                bot.reply_to(message, f"Твоя репутация: 5 \n{status(5)}")
    
    except Exception as e:
        logging.error(f'Ошибка в операции с базой данных: {e}')
        bot.reply_to(message, "Произошла ошибка. Пожалуйста, попробуйте позже.")


def update_user(user_id, reputation=None):
    # Создаем подключение к базе данных
    connection = sqlite3.connect('Users_base.db')
    cursor = connection.cursor()
    
    # Формируем запрос для обновления
    query = "UPDATE Users SET "
    params = []
    
    if reputation is not None:
        query += "reputation = ?"
        params.append(reputation)
    
    # Проверяем, были ли добавлены параметры
    if params:  # Если есть параметры, добавляем WHERE
        query += " WHERE warn_user_id = ?"
        params.append(user_id)
    else:
        # Если нет параметров для обновления, не выполняем запрос
        return None 

    # Выполняем запрос
    cursor.execute(query, params)
    
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()
    
def data_base(chat_id, warn_user_id, message,nfkaz)->int: 
    try:
        resperens=4
        # Создаем подключение к базе данных
        connection = sqlite3.connect('Users_base.db')
        cursor = connection.cursor()
        
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
            new_reputation = current_reputation - nfkaz
            
            # Обновляем репутацию пользователя
            if nfkaz != 0:
                resperens=5
                update_user(warn_user_id, new_reputation)  # Передаем id пользователя для обновления
#            bot.reply_to(message, f'Рейтинг понижен до {new_reputation}')
            connection.commit()
            connection.close()
            return new_reputation
        else:
            # Если пользователь не найден, добавляем его
            cursor.execute('INSERT INTO Users (chat_id, reputation, warn_user_id) VALUES (?, ?, ?)', (chat_id, resperens, warn_user_id))
            connection.commit()
            connection.close()
            return resperens

#            bot.reply_to(message, 'Пользователь добавлен с репутацией 4')
    except Exception as e:
        logging.error(f'Ошибка в операции с базой данных: {e}')
        bot.reply_to(message, "Произошла ошибка. Пожалуйста, попробуйте позже.")
    
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
            bot.send_message(admin_grops,f"репутация снижена >> tg://user?id={message.reply_to_message.from_user.id}, @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} | сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.debug(f"репутация снижена >>  @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.info(f"Пользователь @{message.from_user.username} понизил репутацию ") 
        
        # Проверяем, достаточно ли ответов для бана
            if reputation <= 1:
#           bot.kick_chat_member(chat_id, user_to_ban, until_date=int(time.time()) + 86400)
                bot.send_message(admin_grops,f"грубый нарушитель ! >> tg://user?id={ban_ded} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id}")
        #bot.send_message(admin_grops, f"Пользователь {message.reply_to_message.from_user.username} получил бан на 24 часа за нарушение.")
            #logger.debug(f"Пользователь {message.reply_to_message.from_user.username} получил бан на 24 часа за нарушение.")        

        else:
        #print(f'{report_data=}')
        #chat_id = message.chat.id
        #report_data[chat_id]['message_id'] = message.message_id
        #report_data[chat_id]['responses']  =report_data[chat_id]['responses'] + 1   
            bot.reply_to(message, "Пожалуйста, ответьте командой на сообщение, нарушающее правила, чтобы снизить репутацию") 
    else:
        bot.reply_to(message,['ты не администратор!','только админы вершат правосудие','ты не админ','не а тебе нельзя','нет'][random.randint(0,4)])
                    

@bot.message_handler(commands=['reput'])
def handle_warn(message):
    if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator'] or message.from_user.id =='5194033781':
        if message.reply_to_message:

            chat_id = message.chat.id#инециалезацыя всякой хрени 
            warn_message_text = message.reply_to_message.text
            ban_ded=message.reply_to_message.from_user.id
            warn_chat=message.chat.id
            message_to_warp=str(warn_chat).replace("-100", "")

            reputation=data_base(chat_id,ban_ded,message,-1)#партия довольна вами +1 к репутации
            bot.reply_to(message,f'репутация повышена \nтекущяя репунация пользевателя:{reputation}')
            bot.send_message(admin_grops,f"репутация повышена >> tg://user?id={message.reply_to_message.from_user.id}, @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} | сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.debug(f"репутация повышена >>  @{message.reply_to_message.from_user.username} | https://t.me/c/{message_to_warp}/{message.reply_to_message.message_id} сообщение>> {warn_message_text if message.content_type == 'text' else message.content_type}")
            logger.info(f"Пользователь @{message.from_user.username} повысил репутацию ") 
        
        else:
        #print(f'{report_data=}')
        #chat_id = message.chat.id
        #report_data[chat_id]['message_id'] = message.message_id
        #report_data[chat_id]['responses']  =report_data[chat_id]['responses'] + 1   
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
    bot.reply_to(message,'/monitor - показатели сервера \n/warn - понижение репутации на 1\n/reput - повышение репутации на 1\n/data_base - вся база данных\n/info - узнать репутацию пользователя')


@bot.message_handler(commands=['52'])
def handle_warn(message):
    bot.reply_to(message,'52')

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

user_messages = {}#инициализация словарей 
user_text = {}


SPAM_LIMIT = 8 # Максимальное количество сообщений
SPAM_TIMEFRAME = 4  # Время в секундах для отслеживания спама

# Инициализация логирования
logger.add("cats_message.log", level="TRACE", encoding='utf-8', rotation="500 MB")
# Функция для обработки сообщений
def anti_spam(message):
    
    user_id = message.from_user.id
    current_time = time.time()
    user_text[user_id] = message.text  # Сохраняем текст сообщения для пользователя
    

    # Удаление старых временных меток
    if user_id not in user_messages:
        user_messages[user_id] = []
    user_messages[user_id] = [timestamp for timestamp in user_messages[user_id] if current_time - timestamp < SPAM_TIMEFRAME]

    # Добавление текущего временного штампа
    user_messages[user_id].append(current_time)

    # Проверка на спам
    if len(user_messages[user_id]) > SPAM_LIMIT:
        #bot.kick_chat_member(message.chat.id,user_id, until_date=int(time.time()) + 86400) #выгоняем из чата
        try:
            pass
            '''
            # Ограничиваем пользователя на 24 часа 
            bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                until_date=timedelta(hours=24),
                can_send_messages=False
            )
            '''
            
            #bot.send_message(message.chat.id, f"Пользователь {user_id} замучен на 1 день")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка: {str(e)}")
        #bot.delete_message(message.chat.id,message.message_id)
        id_spam_message=str(message.chat.id).replace("-100", "")
        print(f'Обнаружен спам от пользователя >> tg://user?id={user_id}')
        bot.send_message(admin_groups, f'Обнаружен спам от пользователя >> tg://user?id={user_id}, @{message.from_user.username} | сообщение: {message.text if message.content_type == "text" else "Не текстовое сообщение"} \n|https://t.me/c/{id_spam_message}/{message.message_id}')
        
    else:
        #print(datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S')) вывот даты на будующее
        global is_bot_active
        is_bot_active = True
        if "[help]" in str(user_text[user_id]) or "[Help]" in str(user_text[user_id]):
            id_help_hat=str(message.chat.id).replace("-100", "")
            bot.send_message(admin_groups,  f"@HITHELL , @mggxst есть вопрос от @{message.from_user.username} \nвот он: https://t.me/c/{id_help_hat}/{message.message_id}")
        logs = f"chat>>{message.chat.id} user >> tg://user?id={message.from_user.id}, @{message.from_user.username} | сообщение >> {message.text if message.content_type == 'text' else message.content_type}"
        print("————")
        logger.debug(logs)


@bot.message_handler(content_types=['text', 'sticker', 'photo', 'video'])
def message_handler(message):
    if time.time() - message.date > 1.5:
        return
    anti_spam(message)

# Обработчик всех остальных типов сообщений
@bot.message_handler(func=lambda message: True)
def other_message_handler(message):
    if time.time() - message.date > 1.5:
        return
    anti_spam(message)


#новый юзер 
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        logger.info('new member in chat')
        username = new_member.username if new_member.username else "пользователь"
        welcome_message = [f"Привет, @{username}! Добро пожаловать в наш чат! \n/help для справки",f"новенький скинь ножки \nой не тот текст \nПривет, @{username}! Добро пожаловать в наш чат! \n/help для справки"][random.randint(0,1)]
        #bot.reply_to(message , welcome_message)
        # Открываем исходный GIF
        input_gif_path = 'hello.gif'
        output_gif_path = 'output.gif'
        # Открываем изображение
        gif = Image.open(input_gif_path)
        # Создаем список для хранения кадров с текстом
        frames_with_text = []
        # Настройка шрифта (по умолчанию, если шрифт не найден, будет использован шрифт по умолчанию)
        try:
            font = ImageFont.truetype("arial.ttf", 40)  # Замените "arial.ttf" на путь к вашему шрифту
        except IOError:
            font = ImageFont.load_default(size=40)

        # Добавляем текст на каждый кадр
        for frame in range(gif.n_frames):
            gif.seek(frame)
            # Копируем текущий кадр
            new_frame = gif.copy()
            # Преобразуем в rgba 
            new_frame = new_frame.convert('RGBA')
            draw = ImageDraw.Draw(new_frame)
            # Определяем текст и его позицию
            usernameh=message.from_user.first_name
            if len(username)>15:
                n = 15
                for char in username:
                    if n < 1:
                        break
                    n -= 1
                    usernameh += char
            text = f"привет! {usernameh} добро пожаловать в чат :3 "
            text_position =(160, 345) # Позиция (x, y) для текста

            # Добавляем текст на кадр
            draw.text(text_position, text, font=font, fill=(0, 0, 0))  # Цвет текста задан в формате RGB

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


# Основной цикл
def main():

    while True:
        try:
            bot.polling(none_stop=True)
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
  #          bot.send_message(message.from_user.id, 'Увы, случилась ошибка>>\n' + str(e))
            logger.error(f"Ошибка: {e}")
            time.sleep(4)

if __name__ == '__main__':
    main()
    
