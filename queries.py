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
            return self.get_data(query, params=(f"{name}%",))

    def years(self):
        query = """
		SELECT DISTINCT r.year
		FROM races r
		JOIN lap_times lt ON r.raceId = lt.raceId
		ORDER BY r.year;
		"""
        return self.get_data(query)

    def constructors(self, name=None):
        query = """
		SELECT DISTINCT c.name AS constructor, c.constructorRef
		FROM constructor_standings cs 
		JOIN constructors c ON cs.constructorId = c.constructorId"""
        if name is not None:
            query += " WHERE c.name LIKE ?;"
            return self.get_data(query, params=(f"{name}%",))
        else:
            query += ";"
            return self.get_data(query)

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
		SELECT 
			dr.driverId, 
			(dr.forename + ' ' + dr.surname) AS "Driver Name", 
			COUNT(Results.grid) AS PolePositions
		FROM Results
		JOIN Drivers dr ON Results.driverId = dr.driverId
		WHERE Results.grid = 1
		GROUP BY dr.driverId, dr.forename, dr.surname
		ORDER BY PolePositions DESC;
		"""
        return self.get_data(query)

    def averagePitStopDurationByCircuit(self):
        # TODO: Update query to convert milliseconds to seconds
        query = """
		SELECT 
			c.name, 
			AVG(p.milliseconds) /1000 AS AvgPitStopDuration
		FROM pit_stops p
		JOIN races r2 ON p.raceId = r2.raceId
		JOIN circuits c ON r2.circuitId = c.circuitId
		GROUP BY c.name
		ORDER BY AvgPitStopDuration DESC;
		"""
        return self.get_data(query)

    def averagePitStopDurationByConstructor(self):
        query = """
		SELECT 
			co.name, AVG(ps.milliseconds) AS average_pit_stop_time
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
		WHERE q.q1 < 300 OR q.q2 < 300 OR q.q3 < 300
		GROUP BY ci.name, r.year, d.driverId
		ORDER BY circuit_name, r.year, fastest_qualifying_time;
		"""
        return self.get_data(query)

    def mostSuccessfulDriversAtEachCircuit(self):
        query = """
		SELECT 
			ci.name AS circuit_name, 
			dr.driverRef, 
			COUNT(*) AS wins
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
		GROUP BY r.year, r.round, dr.driverRef, rs.position
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
			WHERE co.name IN (?, ?)
			GROUP BY r.year
			HAVING COUNT(DISTINCT co.constructorRef) = 2
		)
		SELECT r.year, co.constructorRef AS "constructor", SUM(cr.points) AS total_points
		FROM constructor_results cr
		JOIN races r ON cr.raceId = r.raceId
		JOIN constructors co ON cr.constructorId = co.constructorId
		JOIN CompetedYears cy ON r.year = cy.year
		WHERE co.name IN (?, ?)
		GROUP BY r.year, co.constructorRef
		ORDER BY r.year, total_points DESC;
		"""
        # Repeat the constructor names in the same order to match the CTE and main query
        params = (constructor1, constructor2) * 2

        return self.get_data(query, params=params)

    def causes_of_retirements(self):
        query = """
		SELECT c.name AS circuit, COUNT(*) AS retirements
		FROM results r
		JOIN status s ON r.statusId = s.statusId
		JOIN races rc ON r.raceId = rc.raceId
		JOIN circuits c ON rc.circuitId = c.circuitId
		WHERE s.status = 'Retired'
		GROUP BY c.name
		ORDER BY retirements DESC;
		"""
        return self.get_data(query)

    def sprint_results(self):
        query = """
		SELECT
			(d.forename + ' ' +
			d.surname) AS name,
			COUNT(*) AS wins
		FROM sprint_results sr
		JOIN drivers d ON sr.driverId = d.driverId
		WHERE sr.position = 1
		GROUP BY d.forename, d.surname
		ORDER BY wins DESC;
		"""
        return self.get_data(query)

    def lap_time_progression(self, race_year, race_name, driver_name):
        query = """
		SELECT lap_times.lap AS lap, (lap_times.milliseconds / 1000) AS time
		FROM lap_times
		JOIN races ON lap_times.raceId = races.raceId
		JOIN drivers ON lap_times.driverId = drivers.driverId
		WHERE races.year = ? AND races.name = ? AND drivers.forename + ' ' + drivers.surname = ?
		ORDER BY lap_times.lap;
		"""
        return self.get_data(query, params=(race_year, race_name, f'{driver_name}'))

    def co_competitors(self, constructor: str):
        """Returns a dataframe of constructors that have competed in the same years as the input constructor.
		
		constructor -- The constructor of interest.
		Return: The dataframe of constructors that have competed in the same years as the input constructor.
		"""
        query = """
		WITH GivenConstructorSeasons AS (
			SELECT r.year
			FROM constructor_results cr
			JOIN races r ON cr.raceId = r.raceId
			JOIN constructors co ON cr.constructorId = co.constructorId
			WHERE co.name = ?
			GROUP BY r.year
		)
		SELECT co.constructorId, co.name AS constructor, co.constructorRef, COUNT(DISTINCT r.year) AS seasons
		FROM constructor_results cr
		JOIN races r ON cr.raceId = r.raceId
		JOIN constructors co ON cr.constructorId = co.constructorId
		JOIN GivenConstructorSeasons gcs ON r.year = gcs.year
		WHERE co.name != ?
		GROUP BY co.constructorRef, co.constructorId, co.name
		HAVING COUNT(DISTINCT r.year) >= 2;
		"""
        return self.get_data(query, params=(constructor, constructor))

    def grand_prixs(self, year):
        query = """
		SELECT name, year, raceId
		FROM races
		WHERE year = ?
		"""

        return self.get_data(query, params=(year,))

    def drivers_at_gp(self, year, name):
        query = """
		SELECT d.driverRef AS driver_name, d.forename + ' ' + d.surname AS driverName
		FROM races r
		JOIN results res ON r.raceId = res.raceId
		JOIN drivers d ON res.driverId = d.driverId
		WHERE r.year = ? AND r.name = ?
		ORDER BY res.grid;
		"""
        return self.get_data(query, params=(year, name))

# def pole_v_finish(self, driver):
# 	query = """
# 	SELECT r.year, r.round, r.name, r.date, r.time, r.url, rs.grid, rs.position
# 	FROM results rs
# 	JOIN drivers d ON rs.driverId = d.driverId
