# 02 - Hardware setup

- ESP32-C6 DevKit running MicroPython
- SparkFun 6DoF IMU (BMI270)
- USB cable for power + serial

Typical I2C wiring:
- IMU SDA -> ESP32-C6 SDA pin (`firmware/config.py`)
- IMU SCL -> ESP32-C6 SCL pin (`firmware/config.py`)
- GND -> GND
- 3V3 -> 3V3

TODO(hardware): verify exact pin mapping and sensor I2C address for your board.
