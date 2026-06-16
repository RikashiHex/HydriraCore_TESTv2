import time

from simulator import read_data

from database import (
    insert_reading,
    get_reference,
    save_alert,
    save_classification
)

from classifier import classify

from anomaly_detector import detect_anomaly


while True:

    # Obtener datos (simulados por ahora)
    data = read_data()

    if not data:
        continue

    # Guardar lectura en BD
    reading_id = insert_reading(
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

    # Detectar anomalías
    alerts = detect_anomaly(
        data["ph"],
        data["tds"],
        data["ce"],
        ref_ph,
        ref_tds,
        ref_ce
    )

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