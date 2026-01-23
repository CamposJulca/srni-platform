from pathlib import Path
from datetime import datetime


def write_log(base_path: Path, message: str):
    log_file = base_path / "logs.txt"
    timestamp = datetime.now().strftime("%H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
