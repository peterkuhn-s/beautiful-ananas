INSERT INTO MessOrt (nameOrt, koordinateN, koordinateE)
VALUES ('Rothenthrm', 47.1, 8.683333);

INSERT INTO MessReihe (datum, schneeKategorie, temperatur, niederschlag, luftfeuchtigkeit, messort_id)
VALUES ('2024-03-10T15:02:08', 'schnee beregnte', 6, 2, 100, 1);


INSERT INTO Messung (lwcDenothMeter, dichte, tiefeUnterSchnee, bildname, messReihe_id)
VALUES (NULL, NULL, 30, 'bild1.jpg', 1);