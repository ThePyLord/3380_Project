-- constructor_results table
CREATE TABLE constructor_results (
	"constructorResultsId"	INTEGER NOT NULL PRIMARY KEY,
	"raceId"	INTEGER NOT NULL REFERENCES races(raceId),
	"constructorId"	INTEGER NOT NULL REFERENCES constructors(constructorId),
	"points"	INTEGER NOT NULL,
	"status" varchar(max)
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
    "fp1_date"    varchar(max),
	"fp1_time"    varchar(max),
	"fp2_date"    varchar(max),
	"fp2_time"    varchar(max),
	"fp3_date"    varchar(max),
	"fp3_time"    varchar(max),
	"quali_date"  varchar(max),
	"quali_time"  varchar(max),
	"sprint_date" varchar(max),
	"sprint_time" varchar(max)
);

-- drivers table
CREATE TABLE drivers (
    "driverId"    INTEGER PRIMARY KEY,
    "driverRef"   varchar(max),
    "number"      INTEGER,
    "code"        varchar(max),
    "forename"    varchar(max),
    "surname"     varchar(max),
    "dob"         varchar(max),
    "nationality" varchar(max),
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
    "duration"     DECIMAL(6, 3),
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
    "q1"           varchar(max),
    "q2"           varchar(max),
    "q3"           varchar(max)
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
    "time"            varchar(max),
    "milliseconds"    INTEGER,
    "fastestLap"      INTEGER,
    "rank"            INTEGER,
    "fastestLapTime"  varchar(max),
    "fastestLapSpeed" varchar(max),
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
    "fastestLap"    varchar(max),
    "rank"          INTEGER,
    "fastestLapTime"  varchar(max),
    "statusId"      INTEGER REFERENCES status("statusId"),
    PRIMARY KEY ("resultId", "raceId", "driverId")
);