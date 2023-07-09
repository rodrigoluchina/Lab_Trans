-- Criação da tabela "results"
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    km REAL,
    distance REAL,
    highway INTEGER,
    item TEXT
);

-- Criação da tabela "video"
CREATE TABLE IF NOT EXISTS video (
    name TEXT,
    km_ini REAL,
    km_final REAL,
    PRIMARY KEY (name)
);

-- Criação da tabela "rodovia"
CREATE TABLE IF NOT EXISTS rodovia (
    name TEXT,
    km_ini REAL,
    km_final REAL,
    PRIMARY KEY (name)
);

-- Criação da View "views" baseada na tabela "results"
CREATE VIEW IF NOT EXISTS views AS
SELECT highway, km, buraco, remendo, Trinca, placa, drenagem
FROM results;