def calculate_health(
    anomaly_count
):

    health = 100 - anomaly_count

    if health < 0:
        health = 0

    return health