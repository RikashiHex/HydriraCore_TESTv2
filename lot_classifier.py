def classify_lot(stats):

    if (
        stats["avg_tds"] < 300
        and
        stats["avg_ce"] < 500
    ):
        return "ACEPTAR"

    elif (
        stats["avg_tds"] < 700
        and
        stats["avg_ce"] < 900
    ):
        return "REPROCESAR"

    return "DESCARTAR"