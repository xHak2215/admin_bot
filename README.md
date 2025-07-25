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

<details><summary>синтаксис и аргументы</summary><p>
<a id="creat_program_info"></a>
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
- list - альтернативный список отсчет видеться от 0 пример:`list a=1,2,3:1`
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

## Information

### Administrator Bot with Spam Report Notifications  

**To launch the bot, insert your token into the `TOKEN` file without spaces or any additional characters!**  

### Description

This is a bot with spam detection and notifications for chat administrators. It includes configurable anti-spam settings, punishment options, and admin groups.  

It has numerous commands, such as:

- `/help` — Help guide.  
- `/report` — Report a violation.  
- `/monitor` — Track system metrics of a PC/hosting.  
- `/warn` — Lower a user's reputation.  
- `/reput` — Increase a user's reputation.  
- `/me` — Check your own reputation.  
- `/ban` — Ban (block) a user while saving the reason.  
- `/mute` — Temporarily mute a user with a specified reason and duration.  
- `/settings` — Displays the configuration (from `settings.json`). The `-r` parameter reloads settings if they were modified without needing to restart the bot (e.g., `/settings -r`).  
- `/t` — Translate a message into Russian or another language (also supports encoding into binary, hex, and translit). Example: `/t any text:en`.  
- `/download` — Download stickers and voice messages. For symbols, specify the extension (e.g., `/download png`).  
- `/ping` — Check response latency for a URL. Arguments:  
  - `/ping <URL>` (default: `https://ya.ru`).  
  - `/ping <URL>,<number of requests>` — Number of latency checks.  
  - `/ping <URL>,<number of requests>,<mode>` — `True` calculates average latency; default shows each attempt.  
- `/message_info` — Displays message metadata (useful for media).  
- `/log` — Sends the log file.  
- `/search` — Searches for Wikipedia articles (e.g., `search:<query>`). Article language depends on `settings.json` (`auto_translate: "lang"`). Arguments: `-ping` checks latency of `wikipedia.org`.  

It also logs messages and other events.  

### Installation:

Requires [Python 3.12+](https://www.python.org/) or higher.  

```sh
git clone https://github.com/xHak2215/admin_telegram_bot  
cd admin_telegram_bot  
pip install -r requirements.txt  
python aea_bot.py  
```  

### Configuration:

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

- `true` = enabled, `false` = disabled.  
- `bambam` — Automatic mutes/bans.  
- `delete_message` — Auto-deletion of messages (e.g., if a message receives 5 reports, it will be deleted).  
- `admin_groups` — Admin group ID (insert yours).  
- `spam_limit` — Number of messages from one user considered spam (within the time set in `spam_timer`).  
- `spam_timer` — Timeframe for spam detection (see above).  
- `ban_and_mute_command` — Enables `/ban` and `/mute` commands.  
- `console_control` — Allows remote terminal command execution via `/console`. Syntax: `/console :<terminal command>`. Works only in the admin group by the group admin.  
⚠️ **This command can execute malicious code—use with caution!**  
- `auto_translate` — Auto-translates messages to the language specified in `"lang"` (default: `"ru"`). Activation parameter: `"Activate": false`.  

### Supported Formats:  

**Voice messages & audio tracks:**  

- `.mp3` (MPEG Audio Layer III)  
- `.ogg` (Opus/Vorbis)  
- `.m4a` (AAC in MP4 container)  
- `.flac` (Free Lossless Audio Codec)  
- `.wav` (PCM/WAVE)  
- `.aac` (Raw AAC stream)  
- `.webm` (Opus/Vorbis)  
- `.ac3` (Dolby Digital)  
- `.wma` (Windows Media Audio)  
- `.mkv` (Any codec, including FLAC)  

**Stickers/photos:**  

- `.BMP` — BitMaP (uncompressed)  
- `.PNG` — Portable Network Graphics  
- `.JPEG` — Joint Photographic Experts Group  
- `.GIF` — Graphics Interchange Format  
- `.TIFF` — Tagged Image File Format  
- `.WebP` — Google's modern format  
- `.PPM` — Portable Pixmap  
- `.ICO` — Windows Icons  

Bot created for the group [AEA+](https://t.me/+P5wR2FyxnSQzMjIy) :3  
<h1><p align="right"><a href="#top">↑</a></p></h1>
