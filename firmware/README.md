# Firmware folder (`firmware/`)

## Why this folder exists
It contains the MicroPython code that runs directly on the ESP32-C6 and streams sensor data.

## Main concepts
- I2C sensor communication
- Periodic sampling loop
- CSV text output over USB serial

## How the code works
- `config.py` defines board- and experiment-specific constants.
- `bmi270.py` wraps sensor access behind a simple API.
- `main.py` initializes hardware, then prints one CSV row per sample.

## What you can modify later
- Pin mapping and sensor address in `config.py`
- Real BMI270 register reads in `bmi270.py`
- Sampling rate and output fields in `main.py`
