<h3 align="center">Telegram бот админестратор</h3>

<!--
<details>
  <summary>автор</summary>
  <ol>
    <li>
      <ul>
      <li><a href="https://github.com/xHak2215/consol">основной проект</a></li>
      </ul>
     </li>
     <li>
      <ul>
      <li><a href="https://t.me/HITHELL">telegram</a></li>
      </ul>
     </li>
  </ol>
</details>
<a id="readme-top"></a>
-->
<a id="top"></a>
<a id="ru"></a>

## информация


<h3>бот администратора с оповещением о спаме репортах</h3>
<h3>для запуска бота вставите свой токен в файл TOKEN без пробелов или каких либо других символов!</h3>
<h3>описание</h3>
<h4>
Это бот с распознаванием спама и оповещением администраторов чата о нем.имеет настройки анти спама выдаваемых наказаний и группы администрации  <br>
Он имеет множество команд, например:<br>

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

/creat - позволяет создавать скрипты является простейшим "командным языком программирования" находиться в бета тестировании и имеет сомнительный функционал
<a id="creat_program_info"></a>
<details><summary>синтаксис и аргументы</summary><p>

## синтаксис:

### общий синтаксис команды:

  ```script
  /creat
  # создаем переменную
  var a=a
  # отправка переменных
  send a равно:{a}
  ```
  без отступов в начале!

комментарии обозначаться символом:`#`

для вставки переменной обверните ее название в фигурные скобки `{}`

### команды:

- send - отправка сообщений в чат (включено использование html форматирования) пример: `send hello world`
- var - создание переменных пример: `var a=1`

  - подробнее:

    ```script
    # создаем переменную
    var a=1
    # отправка переменных
    send a равно:{a}
    ```
    выход:`a равно:1`
- value - отправка всех переменных в формате словаря 
- calc - исполнение логических операций пример `calc a=1>0` доступные операторв:+, - , * , / , ** , % , == , != , < , <= , > , >=

  - подробнее:
   ```script
   var a=5
   var b=10

   calc out={a}<{b}
   
   send {out}
   ```
- .end - завершение программы 
- random - генерация случайного числа в указанном радиусе пример:`random a=1-5`
- timeout - задержка исполнения пример:`timeout 5`
- if - исполнение команды если условие верно пример: `if 1>0:send True` для запуска нескольких команд пишите их через `;`
- len - cщитает количество символов в строке/переменной пример:`len a=abv`
- list - альтернативный список отсчет видеться от 0 пример:`list a=1,2,3[1]`, так же можно присвоить данные по id элементу списка пример:`list a=1,2,3[1]=0`
- for - выполняет команды заданое количество раз считая от 0 при этом лжит цифру отсчета в переменную , для запуска нескольких команд пишите их через `;` пример:`for i in 5:send num:{i}`
- replace - замена синволоа или нескольких синволов в строке пример:`replace a=текст:старый текст/синвол,новый синвол`

### константы переменных:

- `$reply_to` - текст сообщения на которое был дан ответ командой `/creat` если ответа не было то в перемнной будет находиться `$none`
- `$pi` - математическая константа 'число π' до 10-го числ после запятой
- `$username` - username пользователя на че сообщение был дан ответ командой `/creat` если ответа не было то в перемнной будет находиться `$none`

### примеры простых программ:

> hello world

```senscript
/creat

send hello world
```

> игра рулетка 

```senscript
/creat

random rand=1-3
if {rand}==1:send ты выиграл
if {rand}==2:send ты проиграл, получиться в другой раз
if {rand}==3:send ты проиграл увы
```

</p></details>
</h4>


/data_base — выводит базу данных , аргумент: показывает данные отдельного пользователя пример:`/data_base 1234567890`

/ban — отправляет в бан пример: /бан reason:по рофлу

/мут — отправляет в мут /мут reason:причина time:1.h
 .h — часы (по умолчанию) , .d — дни , .m — минуты
 
/blaklist — добавляет стикер в черный список (стикеры находящиеся в черном списке автоматически удаляются)

/unblaklist — убирает стикер из черного списка

имеет логирывание сообщений и других событий

### установка:

для работы приложения необходим <a href="https://www.python.org/"> python 3.12v</a> или выше  

```sh
git clone https://github.com/xHak2215/admin_telegram_bot

cd admin_telegram_bot

pip install -r requirements.txt

python aea_bot.py
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

### Admin Bot with Spam Report Notifications  
To launch the bot, insert your token into the `TOKEN` file without any spaces or additional characters!  

### Description  
This bot detects spam and notifies chat administrators about it. It includes customizable anti-spam settings, punishment rules, and admin groups.  

It features multiple commands, such as:  

- `/help` — Help guide.  
- `/report` — Report a violation. To leave a comment, add a space after the command and write your comment.  
- `/monitor` — Track system metrics of your PC/hosting.  
- `/warn` — Decrease a user’s reputation by 1.  
- `/reput` — Increase a user’s reputation by 1.  
- `/info` — Get user information. Arguments: `-all` for a full info list.  
-  `/me` — Check your own reputation.  
- `/ban` — Ban a user with reason logging.  
- `/mute` — Temporarily mute a user with reason and duration.  
- `/admin_command` — Admin-only commands.  
- `/настройки` (`/settings`) — Display settings (from the `settings.json` config file). Use `-r` to reload settings without restarting the bot (e.g., `/настройки -r`).  
- `/t` — Translate text to Russian or another language (also supports encoding to binary, hex, and translit). Example: `/t any text:en`.  
- `/download` — Download stickers and voice messages. For symbols, specify the extension (e.g., `/download png`).  
- `/test` — Extensive bot system testing. Argument: `-all` for extra Telegram API details.  
- `/ping` — Check response latency for a URL. Arguments:  
  - `/ping <URL>` (default: `https://ya.ru`).  
  - `/ping <URL>,<number of requests>` — Repeat latency checks.  
  - `/ping <URL>,<requests>,<mode>` — `True` calculates average latency; default shows each attempt.  
- `/message_info` — Display message details (useful for media).  
- `/log` — Send log files.  
- `/serh` (`/search`) — Search Wikipedia articles (e.g., `/serh :<query>`). Article language depends on `settings.json` (`auto_translate: "lang"`). Argument: `-ping` to test `wikipedia.org` latency.  
- `/creat` — A simple scripting language for creating scripts.  
  <details><summary>Syntax and Arguments</summary><p>  

  ### Syntax:  
  #### General command syntax:  
  ```script  
  /creat  
  # Create a variable  
  var a=a  
  # Send variables  
  send a equals: {a}  
  ```  
  (No indentation at the start!)  

  Comments start with `#`.  
  To insert a variable, wrap its name in `{}`.  

  #### Commands:  
  - `send` — Send messages to chat (supports HTML formatting). Example: `send hello world`.  
  - `var` — Create variables. Example: `var a=1`.  
    ```script  
    var a=1  
    send a equals: {a}  
    ```  
    Output: `a equals: 1`.  
  - `value` — Output all variables as a dictionary.  
  - `calc` — Execute logical operations (e.g., `calc a=1>0`). Supported operators: `+`, `-`, `*`, `/`, `**`, `%`, `==`, `!=`, `<`, `<=`, `>`, `>=`.  
    ```script  
    var a=5  
    var b=10  
    calc out={a}<{b}  
    send {out}  
    ```  
  - `.end` — End the program.  
  - `random` — Generate a random number in a range (e.g., `random a=1-5`).  
  - `timeout` — Delay execution (e.g., `timeout 5`).  
  - `if` — Execute a command if a condition is met (e.g., `if 1>0:send True`). For multiple commands, separate them with `;`.  
  - `len` — Count characters in a string/variable (e.g., `len a=abc`).  
  - `list` — Alternative list (zero-indexed). Example: `list a=1,2,3[1]`. Assign values by ID: `list a=1,2,3[1]=0`.  
  - `for` — Run commands a set number of times (stores count in a variable). Example: `for i in 5:send num:{i}`.  
  - `replace` — Replace characters in a string (e.g., `replace a=text:old_char/new_char`).  

  #### Variable Constants:  
  - `$reply_to` — Text of the replied message (or `$none` if no reply).  
  - `$pi` — Math constant π (10 decimal places).  
  - `$username` — Username of the replied user (or `$none`).  

  #### Example Programs:  
  > Hello World  
  ```script  
  /creat  
  send hello world  
  ```  
  > Roulette Game  
  ```script  
  /creat  
  random rand=1-3  
  if {rand}==1:send You win!  
  if {rand}==2:send You lost. Try again!  
  if {rand}==3:send You lost. Better luck next time!  
  ```  
  </p></details>  

- `/data_base` — Display the database. Argument: Show data for a specific user (e.g., `/data_base 1234567890`).  
- `/ban` — Ban a user (e.g., `/ban reason:for trolling`).  
- `/мут` (`/mute`) — Mute a user (e.g., `/mute reason:reason time:1.h`).  
  - `.h` — Hours (default).  
  - `.d` — Days.  
  - `.m` — Minutes.  
- `/blaklist` (`/blacklist`) — Add a sticker to the blacklist (blacklisted stickers are auto-deleted).  
- `/unblaklist` (`/unblacklist`) — Remove a sticker from the blacklist.  
- Logs messages and other events.  

### Installation  
Requires [Python 3.12+](https://www.python.org/).  

```sh  
git clone https://github.com/xHak2215/admin_telegram_bot  
cd admin_telegram_bot  
pip install -r requirements.txt  
python aea_bot.py  
```  

### Configuration (`settings.json`)  
```json  
{  
    "bambam": false,  
    "delet_messadge": true,  
    "admin_grops": "-1001234567890",  
    "spam_limit": 10,  
    "spam_timer": 4,  
    "ban_and_myte_command": true,  
    "console_control": true,  
    "auto_translete": {"laung": "ru", "Activate": false}  
}  
```  

- `true` = enabled, `false` = disabled.  
- `bambam` — Auto-mute/ban.  
- `delet_messadge` — Auto-delete messages (e.g., after 5 reports).  
- `admin_grops` — Admin group ID.  
- `spam_limit` — Messages per user considered spam (within `spam_timer` seconds).  
- `spam_timer` — Time window for spam detection.  
- `ban_and_myte_command` — Enable `/ban` and `/mute`.  
- `console_control` — Allow remote terminal commands via `/console :<command>` (⚠️ risky if misused).  
- `auto_translete` — Auto-translate messages to `"laung"` (default: `"ru"`). Toggle with `"Activate"`.  

--- 


### Supported Formats  
#### Audio/Voice Messages:  
- `.mp3`, `.ogg`, `.m4a`, `.flac`, `.wav`, `.aac`, `.webm`, `.ac3`, `.wma`, `.mkv`.  

#### Stickers/Images:  
- `.BMP`, `.PNG`, `.JPEG`, `.GIF`, `.TIFF`, `.WebP`, `.PPM`, `.ICO`.  

---

Developed for [AEA+ Group](https://t.me/+P5wR2FyxnSQzMjIy) :3  


<h1><p align="right"><a href="#top">↑</a></p></h1>
