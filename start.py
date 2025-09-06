import os
import platform

if platform.platform().startswith('win'):
    os.system("start cmd python aea_bot2.py")
    os.system("start cmd python asets/user_bot.py")
else:
    os.system("gnome-terminal -- virtual/bin/python aea_bot2.py")
    os.system("gnome-terminal -- virtual/bin/python asets/user_bot.py")


