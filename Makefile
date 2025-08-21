install:
        @echo "Run requirements install..."
        @python3 -m venv virtual
        @source virtual/bin/activate
        @virtual/bin/pip3 -r requirements.txt
        @echo "Done"

run:
        @echo "Run app..."
        @python3 aea_bot2.py
