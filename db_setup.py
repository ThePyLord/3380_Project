import os
import pyodbc
from queries import make_connection
from sqlalchemy.exc import SQLAlchemyError

table_order = ['drivers', 'circuits', 'races', 'constructors', 'constructor_standings', 'constructor_results',
                'driver_standings', 'lap_times', 'pit_stops', 'qualifying', 'status', 'results', 'seasons',
                'sprint_results']

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
    
    lap_times_index = table_order.index('lap_times')
    lap_times_inserts = sorted([file[:-4] for file in filenames if 'lap_times' in file])
    table_order.pop(lap_times_index)
    table_order.extend(lap_times_inserts)
    # print('Table order:', table_order)
    percent_complete = 0
    try:
        for table in table_order:
            with engine.begin() as conn:
                try:
                    db_conn = conn.connection
                    print(f"Inserting data into {table}")
                    with open(f'./tables/sql/{table}.sql', encoding='windows-1252') as f:
                        sql = f.read()
                        db_conn.execute(sql)
                        # for line in f:
                        #     sql = line.strip()
                        #     if sql:  # avoid executing empty lines
                        #         db_conn.execute(sql)
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
                    percent_complete += 1 // len(table_order) * 100
                    print(f'{percent_complete:.2f}% complete')
                except pyodbc.Error as e:
                    print(f"Error inserting data into {table}. SQL statement: {sql}")
                    db_conn.rollback()
                    print(e)
    except SQLAlchemyError as e:
        conn.rollback()
        print(e)
    print(f"{percent_complete:.2f}% complete. All data inserted.")


def clear_db():
    """
    Deletes all data from the database

    Return: 0
    """
    engine = make_connection()
    with engine.begin() as conn:
        db_conn = conn.connection
        for table in table_order:
            # Check if the table exists before deleting
            if db_conn.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table}'").fetchone()[0]:
                db_conn.execute(f"DELETE FROM {table}")
                print(f"Data deleted from {table}")
            else:
                print(f"{table} does not exist")
    print("Database cleared")
    return 0

if __name__ == '__main__':
    create_tables()
    insert_data()
    # clear_db()