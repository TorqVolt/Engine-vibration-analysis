"""Shared analysis helpers for vibration notebooks."""

from __future__ import annotations

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ["timestamp_ms", "sample_idx", "ax_g", "ay_g", "az_g"]


def load_measurement_csv(path: str) -> pd.DataFrame:
    """Load CSV and validate required columns."""
    df = pd.read_csv(path)
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df


def estimate_sampling_rate_hz(df: pd.DataFrame) -> float:
    """Estimate sample rate from timestamp_ms median spacing."""
    dt_ms = df["timestamp_ms"].diff().dropna()
    if dt_ms.empty:
        raise ValueError("Not enough samples to estimate sampling rate")
    median_dt_ms = float(dt_ms.median())
    if median_dt_ms <= 0:
        raise ValueError("Non-positive sample interval detected")
    return 1000.0 / median_dt_ms


def add_magnitude(df: pd.DataFrame) -> pd.DataFrame:
    """Return copy with acceleration magnitude column."""
    out = df.copy()
    out["a_mag_g"] = np.sqrt(out["ax_g"] ** 2 + out["ay_g"] ** 2 + out["az_g"] ** 2)
    return out


def remove_dc(signal: np.ndarray) -> np.ndarray:
    """Subtract mean to remove DC offset before FFT."""
    return signal - np.mean(signal)


def compute_fft(signal: np.ndarray, sample_rate_hz: float):
    """Compute one-sided FFT amplitude spectrum."""
    n = len(signal)
    if n < 2:
        raise ValueError("Signal must contain at least two samples")
    centered = remove_dc(signal)
    spectrum = np.fft.rfft(centered)
    freqs = np.fft.rfftfreq(n, d=1.0 / sample_rate_hz)
    amplitudes = np.abs(spectrum) * 2.0 / n
    return freqs, amplitudes


def dominant_peaks(freqs: np.ndarray, amplitudes: np.ndarray, top_n: int = 5) -> pd.DataFrame:
    """Return top frequency peaks sorted by amplitude."""
    if len(freqs) != len(amplitudes):
        raise ValueError("freqs and amplitudes must have same length")
    order = np.argsort(amplitudes)[::-1][:top_n]
    return pd.DataFrame({"frequency_hz": freqs[order], "amplitude": amplitudes[order]}).sort_values(
        by="amplitude", ascending=False
    )


def basic_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute simple time-domain metrics for X, Y, Z."""
    rows = []
    for axis in ["ax_g", "ay_g", "az_g"]:
        values = df[axis].to_numpy()
        rows.append(
            {
                "axis": axis,
                "mean": float(np.mean(values)),
                "rms": float(np.sqrt(np.mean(values**2))),
                "peak": float(np.max(np.abs(values))),
                "std": float(np.std(values)),
            }
        )
    return pd.DataFrame(rows)
