CREATE DATABASE IC_PLACAS_DB;

USE IC_PLACAS_DB;  

CREATE TABLE placas (
    id SERIAL PRIMARY KEY,
    placa VARCHAR(10) NOT NULL UNIQUE,
    descricao TEXT,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO placas (placa, descricao) VALUES ('ABC1D23', 'Arthur Bueno Vitola');

SELECT * FROM placas;
