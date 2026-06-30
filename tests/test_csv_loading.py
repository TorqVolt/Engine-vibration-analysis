from pathlib import Path

from notebooks.helpers import load_measurement_csv


def test_load_measurement_csv_accepts_sample_file():
    path = Path("data/sample/sample_run_01.csv")
    df = load_measurement_csv(str(path))
    assert not df.empty
    assert {"timestamp_ms", "ax_g", "ay_g", "az_g"}.issubset(df.columns)
