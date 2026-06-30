"""MicroPython entry point for ICE vibration streaming."""

import time
from machine import I2C, Pin

import config
from bmi270 import BMI270


def format_csv_row(timestamp_ms: int, sample_idx: int, sample: dict) -> str:
    """Create one CSV line in a fixed, human-readable format."""
    return (
        f"{timestamp_ms},{sample_idx},"
        f"{sample['ax_g']:.6f},{sample['ay_g']:.6f},{sample['az_g']:.6f},"
        f"{sample['gx_dps']:.6f},{sample['gy_dps']:.6f},{sample['gz_dps']:.6f},"
        f"{sample['temp_c']:.2f}"
    )


def run():
    """Initialize hardware and stream CSV samples forever."""
    print(config.CSV_HEADER)

    try:
        i2c = I2C(0, scl=Pin(config.I2C_SCL_PIN), sda=Pin(config.I2C_SDA_PIN), freq=400000)
        imu = BMI270(i2c, address=config.BMI270_I2C_ADDR)
        imu.initialize()
        print("# Sensor initialization successful")
    except Exception as exc:
        print("# ERROR: sensor init failed", exc)
        # Keep firmware alive and visible for debugging.
        while True:
            time.sleep_ms(1000)

    start_ms = time.ticks_ms()
    sample_idx = 0

    while True:
        now_ms = time.ticks_diff(time.ticks_ms(), start_ms)
        sample = imu.read_sample()
        print(format_csv_row(now_ms, sample_idx, sample))
        sample_idx += 1
        time.sleep_ms(config.SAMPLE_PERIOD_MS)


run()
