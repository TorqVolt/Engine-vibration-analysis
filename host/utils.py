"""Helper utilities for serial logging."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

EXPECTED_COLUMNS = [
    "timestamp_ms",
    "sample_idx",
    "ax_g",
    "ay_g",
    "az_g",
    "gx_dps",
    "gy_dps",
    "gz_dps",
    "temp_c",
]


def make_output_path(output_dir: Path) -> Path:
    """Create a timestamped CSV filename inside output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return output_dir / f"measurement_{stamp}.csv"


def parse_csv_line(raw_line: str) -> list[str] | None:
    """Split a CSV line and return fields, or None for ignorable lines."""
    line = raw_line.strip()
    if not line:
        return None
    if line.startswith("#"):
        return None
    parts = [part.strip() for part in line.split(",")]
    if len(parts) != len(EXPECTED_COLUMNS):
        return None
    return parts


def is_numeric_row(parts: list[str]) -> bool:
    """Check all columns can be interpreted as numeric values."""
    try:
        _ = int(parts[0])
        _ = int(parts[1])
        for value in parts[2:]:
            float(value)
    except ValueError:
        return False
    return True
