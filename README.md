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


<h3>бот адменистратор с оповешением о спаме репортах</h3>
<h3>для запуска бота вставите свой токен в файл TOKEN без пробелов или каких либо других символов!</h3>
<h3>описание</h3>
<h4>
Это бот с распознаванием спама и оповещением администраторов чата о нем.имеет настройки анти спама выдаваемых наказаний и группы администрации  <br>
Он имеет множество команд, например:<br>
/help - справка.<br>

/report — для оповещения о нарушении.<br>  

/monitor — для отслеживания системных показателей ПК/хостинга.<br>

/warn - снижение репутации.<br>

/reput - повышение репутации.<br>

/я - своя репутация.<br>

/бан - бан (блокировка) пользователя с сохранением причины.<br>

/мут - мут (временный запрет на отправление сообщений) пользователя с указанием причины и время.<br>

/настройки - отображает настройки(файл конфигурации `settings.json` ) имеет парамитер -r который перезагружает настройки если они были изменены без необходимости перезапуска бота пример :`/настройки -r`.<br>

/t - перевод сообщения на русский или другой язык (дополнительно потдерживает перевод в bin , hex и транслит кодеровки)пример:`/t любой текст:en`.<br>

/download - загруска стикеров и голосовых сообщений , при загруске синволов нужно указать расширение пример:`/download png`.

/ping - проверка задержки отклика по ссылке, аргументы:

- `/ping <ссылка>` для тестирования по умолчанию https://ya.ru 
- количество повторов замера задержки `/ping <ссылка>,<количество запросов>`
- режим расчета True - вычисление средни статисчической задержки из всех попыток. по умолчанию (не указывая значение) отоброжение зажержки каждой попытки `/ping <ссылка>,<количество запросов>,<режим>`.

/message_info - выводит информацию о сообщении полезно для медиа.<br>

/log - отправка файла логов. <br>

/serh - поиск статей на википедии пример: `serh :<promt>` ,язык статей зависит от настройки `settings.json` парамитра `auto_translete`:`laung` аргументы: `-ping` - проверка задержки сйта wikipedia.org. <br>

/creat - позволяет создавать скрипты является простейшим "командным языком программирования"
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
</p></details>
</h4>
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

Here’s the English translation while preserving the original meaning and structure:

---

## Information

### Admin Bot with Spam Report Alerts

**To launch the bot**, insert your token into the `TOKEN` file without spaces or any extra characters!  

### Description  
This bot detects spam and notifies chat administrators about it. It features customizable anti-spam settings, punishment systems, and admin group management.  

#### Available Commands:  
- `/help` — Help guide.  
- `/report` — Report a rule violation.  
- `/monitor` — Track system metrics of your PC/hosting.  
- `/warn` — Reduce a user’s reputation.  
- `/reput` — Increase a user’s reputation.  
- `/me` — Check your own reputation.  
- `/ban` — Ban (block) a user with reason logging.  
- `/mute` — Temporarily mute a user (prevent messaging) with reason and duration.  
- `/settings` — Display settings (from `settings.json`).  
  - Use `-r` to reload settings without restarting the bot (e.g., `/settings -r`).  
- `/t` — Translate text to Russian or other languages (supports binary, hex, and transliteration encoding).  
  - Example: `/t any text:en`.  
- `/download` — Download stickers/voice messages. Specify the extension (e.g., `/download png`).  
- `/ping` — Check latency to a URL. Arguments:  
  - `/ping <URL>` (default: `https://ya.ru`).  
  - `/ping <URL>,<number of requests>`.  
  - `/ping <URL>,<requests>,<mode>`:  
    - `True` = average latency (default: per-attempt results).  
- `/message_info` — Show message metadata (useful for media).  
- `/log` — Send log files.  
- `/search` — Find Wikipedia articles (e.g., `/search :<query>`).  
  - Language depends on `settings.json` (`auto_translate.laung`).  
  - Arguments: `-ping` — Test Wikipedia.org latency.  
- `/creat` — A simple scripting language for creating scripts.  
  <details><summary>Syntax and Arguments</summary>  

  #### Syntax:  
  
  ```script
  /creat
  # Create a variable
  var a=a
  # Send variables
  send a equals: {a}
  ```  
  - No indentation! Comments start with `#`.  
  - Variables are wrapped in `{}`.  

  #### Commands:  
  - `send` — Send messages (supports HTML formatting).  
  - `var` — Create variables (e.g., `var a=1`).  
  - `value` — Output all variables as a dictionary.  
  - `calc` — Execute math/logic operations (`+`, `-`, `*`, `/`, `**`, `%`, `==`, `!=`, `<`, `<=`, `>`, `>=`).  
  - `.end` — Terminate the program.  
  - `random` — Generate a random number (e.g., `random a=1-5`).  
  - `timeout` — Delay execution (e.g., `timeout 5`).  
  - `if` — Conditional execution (e.g., `if 1>0:send True`).  
  - `len` — Count characters in a string/variable (e.g., `len a=abc`).  
  - `list` — Array-like lists (zero-indexed; e.g., `list a=1,2,3[1]`).  
  - `for` — Loop (e.g., `for i in 5:send num:{i}`).  
  </details>  

The bot logs messages and events.  

---

### Installation  
Requires [Python 3.12+](https://www.python.org/).  

```sh
git clone https://github.com/xHak2215/admin_telegram_bot
cd admin_telegram_bot
pip install -r requirements.txt
python aea_bot.py
```

---

### Configuration/settings (`settings.json`)  

```json
{
  "bambam": false,
  "delete_message": true,
  "admin_groups": "-1001234567890",
  "spam_limit": 10,
  "spam_timer": 4,
  "ban_and_mute_command": true,
  "console_control": true,
  "auto_translate": {"laung": "ru", "Activate": false}
}
```

- **`true`/`false`**: Toggle features.  
- **`bambam`**: Auto-mute/ban.  
- **`delete_message`**: Auto-delete messages (e.g., after 5 reports).  
- **`admin_groups`**: Admin group ID.  
- **`spam_limit`**: Messages per user to trigger spam detection (within `spam_timer` seconds).  
- **`ban_and_mute_command`**: Enable `/ban` and `/mute`.  
- **`console_control`**: Remote terminal commands via `/console` (⚠️ **Risky!**).  
- **`auto_translate`**: Auto-translate messages to `laung` (default: `ru`).  

---

### Supported Formats  
#### Audio/Voice Messages:  
- `.mp3`, `.ogg`, `.m4a`, `.flac`, `.wav`, `.aac`, `.webm`, `.ac3`, `.wma`, `.mkv`.  

#### Stickers/Images:  
- `.BMP`, `.PNG`, `.JPEG`, `.GIF`, `.TIFF`, `.WebP`, `.PPM`, `.ICO`.  

---

Developed for [AEA+ Group](https://t.me/+P5wR2FyxnSQzMjIy) :3  


<h1><p align="right"><a href="#top">↑</a></p></h1>
