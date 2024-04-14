CREATE VIEW Minimal_Messung_Tape_View AS
SELECT m.LwcDenothMeter, t.RedVsWhite, t.AvgRadius
FROM Measurment m
JOIN Tape t ON m.id = t.Measurment_id;


CREATE VIEW Full_Measurement_View AS
SELECT mo.id AS place_id, mo.Name, mo.CoordinateN, mo.CoordinateE,
       mr.id AS MeasurmentSeries_id, mr.Date, mr.SnowType, mr.Temperatur, mr.Rainfall, mr.Humidity,
       m.id AS messung_id, m.lwcDenothMeter, m.dichte, m.tiefeUnterSchnee, m.bildname,
       t.id AS tape_id, t.RedVsWhite, t.radiusAvg, t.RadiusSD, t.XAxeAvg, t.XAxeSD, t.yAxesMittelwert, t.YAxeSD, t.Roundness
FROM Place mo
JOIN MeasurmentSeries mr ON mo.id = mr.Place_id
JOIN Measurment m ON mr.id = m.MeasurmentSeries_id
JOIN Tape t ON m.id = t.Measurment_id;
