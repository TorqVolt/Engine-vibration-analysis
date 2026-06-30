# ice-vibration-measurement

A learning-first project for measuring and analyzing internal combustion engine (ICE) vibration.

This repository keeps the first working version intentionally simple:
- Accelerometer data first (X/Y/Z)
- Human-readable CSV over USB serial
- Clear, beginner-friendly Python and MicroPython code

## What you will build

- ESP32-C6 (MicroPython) reads IMU data from a BMI270-based SparkFun 6DoF board
- ESP32-C6 streams one CSV line per sample over USB serial
- PC Python script logs the serial stream to CSV files
- Jupyter notebooks analyze one recording or compare two recordings

## What you will learn

- Basic I2C sensor communication ideas in MicroPython
- Practical streaming formats for serial data logging
- CSV-based data pipelines for repeatable measurements
- Time-domain and frequency-domain vibration analysis (FFT)
- How to compare dominant vibration frequencies between runs

## Getting started (beginner path)

1. **Prepare Python environment on PC**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Wire hardware** following `docs/02_hardware_setup.md`.
3. **Flash/copy firmware files** in `firmware/` to ESP32-C6 running MicroPython.
4. **Run firmware** and check serial output is CSV-like text.
5. **Log data** from PC:
   ```bash
   python host/serial_logger.py --port /dev/ttyACM0 --duration 10
   ```
6. **Open notebooks** in `notebooks/` and analyze saved CSV files.

## Staged development plan

- **Stage 1: sensor communication test**
  - Confirm I2C bus and sensor address
  - Read simple data and print values
- **Stage 2: serial streaming test**
  - Stream stable header + rows over USB serial
- **Stage 3: CSV logging**
  - Capture stream on PC into timestamped CSV files
- **Stage 4: single-file notebook analysis**
  - Plot X/Y/Z and compute basic metrics + FFT
- **Stage 5: two-file comparison**
  - Overlay spectra and compare dominant frequencies
- **Stage 6: reuse and extension**
  - Add optional filtering, metadata, and advanced methods

## Repository structure

```text
.
├─ README.md
├─ LICENSE
├─ .gitignore
├─ requirements.txt
├─ firmware/
│  ├─ main.py
│  ├─ bmi270.py
│  ├─ config.py
│  └─ README.md
├─ host/
│  ├─ serial_logger.py
│  ├─ utils.py
│  └─ README.md
├─ notebooks/
│  ├─ 01_single_run_analysis.ipynb
│  ├─ 02_two_run_comparison.ipynb
│  └─ helpers.py
├─ data/
│  ├─ raw/
│  ├─ processed/
│  └─ sample/
├─ docs/
│  ├─ 01_project_overview.md
│  ├─ 02_hardware_setup.md
│  ├─ 03_micropython_basics.md
│  ├─ 04_serial_logging.md
│  ├─ 05_csv_format.md
│  ├─ 06_signal_analysis_basics.md
│  └─ 07_future_improvements.md
└─ tests/
   ├─ test_csv_loading.py
   └─ test_analysis_helpers.py
```

## CSV format (stream + files)

Header:

```text
timestamp_ms,sample_idx,ax_g,ay_g,az_g,gx_dps,gy_dps,gz_dps,temp_c
```

Notes:
- `timestamp_ms`: milliseconds since firmware start
- `sample_idx`: monotonically increasing integer
- `ax_g`, `ay_g`, `az_g`: acceleration in g units
- gyro and temp columns are optional by implementation, but present in this scaffold

## Important files explained

### `firmware/main.py`
- **Why it exists:** Entry point on ESP32-C6.
- **Main concepts:** initialization, acquisition loop, CSV streaming.
- **How it works:** reads sensor sample, formats CSV line, prints over serial.
- **What to modify later:** sample rate, enabled channels, error handling policy.

### `firmware/bmi270.py`
- **Why it exists:** sensor-specific access layer.
- **Main concepts:** I2C communication, sensor abstraction.
- **How it works:** wraps sensor initialization and sample reads behind simple methods.
- **What to modify later:** replace placeholder reads with full BMI270 register config if needed.

### `firmware/config.py`
- **Why it exists:** hardware-dependent constants in one place.
- **Main concepts:** I2C pins, address, sample period.
- **How it works:** central constants imported by firmware logic.
- **What to modify later:** board pin mapping and timing values.

### `host/serial_logger.py`
- **Why it exists:** PC-side recorder for reusable measurements.
- **Main concepts:** serial read loop, CSV writing, run duration.
- **How it works:** validates incoming lines and appends to timestamped file.
- **What to modify later:** CLI options, richer metadata, live dashboards.

### `host/utils.py`
- **Why it exists:** keeps logger logic simple by separating helpers.
- **Main concepts:** parsing, validation, output naming.
- **How it works:** turns raw serial line into validated CSV row.
- **What to modify later:** stricter schema checks or custom naming conventions.

### `notebooks/helpers.py`
- **Why it exists:** shared analysis functions for both notebooks.
- **Main concepts:** loading, sampling estimation, FFT, dominant peaks.
- **How it works:** provides small reusable numpy/pandas utilities.
- **What to modify later:** filtering, PSD, order analysis functions.

### `notebooks/*.ipynb`
- **Why they exist:** step-by-step learning walkthroughs.
- **Main concepts:** plotting, metrics, FFT, comparison.
- **How they work:** markdown explains each analysis stage; code executes it.
- **What to modify later:** your own plots, thresholds, and interpretation templates.

### `docs/*.md`
- **Why they exist:** short tutorials for each subsystem.
- **Main concepts:** practical implementation choices and limitations.
- **How they work:** each document introduces one topic in plain language.
- **What to modify later:** add photos, hardware diagrams, troubleshooting notes.

## Sampling rate and limitations

- Default target sample period is configured in `firmware/config.py`.
- Real rate depends on MicroPython loop timing, USB serial throughput, and sensor config.
- Always estimate actual sampling interval from `timestamp_ms` during analysis.

## Future enhancements

- Time-domain filtering
- Window functions before FFT
- Power Spectral Density (PSD)
- Order tracking
- RPM synchronization
- Trigger-based capture
- Per-measurement metadata sidecar files (JSON/YAML)
- Lightweight GUI app for non-programmer use

## License

MIT (see `LICENSE`).
