"""Hardware and runtime configuration for ESP32-C6 + BMI270."""

# TODO(hardware): verify these pins match your ESP32-C6 board wiring.
I2C_SCL_PIN = 6
I2C_SDA_PIN = 7

# Typical BMI270 I2C addresses are 0x68 or 0x69 depending on board strap.
# TODO(hardware): confirm actual sensor address with I2C scan.
BMI270_I2C_ADDR = 0x68

# Human-readable CSV stream format.
CSV_HEADER = "timestamp_ms,sample_idx,ax_g,ay_g,az_g,gx_dps,gy_dps,gz_dps,temp_c"

# First version keeps rate modest and stable.
SAMPLE_PERIOD_MS = 20  # ~50 Hz target
