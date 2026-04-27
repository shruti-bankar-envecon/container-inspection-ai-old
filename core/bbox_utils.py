# core/bbox_utils.py
"""
Bounding Box Utilities for Container Inspection
Provides functions for validating, normalizing, and manipulating bounding boxes
"""

import numpy as np
from typing import List, Tuple, Optional, Dict


def validate_bbox(bbox: List[int], image_shape: Tuple[int, int]) -> bool:
    """
    Validate that a bounding box is within image bounds and has valid dimensions.
    
    Args:
        bbox: Bounding box as [x, y, width, height]
        image_shape: Image shape as (height, width)
    
    Returns:
        True if bbox is valid, False otherwise
    """
    if not bbox or len(bbox) < 4:
        return False
    
    x, y, w, h = bbox
    img_h, img_w = image_shape
    
    # Check if coordinates are valid
    if x < 0 or y < 0 or w <= 0 or h <= 0:
        return False
    
    # Check if bbox is within image bounds
    if x + w > img_w or y + h > img_h:
        return False
    
    return True


def normalize_bbox(bbox: List[float], image_shape: Tuple[int, int]) -> List[int]:
    """
    Normalize and clip bounding box to image bounds.
    
    Args:
        bbox: Bounding box as [x, y, width, height]
        image_shape: Image shape as (height, width)
    
    Returns:
        Normalized bbox as [x, y, width, height] with integer coordinates
    """
    if not bbox or len(bbox) < 4:
        return [0, 0, 0, 0]
    
    x, y, w, h = bbox
    img_h, img_w = image_shape
    
    # Convert to integers
    x, y, w, h = int(x), int(y), int(w), int(h)
    
    # Clip to image bounds
    x = max(0, min(x, img_w - 1))
    y = max(0, min(y, img_h - 1))
    w = max(1, min(w, img_w - x))
    h = max(1, min(h, img_h - y))
    
    return [x, y, w, h]


def calculate_iou(bbox1: List[int], bbox2: List[int]) -> float:
    """
    Calculate Intersection over Union (IoU) between two bounding boxes.
    
    Args:
        bbox1: First bounding box as [x, y, width, height]
        bbox2: Second bounding box as [x, y, width, height]
    
    Returns:
        IoU score between 0 and 1
    """
    if not bbox1 or not bbox2 or len(bbox1) < 4 or len(bbox2) < 4:
        return 0.0
    
    x1, y1, w1, h1 = bbox1
    x2, y2, w2, h2 = bbox2
    
    # Calculate intersection
    x_left = max(x1, x2)
    y_top = max(y1, y2)
    x_right = min(x1 + w1, x2 + w2)
    y_bottom = min(y1 + h1, y2 + h2)
    
    if x_right < x_left or y_bottom < y_top:
        return 0.0
    
    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    
    # Calculate union
    bbox1_area = w1 * h1
    bbox2_area = w2 * h2
    union_area = bbox1_area + bbox2_area - intersection_area
    
    if union_area == 0:
        return 0.0
    
    return intersection_area / union_area


def merge_overlapping_bboxes(bboxes: List[Dict], iou_threshold: float = 0.5) -> List[Dict]:
    """
    Merge overlapping bounding boxes based on IoU threshold.
    
    Args:
        bboxes: List of bbox dictionaries with 'bbox' key
        iou_threshold: IoU threshold for merging (default: 0.5)
    
    Returns:
        List of merged bounding boxes
    """
    if not bboxes:
        return []
    
    merged = []
    used = set()
    
    for i, bbox1 in enumerate(bboxes):
        if i in used:
            continue
        
        if 'bbox' not in bbox1 or not bbox1['bbox']:
            merged.append(bbox1)
            continue
        
        # Find all overlapping boxes
        overlapping = [bbox1]
        for j, bbox2 in enumerate(bboxes):
            if i == j or j in used:
                continue
            
            if 'bbox' not in bbox2 or not bbox2['bbox']:
                continue
            
            iou = calculate_iou(bbox1['bbox'], bbox2['bbox'])
            if iou > iou_threshold:
                overlapping.append(bbox2)
                used.add(j)
        
        # Merge overlapping boxes
        if len(overlapping) > 1:
            merged_bbox = merge_bboxes([b['bbox'] for b in overlapping])
            merged_entry = bbox1.copy()
            merged_entry['bbox'] = merged_bbox
            merged_entry['confidence'] = max(b.get('confidence', 0) for b in overlapping)
            merged.append(merged_entry)
        else:
            merged.append(bbox1)
    
    return merged


def merge_bboxes(bboxes: List[List[int]]) -> List[int]:
    """
    Merge multiple bounding boxes into a single bounding box that encompasses all.
    
    Args:
        bboxes: List of bounding boxes as [x, y, width, height]
    
    Returns:
        Merged bounding box as [x, y, width, height]
    """
    if not bboxes:
        return [0, 0, 0, 0]
    
    if len(bboxes) == 1:
        return bboxes[0]
    
    # Find min/max coordinates
    x_min = min(bbox[0] for bbox in bboxes)
    y_min = min(bbox[1] for bbox in bboxes)
    x_max = max(bbox[0] + bbox[2] for bbox in bboxes)
    y_max = max(bbox[1] + bbox[3] for bbox in bboxes)
    
    return [x_min, y_min, x_max - x_min, y_max - y_min]


def expand_bbox(bbox: List[int], expansion_ratio: float, image_shape: Tuple[int, int]) -> List[int]:
    """
    Expand a bounding box by a given ratio while keeping it within image bounds.
    
    Args:
        bbox: Bounding box as [x, y, width, height]
        expansion_ratio: Ratio to expand (e.g., 0.1 for 10% expansion)
        image_shape: Image shape as (height, width)
    
    Returns:
        Expanded bounding box as [x, y, width, height]
    """
    if not bbox or len(bbox) < 4:
        return [0, 0, 0, 0]
    
    x, y, w, h = bbox
    img_h, img_w = image_shape
    
    # Calculate expansion
    expand_w = int(w * expansion_ratio)
    expand_h = int(h * expansion_ratio)
    
    # Apply expansion
    new_x = max(0, x - expand_w // 2)
    new_y = max(0, y - expand_h // 2)
    new_w = min(img_w - new_x, w + expand_w)
    new_h = min(img_h - new_y, h + expand_h)
    
    return [new_x, new_y, new_w, new_h]


def bbox_center(bbox: List[int]) -> Tuple[int, int]:
    """
    Calculate the center point of a bounding box.
    
    Args:
        bbox: Bounding box as [x, y, width, height]
    
    Returns:
        Center point as (cx, cy)
    """
    if not bbox or len(bbox) < 4:
        return (0, 0)
    
    x, y, w, h = bbox
    return (x + w // 2, y + h // 2)


def bbox_area(bbox: List[int]) -> int:
    """
    Calculate the area of a bounding box.
    
    Args:
        bbox: Bounding box as [x, y, width, height]
    
    Returns:
        Area in pixels
    """
    if not bbox or len(bbox) < 4:
        return 0
    
    return bbox[2] * bbox[3]


def filter_small_bboxes(bboxes: List[Dict], min_area: int = 100) -> List[Dict]:
    """
    Filter out bounding boxes smaller than a minimum area.
    
    Args:
        bboxes: List of bbox dictionaries with 'bbox' key
        min_area: Minimum area in pixels (default: 100)
    
    Returns:
        Filtered list of bounding boxes
    """
    filtered = []
    for bbox_dict in bboxes:
        if 'bbox' not in bbox_dict or not bbox_dict['bbox']:
            continue
        
        if bbox_area(bbox_dict['bbox']) >= min_area:
            filtered.append(bbox_dict)
    
    return filtered


def filter_oversized_bboxes(bboxes: List[Dict], image_shape: Tuple[int, int], max_ratio: float = 0.25) -> List[Dict]:
    """
    Filter out bounding boxes that are too large (likely covering entire panels instead of specific damage).
    
    Args:
        bboxes: List of bbox dictionaries with 'bbox' key
        image_shape: Image shape as (height, width)
        max_ratio: Maximum ratio of bbox area to image area (default: 0.25 = 25%)
    
    Returns:
        Filtered list of bounding boxes (oversized boxes are removed, damage entry kept without bbox)
    """
    if not bboxes:
        return []
    
    img_h, img_w = image_shape
    image_area = img_h * img_w
    max_area = image_area * max_ratio
    
    filtered = []
    for bbox_dict in bboxes:
        bbox_dict_copy = bbox_dict.copy()
        
        if 'bbox' not in bbox_dict or not bbox_dict['bbox']:
            filtered.append(bbox_dict_copy)
            continue
        
        area = bbox_area(bbox_dict['bbox'])
        
        # If bbox is too large, remove it but keep the damage entry
        if area > max_area:
            bbox_dict_copy.pop('bbox', None)
            bbox_dict_copy['bbox_removed'] = 'oversized'
        
        filtered.append(bbox_dict_copy)
    
    return filtered


def convert_bbox_format(bbox: List[int], from_format: str = 'xywh', to_format: str = 'xyxy') -> List[int]:
    """
    Convert bounding box between different formats.
    
    Args:
        bbox: Bounding box coordinates
        from_format: Source format ('xywh' or 'xyxy')
        to_format: Target format ('xywh' or 'xyxy')
    
    Returns:
        Converted bounding box
    """
    if not bbox or len(bbox) < 4:
        return [0, 0, 0, 0]
    
    if from_format == to_format:
        return bbox
    
    if from_format == 'xywh' and to_format == 'xyxy':
        x, y, w, h = bbox
        return [x, y, x + w, y + h]
    
    elif from_format == 'xyxy' and to_format == 'xywh':
        x1, y1, x2, y2 = bbox
        return [x1, y1, x2 - x1, y2 - y1]
    
    return bbox
