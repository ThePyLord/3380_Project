import pandas as pd
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


class Queries:
    def __init__(self):
        self.engine = make_connection()

    def get_data(self, query, params=None):
        res = pd.read_sql(query, self.engine, params=params)
        return res

    def circuits(self, name=None):
        if name is None:
            query = """
			SELECT circuitRef AS refName, 
				name, 
				location, 
				country, 
				lat, lng, 
				alt AS elevation 
			FROM circuits;"""
            return self.get_data(query)
        else:
            query = """
			SELECT circuitRef AS refName, 
				name, 
				location, 
				country, 
				lat, lng, 
				alt AS elevation
			FROM circuits
			WHERE circuitRef LIKE ? OR name LIKE ?;"""
            return self.get_data(query, params=(f'{name}%',))	

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

    def constructorPoints(self, year):
        query = """
		SELECT c.name AS "Constructor Name", SUM(rs.points) AS Points
		FROM results rs
		JOIN constructors c ON rs.constructorId = c.constructorId
		JOIN races r ON rs.raceId = r.raceId
		WHERE r.year = ?
		GROUP BY c.name
		HAVING SUM(rs.points) > 0
		ORDER BY Points DESC;
		"""
        return self.get_data(query, params=(year,))

    def driverPoints(self, year):
        query = f"""
		SELECT d.forename + ' ' + d.surname AS "Driver Name", SUM(rs.points) AS Points
		FROM results rs
		JOIN drivers d ON rs.driverId = d.driverId
		JOIN races r ON rs.raceId = r.raceId
		WHERE r.year = ? 
		GROUP BY d.forename, d.surname
		HAVING SUM(rs.points) > 0
		ORDER BY Points DESC;
		"""
        return self.get_data(query, params=(year,))

    def polePositions(self):
        query = """
		SELECT Drivers.driverId, (Drivers.forename + ' ' + Drivers.surname) AS "Driver Name", COUNT(Results.grid) AS PolePositions
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
		SELECT co.name, AVG(ps.milliseconds) AS average_pit_stop_time
		FROM pit_stops ps
		JOIN results rs ON ps.raceId = rs.raceId AND ps.driverId = rs.driverId
		JOIN constructors co ON rs.constructorId = co.constructorId
		GROUP BY co.name
		ORDER BY average_pit_stop_time ASC;
		"""
        return self.get_data(query)

    def fastestQualifyingTimesByCircuit(self, circuit = None):
        query = """
		SELECT
			ci.name AS circuit_name,
			r.year,
			d.driverId,
			MIN(COALESCE(q.q3, q.q2, q.q1)) AS fastest_qualifying_time
		FROM qualifying q
		JOIN races r ON q.raceId = r.raceId
		JOIN circuits ci ON r.circuitId = ci.circuitId
		JOIN drivers d ON q.driverId = d.driverId
		GROUP BY ci.name, r.year, d.driverId
		ORDER BY circuit_name, r.year, fastest_qualifying_time;
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
        query = """
		SELECT r.year, r.round, dr.driverRef, rs.position
		FROM results rs
		JOIN races r ON rs.raceId = r.raceId
		JOIN drivers dr ON rs.driverId = dr.driverId
		WHERE dr.forename LIKE ? OR dr.surname LIKE ?
		ORDER BY r.year, r.round;
		"""
        return self.get_data(query, params=(f'{forename}%',f'{surname}%',))

    def compareConstructorPerformance(self, constructor1, constructor2):
        query = """
		WITH CompetedYears AS (
			SELECT r.year
			FROM constructor_results cr
			JOIN races r ON cr.raceId = r.raceId
			JOIN constructors co ON cr.constructorId = co.constructorId
			WHERE co.constructorRef IN (?, ?)
			GROUP BY r.year
			HAVING COUNT(DISTINCT co.constructorRef) = 2
    	)
		SELECT r.year, co.constructorRef AS "constructor", SUM(cr.points) AS total_points
		FROM constructor_results cr
		JOIN races r ON cr.raceId = r.raceId
		JOIN constructors co ON cr.constructorId = co.constructorId
        JOIN CompetedYears cy ON r.year = cy.year
		WHERE co.constructorRef IN (?, ?)
		GROUP BY r.year, co.constructorRef
		ORDER BY r.year, total_points DESC;
		"""
        # Repeat the constructor names in the same order to match the CTE and main query
        params = (constructor1, constructor2) * 2
        return self.get_data(query, params=params)


# def pole_v_finish(self, driver):
# 	query = """
# 	SELECT r.year, r.round, r.name, r.date, r.time, r.url, rs.grid, rs.position
# 	FROM results rs
# 	JOIN drivers d ON rs.driverId = d.driverId
