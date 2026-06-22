import serial
from config.config import *

ser = serial.Serial(
    SERIAL_PORT,
    BAUDRATE,
    timeout=1
)

def read_data():

    line = ser.readline().decode().strip()

    if not line:
        return None

    try:

        ph, tds, ce, temp = map(
            float,
            line.split(",")
        )

        print(
            f"Lectura recibida: ph={ph}, tds={tds}, ce={ce}, temp={temp}"
        )

        return {
            "ph": ph,
            "tds": tds,
            "ce": ce,
            "temp": temp
        }

    except:
        return None