import pandas as pd
# import pyodbc
from sqlalchemy import create_engine
from config_load import config


def make_connection():
    SERVER = config["SERVER"]
    DATABASE = config["DATABASE"]
    USERNAME = config["USERNAME"]
    PASSWORD = config["PASSWORD"]
    try:
        # conn_url = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}"
        engine = create_engine(
            f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
        )
        return engine
    except Exception as e:
        print("Failed to connect")
        return None


def get_data(query):
    engine = make_connection()
    res = pd.read_sql(query, engine)
    return res


class Queries:
    def __init__(self):
        self.engine = make_connection()

    def get_data(self, query, params=None):
        res = pd.read_sql(query, self.engine, params=params)
        return res

    # @staticmethod
    def fastestLaps(self):
        query = """
        SELECT d.forename + ' ' + d.surname AS driver_name, COUNT(*) AS fastest_laps
        FROM results r
        JOIN drivers d ON r.driverId = d.driverId
        WHERE r.rank = 1
        GROUP BY d.forename, d.surname
        ORDER BY fastest_laps DESC;
        """
        return self.get_data(query)

    # @staticmethod
    def constructorPoints(self, year):
        query = f"""
        SELECT c.name, SUM(rs.points) AS Points
        FROM results rs
        JOIN constructors c ON rs.constructorId = c.constructorId
        JOIN races r ON rs.raceId = r.raceId
        WHERE r.year = {year}
        GROUP BY c.name
        ORDER BY Points DESC;
        """
        return self.get_data(query)
    
    # @staticmethod
    def driverPoints(self, year):
        query = f"""
        SELECT d.forename + ' ' + d.surname AS driver_name, SUM(rs.points) AS Points
        FROM results rs
        JOIN drivers d ON rs.driverId = d.driverId
        JOIN races r ON rs.raceId = r.raceId
        WHERE r.year = {year}
        GROUP BY d.forename, d.surname
        ORDER BY Points DESC;
        """
        return self.get_data(query)
