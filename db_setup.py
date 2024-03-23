import os
import pandas as pd
from queries import make_connection

def create_tables():
	engine = make_connection()
	tables = './tables/tables.sql'
	with engine.connect() as conn:
		with open(tables) as f:
			sql = f.read()
			conn.execute(sql)
	print("Tables created")


def insert_data():
	engine = make_connection()
	filenames = os.listdir('./tables/sql')
	with engine.connect() as conn:
		for file in filenames:
			table = file[:-4]
			if 'lap_times' in file:
				table = 'lap_times'
			print(f"""DROP TABLE IF EXISTS {table};""")
			# with open(f'./tables/sql/{file}') as f:
			# 	sql = f.read()
			# 	conn.execute(sql)

insert_data()