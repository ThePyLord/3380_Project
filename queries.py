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
    
    def polePositions(self):
        query = """
        SELECT Drivers.driverId, (Drivers.forename + ' ' + Drivers.surname) AS name, COUNT(Results.grid) AS PolePositions
        FROM Results
        JOIN Drivers ON Results.driverId = Drivers.driverId
        WHERE Results.grid = 1
        GROUP BY Drivers.driverId, Drivers.forename, Drivers.surname
        ORDER BY PolePositions DESC;
        """
        return self.get_data(query)

    def averagePitStopDurationByCircuit(self):
        query = """
        SELECT c.name, AVG(p.duration) AS AvgPitStopDuration
        FROM pit_stops p
        JOIN races r2 ON p.raceId = r2.raceId
        JOIN circuits c ON r2.circuitId = c.circuitId
        GROUP BY c.name
        ORDER BY AvgPitStopDuration DESC;
        """
        return self.get_data(query)

    def averagePitStopDurationByConstructor(self):
        query = """
        SELECT co.name, AVG(ps.duration) AS average_pit_stop_time
        FROM pit_stops ps
        JOIN results rs ON ps.raceId = rs.raceId AND ps.driverId = rs.driverId
        JOIN constructors co ON rs.constructorId = co.constructorId
        GROUP BY co.name
        ORDER BY average_pit_stop_time ASC;
        """
        return self.get_data(query)

    def fastestQualifyingTimesByCircuit(self):
        query = """
        SELECT ci.name AS circuit_name, r.year, q.driverId, MIN(q.qualifyingTime) AS fastest_qualifying_time
        FROM qualifying q
        JOIN races r ON q.raceId = r.raceId
        JOIN circuits ci ON r.circuitId = ci.circuitId
        GROUP BY circuit_name, r.year
        ORDER BY circuit_name, fastest_qualifying_time ASC;
        """
        return self.get_data(query)

    def mostSuccessfulDriversAtEachCircuit(self):
        query = """
        SELECT ci.name AS circuit_name, dr.driverRef, COUNT(*) AS wins
        FROM results rs
        JOIN races r ON rs.raceId = r.raceId
        JOIN circuits ci ON r.circuitId = ci.circuitId
        JOIN drivers dr ON rs.driverId = dr.driverId
        WHERE rs.position = 1
        GROUP BY circuit_name, dr.driverRef
        ORDER BY wins DESC;
        """
        return self.get_data(query)

    def driverStandingsOverTime(self, forename, surname):
        query = f"""
        SELECT r.year, r.round, dr.driverRef, rs.position
        FROM results rs
        JOIN races r ON rs.raceId = r.raceId
        JOIN drivers dr ON rs.driverId = dr.driverId
        WHERE dr.forename = '{forename}' AND dr.surname = '{surname}'
        ORDER BY r.year, r.round;
        """
        return self.get_data(query)

    def compareConstructorPerformance(self, constructor1, constructor2):
        query = f"""
        SELECT r.year, co.constructorRef, SUM(cr.points) AS total_points
        FROM constructor_results cr
        JOIN races r ON cr.raceId = r.raceId
        JOIN constructors co ON cr.constructorId = co.constructorId
        WHERE co.constructorRef IN ('{constructor1}', '{constructor2}')
        GROUP BY r.year, co.constructorRef
        ORDER BY r.year, total_points DESC;
        """
        return self.get_data(query)