from __future__ import annotations

from typing import Any, Dict, List


def assess_damage_severity(
    image,
    damages: List[Dict[str, Any]],
    config: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    """
    Minimal severity model stub.

    Ensures each damage entry has a `severity` field so downstream
    reporting logic can operate without requiring a trained model.
    """
    if not isinstance(damages, list):
        return []

    output: List[Dict[str, Any]] = []
    for d in damages:
        if not isinstance(d, dict):
            continue
        entry = d.copy()

        # If severity already present, leave it alone; otherwise default to "minor"
        severity = str(entry.get("severity") or "").strip().lower()
        if severity not in ("minor", "major", "critical"):
            # Simple heuristic based on confidence if available
            try:
                conf = float(entry.get("confidence", 0.0) or 0.0)
            except Exception:
                conf = 0.0

            if conf >= 0.85:
                severity = "major"
            elif conf >= 0.6:
                severity = "minor"
            else:
                severity = "minor"

        entry["severity"] = severity
        output.append(entry)

    return output

