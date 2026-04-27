from __future__ import annotations

from typing import Any, Dict, List


def refine_damage_boundaries(
    image,
    damages: List[Dict[str, Any]],
    config: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    """
    Placeholder for segmentation-based boundary refinement.

    In this lightweight implementation, we simply return the input damages.
    The function exists so that `InspectionPipeline` can run even when
    advanced segmentation models (e.g., SAM / Mask R-CNN) are not installed.
    """
    if not isinstance(damages, list):
        return []
    return damages

