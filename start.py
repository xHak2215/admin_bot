import os
import platform

if platform.platform().startswith('win'):
    os.system("start cmd python aea_bot2.py")
else:
    os.system("gnome-terminal -- virtual/bin/python aea_bot2.py")


