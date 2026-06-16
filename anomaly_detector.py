def detect_anomaly(
    ph,
    tds,
    ce,
    ref_ph,
    ref_tds,
    ref_ce
):

    alerts = []

    ratio_ref = ref_tds / ref_ce
    ratio_now = tds / ce

    ratio_error = abs(
        ratio_ref - ratio_now
    )

    if ratio_error > 1:

        alerts.append(
            "Relacion TDS/CE anormal"
        )

    if tds > ref_tds * 4:

        alerts.append(
            "TDS mas alto de lo normal"
        )

    if ce < ref_ce * 0.5:

        alerts.append(
            "CE mas baja de lo normal"
        )

    if ph < 6.5 or ph > 8.5:

        alerts.append(
            "pH fuera de rango"
        )

    return alerts