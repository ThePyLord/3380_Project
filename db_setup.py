import os

import pyodbc
import pandas as pd
from queries import make_connection
from sqlalchemy.exc import SQLAlchemyError


def create_tables():
    engine = make_connection()
    tables = './tables/tables.sql'
    with engine.begin() as conn:
        db_conn = conn.connection
        with open(tables) as f:
            sql = f.read()
            db_conn.execute(sql)
    print("Tables created")


def insert_data():
    engine = make_connection()
    filenames = os.listdir('./tables/sql')
    # Sort the filenames into the order defined in the tables.sql fil
    table_order = ['drivers', 'circuits', 'races', 'constructors', 'constructor_standings', 'constructor_results',
                   'driver_standings', 'lap_times', 'pit_stops', 'qualifying', 'status', 'results', 'seasons',
                   'sprint_results']
    lap_times_index = table_order.index('lap_times')
    lap_times_inserts = sorted([file[:-4] for file in filenames if 'lap_times' in file])
    table_order.pop(lap_times_index)
    table_order.extend(lap_times_inserts)
    # print('Table order:', table_order)

    try:
        with engine.begin() as conn:
            db_conn = conn.connection
            for table in table_order:
                try:
                    print(f"Inserting data into {table}")
                    with open(f'./tables/sql/{table}.sql', encoding='windows-1252') as f:
                        for line in f:
                            sql = line.strip()
                            if sql:  # avoid executing empty lines
                                db_conn.execute(sql)
                            # table_schema = f"""
                            # 				SELECT COLUMN_NAME, DATA_TYPE
                            # 				FROM INFORMATION_SCHEMA.COLUMNS
                            # 				WHERE TABLE_NAME='{table}';"""
                            # Use pandas to read the table schema
                            # table_schema = pd.read_sql(table_schema, conn)
                            # print(table_schema)
                            # Check for TIME, NUMERIC, DECIMAL and DATETIME data types
                            # if 'TIME' in table_schema['DATA_TYPE'].values:
                            # 	# Convert the time data type using pd.to_datetime

                    print(f"Data inserted into {table}")
                except pyodbc.Error as e:
                    print(f"Error inserting data into {table}. SQL statement: {sql}")
                    print(e)
    except SQLAlchemyError as e:
        conn.rollback()
        print(e)
    print("Data inserted")


if __name__ == '__main__':
    create_tables()
    # insert_data()
