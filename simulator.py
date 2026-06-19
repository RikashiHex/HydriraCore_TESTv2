import random

counter = 0

tds_actual = 800
ce_actual = 1200
ph_actual = 8.8


def reset_batch():

    global tds_actual
    global ce_actual
    global ph_actual

    tds_actual = random.randint(
        700,
        1200
    )

    ce_actual = random.randint(
        900,
        1800
    )

    ph_actual = round(
        random.uniform(
            8.2,
            9.5
        ),
        2
    )


def read_data():

    global counter
    global tds_actual
    global ce_actual
    global ph_actual

    counter += 1

    # Cada lote dura 20 lecturas
    # La lectura 1 del lote inicia "sucia"

    if counter % 20 == 1:

        reset_batch()

    # Reducir gradualmente

    if tds_actual > 120:

        tds_actual -= random.randint(
            15,
            50
        )

    if ce_actual > 250:

        ce_actual -= random.randint(
            20,
            80
        )

    if ph_actual > 7.0:

        ph_actual -= round(
            random.uniform(
                0.03,
                0.10
            ),
            2
        )

    # Evento anómalo ocasional

    if counter % 45 == 0:

        return {
            "ph": 7.0,
            "tds": 720,
            "ce": 50,
            "temp": 25
        }

    return {

        "ph": round(ph_actual, 2),

        "tds": max(
            120,
            int(tds_actual)
        ),

        "ce": max(
            250,
            int(ce_actual)
        ),

        "temp": round(
            random.uniform(
                20,
                28
            ),
            1
        )
    }