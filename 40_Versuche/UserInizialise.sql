CREATE USER RaspberryKamera WITH PASSWORD 'abscaaksd.tt33';
-- Grant insert and update permissions on specific tables
GRANT INSERT ON TABLE Kreis TO RaspberryKamera;
GRANT INSERT ON TABLE Messung TO RaspberryKamera;
GRANT INSERT ON TABLE Tape TO RaspberryKamera;


CREATE USER Feldversuch WITH PASSWORD 'bsacauxiaxbc222/';
-- Grant insert permissions on specific tables
GRANT INSERT ON TABLE Messung TO Feldversuch;
GRANT INSERT ON TABLE Messreihe TO Feldversuch;
GRANT INSERT ON TABLE Messort TO Feldversuch;

CREATE USER Analyst WITH PASSWORD 'rabgkkaadggg221!';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO Analyst;

CREATE USER admin WITH PASSWORD 'sgintyiijyj77(';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON SCHEMA public TO admin;
