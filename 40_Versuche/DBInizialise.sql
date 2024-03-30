CREATE DATABASE TapeMessungenBAKuhn;

CREATE TABLE MessOrt (
    id SERIAL PRIMARY KEY,
    nameOrt VARCHAR(255) NOT NULL,
    koordinateN FLOAT,
    koordinateE FLOAT
);

CREATE TABLE MessReihe (
    id SERIAL PRIMARY KEY,
    datum TIMESTAMP WITH TIME ZONE NOT NULL,
    schneeKategorie VARCHAR(255),
    temperatur FLOAT,
    niederschlag INT,
    luftfeuchtigkeit FLOAT,
    -- Foreign Key reference to MessOrt
    messOrt_id INT REFERENCES MessOrt(id)
);

CREATE TABLE Messung (
    id SERIAL PRIMARY KEY,
    lwcDenothMeter FLOAT,
    dichte FLOAT,
    tiefeUnterSchnee INT NOT NULL,
    bildname VARCHAR(255) NOT NULL,
    -- Foreign Key reference to MessReihe
    messReihe_id INT REFERENCES MessReihe(id)
);

CREATE TABLE Tape (
    id SERIAL PRIMARY KEY,
    rotVsWeiss FLOAT NOT NULL,
    radiusMittelwert FLOAT NOT NULL,
    radiusSD FLOAT NOT NULL,
    xAxeMittelwert FLOAT NOT NULL,
    xAxeSD FLOAT NOT NULL,
    yAxesMittelwert FLOAT NOT NULL,
    yAxeSD FLOAT NOT NULL,
    rundheit FLOAT NOT NULL,
    -- Foreign Key reference to Messung
    messung_id INT REFERENCES Messung(id)
);

CREATE TABLE Kreis (
    id SERIAL PRIMARY KEY,
    Radius FLOAT NOT NULL,
    xKooridnate INT NOT NULL,
    yKooridnate INT NOT NULL,
    -- Foreign Key reference to Tape
    tape_id INT REFERENCES Tape(id)
);
