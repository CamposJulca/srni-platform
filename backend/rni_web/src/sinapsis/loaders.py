# sinapsis/loaders.py

import json
from pathlib import Path
from typing import Any, Dict, List


def load_json_snapshot(path: str | Path) -> List[Dict[str, Any]]:
    """
    Carga un snapshot JSON desde disco.
    No valida ni transforma.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Snapshot no encontrado: {path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
