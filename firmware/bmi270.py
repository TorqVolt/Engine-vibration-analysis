"""Minimal BMI270 sensor interface for MicroPython.

This file intentionally favors clarity over complete register-level implementation.
If your exact board/library behavior differs, adjust the TODO sections.
"""

from machine import I2C


class BMI270:
    """Simple wrapper around a BMI270-like IMU over I2C."""

    WHO_AM_I_REG = 0x00

    def __init__(self, i2c: I2C, address: int = 0x68):
        self.i2c = i2c
        self.address = address

    def initialize(self) -> None:
        """Initialize the sensor.

        TODO(hardware): replace this placeholder with full BMI270 setup sequence
        if your board needs explicit config upload/register writes.
        """
        devices = self.i2c.scan()
        if self.address not in devices:
            raise OSError("BMI270 not found on I2C bus")

    def read_sample(self):
        """Return one sample as a dictionary.

        Returns default zero values as a safe scaffold until full sensor readout is wired.
        TODO(hardware): read raw accel/gyro/temp registers and apply scaling.
        """
        return {
            "ax_g": 0.0,
            "ay_g": 0.0,
            "az_g": 1.0,
            "gx_dps": 0.0,
            "gy_dps": 0.0,
            "gz_dps": 0.0,
            "temp_c": 25.0,
        }
