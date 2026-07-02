from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_incidents(path: Path | str = Path("docs/incidents/previous_incidents.json")) -> list[dict[str, Any]]:
    incident_path = Path(path)
    if not incident_path.exists():
        return []
    payload = json.loads(incident_path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []
