# core/detection.py
import numpy as np
from pathlib import Path

# Lazy import torch to handle DLL loading errors gracefully
_torch = None
_torch_error = None

def _import_torch():
    """Lazy import torch with error handling."""
    global _torch, _torch_error
    if _torch_error is not None:
        raise _torch_error
    if _torch is None:
        try:
            import torch
            _torch = torch
        except Exception as e:
            _torch_error = e
            raise ImportError(
                f"Failed to import PyTorch: {e}\n"
                "This is often caused by missing Visual C++ Redistributables on Windows.\n"
                "Please install: https://aka.ms/vs/17/release/vc_redist.x64.exe"
            ) from e
    return _torch

# Import Ultralytics YOLO (required)
try:
    # Try importing torch first (ultralytics needs it)
    _import_torch()
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except (ImportError, OSError) as e:
    YOLO_AVAILABLE = False
    print(f"ERROR: Failed to load PyTorch/Ultralytics: {e}")
    print("Please install Visual C++ Redistributables: https://aka.ms/vs/17/release/vc_redist.x64.exe")

from core.pytorch_compat import apply_pytorch_compatibility_fix


class Detector:
    def __init__(self, model_path, class_names):
        """Load a real Ultralytics YOLOv8 model from the given weights path.

        Args:
            model_path (str): Path to a .pt weights file.
            class_names (dict): Optional mapping of class indices to names. Used for fallback/validation.
        """
        if not YOLO_AVAILABLE:
            raise ImportError(
                "PyTorch/Ultralytics not available. "
                "This is often caused by missing Visual C++ Redistributables on Windows.\n"
                "Please install: https://aka.ms/vs/17/release/vc_redist.x64.exe"
            )
        
        # Ensure torch is imported
        _import_torch()

        # Ensure weights exist
        weights_path = Path(model_path)
        if not weights_path.exists():
            raise FileNotFoundError(f"YOLO weights not found at: {weights_path}")

        # Apply PyTorch 2.6 compatibility fixes before loading
        apply_pytorch_compatibility_fix()

        # Load model
        self.model = YOLO(str(weights_path))
        self._fallback_names = class_names if isinstance(class_names, dict) else {}

        # Use model's own names when available
        try:
            self.names = self.model.names if hasattr(self.model, 'names') else self._fallback_names
        except Exception:
            self.names = self._fallback_names

    def detect(self, image, confidence_threshold=0.5):
        """Run inference and return detections in the project's expected format.

        Returns list of dicts: {"class": str, "bbox": [x, y, w, h], "confidence": float}
        """
        # Ultralytics accepts numpy arrays (BGR) directly
        results = self.model.predict(image, conf=confidence_threshold, verbose=False)

        detections = []
        for result in results:
            # Prefer result.names; fallback to model names or provided mapping
            result_names = getattr(result, 'names', None) or getattr(self, 'names', {}) or self._fallback_names
            boxes = getattr(result, 'boxes', [])
            for box in boxes:
                # xyxy, conf, cls are torch tensors in Ultralytics results
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                cls_name = result_names.get(cls_id, 'unknown') if isinstance(result_names, dict) else str(cls_id)

                detections.append({
                    "class": cls_name,
                    "bbox": [x1, y1, x2 - x1, y2 - y1],
                    "confidence": conf
                })

        return detections
