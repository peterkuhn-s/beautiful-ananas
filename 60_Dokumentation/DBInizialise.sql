CREATE DATABASE TapeMessungenBAKuhn;

CREATE TABLE Place (
    id SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    CoordinateN FLOAT,
    CoordinateE FLOAT
);

CREATE TABLE MeasurmentSeries (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    SnowType VARCHAR(255),
    TemperaturAir FLOAT,
    Rainfall INT,
    Humidity FLOAT,
    -- Foreign Key reference to MessOrt
    Place_id INT REFERENCES Place(id)
);

CREATE TABLE Measumrment (
    id SERIAL PRIMARY KEY,
    LwcDenothMeter FLOAT,
    Density FLOAT,
    DepthBelowSurface INT NOT NULL,
    PhotoName VARCHAR(255) NOT NULL,
    AvgRedVsWhite FLOAT,
    AvgRadius FLOAT,
    -- Foreign Key reference to MessReihe
    MeasurmentSeries_id INT REFERENCES MeasurmentSeries(id)
);

CREATE TABLE Tape (
    id SERIAL PRIMARY KEY,
    RedVsWhite FLOAT NOT NULL,
    RadiusAvg FLOAT NOT NULL,
    RadiusSD FLOAT NOT NULL,
    XAxeAvg FLOAT NOT NULL,
    XAxeSD FLOAT NOT NULL,
    YAxesAvg FLOAT NOT NULL,
    YAxeSD FLOAT NOT NULL,
    Roundness FLOAT NOT NULL,
    -- Foreign Key reference to Messung
    Measurment_id INT REFERENCES Measurment(id)
);

CREATE TABLE Circle (
    id SERIAL PRIMARY KEY,
    Radius FLOAT NOT NULL,
    XCooridnate INT NOT NULL,
    YCooridnate INT NOT NULL,
    -- Foreign Key reference to Tape
    tape_id INT REFERENCES Tape(id)
);
