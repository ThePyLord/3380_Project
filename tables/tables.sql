-- drivers table
CREATE TABLE drivers (
    "driverId"    INTEGER PRIMARY KEY,
    "driverRef"   varchar(max),
    "number"      INTEGER,
    "code"        varchar(max),
    "forename"    varchar(max),
    "surname"     varchar(max),
    "dob"         DATE,
    "nationality" varchar(max),
);

CREATE TABLE circuits (
    "circuitId" INT PRIMARY KEY NOT NULL,
    "circuitRef" varchar(max),
    "name" varchar(max),
    "location" varchar(max),
    "country" varchar(max),
    "lat" NUMERIC(7, 5),
    "lng" NUMERIC(9, 6),
    "alt" varchar(max),
    "url" varchar(max),
);

-- races table
CREATE TABLE races (
    "raceId"      INTEGER PRIMARY KEY NOT NULL,
    "year"        INTEGER             NOT NULL,
    "round"       INTEGER             NOT NULL,
    "circuitId"   INTEGER             NOT NULL REFERENCES circuits(circuitId),
    "name"        varchar(max)        NOT NULL,
    "date"        varchar(max)        NOT NULL,
    "time"        varchar(max),
    "url"         varchar(max),
    "fp1_date"    DATE,
	"fp1_time"    varchar(max),
	"fp2_date"    DATE,
	"fp2_time"    varchar(max),
	"fp3_date"    DATE,
	"fp3_time"    varchar(max),
	"quali_date"  varchar(max),
	"quali_time"  varchar(max),
	"sprint_date" varchar(max),
	"sprint_time" varchar(max)
);

CREATE TABLE constructors (
    "constructorId" INT PRIMARY KEY NOT NULL,
    "constructorRef" varchar(max),
    "name" varchar(max),
    "nationality" varchar(max),
    "url" varchar(max)
);

-- constructor_standings table
CREATE TABLE constructor_standings (
	"constructorStandingsId" INTEGER NOT NULL PRIMARY KEY,
	"raceId"	INTEGER NOT NULL REFERENCES races(raceId),
	"constructorId"	INTEGER NOT NULL REFERENCES constructors(constructorId),
	"points"	INTEGER NOT NULL,
	"position"	INTEGER NOT NULL,
	"positionText"	VARCHAR(max) NOT NULL,
	"wins"	INTEGER NOT NULL
);

-- constructor_results table
CREATE TABLE constructor_results (
	"constructorResultsId"	INTEGER NOT NULL PRIMARY KEY,
	"raceId"	INTEGER NOT NULL REFERENCES races(raceId),
	"constructorId"	INTEGER NOT NULL REFERENCES constructors(constructorId),
	"points"	INTEGER NOT NULL,
	"status" varchar(max)
);

-- driver_standings table
CREATE TABLE driver_standings (
	"driverStandingsId"	INTEGER NOT NULL PRIMARY KEY,
	"raceId"	INTEGER NOT NULL REFERENCES races(raceId),
	"driverId"	INTEGER NOT NULL REFERENCES drivers(driverId),
	"points"	INTEGER NOT NULL,
	"position"	INTEGER NOT NULL,
	"positionText" varchar(max) NOT NULL,
	"wins"	INTEGER NOT NULL
);

-- lap_times table
CREATE TABLE lap_times (
    "lapTimeId"   INTEGER PRIMARY KEY IDENTITY (1,1),
    "raceId"       INTEGER NOT NULL REFERENCES races("raceId"),
    "driverId"     INTEGER NOT NULL REFERENCES drivers(driverId),
    "lap"          INTEGER NOT NULL,
    "position"     INTEGER,
    "time"         varchar(max),
    "milliseconds" INTEGER
);

-- pit_stops table
CREATE TABLE pit_stops (
    "raceId"       INTEGER NOT NULL REFERENCES races(raceId),
    "driverId"     INTEGER NOT NULL REFERENCES drivers(driverId),
    "stop"         INTEGER NOT NULL,
    "lap"          INTEGER NOT NULL,
    "time"         TIME,
    "duration"     varchar(max),
    "milliseconds" INTEGER,
    -- Added the stop column to the primary key to make it unique
    -- Might modify it if need be.
    PRIMARY KEY ("raceId", "driverId", "stop")
);

-- qualifying table
CREATE TABLE qualifying (
    "qualifyId" INTEGER PRIMARY KEY,
    "raceId"         INTEGER NOT NULL REFERENCES races(raceId),
    "driverId"       INTEGER NOT NULL REFERENCES drivers(driverId),
    "constructorId"  INTEGER NOT NULL REFERENCES constructors(constructorId),
    "number"       INTEGER,
    "position"     INTEGER,
    "q1"           TIME,
    "q2"           TIME,
    "q3"           TIME
);

-- status table
CREATE TABLE status (
	"statusId" INTEGER PRIMARY KEY,
	"status" varchar(max) NOT NULL
);

-- results table
CREATE TABLE results (
    "resultId"        INTEGER PRIMARY KEY,
    "raceId"          INTEGER REFERENCES races("raceId"),
    "driverId"        INTEGER REFERENCES drivers("driverId"),
    "constructorId"   INTEGER REFERENCES constructors("constructorId"),
    "number"          INTEGER,
    "grid"            INTEGER,
    "position"        INTEGER,
    "positionText"    varchar(max),
    "positionOrder"   INTEGER,
    "points"          INTEGER,
    "laps"            INTEGER,
    "time"            TIME,
    "milliseconds"    INTEGER,
    "fastestLap"      INTEGER,
    "rank"            INTEGER,
    "fastestLapTime"  TIME,
    "fastestLapSpeed" DECIMAL(7, 3),
    "statusId"        INTEGER REFERENCES status("statusId")
);

-- seasons table
CREATE TABLE seasons (
    "year" INTEGER NOT NULL PRIMARY KEY,
    "url" varchar(max) NOT NULL
);

-- sprint_results table
CREATE TABLE sprint_results (
    "resultId"      INTEGER REFERENCES results("resultId"),
    "raceId"        INTEGER REFERENCES races("raceId") ,
    "driverId"      INTEGER REFERENCES drivers("driverId"),
    "constructorId" INTEGER REFERENCES constructors("constructorId"),
    "number"        INTEGER,
    "grid"          INTEGER      NOT NULL,
    "position"      INTEGER      NOT NULL,
    "positionText"  varchar(max) NOT NULL,
    "positionOrder" INTEGER      NOT NULL,
    "points"        INTEGER      NOT NULL,
    "laps"          INTEGER      NOT NULL,
    "time"          varchar(max),
    "milliseconds"  INTEGER,
    "fastestLap"    INTEGER,
    "rank"          INTEGER,
    "fastestLapTime"  TIME,
    "statusId"      INTEGER REFERENCES status("statusId"),
    PRIMARY KEY ("resultId", "raceId", "driverId")
);