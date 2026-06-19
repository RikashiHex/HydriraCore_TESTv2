import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from app import app
from database import get_connection


@app.route("/api/latest")
def latest():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            ph,
            tds,
            ce,
            temperatura,
            fecha
        FROM lecturas
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "id": row[0],
        "ph": row[1],
        "tds": row[2],
        "ce": row[3],
        "temperatura": row[4],
        "fecha": str(row[5])
    }


@app.route("/api/dashboard")
def dashboard():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT
            ph,
            tds,
            ce,
            temperatura,
            fecha
        FROM lecturas
        ORDER BY id DESC
        LIMIT 1
    """)

    reading = cur.fetchone()

    cur.execute("""
        SELECT calidad
        FROM clasificaciones
        ORDER BY id DESC
        LIMIT 1
    """)

    classification = cur.fetchone()

    cur.execute("""
        SELECT
            vida_util,
            score_desgaste
        FROM estado_filtro
        ORDER BY id DESC
        LIMIT 1
    """)

    filter_state = cur.fetchone()

    cur.execute("""
        SELECT id
        FROM lotes
        WHERE estado='ACTIVO'
        LIMIT 1
    """)

    lot = cur.fetchone()

    cur.close()
    conn.close()
        
    return {

        "ph": reading[0],
        "tds": reading[1],
        "ce": reading[2],
        "temperatura": reading[3],

        "calidad": classification[0],

        "vida_util": filter_state[0],
        "score_desgaste": filter_state[1],

        "lote_actual": lot[0],
        "fecha": str(reading[4])
    }


@app.route("/api/fulldata")
def fulldata():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""SELECT * FROM lecturas ORDER BY id ASC""")
    data = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "lecturas": [
            {
                "1-id": row[0],
                "2-fecha": row[1],
                "3-ph": row[2],
                "4-tds": row[3],
                "5-ce": row[4],
                "6-temperatura": row[5],
                "7-lote_id": row[6]
            }
            for row in data
        ]
    }

@app.route("/api/fullalerts")
def fullalerts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""SELECT * FROM alertas ORDER BY id ASC""")
    data = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "reportes": [
            {
                "1-id": row[0],
                "2-lectura_id": row[1],
                "3-tipo": row[2],
                "4-mensaje": row[3],
                "5-gravedad": row[4],
                "6-fecha": str(row[5])
            }
            for row in data
        ]
    }