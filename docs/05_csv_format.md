# 05 - CSV format

Expected columns:

`timestamp_ms,sample_idx,ax_g,ay_g,az_g,gx_dps,gy_dps,gz_dps,temp_c`

- `timestamp_ms` is preferred for real sample interval estimation.
- `sample_idx` helps detect dropped lines.
- `ax_g/ay_g/az_g` are required for first analysis stage.
