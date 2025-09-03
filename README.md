<h3 align="center">Telegram бот админестратор</h3>

![GitHub](https://img.shields.io/github/license/1yib/vsc-bundle?color=A3BE8C&style=flat-square)

<a id="top"></a>
<a id="ru"></a>

## информация


<h3>бот администратора с оповещением о спаме репортах</h3>
<h3>описание</h3>
<h4>
Это бот помошник администрации с довольно полезным функцианалом для пользователей и админов основной функционал:
  
- анти спам
- пометки для вопросов для адмиистрации
- система репутации и подсчета сообщений
  
---

основные команды:

/help - справка.<br>

/report — для оповещения о нарушении, чтобы оставить коментарий сделайте отступ от команды и напишите его.<br>  

/monitor — для отслеживания системных показателей ПК/хостинга.<br>

/warn - снижение репутации на 1.<br>

/reput - повышение репутации на 1.<br>

/info - информация о пользователе аргументы: `-all` - полный список информации 

/я - своя репутация.<br>

/бан - бан (блокировка) пользователя с сохранением причины.<br>

/мут - мут (временный запрет на отправление сообщений) пользователя с указанием причины и время.

/admin_command - команды администраторов

/настройки - отображает настройки(файл конфигурации `settings.json` ) имеет парамитер -r который перезагружает настройки если они были изменены без необходимости перезапуска бота пример :`/настройки -r`.<br>

/t - перевод сообщения на русский или другой язык (дополнительно потдерживает перевод в bin , hex и транслит кодеровки)пример:`/t любой текст:en`.<br>

/download - загруска стикеров и голосовых сообщений , при загруске синволов нужно указать расширение пример:`/download png`.

/test - обширное тестирование систем бота аргумент: `-all`:вывод дополнительной информации о связи с Telegram api

/ping - проверка задержки отклика по ссылке, аргументы:

- `/ping <ссылка>` для тестирования по умолчанию https://ya.ru 
- количество повторов замера задержки `/ping <ссылка>,<количество запросов>`
- режим расчета True - вычисление средни статисчической задержки из всех попыток. по умолчанию (не указывая значение) отоброжение зажержки каждой попытки `/ping <ссылка>,<количество запросов>,<режим>`.

/message_info - выводит информацию о сообщении полезно для медиа.<br>

/log - отправка файла логов. <br>

/data_base - выводит базу данных для поиска конкретного пользователя в базе припишите его ID к команде через пробел, пример: `/data_base 5194033781`

/serh - поиск статей на википедии пример: `serh :<promt>` ,язык статей зависит от настройки `settings.json` парамитра `auto_translete`:`laung` аргументы: `-ping` - проверка задержки сйта wikipedia.org. <br>

/blaklist — добавляет стикер в черный список добавляет стикер в черный список (стикеры находящиеся в черном списке автоматически удаляются если удаление разрешено в настройках ) аргумент: `-info` - отображает количество стикеров в черном списке 

/unblaklist — убирает стикер из черного списка

/creat - позволяет создавать скрипты является простейшим "командным языком программирования" находиться в бета тестировании и имеет сомнительный функционал. (из за спама с помощю этой команды она была отключена в обших чатах доступно только в личных) 
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


</h4>

имеет логирывание сообщений и других событий

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

true - включено , false - выключено  
bambam - автоматичиские муты/баны.<br>

delet_messadge - автоматическое удаление сообщений (в частности при 5 репортах на одном сообщении оно будет удаляться).<br>

admin_grops - группа администрации (впишите ее ID).<br>

spam_limit - количество сообщений от одного пользователя которое будет считаться спамом (за отрезок времени указанный в spam_timer).<br>

spam_timer - функционал описан выше. <br>

ban_and_myte_command - включает команды /бан и /мут для банов и мутов соотвецтвено. <br>

console_control - разрешения удалённого запуска команд в терминале с помощью команды /console, синтаксис /console :<команда терминала> работает только в группе администрации администратором группы.<br>
(⚠️данная команда может выполнять в том числе и вредоносные команды буте внимательны с ее включением).<br>

auto_translete - авто перевод сообщений в чате с иностранного на указанный в `laung` по умолчанию `"laung":"ru"` параметр активации `Activate` по умолчанию `"Activate":false`.

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

### Administrator Bot with Spam Report Notifications

### Description

This is an assistant bot for administrators with quite useful functionality for both users and admins. Core features:

· Anti-spam
· Notes for questions directed to administration
· Reputation system and message counting

---

Main commands:

/help - Help.

/report - To report a violation. To leave a comment, add a space after the command and write your comment.

/monitor - For tracking PC/hosting system metrics.

/warn - Decrease reputation by 1.

/reput - Increase reputation by 1.

/info - User information. Arguments: -all - full information list.

/me - Check your own reputation.

/ban - Ban (block) a user, saving the reason.

/mute - Mute (temporarily restrict from sending messages) a user, specifying the reason and duration.

/admin_command - Administrator commands.

/settings - Displays settings (configuration file settings.json). Has a -r parameter which reloads the settings if they were changed without needing to restart the bot. Example: /settings -r.

/t - Translate a message to Russian or another language (additionally supports encoding to bin, hex, and translit). Example: /t any text:en.

/download - Download stickers and voice messages. When downloading symbols, specify the file extension. Example: /download png.

/test - Extensive bot system testing. Argument: -all: outputs additional information about the connection with the Telegram API.

/ping - Check response latency for a URL. Arguments:

· /ping <url> for testing (default is https://ya.ru).
· Number of latency measurement attempts: /ping <url>,<number of requests>.
· Calculation mode: True - calculate average statistical latency from all attempts. Default (if value is not specified) shows latency for each attempt: /ping <url>,<number of requests>,<mode>.

/message_info - Displays information about a message, useful for media.

/log - Send the log file.

/data_base - Outputs the database. To search for a specific user in the database, add their ID to the command separated by a space. Example: `/data_base 5194033781`

/search - Search for articles on Wikipedia. Example: search :<prompt>. Article language depends on the auto_translate:lang parameter in settings.json. Arguments: -ping - check latency of the wikipedia.org site.

/blacklist - Add a sticker to the blacklist (stickers on the blacklist are automatically deleted if deletion is enabled in the settings). Argument: -info - shows the number of stickers on the blacklist.

/unblacklist - Remove a sticker from the blacklist.

/creat - Allows creating scripts. It is a simple "command programming language", is in beta testing, and has questionable functionality. (Due to spam using this command, it has been disabled in group chats and is only available in private messages). <a id="creat_program_info"></a>

<details><summary>Syntax and Arguments</summary><p>

Syntax:

General command syntax:

```sencoscript
  /creat
  # create a variable
  var a=a
  # send variables
  send "a equals: {a}"
```

No indentation at the beginning!

Comments are marked with the symbol: #

To insert a variable, wrap its name in curly braces `{}`

Commands:

· send - Send messages to the chat (HTML formatting is supported). Example: send "hello world"
· var - Create variables. Example: var a=1
  · Details:
    ```sencoscript
    # create a variable
    var a=1
    # send variables
    send "a equals: {a}"
    ```
    Output: a equals: 1
· value - Send all variables in dictionary format.
· calc - Execute logical operations. Example: calc a=1>0. Available operators: +, -, *, /, **, %, ==, !=, <, <=, >, >=
  · Details:
  ```sencoscript
   var a=5
   var b=10
  
   calc out={a}<{b}
   
   send "{out}"
  ```
· .end - End the program.
· random - Generate a random number within a specified range. Example: random a=1-5
· timeout - Execution delay. Example: timeout 5
· if - Execute a command if a condition is true. Example: if 1>0:send "True". To run multiple commands, separate them with &.
· len - Count the number of characters in a string/variable. Example: len a=abc
· list - Alternative list (indexing starts from 0). Example: list a=1,2,3[1]. You can also assign data by list element ID. Example: list a=1,2,3[1]=0
· for - Executes commands a specified number of times, counting from 0, and places the counter value in a variable. To run multiple commands, separate them with ;. Example: for i in 5:send "num:{i}"
· replace - Replace a character or several characters in a string. Example: replace a=text:old text/character,new character

Variable constants:

· $reply_to - The text of the message that was replied to with the /creat command. If there was no reply, the variable will contain $none.
· $pi - Mathematical constant 'π' (pi) up to 10 decimal places.
· $username - The username of the user whose message was replied to with the /creat command. If there was no reply, the variable will contain $none.

Example simple programs:

Hello World

```sencoscript
/creat

send "hello world"
```

Roulette game

```sencoscript
/creat

random rand=1-3
if {rand}==1:send "you won"
if {rand}==2:send "you lost, try again next time"
if {rand}==3:send "you lost alas",;send "try again next time"
```

Russian Roulette game

```sencoscript
/creat 

program Russian Roulette

for i in 6:random r=0-{i};if {r}==1:send"you lost"&.end;if {i} == 5:send"you won"

```

</p></details>


It features logging of messages and other events.

Installation:

To run the bot, insert your token into the TOKEN file without any spaces or other characters!

The application requires <a href="https://www.python.org/">Python 3.12</a> or higher.

```sh
git clone https://github.com/xHak2215/admin_telegram_bot

cd admin_telegram_bot

pip install -r requirements.txt

python aea_bot.py

```

Installation using make:

Download and install dependencies

```sh
git clone https://github.com/xHak2215/admin_telegram_bot

cd admin_telegram_bot

make install

```

Run:

```sh
make run
```

Configuration:

```json
{
    "bambam": false,
    "delete_message": true,
    "admin_groups": "-1001234567890",
    "spam_limit": 10,
    "spam_timer": 4,
    "ban_and_mute_command": true,
    "console_control": true,
    "auto_translate": {"lang": "ru", "Activate": false}
}
```

true - enabled, false - disabled. bambam- Automatic mutes/bans.

delete_message - Automatic message deletion (specifically, a message will be deleted after 5 reports).

admin_groups - Administration group (enter its ID).

spam_limit - Number of messages from one user considered spam (within the time period specified in spam_timer).

spam_timer - Functionality described above.

ban_and_mute_command - Enables the /ban and /mute commands for bans and mutes respectively.

console_control - Allows remote execution of terminal commands using the /console command. Syntax: `/console <terminal command>`. Works only in the administration group by the group administrator. (⚠️This command can execute malicious commands as well;be very careful with enabling this).

auto_translate - Auto-translate foreign language messages in the chat to the language specified in lang (default "lang":"ru"). Activation parameter Activate (default "Activate":false).

--- 


### Supported Formats  
#### Audio/Voice Messages:  
- `.mp3`, `.ogg`, `.m4a`, `.flac`, `.wav`, `.aac`, `.webm`, `.ac3`, `.wma`, `.mkv`.  

#### Stickers/Images:  
- `.BMP`, `.PNG`, `.JPEG`, `.GIF`, `.TIFF`, `.WebP`, `.PPM`, `.ICO`.  

---

Developed for [AEA+ Group](https://t.me/+P5wR2FyxnSQzMjIy) :3  


<h1><p align="right"><a href="#top">↑</a></p></h1>
