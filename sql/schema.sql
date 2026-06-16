CREATE DATABASE IF NOT EXISTS water_monitor;

USE water_monitor;

CREATE TABLE lecturas (
    id INT AUTO_INCREMENT PRIMARY KEY,

    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

    ph FLOAT NOT NULL,

    tds FLOAT NOT NULL,

    ce FLOAT NOT NULL,

    temperatura FLOAT NOT NULL
);

CREATE TABLE clasificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,

    lectura_id INT,

    calidad VARCHAR(20),

    confianza FLOAT,

    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (lectura_id)
    REFERENCES lecturas(id)
);

CREATE TABLE alertas (
    id INT AUTO_INCREMENT PRIMARY KEY,

    lectura_id INT,

    tipo VARCHAR(50),

    mensaje TEXT,

    gravedad VARCHAR(20),

    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (lectura_id)
    REFERENCES lecturas(id)
);

CREATE TABLE estado_filtro (
    id INT AUTO_INCREMENT PRIMARY KEY,

    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

    vida_util FLOAT,

    score_desgaste FLOAT,

    observacion TEXT
);

CREATE TABLE referencia_sistema (
    id INT AUTO_INCREMENT PRIMARY KEY,

    ph FLOAT,

    tds FLOAT,

    ce FLOAT,

    temperatura FLOAT,

    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
);