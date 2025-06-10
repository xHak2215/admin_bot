
<a id="readme-top"></a>

  <h3 align="center">Telegram бот админестратор</h3>



<details>
  <summary>автор</summary>
  <ol>
      <ul>
      <li><a href="https://t.me/HITHELL">telegram</a></li>
      </ul>
  </ol>
</details>


<h2>информация </h2>

<h3>бот адменистратор с оповешением о спаме репортах</h3>
<h3>описание</h3>
<h4>
Это бот с распознаванием спама и оповещением администраторов чата о нем.имеет настройки анти спама выдаваемых наказаний и группы администрации  <br>
Он имеет множество команд, например:<br>
/help - справка с командами.<br>

/report — для оповещения о нарушении.<br>  

/monitor — для отслеживания системных показателей ПК/хостинга.<br>

/warn - снижение репутации.<br>

/reput - повышение репутации.<br>

/я - своя репутация.<br>

/бан - бан (блокировка) пользователя с сохранением причины.<br>

/мут - мут (временный запрет на отправление сообщений) пользователя с указанием причины и время.<br>

/настройки - отображает настройки(файл конфигурации `settings.json` ) имеет парамитер -r который перезагружает настройки если они были изменены без необходимости перезапуска бота пример :`/настройки -r` <br>

/t (/translate)- перевод сообщения на русский <br>

/info - выводит информацию о пользователе (количество сообщений ,репутация  ) параметре -all выводит всю информацию<br>

имеет логирывание сообщений и других событий

</h4>

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
    "delet_messadge":false,
    "admin_grops":"-1002284704738",
    "spam_limit":10,
    "spam_timer":4,
    "ban_and_myte_command":true,
    "console_control":true

}
```
true - включено , false - выключено  
bambam - автоматичиские муты/баны<br>
delet_messadge - автоматическое удаление сообщений (в частности при 5 репортах на одном сообщении оно будет удаляться) так же включает кнопку "удалить спам" кнопка прикреплена к сообщению о спаме<br>
admin_grops - группа администрации (впишите ее ID)<br>
spam_limit - количество сообщений от одного пользователя которое будет считаться спамом (за отрезок времени указанный в spam_timer)<br>
spam_timer - функционал описан выше <br>
ban_and_myte_command - включает команды /бан и /мут для банов и мутов соотвецтвено <br>
console_control - разрешения удалённого запуска команд в терминале с помощью команды /console, синтаксис /console :<команда терминала> работает только в группе администрации администратором группы<br>

(⚠️данная команда может выполнять в том числе и вредоносные команды буте внимательны с ее включением)

бот сделан для группы <a href="https://t.me/+P5wR2FyxnSQzMjIy">AEA+</a> :3

<h3>eng</h3>
This is a bot designed to detect spam and notify chat administrators about it. It features customizable anti-spam settings, punishment systems, and admin group management.<br>
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

/config - displays the current settings (from the configuration file `settings.json` ), Parameter: -r - reloads the settings if they have been modified, eliminating the need to restart the bot using: `/config -r`<br>

/t -more translation of the Russian<br>

/info - displays user information (message count, reputation). The -all parameter shows complete information.<br>

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
    "delet_messadge":false,
    "admin_grops":"-1002284704738",
    "spam_limit":10,
    "spam_timer":4,
    "ban_and_myte_command":true,
    "console_control":true

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
(⚠️ This command can execute malicious commands as well—be cautious when enabling it.)

The bot was developed for the <a href="https://t.me/+P5wR2FyxnSQzMjIy">AEA+</a> chat :3
<h1><p align="right"><a href="#readme-top">↑</a></p></h1>
<h3><input type="button" name="↑" value="#readme-top"/></h3>










