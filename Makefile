VENV = virtual
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

install:
	@echo "Creating virtual environment..."
	@python3 -m venv $(VENV)
	@echo "Installing requirements..."
	@$(PIP) install -r requirements.txt
	@echo "Done"

run:
	@echo "Running app..."
	@$(PYTHON) start.py

clean:
	@echo "Cleaning virtual environment..."
	@rm -rf $(VENV)
	@echo "Done"

.PHONY: install run clean
