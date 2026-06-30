"""Serial logger for ESP32-C6 vibration CSV stream."""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

from utils import EXPECTED_COLUMNS, is_numeric_row, make_output_path, parse_csv_line

try:
    import serial
except ImportError as exc:  # pragma: no cover
    raise SystemExit("pyserial is required. Install with: pip install pyserial") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Log vibration CSV data from serial")
    parser.add_argument("--port", required=True, help="Serial port (example: /dev/ttyACM0 or COM3)")
    parser.add_argument("--baudrate", type=int, default=115200)
    parser.add_argument("--duration", type=float, default=10.0, help="Capture duration in seconds")
    parser.add_argument("--output-dir", default="data/raw")
    parser.add_argument("--timeout", type=float, default=1.0)
    return parser.parse_args()


def log_serial_to_csv(port: str, baudrate: int, duration: float, output_dir: Path, timeout: float) -> Path:
    """Read serial lines and save valid rows to CSV."""
    out_path = make_output_path(output_dir)
    deadline = time.time() + duration

    with serial.Serial(port=port, baudrate=baudrate, timeout=timeout) as ser, out_path.open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.writer(f)
        writer.writerow(EXPECTED_COLUMNS)

        while time.time() < deadline:
            raw = ser.readline().decode("utf-8", errors="replace")
            parts = parse_csv_line(raw)
            if not parts:
                continue
            if not is_numeric_row(parts):
                continue
            writer.writerow(parts)

    return out_path


def main() -> int:
    args = parse_args()
    try:
        path = log_serial_to_csv(
            port=args.port,
            baudrate=args.baudrate,
            duration=args.duration,
            output_dir=Path(args.output_dir),
            timeout=args.timeout,
        )
    except Exception as exc:
        print(f"ERROR: logging failed: {exc}", file=sys.stderr)
        return 1

    print(f"Saved: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
