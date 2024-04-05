all: create_env install_reqs db run

PYTHON = .venv/bin/python3
PIP = .venv/bin/pip

create_env:
	@echo "Setting up"
	python3 -m venv .venv

venv/bin/activate:
	chmod +x .venv/bin/activate
	. .venv/bin/activate
	#  pip install -r requirements.txt

activate_env: venv/bin/activate
	@echo "Activating environment"
	. .venv/bin/activate

install_reqs: activate_env
	$(PIP) install -r requirements.txt

db:
	@echo "Creating database"
	$(PYTHON) db_setup.py 

run: activate_env
	@echo "Running the app"
	$(PYTHON) app.py