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
TOKEN = " token "  

help_user = '/report - забань дебила в чате (временно не работает)\nчтобы получить список правил \n/правило \n Если есть вопросы задайте его добвавив в сообщение [help] и наши хелперы по возмодности помогут вам \n ' 
message_reminder = 'Не забывайте про команду /report для сообщений о нарушении правил.'
logse="nan"
is_bot_active = False
i=0

admin_grops="-1002284704738"
admin_groups=admin_grops

bot = telebot.TeleBot(TOKEN)
#updater = Updater(token=TOKEN)
#dispatcher = updater.dispatcher
os.chdir('C:/Users/User/Desktop/AEA_bot')

#print(__name__)
now = datetime.now()
current_time = now.strftime("%H:%M")
bot.send_message(admin_grops, f"бот запущен \ntime>> {current_time}")
logger.info("бот запущен")
try:
    if e !='1':
         bot.send_message('message.chat.id','Увы, случилась ошибка>> \n' + str(e))
except :
    print("\033[32m{}\033[0m".format('нет ошибок :3 '))
    

# Функция для пинга
def ping():
    start_time = time.time()
    response = requests.get('https://yandex.ru')
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
    print(f"CPU: {cpu_percent}%,\nRAM: {ram_percent}%,\nDisk: {disk_percent}%,\nPing: {response_time}")
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
            bot.reply_to(message.chat.id,f"ты недостоин \nты не админ")
    except Exception as e:
        bot.send_message(admin_grops,f"error logs file>> {e} ")
        logger.error(f"log null error >> {e}")

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
            bot.reply_to(message.chat.id,f"ты не достоин \nты не админ")
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
        bot.reply_to(message.chat.id,f"ты не достоин \nты не админ")

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
@bot.message_handler(commands=['правило'])
def time_server_command(message):
    bot.send_message(message.chat.id, f"Правила \nЗапрещается:\n\n\nРасизм,нацизм, выведение своих полит.взглядов,зоофилия, 18+ контент, жестокие сцены (любые), оскорбление администрации (с учетом что она вас не провоцировала), оскорбление и ущемление пола, нации и т.д, оскорбления, многочисленные упоминания и восхваления полит и просто преступников, спам, вред группе(любой), любое уклонение от правил и поиск лазеек в них. \nЭто карается предупреждением, после мутом, после блокировкой в группе")

# Хранение данных о репортах
report_data =  {}
# Обработка ответа на сообщение с /report
@bot.message_handler(commands=['report','репорт'])
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
         
        bot.send_message(admin_grops,f"послали репорт на >> tg://user?id={message.reply_to_message.from_user.id}, @{message.reply_to_message.from_user.username} | сообщение>>" + reported_message_text)
        logger.debug(f"послали репорт на >>  @{message.reply_to_message.from_user.username} | https://t.me/c/{report_chat}/{message.reply_to_message.message_id} сообщение>> " + reported_message_text)
        logger.info(f"Пользователь @{message.from_user.username} сообщил о нарушении.")
        
        # Проверяем, достаточно ли ответов для бана
        if len(report['responses']) >= 5:
#           bot.kick_chat_member(chat_id, user_to_ban, until_date=int(time.time()) + 86400)
            bot.send_message(admin_grops,f"грубый нарушитель ! >> tg://user?id={ban_ded}")
 

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


# Периодическое напоминание
def send_reminder():
    chat_id = '-1002170027967'# Укажите ID чата для отправки напоминаний
    bot.send_message(chat_id, message_reminder)

# Планирование напоминаний
#schedule.every().day.at("12:00").do(send_reminder)

user_messages = {}#инициализация словарей 
user_text = {}

SPAM_LIMIT = 7 # Максимальное количество сообщений
SPAM_TIMEFRAME = 4  # Время в секундах для отслеживания спама

# Инициализация логирования
logger.add("cats_message.log", level="TRACE", encoding='utf-8', rotation="500 MB")

# Функция для обработки сообщений
def handle_message(message):
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
        print(f'Обнаружен спам от пользователя >> tg://user?id={user_id}')
        if i >=1:
            bot.send_message(admin_groups, f'Обнаружен спам от пользователя >> tg://user?id={user_id}, @{message.from_user.username} | сообщение: {message.text if message.content_type == "text" else "Не текстовое сообщение"}')
        i+=1
    else:
        global is_bot_active
        is_bot_active = True
        if "[help]" in str(user_text[user_id]) or "[Help]" in str(user_text[user_id]):
            id_help_hat=str(message.chat.id).replace("-100", "")
            bot.send_message(admin_groups,  f"@HITHELL , @mggxst есть вопрос от @{message.from_user.username} \n вот он: https://t.me/c/{id_help_hat}/{message.message_id}")
        logs = f"chat>>{message.chat.id} user >> tg://user?id={message.from_user.id}, @{message.from_user.username} | сообщение >> {message.text if message.content_type == 'text' else message.content_type}"
        print("————")
        logger.debug(logs)

@bot.message_handler(content_types=['text', 'sticker', 'photo', 'video'])
def message_handler(message):
    handle_message(message)

# Обработчик всех остальных типов сообщений
@bot.message_handler(func=lambda message: True)
def other_message_handler(message):
    handle_message(message)

#привецтвие новых пользывателей
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    welcome_message = f"Привет, {message.new_chat_members.from_user.username}! Добро пожаловать в наш чат! \n /help для справки"
    bot.reply_to(message.chat.id, welcome_message)

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
            time.sleep(5)

if __name__ == '__main__':
    main()
    
