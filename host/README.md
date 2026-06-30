# Host logger folder (`host/`)

## Why this folder exists
It contains PC-side scripts that receive serial data and save measurement files.

## Main concepts
- Serial communication over USB
- CSV schema validation
- Timestamped file naming for repeatable experiments

## How the code works
- `serial_logger.py` reads serial lines for a fixed duration and writes valid rows.
- `utils.py` provides parsing, numeric checks, and output path creation.

## What you can modify later
- Add metadata capture (RPM, load, ambient temp)
- Add optional real-time plots while logging
- Add start/stop trigger logic
