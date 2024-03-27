all: install db run

install:
	echo "Installing dependencies"
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt

db:
	echo "Creating database"
	python3 db_setup.py 

run:
	echo "Running the app"
	python3 app.py