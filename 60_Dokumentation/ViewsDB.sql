CREATE VIEW Minimal_Messung_Tape_View AS
SELECT m.lwcDenothMeter, t.rotVsWeiss, t.radiusMittelwert
FROM Messung m
JOIN Tape t ON m.id = t.messung_id;


CREATE VIEW Full_Measurement_View AS
SELECT mo.id AS messort_id, mo.nameOrt, mo.koordinateN, mo.koordinateE,
       mr.id AS messreihe_id, mr.datum, mr.schneeKategorie, mr.temperatur, mr.niederschlag, mr.luftfeuchtigkeit,
       m.id AS messung_id, m.lwcDenothMeter, m.dichte, m.tiefeUnterSchnee, m.bildname,
       t.id AS tape_id, t.rotVsWeiss, t.radiusMittelwert, t.radiusSD, t.xAxeMittelwert, t.xAxeSD, t.yAxesMittelwert, t.yAxeSD, t.rundheit
FROM MessOrt mo
JOIN MessReihe mr ON mo.id = mr.messOrt_id
JOIN Messung m ON mr.id = m.messReihe_id
JOIN Tape t ON m.id = t.messung_id;
