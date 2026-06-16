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

lot_id = create_lot(50)

reading_counter = 0

while True:

    # Obtener datos (simulados por ahora)
    data = read_data()

    if not data:
        continue

    # Guardar lectura en BD
    reading_id = insert_reading(
        lot_id,
        data["ph"],
        data["tds"],
        data["ce"],
        data["temp"]
    )

    # Clasificar calidad
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

    print("\n-------------------")
    print(f"Lectura ID: {reading_id}")
    print(f"pH: {data['ph']}")
    print(f"TDS: {data['tds']}")
    print(f"CE: {data['ce']}")
    print(f"Temp: {data['temp']}")
    print(f"Calidad: {quality}")

    # Obtener referencia del sistema
    ref = get_reference()

    ref_ph = ref[0]
    ref_tds = ref[1]
    ref_ce = ref[2]

    health, wear_score = calculate_filter_health(
        data["ph"],
        data["tds"],
        data["ce"],
        ref_ph,
        ref_tds,
        ref_ce
    )

    save_filter_state(
        reading_id,
        health,
        wear_score,
        "Calculo V1"
    )
    print(f"Vida útil filtro: {health}%")
    print(f"Desgaste: {wear_score}")

    # Detectar anomalías
    alerts = detect_anomaly(
        data["ph"],
        data["tds"],
        data["ce"],
        ref_ph,
        ref_tds,
        ref_ce
    )

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


    # Guardar alertas si existen
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

    time.sleep(1)