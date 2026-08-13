"""Export experiment run records to CSV and JSON."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


def write_json(path: str | Path, records: Sequence[Mapping[str, Any]]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(list(records), indent=2, sort_keys=True),
        encoding="utf-8",
    )


def write_csv(path: str | Path, records: Sequence[Mapping[str, Any]]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        out.write_text("", encoding="utf-8")
        return
    fieldnames = list(records[0].keys())
    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in records:
            writer.writerow(row)
