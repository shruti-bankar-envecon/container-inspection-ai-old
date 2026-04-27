from __future__ import annotations

from typing import Any, Dict, List

import cv2
import numpy as np

from core.utils import draw_results_on_image


class DamageVisualizer:
    """
    Utility class for creating annotated images and YOLO label files.

    This is a lightweight implementation focused on keeping the API that
    `InspectionPipeline` expects (`create_insurance_annotated_image`,
    `create_annotated_image`, `save_yolo_labels`) while avoiding any heavy
    additional dependencies.
    """

    def __init__(self, config: Dict[str, Any] | None = None):
        self.config = config or {}

    # --- Image generation helpers -------------------------------------------------

    def _draw_basic_boxes(self, image: np.ndarray, damages: List[Dict[str, Any]]) -> np.ndarray:
        """
        Draw simple bounding boxes for damages on a copy of the image.
        """
        img = image.copy()
        for d in damages or []:
            bbox = d.get("bbox")
            if not isinstance(bbox, (list, tuple)) or len(bbox) < 4:
                continue
            try:
                x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            except Exception:
                continue
            if w <= 0 or h <= 0:
                continue

            # Red rectangles for damage regions
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        return img

    def create_insurance_annotated_image(
        self,
        image: np.ndarray,
        damages: List[Dict[str, Any]],
    ) -> np.ndarray:
        """
        Create an annotated image suitable for insurance-style previews.

        For now this is equivalent to a simple bounding-box visualization.
        """
        # Reuse the generic drawing helper to keep behavior consistent
        return self._draw_basic_boxes(image, damages)

    def create_annotated_image(
        self,
        image: np.ndarray,
        damages: List[Dict[str, Any]],
    ) -> np.ndarray:
        """
        Create a richer annotated image for QA / YOLO training previews.

        Currently this mirrors the insurance preview but can be extended
        with labels, ticks, and legends in the future.
        """
        return self._draw_basic_boxes(image, damages)

    # --- YOLO label export --------------------------------------------------------

    def save_yolo_labels(
        self,
        damage_visualization_data: Dict[str, Any],
        label_path: str,
        img_w: int,
        img_h: int,
    ) -> None:
        """
        Save YOLO-format labels for the given damages.

        Expects each damage entry to contain:
          - `class_id` (int)
          - `bbox` as [x, y, w, h] in pixel coordinates

        Output format (per line):
          <class_id> <cx> <cy> <w> <h>
        where coordinates are normalized to [0, 1].
        """
        damages = damage_visualization_data.get("damages", []) or []
        lines: List[str] = []

        iw = float(max(1, img_w))
        ih = float(max(1, img_h))

        for d in damages:
            if not isinstance(d, dict):
                continue

            bbox = d.get("bbox")
            if not isinstance(bbox, (list, tuple)) or len(bbox) < 4:
                continue

            try:
                x, y, w, h = float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])
            except Exception:
                continue

            if w <= 0 or h <= 0:
                continue

            cx = (x + w / 2.0) / iw
            cy = (y + h / 2.0) / ih
            nw = w / iw
            nh = h / ih

            try:
                class_id = int(d.get("class_id", 0))
            except Exception:
                class_id = 0

            line = f"{class_id} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}"
            lines.append(line)

        with open(label_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

