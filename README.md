
<a id="readme-top"></a>





<!-- PROJECT LOGO -->


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






<!-- consolSH -->
<h2>информация </h2>

<h3>бот адменистратор с оповешением о спаме репортах
</h3>
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
    "admin_grops":"-1001234000000",
    "spam_limit":10,
    "spam_timer":4,
    "ban_and_myte_command":true

}
```
bambam - автоматичиские муты/баны<br>
delet_messadge - автоматическое удаление сообщений (в частности при 5 репортах на одном сообщении оно будет удаляться)<br>
admin_grops - группа администрации (впишите ее ID)<br>
spam_limit - количество сообщений от одного пользователя которое будет считаться спамом (за отрезок времени указанный в spam_timer)<br>
spam_timer - функционал описан выше <br>
ban_and_myte_command - включает команды /бан и / мут для банов и мутов соотвецтвено <br>

бот сделан для группы <a href="https://t.me/+P5wR2FyxnSQzMjIy">AEA+</a> :3

<p align="right">(<a href="#readme-top">↑верх↑</a>)</p>

<input type="button" name="↑верх↑" value="#readme-top"/>










