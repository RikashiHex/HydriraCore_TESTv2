def calculate_filter_health(
    previous_health,
    ph,
    tds,
    ce,
    ref_ph,
    ref_tds,
    ref_ce,
    anomaly_count=0
):

    ph_error = abs(ph - ref_ph) / ref_ph

    tds_error = abs(tds - ref_tds) / ref_tds

    ce_error = abs(ce - ref_ce) / ref_ce

    wear_score = (
        ph_error +
        tds_error +
        ce_error
    ) / 3

    wear_amount = wear_score * 2

    wear_amount += anomaly_count * 0.5

    health = previous_health - wear_amount

    if health < 0:
        health = 0

    return round(health, 2), round(wear_score, 4)