import numpy as np

from notebooks.helpers import compute_fft, dominant_peaks


def test_compute_fft_and_peaks_detects_known_frequency():
    fs = 100.0
    t = np.arange(0.0, 2.0, 1.0 / fs)
    signal = np.sin(2 * np.pi * 10.0 * t)

    freqs, amps = compute_fft(signal, fs)
    peaks = dominant_peaks(freqs, amps, top_n=3)

    assert np.isclose(peaks.iloc[0]["frequency_hz"], 10.0, atol=0.6)
    assert peaks.iloc[0]["amplitude"] > 0.5
