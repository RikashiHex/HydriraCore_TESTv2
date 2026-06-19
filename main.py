import time

from simulator import read_data

from database import (
    create_lot,
    close_lot,
    get_lot_stats,
    insert_reading,
    get_reference,
    save_alert,
    save_classification,
    save_filter_state,
    get_last_filter_health
)

from classifier import classify
from filter_health import calculate_filter_health
from anomaly_detector import detect_anomaly


# =====================================================
# INICIO DEL SISTEMA
# =====================================================

lot_id = create_lot(50)

reading_counter = 0

while True:

    # =================================================
    # OBTENER DATOS DEL SENSOR / SIMULADOR
    # =================================================

    data = read_data()

    if not data:
        continue

    # =================================================
    # GUARDAR LECTURA
    # =================================================

    reading_id = insert_reading(
        lot_id,
        data["ph"],
        data["tds"],
        data["ce"],
        data["temp"]
    )

    # =================================================
    # CLASIFICAR CALIDAD DEL AGUA
    # =================================================

    quality, confidence = classify(
        data["ph"],
        data["tds"],
        data["ce"]
    )

    save_classification(
        reading_id,
        quality,
        confidence
    )

    # =================================================
    # OBTENER REFERENCIA DEL SISTEMA
    # =================================================

    ref = get_reference()

    # V2
    # Protección por si la tabla referencia_sistema está vacía

    if ref is None:

        print(
            "ERROR: No existe referencia_sistema"
        )

        time.sleep(5)

        continue

    ref_ph = ref[0]
    ref_tds = ref[1]
    ref_ce = ref[2]

    # =================================================
    # DETECCIÓN DE ANOMALÍAS
    # =================================================

    alerts = detect_anomaly(
        data["ph"],
        data["tds"],
        data["ce"],
        ref_ph,
        ref_tds,
        ref_ce
    )

    # =================================================
    # V2 - CÁLCULO ACUMULATIVO DE VIDA ÚTIL
    # =================================================

    previous_health = get_last_filter_health()

    health, wear_score = calculate_filter_health(
        previous_health,
        data["ph"],
        data["tds"],
        data["ce"],
        ref_ph,
        ref_tds,
        ref_ce,
        len(alerts)
    )

    save_filter_state(
        reading_id,
        health,
        wear_score,
        "Calculo V2"
    )

    # =================================================
    # MOSTRAR INFORMACIÓN
    # =================================================

    print("\n-------------------")
    print(f"Lectura ID: {reading_id}")
    print(f"pH: {data['ph']}")
    print(f"TDS: {data['tds']}")
    print(f"CE: {data['ce']}")
    print(f"Temp: {data['temp']}")
    print(f"Calidad: {quality}")

    # V2
    print(f"Vida útil filtro: {health}%")
    print(f"Desgaste: {wear_score}")

    # =================================================
    # CONTROL DE LOTES
    # =================================================

    reading_counter += 1

    if reading_counter >= 20:

        print(f"\n📦 Lote {lot_id} finalizado")

        close_lot(
            lot_id,
            "PENDIENTE"
        )

        stats = get_lot_stats(lot_id)

        print("\n===== ESTADISTICAS DEL LOTE =====")
        print(stats)

        lot_id = create_lot(50)

        print(f"📦 Nuevo lote creado: {lot_id}")

        reading_counter = 0

    # =================================================
    # GUARDAR ALERTAS
    # =================================================

    if alerts:

        print("\n⚠ ANOMALÍAS DETECTADAS:")

        for alert in alerts:

            save_alert(
                reading_id,
                alert
            )

            print(f" - {alert}")

    else:

        print("Sin anomalías")

    time.sleep(60)