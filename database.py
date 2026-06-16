import mariadb
from config.config import *

def get_connection():

    return mariadb.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='12345678',
        database='water_monitor'
    )

def insert_reading(
    lot_id,
    ph,
    tds,
    ce,
    temp
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO lecturas
        (
            lote_id,
            ph,
            tds,
            ce,
            temperatura
        )
        VALUES
        (
            ?,
            ?,
            ?,
            ?,
            ?
        )
    """,
    (
        lot_id,
        ph,
        tds,
        ce,
        temp
    ))

    conn.commit()

    reading_id = cur.lastrowid

    cur.close()
    conn.close()

    return reading_id


def save_classification(
    reading_id,
    quality,
    confidence
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO clasificaciones
        (
            lectura_id,
            calidad,
            confianza
        )
        VALUES
        (
            ?,
            ?,
            ?
        )
    """,
    (
        reading_id,
        quality,
        confidence
    ))

    conn.commit()

    cur.close()
    conn.close()


def get_reference():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT
            ph,
            tds,
            ce,
            temperatura
        FROM referencia_sistema
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    return row

def save_alert(
    reading_id,
    alert
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO alertas
        (
            lectura_id,
            tipo,
            mensaje,
            gravedad
        )
        VALUES
        (
            ?,
            'ANOMALIA',
            ?,
            'ALTA'
        )
    """,
    (
        reading_id,
        alert
    ))

    conn.commit()

    cur.close()
    conn.close()

def create_lot(volume):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO lotes
        (
            volumen_litros
        )
        VALUES
        (
            ?
        )
    """,
    (volume,)
    )

    conn.commit()

    lot_id = cur.lastrowid

    cur.close()
    conn.close()

    return lot_id


def close_lot(
    lot_id,
    decision,
    observations=""
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        UPDATE lotes
        SET
            fecha_fin = NOW(),
            estado = 'FINALIZADO',
            decision = ?,
            observaciones = ?
        WHERE id = ?
    """,
    (
        decision,
        observations,
        lot_id
    ))

    conn.commit()

    cur.close()
    conn.close()



def get_lot_stats(lot_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT
            AVG(ph),
            AVG(tds),
            AVG(ce),
            COUNT(*)
        FROM lecturas
        WHERE lote_id = ?
    """,
    (lot_id,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "avg_ph": row[0],
        "avg_tds": row[1],
        "avg_ce": row[2],
        "samples": row[3]
    }


def save_filter_state(
    lectura_id,
    vida_util,
    score_desgaste,
    observacion=""
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO estado_filtro
        (
            lectura_id,
            vida_util,
            score_desgaste,
            observacion
        )
        VALUES
        (
            ?,
            ?,
            ?,
            ?
        )
    """,
    (
        lectura_id,
        vida_util,
        score_desgaste,
        observacion
    ))

    conn.commit()

    cur.close()
    conn.close()

def get_last_filter_health():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT vida_util
        FROM estado_filtro
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return row[0]

    return 100.0