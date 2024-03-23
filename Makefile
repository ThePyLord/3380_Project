all: install db run

install:
	echo "Installing dependencies"
	pip install -r requirements.txt

db:
	echo "Creating database"
	python3 db_setup.py 

run:
	echo "Running the app"
	python3 app.py