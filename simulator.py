import random

counter = 0

def read_data():

    global counter

    counter += 1

    # Cada 20 lecturas:
    # anomalía de relaciones
    if counter % 20 == 0:

        return {
            "ph": 7.0,
            "tds": 720,
            "ce": 50,
            "temp": 25
        }

    # Cada 35 lecturas:
    # agua mala
    if counter % 35 == 0:

        return {
            "ph": 9.2,
            "tds": 1400,
            "ce": 1800,
            "temp": 25
        }

    # Lectura normal
    return {
        "ph": round(random.uniform(6.8, 7.4), 2),
        "tds": random.randint(100, 200),
        "ce": random.randint(200, 400),
        "temp": round(random.uniform(20, 28), 1)
    }