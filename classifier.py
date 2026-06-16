def classify(ph, tds, ce):

    if (
        6.5 <= ph <= 8.5
        and tds < 1000
        and ce < 1000
    ):
        return "EXCELENTE", 1.0

    return "MALA", 1.0