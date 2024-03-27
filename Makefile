all: install activate_env db run

install:
	echo "Setting up"
	python3 -m venv .venv

activate_env:
	echo "Activating environment"
	source .venv/bin/activate
	pip install -r requirements.txt

db:
	echo "Creating database"
	python3 db_setup.py 

run: activate_env
	echo "Running the app"
	python3 app.py