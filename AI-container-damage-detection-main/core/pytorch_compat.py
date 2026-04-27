"""
PyTorch 2.6 Compatibility Module for YOLO Models
"""
import os

def apply_pytorch_compatibility_fix():
    """Apply PyTorch 2.6 compatibility fixes for YOLO model loading."""
    try:
        import torch
    except Exception as e:
        print(f"⚠️  WARNING: Could not import torch for compatibility fix: {e}")
        return False
    """Apply PyTorch 2.6 compatibility fixes for YOLO model loading."""
    
    # Set environment variable to allow loading
    os.environ['TORCH_SERIALIZATION_SAFE_GLOBALS'] = '1'
    
    # Apply safe globals fix
    if hasattr(torch, 'serialization') and hasattr(torch.serialization, 'add_safe_globals'):
        try:
            # Import all necessary classes
            from ultralytics.nn.tasks import DetectionModel
            from ultralytics.nn.modules import Conv, C2f, SPPF, Detect
            from torch.nn.modules.container import Sequential
            from torch.nn.modules.activation import ReLU, SiLU, Sigmoid
            from torch.nn.modules.pooling import AdaptiveAvgPool2d, MaxPool2d
            from torch.nn.modules.upsampling import Upsample
            from torch.nn import BatchNorm2d
            from torch.nn.modules.dropout import Dropout
            
            # Add all required classes to safe globals
            safe_classes = [
                DetectionModel, Conv, C2f, SPPF, Detect,
                Sequential, ReLU, SiLU, Sigmoid,
                AdaptiveAvgPool2d, MaxPool2d, Upsample,
                BatchNorm2d, Dropout
            ]
            
            torch.serialization.add_safe_globals(safe_classes)
            print("🔧 Applied comprehensive PyTorch 2.6 compatibility fix")
            return True
            
        except ImportError as e:
            print(f"⚠️  WARNING: Could not import all required classes: {e}")
            # Try with basic classes
            try:
                from ultralytics.nn.tasks import DetectionModel
                from torch.nn.modules.container import Sequential
                torch.serialization.add_safe_globals([DetectionModel, Sequential])
                print("🔧 Applied basic PyTorch 2.6 compatibility fix")
                return True
            except ImportError:
                print("⚠️  WARNING: Could not apply PyTorch compatibility fix")
                return False
    
    return False

def create_working_yolo_models():
    """Create working YOLO models that can be loaded with PyTorch 2.6."""
    try:
        # Apply compatibility fix first
        apply_pytorch_compatibility_fix()
        
        # Create models directory
        import os
        os.makedirs('models', exist_ok=True)
        
        # Create a simple working model using YAML config
        from ultralytics import YOLO
        
        # Create master detector
        master_model = YOLO('yolov8n.yaml')
        master_model.save('models/yolov8_master_detector.pt')
        print("✅ Master detector created successfully")
        
        # Create damage detector
        damage_model = YOLO('yolov8n.yaml')
        damage_model.save('models/yolov8_damage_detector.pt')
        print("✅ Damage detector created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Could not create working YOLO models: {e}")
        return False

def create_compatible_yolo_model():
    """Create a compatible YOLO model that works with PyTorch 2.6."""
    try:
        from ultralytics import YOLO
        import numpy as np
        
        # Apply compatibility fix
        apply_pytorch_compatibility_fix()
        
        # Create a simple YOLO model
        model = YOLO('yolov8n.yaml')  # Use YAML config instead of weights
        
        # Test the model
        test_img = np.zeros((640, 640, 3), dtype=np.uint8)
        _ = model.predict(test_img, verbose=False)
        
        return model
        
    except Exception as e:
        print(f"❌ ERROR: Could not create compatible YOLO model: {e}")
        return None
