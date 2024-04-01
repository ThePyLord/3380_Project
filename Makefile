all: create_env activate_env install_reqs db run

create_env:
	@echo "Setting up"
	python3 -m venv .venv

venv/bin/activate:
	chmod +x .venv/bin/activate
	. .venv/bin/activate
	pip install -r requirements.txt

activate_env: venv/bin/activate
	@echo "Activating environment"
	. .venv/bin/activate

install_reqs:
	pip install -r requirements.txt

db:
	@echo "Creating database"
	python3 db_setup.py 

run: activate_env
	@echo "Running the app"
	python3 app.py