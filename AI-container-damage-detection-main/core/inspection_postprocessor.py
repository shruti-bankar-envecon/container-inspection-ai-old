from __future__ import annotations

from typing import Any, Dict, List, Tuple


def postprocess_damages(
    damages: List[Dict[str, Any]],
    image_shape: Tuple[int, int] | None = None,
    min_confidence_for_auto: float = 0.85,
) -> Dict[str, Any]:
    """
    Lightweight, conservative post-processing for damage detections.

    This is intentionally simple so that the backend can run even without
    a more sophisticated rules engine. It:
      - normalizes basic fields
      - counts low-confidence items for human review
      - returns the original list unchanged by default
    """
    if not isinstance(damages, list):
        damages = []

    cleaned: List[Dict[str, Any]] = []
    needs_human_review_count = 0
    false_positive_likely_count = 0

    for d in damages:
        if not isinstance(d, dict):
            continue

        entry = d.copy()

        # Normalize confidence field
        try:
            conf = float(entry.get("confidence", 0.0) or 0.0)
        except Exception:
            conf = 0.0
        conf = max(0.0, min(1.0, conf))
        entry["confidence"] = conf

        # Very low confidence → mark as likely needing review
        if conf < min_confidence_for_auto:
            needs_human_review_count += 1
            entry.setdefault("needs_human_review", True)

        # Placeholder heuristic for false positives (extremely low confidence)
        if conf < 0.2:
            false_positive_likely_count += 1
            entry.setdefault("false_positive_likely", True)

        cleaned.append(entry)

    summary = {
        "total_damages": len(cleaned),
        "needs_human_review_count": int(needs_human_review_count),
        "false_positive_likely_count": int(false_positive_likely_count),
        "image_shape": image_shape,
        "min_confidence_for_auto": float(min_confidence_for_auto),
    }

    return {
        "damages": cleaned,
        "summary": summary,
    }

