# core/location_code_manager.py
"""
Location Code Manager for Container Damage Detection

Location Code Format:
- First letter indicates side/position:
  L = Left, R = Right, T = Top, D = Door, B = Bottom, 
  U = Underneath, F = Front, M = Machinery, I = Inside, E = End
- Second letter indicates component type:
  T = Top rail, B = Bottom rail, N = Panel, H = Hinge, 
  X = Cross member, R = Rail, L = Locking, G = Gasket
- Numbers indicate panel/section position (01-99)
- N suffix often indicates "Near" or specific sub-location
- W suffix indicates "Wide" or full width
"""

import os
import pandas as pd
from typing import Optional, List, Dict, Tuple


class LocationCodeManager:
    """Manages container damage location codes based on industry standards."""
    
    # Position prefix mapping
    POSITION_PREFIX = {
        'left': 'L',
        'right': 'R', 
        'top': 'T',
        'door': 'D',
        'bottom': 'B',
        'underneath': 'U',
        'front': 'F',
        'rear': 'E',  # End
        'back': 'E',
        'machinery': 'M',
        'inside': 'I',
    }
    
    # Component type mapping (second letter)
    COMPONENT_TYPE = {
        'rail': 'R',
        'panel': 'N',
        'hinge': 'H',
        'cross_member': 'X',
        'locking': 'L',
        'gasket': 'G',
        'top_rail': 'T',
        'bottom_rail': 'B',
        'corner_post': 'C',
        'frame': 'F',
        'floor': 'L',
        'roof': 'T',
    }
    
    # Zone to position mapping
    ZONE_TO_POSITION = {
        'door': 'door',
        'side_panel': 'left',  # Default, will be refined by bbox position
        'side': 'left',
        'roof': 'top',
        'floor': 'bottom',
        'corner_post': 'left',  # Will be refined
        'rail': 'left',
        'hinge': 'door',
        'frame': 'left',
        'front': 'front',
        'rear': 'rear',
        'left': 'left',
        'right': 'right',
        'top': 'top',
        'bottom': 'bottom',
    }
    
    def __init__(self, excel_path: str = None):
        """Initialize with optional Excel file containing valid location codes."""
        self.valid_codes = set()
        self.code_list = []
        
        if excel_path and os.path.exists(excel_path):
            self._load_codes_from_excel(excel_path)
        else:
            # Try default path
            default_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                'Location code.xlsx'
            )
            if os.path.exists(default_path):
                self._load_codes_from_excel(default_path)
    
    def _load_codes_from_excel(self, excel_path: str):
        """Load valid location codes from Excel file."""
        try:
            df = pd.read_excel(excel_path)
            # Find the column containing location codes
            for col in df.columns:
                if 'location' in col.lower() or 'code' in col.lower():
                    codes = df[col].dropna().astype(str).tolist()
                    self.valid_codes = set(codes)
                    self.code_list = codes
                    break
            
            # If no matching column found, try the last column
            if not self.valid_codes:
                codes = df.iloc[:, -1].dropna().astype(str).tolist()
                self.valid_codes = set(codes)
                self.code_list = codes
                
            print(f"INFO: Loaded {len(self.valid_codes)} valid location codes from {excel_path}")
        except Exception as e:
            print(f"WARNING: Could not load location codes from Excel: {e}")
    
    def generate_location_code(
        self, 
        zone: str, 
        bbox: List[int] = None, 
        image_width: int = None,
        image_height: int = None,
        damage_type: str = None
    ) -> str:
        """
        Generate a location code based on damage zone and position.
        
        Args:
            zone: Damage zone (door, side_panel, roof, etc.)
            bbox: Bounding box [x, y, width, height]
            image_width: Image width for position calculation
            image_height: Image height for position calculation
            damage_type: Type of damage for component inference
            
        Returns:
            Location code string (e.g., 'LN45', 'DR23', 'TB12')
        """
        zone_lower = zone.lower() if zone else 'unknown'
        
        # Determine position (first letter)
        position = self.ZONE_TO_POSITION.get(zone_lower, 'left')
        
        # Refine position based on bbox location in image
        if bbox and image_width:
            center_x = bbox[0] + bbox[2] / 2
            relative_x = center_x / image_width
            
            # Determine left/right based on horizontal position
            if zone_lower in ['side_panel', 'side', 'corner_post', 'rail', 'frame']:
                if relative_x < 0.4:
                    position = 'left'
                elif relative_x > 0.6:
                    position = 'right'
        
        position_letter = self.POSITION_PREFIX.get(position, 'L')
        
        # Determine component type (second letter)
        component = self._infer_component(zone_lower, damage_type)
        component_letter = self.COMPONENT_TYPE.get(component, 'N')
        
        # Calculate panel number based on position
        panel_number = self._calculate_panel_number(bbox, image_width, image_height)
        
        # Build the code
        code = f"{position_letter}{component_letter}{panel_number}"
        
        # Validate against known codes and find closest match
        validated_code = self._validate_or_find_closest(code)
        
        return validated_code
    
    def _infer_component(self, zone: str, damage_type: str = None) -> str:
        """Infer component type from zone and damage type."""
        zone_to_component = {
            'door': 'panel',
            'side_panel': 'panel',
            'side': 'panel',
            'roof': 'top_rail',
            'floor': 'floor',
            'corner_post': 'corner_post',
            'rail': 'rail',
            'hinge': 'hinge',
            'frame': 'frame',
        }
        return zone_to_component.get(zone, 'panel')
    
    def _calculate_panel_number(
        self, 
        bbox: List[int], 
        image_width: int, 
        image_height: int
    ) -> str:
        """Calculate panel number based on damage position."""
        if not bbox or not image_width or not image_height:
            return "1N"  # Default
        
        # Calculate center position
        center_x = bbox[0] + bbox[2] / 2
        center_y = bbox[1] + bbox[3] / 2
        
        # Divide container into grid (10 horizontal x 10 vertical sections)
        x_section = min(9, int((center_x / image_width) * 10))
        y_section = min(9, int((center_y / image_height) * 10))
        
        # Generate panel number (1-99)
        panel_num = y_section * 10 + x_section + 1
        
        # Format as 2 digits or digit + N
        if panel_num < 10:
            return f"{panel_num}N"
        else:
            return str(panel_num)
    
    def _validate_or_find_closest(self, code: str) -> str:
        """Validate code against known codes or find closest match."""
        if not self.valid_codes:
            return code
        
        # Check if exact match exists
        if code in self.valid_codes:
            return code
        
        # Try variations
        variations = [
            code,
            code + 'N',
            code[:-1] if code.endswith('N') else code,
            code[:2] + code[2:].zfill(2),
        ]
        
        for var in variations:
            if var in self.valid_codes:
                return var
        
        # Find closest match by prefix
        prefix = code[:2]
        matching_codes = [c for c in self.valid_codes if c.startswith(prefix)]
        if matching_codes:
            return matching_codes[0]
        
        # Find by first letter only
        first_letter = code[0]
        matching_codes = [c for c in self.valid_codes if c.startswith(first_letter)]
        if matching_codes:
            # Try to find one with similar number
            return matching_codes[0]
        
        # Return original if no match found
        return code
    
    def get_code_description(self, code: str) -> str:
        """Get human-readable description of a location code."""
        if len(code) < 2:
            return "Unknown location"
        
        position_desc = {
            'L': 'Left',
            'R': 'Right',
            'T': 'Top',
            'D': 'Door',
            'B': 'Bottom',
            'U': 'Underneath',
            'F': 'Front',
            'M': 'Machinery',
            'I': 'Inside',
            'E': 'End/Rear',
        }
        
        component_desc = {
            'T': 'Top Rail',
            'B': 'Bottom Rail',
            'N': 'Panel',
            'H': 'Hinge',
            'X': 'Cross Member',
            'R': 'Rail',
            'L': 'Locking/Floor',
            'G': 'Gasket',
            'C': 'Corner Post',
            'F': 'Frame',
        }
        
        pos = position_desc.get(code[0], 'Unknown')
        comp = component_desc.get(code[1], 'Section')
        section = code[2:] if len(code) > 2 else ''
        
        return f"{pos} {comp} {section}".strip()
    
    def get_all_valid_codes(self) -> List[str]:
        """Return list of all valid location codes."""
        return self.code_list
    
    def is_valid_code(self, code: str) -> bool:
        """Check if a code is in the valid codes list."""
        return code in self.valid_codes


# Singleton instance for easy access
_location_manager = None

def get_location_manager(excel_path: str = None) -> LocationCodeManager:
    """Get or create the location code manager singleton."""
    global _location_manager
    if _location_manager is None:
        _location_manager = LocationCodeManager(excel_path)
    return _location_manager
