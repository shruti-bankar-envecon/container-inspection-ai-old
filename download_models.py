#!/usr/bin/env python3
"""
Download and setup YOLO models for Container Inspection AI
"""
import os
import requests
from pathlib import Path
from ultralytics import YOLO

def download_yolo_model(model_name, model_path):
    """Create a working YOLO model with PyTorch 2.6 compatibility."""
    print(f"📥 Creating {model_name}...")
    try:
        # Create models directory if it doesn't exist
        os.makedirs("models", exist_ok=True)
        
        # Apply PyTorch 2.6 compatibility fix
        from core.pytorch_compat import apply_pytorch_compatibility_fix
        apply_pytorch_compatibility_fix()
        
        # Simply copy the existing yolov8n.pt file to create our models
        # This ensures we have properly formatted model files
        import shutil
        if os.path.exists('yolov8n.pt'):
            shutil.copy('yolov8n.pt', model_path)
            print(f"✅ {model_name} created successfully at {model_path}")
            return True
        else:
            # If no existing model, download a fresh one
            model = YOLO('yolov8n.pt')  # This will download if not present
            
            # Test the model
            import numpy as np
            test_img = np.zeros((640, 640, 3), dtype=np.uint8)
            _ = model.predict(test_img, verbose=False)
            
            # Save the model
            model.save(model_path)
            
            print(f"✅ {model_name} created and tested successfully at {model_path}")
            return True
            
    except Exception as e:
        print(f"❌ Failed to create {model_name}: {e}")
        return False

def download_custom_models():
    """Download custom trained models for container inspection."""
    print("🚀 Setting up Container Inspection AI Models...")
    print("=" * 50)
    
    # Model configurations
    models = [
        {
            "name": "yolov8n.pt",
            "path": "models/yolov8_master_detector.pt",
            "description": "Master detector for container metadata (ID, data plate, etc.)"
        },
        {
            "name": "yolov8n.pt", 
            "path": "models/yolov8_damage_detector.pt",
            "description": "Damage detector for dents, rust, cracks, etc."
        }
    ]
    
    success_count = 0
    for model in models:
        print(f"\n📦 {model['description']}")
        if download_yolo_model(model["name"], model["path"]):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Download Summary: {success_count}/{len(models)} models downloaded")
    
    if success_count == len(models):
        print("🎉 All models downloaded successfully!")
        print("\n📝 Next steps:")
        print("1. Train custom models on your container dataset")
        print("2. Replace the downloaded models with your trained weights")
        print("3. Update the class names in configs/config.yaml")
    else:
        print("⚠️  Some models failed to download. Check your internet connection.")
        print("💡 You can also manually place your trained models in the models/ directory")

def create_model_info():
    """Create model information file."""
    model_info = """
# Container Inspection AI - Model Information

## Required Models

### 1. Master Detector (yolov8_master_detector.pt)
- **Purpose**: Detects container metadata regions
- **Classes**: container_id, data_plate, license_plate, seal, logo
- **Input**: Full container image
- **Output**: Bounding boxes for metadata regions

### 2. Damage Detector (yolov8_damage_detector.pt)
- **Purpose**: Detects container damage
- **Classes**: dent, crack, rust, scratch, hole, seal_issue
- **Input**: Full container image
- **Output**: Bounding boxes for damage regions

## Training Recommendations

1. **Dataset**: Collect 1000+ container images with annotations
2. **Augmentation**: Use rotation, brightness, contrast variations
3. **Classes**: Ensure balanced representation of all classes
4. **Validation**: Use 20% of data for validation
5. **Epochs**: Train for 100-300 epochs depending on dataset size

## Model Performance Targets

- **mAP@0.5**: >0.8 for master detector
- **mAP@0.5**: >0.7 for damage detector
- **Inference Time**: <100ms per image
- **Model Size**: <50MB per model

## Usage

Once you have trained models:
1. Place them in the `models/` directory
2. Update class names in `configs/config.yaml`
3. The system will automatically use real models instead of mocks
"""
    
    with open("models/README.md", "w") as f:
        f.write(model_info)
    print("📄 Created models/README.md with training guidelines")

if __name__ == "__main__":
    print("🔧 Container Inspection AI - Model Setup")
    print("=" * 50)
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Download base models
    download_custom_models()
    
    # Create model information
    create_model_info()
    
    print("\n🎯 Ready to train your custom models!")
