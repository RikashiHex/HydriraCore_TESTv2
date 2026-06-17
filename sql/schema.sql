CREATE DATABASE IF NOT EXISTS water_monitor;

USE water_monitor;

-- =====================================
-- REFERENCIA DEL SISTEMA
-- =====================================

CREATE TABLE referencia_sistema (
    id INT AUTO_INCREMENT PRIMARY KEY,

    ph FLOAT NOT NULL,
    tds FLOAT NOT NULL,
    ce FLOAT NOT NULL,
    temperatura FLOAT NOT NULL,

    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO referencia_sistema
(
    ph,
    tds,
    ce,
    temperatura
)
VALUES
(
    7.0,
    120,
    250,
    25
);

-- =====================================
-- LOTES
-- =====================================

CREATE TABLE lotes (

    id INT AUTO_INCREMENT PRIMARY KEY,

    fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,

    fecha_fin DATETIME NULL,

    volumen_litros FLOAT NOT NULL,

    estado VARCHAR(20) DEFAULT 'ACTIVO',

    decision VARCHAR(20) DEFAULT NULL,

    observaciones TEXT,

    calidad_lote VARCHAR(20) NULL
);

-- =====================================
-- LECTURAS
-- =====================================

CREATE TABLE lecturas (

    id INT AUTO_INCREMENT PRIMARY KEY,

    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

    ph FLOAT NOT NULL,
    tds FLOAT NOT NULL,
    ce FLOAT NOT NULL,
    temperatura FLOAT NOT NULL,

    lote_id INT NULL,

    CONSTRAINT fk_lecturas_lotes
    FOREIGN KEY (lote_id)
    REFERENCES lotes(id)
    ON DELETE CASCADE
);

-- =====================================
-- CLASIFICACIONES
-- =====================================

CREATE TABLE clasificaciones (

    id INT AUTO_INCREMENT PRIMARY KEY,

    lectura_id INT NOT NULL,

    calidad VARCHAR(20) NOT NULL,

    confianza FLOAT NOT NULL,

    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_clasificaciones_lecturas
    FOREIGN KEY (lectura_id)
    REFERENCES lecturas(id)
    ON DELETE CASCADE
);

-- =====================================
-- ALERTAS
-- =====================================

CREATE TABLE alertas (

    id INT AUTO_INCREMENT PRIMARY KEY,

    lectura_id INT NOT NULL,

    tipo VARCHAR(50) NOT NULL,

    mensaje TEXT NOT NULL,

    gravedad VARCHAR(20) NOT NULL,

    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_alertas_lecturas
    FOREIGN KEY (lectura_id)
    REFERENCES lecturas(id)
    ON DELETE CASCADE
);

-- =====================================
-- ESTADO DEL FILTRO
-- =====================================

CREATE TABLE estado_filtro (

    id INT AUTO_INCREMENT PRIMARY KEY,

    lectura_id INT NOT NULL,

    vida_util FLOAT NOT NULL,

    score_desgaste FLOAT NOT NULL,

    observacion TEXT,

    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_estado_filtro_lecturas
    FOREIGN KEY (lectura_id)
    REFERENCES lecturas(id)
    ON DELETE CASCADE
);