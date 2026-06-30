# 03 - MicroPython basics

`main.py` executes automatically on boot.

Key steps:
- Initialize I2C
- Initialize sensor
- Enter sampling loop
- Print one CSV row per iteration

If init fails, firmware prints an error and keeps running so debugging is visible on serial.
