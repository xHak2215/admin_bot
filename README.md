<h3 align="center">Telegram бот админестратор</h3>

<a id="top"></a>
<a id="ru"></a>

## информация


<h3>бот администратор с оповещением о спаме, репортах и вопросов</h3>
<h3>описание</h3>
<h4>
Это бот помошник администрации с довольно полезным функцианалом для пользователей и админов основной функционал:
  
- анти спам
- пометки вопросов для адмиистрации
- система репутации и подсчета сообщений
- приветствие пользователей и сохранение даты входа 
  
---

<a id="doc_commad"></a>

основные команды:

/help - справка.<br>

/report — для оповещения о нарушении(приходит в группу администрации), чтобы оставить коментарий сделайте отступ от команды и напишите его.<br>  

/monitor — для отслеживания системных показателей ПК/хостинга.<br>

/warn - снижение репутации на 1.<br>

/reput - повышение репутации на 1.<br>

/info - информация о пользователе аргументы: `-all` - полный список информации требует права администратора.

/я - своя репутация и количество сообщений.<br>

/бан - бан (блокировка) пользователя с сохранением причины, пример:`/бан for @username reason:причина`.<br>

/мут - мут (временный запрет на отправление сообщений) пользователя с указанием причины и времени пример:`/мут for @username time: 1 hours reason:причина мута`.

/admin_command - команды администраторов.

/настройки - отображает настройки(файл конфигурации `settings.json` ) имеет парамитер -r который перезагружает настройки если они были изменены без необходимости перезапуска бота пример :`/настройки -r`.<br>

/t - перевод сообщения на русский или другой язык (дополнительно потдерживает перевод в bin(двоичные) , hex(шестнадцатеричные) и транслит кодеровки)пример:`/t любой текст:en`.<br>

/download - загруска стикеров и голосовых сообщений , при загруске синволов нужно указать расширение пример:`/download png`.

/test - обширное тестирование систем бота аргумент: `-all`:вывод дополнительной информации о связи с Telegram api и user bot.

/ping - проверка задержки отклика по ссылке, аргументы:

- `/ping <ссылка>` для тестирования по умолчанию https://ya.ru 
- количество повторов замера задержки `/ping <ссылка>,<количество запросов>`
- режим расчета True - вычисление средни статисчической задержки из всех попыток. по умолчанию (не указывая значение) отоброжение зажержки каждой попытки `/ping <ссылка>,<количество запросов>,<режим>`.

/message_info - выводит информацию о сообщении полезно для медиа.<br>

/log - отправка файла логов. <br>

/data_base - выводит базу данных для поиска конкретного пользователя в базе припишите его ID к команде через пробел, пример: `/data_base 5194033781`.

/serh - поиск статей на википедии пример: `serh :<promt>` ,язык статей зависит от настройки `settings.json` парамитра `auto_translete`:`laung` аргументы: `-ping` - проверка задержки сйта wikipedia.org. <br>

/blaklist — добавляет стикер в черный список добавляет стикер в черный список (стикеры находящиеся в черном списке автоматически удаляются если удаление разрешено в настройках ) аргумент: `-info` - отображает количество стикеров в черном списке.

/unblaklist — убирает стикер из черного списка.

/creat - позволяет создавать скрипты является простейшим "командным языком программирования" находиться в бета тестировании и имеет сомнительный функционал. (из за спама с помощю этой команды она была отключена в обших, и чатах доступно только в личных)
<a id="creat_program_info"></a>
<details><summary>синтаксис и аргументы</summary><p>

## синтаксис:

### общий синтаксис команды:

  ```script
  /creat
  # создаем переменную
  var a=a
  # отправка переменных
  send "a равно:{a}"
  ```
  без отступов в начале!

комментарии обозначаться символом:`#`

для вставки переменной обверните ее название в фигурные скобки `{}`

### команды:

- send - отправка сообщений в чат (включено использование html форматирования) пример: `send "hello world"`
- var - создание переменных пример: `var a=1`

  - подробнее:

    ```script
    # создаем переменную
    var a=1
    # отправка переменных
    send "a равно:{a}"
    ```
    выход:`a равно:1`
- value - отправка всех переменных в формате словаря 
- calc - исполнение логических операций пример `calc a=1>0` доступные операторв:+, - , * , / , ** , % , == , != , < , <= , > , >=

  - подробнее:
   ```script
   var a=5
   var b=10

   calc out={a}<{b}
   
   send "{out}"
   ```
- .end - завершение программы 
- random - генерация случайного числа в указанном радиусе пример:`random a=1-5`
- timeout - задержка исполнения пример:`timeout 5`
- if - исполнение команды если условие верно пример: `if 1>0:send "True"` для запуска нескольких команд пишите их через `&`
- len - cщитает количество символов в строке/переменной пример:`len a=abv`
- list - альтернативный список отсчет видеться от 0 пример:`list a=1,2,3[1]`, так же можно присвоить данные по id элементу списка пример:`list a=1,2,3[1]=0`
- for - выполняет команды заданое количество раз считая от 0 при этом лжит цифру отсчета в переменную , для запуска нескольких команд пишите их через `;` пример:`for i in 5:send "num:{i}"`
- replace - замена синволоа или нескольких синволов в строке пример:`replace a=текст:старый текст/синвол,новый синвол`

### константы переменных:

- `$reply_to` - текст сообщения на которое был дан ответ командой `/creat` если ответа не было то в перемнной будет находиться `$none`
- `$pi` - математическая константа 'число π' до 10-го числ после запятой
- `$username` - username пользователя на че сообщение был дан ответ командой `/creat` если ответа не было то в перемнной будет находиться `$none`

### примеры простых программ:

> hello world

```senscript
/creat

send "hello world"
```

> игра рулетка 

```senscript
/creat

random rand=1-3
if {rand}==1:send "ты выиграл"
if {rand}==2:send "ты проиграл, получиться в другой раз"
if {rand}==3:send "ты проиграл увы",;send "получиться в другой раз"
```

> игра русская рулетка 

```
/creat 

program Русская рулетка

for i in 6:random r=0-{i};if {r}==1:send"ты проиграл"&.end;if {i} == 5:send"ты выйграл"

```

</p></details>

/team - команда позволяющяя создавать свои команды/кланы. 
Использование:
- `/team создать <имя_команды>` - имя должно быть не более 70 символов и быть без пробелов все пробелы автамтически убераються;
- `/team пригласить в <имя_команды>` - ответе на сообщения того человека которого хотите пригласить в команду;
- `/team инфо <имя_команды>` - информация о команде а именно время создания, участники,создатель команды;
- `/team сбор <имя_команды>` - тегает всех учасиков команды';
- `/team покинуть <имя_команды>` - удаляет вас из команды если вы не ее создатель;

(команда в разработке)

</h4>

имеет логирывание сообщений и других событий

---

### установка:

<h3>для запуска бота вставите свой токен в файл TOKEN без пробелов или каких либо других символов!</h3>

для работы приложения необходим <a href="https://www.python.org/"> python 3.12v</a> или выше  

```sh
git clone https://github.com/xHak2215/admin_telegram_bot

cd admin_telegram_bot

pip install -r requirements.txt

python aea_bot.py

```
установки используя `make`:

загрузка и установка зависимостей 

```sh
git clone https://github.com/xHak2215/admin_telegram_bot

cd admin_telegram_bot

make install

```

запуск :

```sh
make run
```

### настройка:

```json
{
    "bambam":false,
    "delet_messadge":true,
    "admin_grops":"-1001234567890",
    "spam_limit":10,
    "spam_timer":4,
    "ban_and_myte_command":true,
    "console_control":true,
    "auto_translete":{"laung":"ru","Activate":false}

}
```

bambam - автоматичиские муты/баны.<br>

delet_messadge - автоматическое удаление сообщений (в частности при 5 репортах на одном сообщении оно будет удаляться).<br>

admin_grops - группа администрации (впишите ее ID).<br>

spam_limit - количество сообщений от одного пользователя которое будет считаться спамом (за отрезок времени указанный в spam_timer).<br>

spam_timer - функционал описан выше. <br>

ban_and_myte_command - включает команды /бан и /мут для банов и мутов соотвецтвено. <br>

console_control - разрешения удалённого запуска команд в терминале с помощью команды /console, синтаксис `/console <команда терминала>` работает только в группе администрации администратором группы.<br>
(⚠️данная команда может выполнять в том числе и вредоносные команды буте внимательны с ее включением).<br>

auto_translete - авто перевод сообщений в чате с иностранного на указанный в `laung` по умолчанию `"laung":"ru"` параметр активации `Activate` по умолчанию `"Activate":false`.


### настройка user bot 

user bot нужен для расширения функционала бота и обхода ограничений обычных телеграм бота 

файл конфигурации:

```json
{
    "API_ID":"00000000", 
    "API_HASH":"75fg6c01487e616410d8e79e7b2263c7d",
    "PHONE_NUMBER":"+11111111111",
    "passworld":"000000"

}
```

`API_ID` - этот api ID можно получить на <a href="https://my.telegram.org/auth?to=deactivate">этом</a> сайте в разделе developer.

`API_HASH` - можно получить там же где и `API_ID`.

`PHONE_NUMBER` - это номер телефона на который зарегистрирован аккаунт.

`passworld` - это облачный пароль аккаунта, если его нет то задайте новый.

<a id="format"></a>

поддерживаемые форматы:<br>
загрузка голосовых сообщений и аудио дорожек:

- .mp3 (MPEG Audio Layer III)
- .ogg (Opus/Vorbis)
- .m4a (AAC в MP4-контейнере)
- .flac (Free Lossless Audio Codec)
- .wav (PCM/WAVE)
- .aac (Raw AAC-поток)
- .webm (Opus/Vorbis)
- .ac3 (Dolby Digital)
- .wma (Windows Media Audio)
- .mkv (Любой кодек, включая FLAC)<br>

загрузка стикеров/фото :

- .BMP	BitMaP (без сжатия)	1, L, P, RGB, RGBA
- .PNG	Portable Network Graphics	L, LA, P, RGB, RGBA
- .JPEG	Joint Photographic Experts Group	L, RGB
- .GIF	Graphics Interchange Format	L, P
- .TIFF	Tagged Image File Format	L, LA, P, RGB, RGBA
- .WebP	Современный формат от Google	RGB, RGBA
- .PPM	Portable Pixmap	RGB
- .ICO	Иконки Windows	RGBA

бот сделан для группы <a href="https://t.me/+P5wR2FyxnSQzMjIy">AEA+</a> :3

<a id="en"></a>

<h3 align="center">English</h3>

---

## Information 

<h3>Admin bot with spam, report and question notifications</h3>
<h3>Description</h3>
<h4>
This is an administration assistant bot with useful features for users and admins. Main functionality:

- anti-spam  
- marking questions for administration  
- reputation system and message counting  
- welcoming users and saving join date  

---

<a id="doc_commad"></a>

Main commands:

/help - help.<br>

/report — to notify about a violation (sent to the admin group). To leave a comment, put a space after the command and type it.<br>

/monitor — to monitor system metrics of the PC/hosting.<br>

/warn - decrease reputation by 1.<br>

/reput - increase reputation by 1.<br>

/info - user information. Arguments: `-all` - full list of information (requires admin rights).<br>

/me - your reputation and message count.<br>

/ban - ban (block) a user with reason preserved, example: `/бан for @username reason:reason`.<br>

/myte - mute (temporary restriction from sending messages) a user with reason and time, example: `/мут for @username time: 1 hours reason:reason`.<br>

/admin_command - administrator commands.<br>

/config - shows settings (configuration file `settings.json`). Has parameter `-r` which reloads settings if they were changed without restarting the bot, example: `/настройки -r`.<br>

/t - translate a message to Russian or another language (also supports conversion to bin (binary), hex (hexadecimal) and transliteration encodings). Example: `/t any text:en`.<br>

/download - download stickers and voice messages. When downloading symbols, specify the extension, e.g.: `/download png`.<br>

/test - extensive bot system testing. Argument: `-all` outputs additional info about connection to Telegram API and user bot.<br>

/ping - check response latency to a URL. Arguments:
- `/ping <url>` to test; default is https://ya.ru  
- number of repeats `/ping <url>,<count>`  
- calculation mode True — compute average statistical latency across all attempts. By default (if not specified) shows latency for each attempt: `/ping <url>,<count>,<mode>`.<br>

/message_info - outputs information about a message (useful for media).<br>

/log - send log file.<br>

/data_base - outputs the database to search for a specific user; append their ID after the command separated by a space, example: `/data_base 5194033781`.<br>

/serh - search articles on Wikipedia, example: `serh :<prompt>`. Article language depends on `settings.json` parameter `auto_translete`:`laung`. Arguments: `-ping` - check latency to wikipedia.org. <br>

/blaklist — adds a sticker to the blacklist (stickers in the blacklist are automatically removed if deletion is allowed in settings). Argument: `-info` - shows number of stickers in the blacklist.<br>

/unblaklist — removes a sticker from the blacklist.<br>

/creat - allows creating scripts; a simple "command programming language", in beta with limited functionality. (Disabled in groups and public chats due to spam — available only in private chats.)
<a id="creat_program_info"></a>
<details><summary>Syntax and arguments</summary><p>

## Syntax:

### General command syntax:

  ```script
  /creat
  # create a variable
  var a=a
  # send variables
  send "a equals:{a}"
  ```
  No leading indentation!

Comments start with `#`.

To insert a variable wrap its name with curly braces `{}`.

### Commands:

- send - send messages to chat (HTML formatting supported), example: `send "hello world"`  
- var - create variables, example: `var a=1`

  - Details:

    ```script
    # create a variable
    var a=1
    # send variable
    send "a equals:{a}"
    ```
    Output: `a equals:1`
- value - send all variables as a dictionary  
- calc - perform logical/math operations, example `calc a=1>0`. Available operators: +, -, *, /, **, %, ==, !=, <, <=, >, >=

  - Details:
   ```script
   var a=5
   var b=10

   calc out={a}<{b}
   
   send "{out}"
   ```
- .end - terminate the program  
- random - generate a random number in given range, example:`random a=1-5`  
- timeout - execution delay, example:`timeout 5`  
- if - execute command if condition true, example: `if 1>0:send "True"`. For multiple commands separate them with `&`.  
- len - counts characters in a string/variable, example:`len a=abv`  
- list - alternative indexed list starting at 0, example:`list a=1,2,3[1]`. You can assign by index: `list a=1,2,3[1]=0`  
- for - run commands a number of times counting from 0; the counter is placed in a variable. For multiple commands separate with `;`, example:`for i in 5:send "num:{i}"`  
- replace - replace character(s) in a string, example:`replace a=text:old,new`

### Variable constants:

- `$reply_to` - text of the message replied to when running `/creat`; if none, value is `$none`  
- `$pi` - π to 10 decimal places  
- `$username` - username of the user whose message was replied to when running `/creat`; if none, value is `$none`

### Example simple programs:

> hello world

```senscript
/creat

send "hello world"
```

> roulette game

```senscript
/creat

random rand=1-3
if {rand}==1:send "you won"
if {rand}==2:send "you lost, try next time"
if {rand}==3:send "you lost unfortunately",;send "try next time"
```

> Russian roulette

```
/creat 

program Russian roulette

for i in 6:random r=0-{i};if {r}==1:send"you lost"&.end;if {i} == 5:send"you won"

```

</p></details>

/team - command for creating teams/clans.
Usage:
- `/team создать <team_name>` - name must be max 70 characters and contain no spaces (spaces are removed automatically);  
- `/team пригласить в <team_name>` - reply to the message of the person you want to invite;  
- `/team инфо <team_name>` - team info: creation time, members, team creator;  
- `/team сбор <team_name>` - mention all team members;  
- `/team покинуть <team_name>` - removes you from the team if you are not its creator;

(command is in development)

</h4>

The bot logs messages and other events.

---

### Installation:

<h3>To run the bot, paste your token into the TOKEN file without spaces or any other characters!</h3>

The application requires Python 3.12 or higher.

```sh
git clone https://github.com/xHak2215/admin_telegram_bot

cd admin_telegram_bot

pip install -r requirements.txt

python aea_bot.py

```
Install using `make`:

```sh
git clone https://github.com/xHak2215/admin_telegram_bot

cd admin_telegram_bot

make install

```

Run:

```sh
make run
```

### Configuration:

```json
{
    "bambam":false,
    "delet_messadge":true,
    "admin_grops":"-1001234567890",
    "spam_limit":10,
    "spam_timer":4,
    "ban_and_myte_command":true,
    "console_control":true,
    "auto_translete":{"laung":"ru","Activate":false}

}
```

bambam - automatic mutes/bans.<br>

delet_messadge - automatic deletion of messages (e.g., a message will be deleted after 5 reports).<br>

admin_grops - admin group ID (fill it with the group ID).<br>

spam_limit - number of messages from one user considered spam within the time window spam_timer.<br>

spam_timer - as described above.<br>

ban_and_myte_command - enables /бан and /мут commands for bans and mutes respectively.<br>

console_control - allows remote execution of terminal commands via `/console`. Syntax `/console <terminal command>` works only in the admin group by a group admin.  
(⚠️ This command can execute harmful commands as well — be careful enabling it).<br>

auto_translete - auto-translate messages in chat from foreign languages to the language set in `laung`. Default `"laung":"ru"`. Activation parameter `Activate` default is `false`.

### User bot setup

A user bot is needed to extend functionality and bypass limitations of a regular Telegram bot.

Config file:

```json
{
    "API_ID":"00000000", 
    "API_HASH":"75fg6c01487e616410d8e79e7b2263c7d",
    "PHONE_NUMBER":"+11111111111",
    "passworld":"000000"

}
```

`API_ID` - API ID, obtainable at https://my.telegram.org/ in the developer section.

`API_HASH` - obtained together with `API_ID`.

`PHONE_NUMBER` - phone number of the account.

`passworld` - cloud password for the account; if none, set a new one.

--- 


### Supported Formats  
#### Audio/Voice Messages:  
- `.mp3`, `.ogg`, `.m4a`, `.flac`, `.wav`, `.aac`, `.webm`, `.ac3`, `.wma`, `.mkv`.  

#### Stickers/Images:  
- `.BMP`, `.PNG`, `.JPEG`, `.GIF`, `.TIFF`, `.WebP`, `.PPM`, `.ICO`.  

---

Developed for [AEA+ Group](https://t.me/+P5wR2FyxnSQzMjIy) :3  


<h1><p align="right"><a href="#top">↑</a></p></h1>
