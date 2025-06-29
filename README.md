  <h3 align="center">Telegram бот админестратор</h3>



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

<h2>информация </h2>

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

/настройки - отображает настройки(файл конфигурации `settings.json` ) имеет парамитер -r который перезагружает настройки если они были изменены без необходимости перезапуска бота пример :`/настройки -r` <br>

/t - перевод сообщения на русский <br>

/download - загруска стикеров и голосовых сообщений , при загруске синволов нужно указать расширение пример:`/download png`


/ping - проверка задержки отклика по ссылке, аргументы: `/ping <ссылка>` для тестирования по умолчанию https://ya.ru ,количество повторов замера задержки `/ping <ссылка>,<количество запросов>` , режим расчета True - вычисление средни статисчической задержки из всех попыток. по умолчанию (не указывая значение) отоброжение зажержки каждой попытки `/ping <ссылка>,<количество запросов>,<режим>`

/message_info - выводит информацию о сообщении полезно для медиа
</h4>
имеет логирывание сообщений и других событий
<h3> установка: </h3>

для работы приложения необходим <a href="https://www.python.org/"> python 3.12v</a> или выше  

```sh
git clone https://github.com/xHak2215/admin_telegram_bot

cd admin_telegram_bot

pip install -r requirements.txt

python aea_bot.py
```

<h3> настройка: </h3>

```json
{
    "bambam":false,
    "delet_messadge":true,
    "admin_grops":"-1002428028295",
    "spam_limit":10,
    "spam_timer":4,
    "ban_and_myte_command":true,
    "console_control":true,
    "auto_translete":{"laung":"ru","Activate":false}

}
```
true - включено , false - выключено  
bambam - автоматичиские муты/баны<br>
delet_messadge - автоматическое удаление сообщений (в частности при 5 репортах на одном сообщении оно будет удаляться)<br>
admin_grops - группа администрации (впишите ее ID)<br>
spam_limit - количество сообщений от одного пользователя которое будет считаться спамом (за отрезок времени указанный в spam_timer)<br>
spam_timer - функционал описан выше <br>
ban_and_myte_command - включает команды /бан и /мут для банов и мутов соотвецтвено <br>
console_control - разрешения удалённого запуска команд в терминале с помощью команды /console, синтаксис /console :<команда терминала> работает только в группе администрации администратором группы<br>
(⚠️данная команда может выполнять в том числе и вредоносные команды буте внимательны с ее включением)<br>
auto_translet - авто перевод сообщений в чате с иностранного на указанный в `laung` по умолчанию `"laung":"ru"` параметр активации `Activate` по умолчанию `"Activate":false`<br>
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

---

<h3>eng</h3>
This is a bot designed to detect spam and notify chat administrators about it. It features customizable anti-spam settings, punishment systems, and admin group management.<br>
<h3>To launch the bot, insert your token into the TOKIN file without spaces or any others!</h3>
Key Functions:<br>
Spam detection with instant admin notifications<br>
Adjustable anti-spam thresholds and penalty settings<br>
Admin group hierarchy support<br>

Command List:<br>

/help - Displays help information<br>

/report - Reports rule violations<br>

/monitor - Tracks system metrics of PC/hosting<br>

/warn - Decreases user reputation<br>

/reput - Increases user reputation<br>

/me - Checks your own reputation<br>

/ban - Bans user with reason logging<br>

/mute - Temporarily mutes user with specified duration and reason<br>

/config - displays the current settings (from the configuration file `settings.json` ), Parameter: -r - reloads the settings if they have been modified, eliminating the need to restart the bot using: `/config -r`

/t -more translation of the Russian

/download - Download stickers and voice messages. When downloading symbols, you must specify the file extension, example: `/download png`

/ping - Check response latency for a URL. Arguments:  
• Basic: `/ping <URL>` (default test URL: https://ya.ru)  
• With attempts: `/ping <URL>,<number_of_requests>`  
• Calculation mode:  
  - `True`: Displays average statistical latency from all attempts  
  - Default (when not specified): Shows latency for each individual attempt  
Full format: `/ping <URL>,<number_of_requests>,<mode>`

/message_info - Displays message metadata (particularly useful for media analysis)

<h3>Installation:</h3>

To run the application, <a href="https://www.python.org/">Python 3.12</a> or higher is required.
```sh
git clone https://github.com/xHak2215/admin_telegram_bot

cd admin_telegram_bot

pip install -r requirements.txt

python aea_bot.py
```
<h3> settings: </h3>

```json
{
    "bambam":false,
    "delet_messadge":true,
    "admin_grops":"-1002428028295",
    "spam_limit":10,
    "spam_timer":4,
    "ban_and_myte_command":true,
    "console_control":true,
    "auto_translete":{"laung":"ru","Activate":false}

}
```
true - enabled, false - disabled  
bambam - automatic mutes/bans<br>
delet_messadge - automatic message deletion (specifically, a message will be deleted after 5 reports)<br>
admin_grops - admin group (enter its ID)<br>
spam_limit - number of messages from a single user that will be considered spam (within the time frame specified in spam_timer)<br>
spam_timer - functionality described above<br>
ban_and_myte_command - enables the /ban and /mute commands for bans and mutes, respectively<br>
console_control - permissions for remote execution of terminal commands via the /console command. Syntax: /console :<terminal command>. Works only in the admin group and can be used solely by the group administrator.<br>
(⚠️ This command can execute malicious commands as well—be cautious when enabling it.)<br>
auto_translate - Automatic chat message translation from foreign languages to the language specified in `laung` (default: `"laung":"ru"`). Activation parameter: `Activate` (default: `"Activate":false`).

Supported formats:
download voice messages and audio tracks:
- .mp3 (MPEG Audio Layer III)
- .ogg (Opus/Vorbis)
- .m4a (AAC в MP4-контейнере)
- .flac (Free Lossless Audio Codec)
- .wav (PCM/WAVE)
- .aac (Raw AAC-поток)
- .webm (Opus/Vorbis)
- .ac3 (Dolby Digital)
- .wma (Windows Media Audio)
- .mp4 (AAC/ALAC)
- .mkv (Любой кодек, включая FLAC)<br>

download sticker/photo:
- .BMP	BitMaP (без сжатия)	1, L, P, RGB, RGBA
- .PNG	Portable Network Graphics	L, LA, P, RGB, RGBA
- .JPEG	Joint Photographic Experts Group	L, RGB
- .GIF	Graphics Interchange Format	L, P
- .TIFF	Tagged Image File Format	L, LA, P, RGB, RGBA
- .WebP	Современный формат от Google	RGB, RGBA
- .PPM	Portable Pixmap	RGB
- .ICO	Иконки Windows	RGBA

The bot was developed for the <a href="https://t.me/+P5wR2FyxnSQzMjIy">AEA+</a> chat :3
<h1><p align="right"><a href="#readme-top">↑</a></p></h1>
<h3><input type="button" name="↑" value="#readme-top"/></h3>
