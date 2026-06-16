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

def insert_reading(ph, tds, ce, temp):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO lecturas
        (ph,tds,ce,temperatura)

        VALUES (?,?,?,?)
    """,
    (ph,tds,ce,temp))

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