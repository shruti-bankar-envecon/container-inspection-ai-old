# core/utils.py
import yaml
import cv2
import numpy as np
from dotenv import load_dotenv
import os
import json
import re

def load_config():
    """Loads the main YAML configuration file and API key from .env."""
    with open('configs/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    load_dotenv()
    config['llm']['api_key'] = os.getenv("OPENAI_API_KEY")
    if not config['llm']['api_key']:
        print("WARNING: OPENAI_API_KEY not found in .env file. LLM Validator will not work.")
    return config

def format_currency_inr(amount: float) -> str:
    """Format currency in Indian format: Rs. 29.88K, Rs. 2.5L, Rs. 1.2Cr"""
    if amount >= 10000000:  # 1 Crore or more
        return f"Rs. {amount/10000000:.2f}Cr"
    elif amount >= 100000:  # 1 Lakh or more
        return f"Rs. {amount/100000:.2f}L"
    elif amount >= 1000:  # 1 Thousand or more
        return f"Rs. {amount/1000:.2f}K"
    else:
        return f"Rs. {amount:.0f}"

def draw_results_on_image(image: np.ndarray, damages: list, metadata_rois: list, container_id: str, container_details: dict = None) -> np.ndarray:
    """Draws bounding boxes and labels for damages and location codes on the image.
    
    Displays damage boxes with location codes for easy identification.
    """
    drawn_image = image.copy()
    
    # Draw damage boxes (Red) - bounding boxes only, no labels
    for damage in damages:
        if 'bbox' not in damage or not damage['bbox'] or len(damage['bbox']) < 4:
            continue
        x, y, w, h = damage['bbox']
        # Ensure coordinates are integers
        x, y, w, h = int(x), int(y), int(w), int(h)
        # Draw the bounding box only
        cv2.rectangle(drawn_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    # Draw location codes and identification markers (NO LABELS - boxes only)
    if container_details:
        # Container number bbox (Green) - no label
        if container_details.get('container_number_bbox'):
            bbox = container_details['container_number_bbox']
            if bbox and len(bbox) >= 4:
                x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
                cv2.rectangle(drawn_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Data plate bbox (Cyan) - no label
        if container_details.get('data_plate_info') and container_details['data_plate_info'].get('bbox'):
            bbox = container_details['data_plate_info']['bbox']
            if bbox and len(bbox) >= 4:
                x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
                cv2.rectangle(drawn_image, (x, y), (x + w, y + h), (255, 255, 0), 2)
        
        # Location codes (Yellow) - no labels
        if container_details.get('location_codes'):
            for loc_code in container_details['location_codes']:
                bbox = loc_code.get('bbox')
                if bbox and len(bbox) >= 4:
                    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
                    cv2.rectangle(drawn_image, (x, y), (x + w, y + h), (0, 255, 255), 2)
    
    # Fallback: Draw YOLO metadata ROIs if no GPT-5 container details (no labels)
    if not container_details or not container_details.get('container_number_bbox'):
        for roi in metadata_rois:
            x, y, w, h = roi['bbox']
            x, y, w, h = int(x), int(y), int(w), int(h)
            cv2.rectangle(drawn_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # No legend box on image - will be displayed separately in UI
    return drawn_image

def _iso6346_check_digit(owner: str, serial: str) -> int:
    """Compute ISO 6346 check digit for owner (4 letters) + serial (6 digits)."""
    # Mapping A=10, B=12, ... Z=38 (2^position % 11 % 10)
    weights = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    def char_value(ch: str) -> int:
        if ch.isdigit():
            return int(ch)
        # Letters: A=10, B=12, ... Z=38 skipping 11,22,33
        val = ord(ch) - 55  # A->10
        return val
    code = (owner + serial).upper()
    total = 0
    for i, ch in enumerate(code):
        total += char_value(ch) * weights[i]
    return (total % 11) % 10

def extract_iso6346_from_text(raw_text: str) -> str:
    """Find and validate ISO 6346 container number in raw OCR text.
    Returns normalized string like ABCD1234567 or "N/A" if none.
    """
    if not raw_text:
        return "N/A"
    text = re.sub(r"[^A-Za-z0-9]", "", raw_text).upper()
    # Search over all 11-length windows
    for i in range(0, max(0, len(text) - 10)):
        cand = text[i:i+11]
        if len(cand) < 11:
            break
        if not re.match(r"^[A-Z]{4}[0-9]{7}$", cand):
            continue
        owner = cand[:4]
        serial = cand[4:10]
        check = int(cand[10])
        if _iso6346_check_digit(owner, serial) == check:
            return cand
    return "N/A"