# 04 - Serial logging

Use `host/serial_logger.py` to record data.

Example:
```bash
python host/serial_logger.py --port /dev/ttyACM0 --duration 15
```

The script ignores invalid/comment lines and writes only validated numeric rows.
