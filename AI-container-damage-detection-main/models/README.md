
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
