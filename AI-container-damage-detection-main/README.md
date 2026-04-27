# Container Inspection AI - Production Ready

A production-grade automated shipping container inspection system using GPT-4 Vision and YOLOv8 for damage detection, OCR-based metadata extraction, and comprehensive reporting.

## ✨ NEW: Modern UI/UX (v2.0)

🎨 **Enterprise-grade interface redesign** with dark mode, animations, and professional styling!

- **Modern Dark Theme**: Teal accents on deep blue background
- **Smooth Animations**: Scan lines, hover effects, progress bars
- **Responsive Design**: Works beautifully on all devices
- **Enhanced UX**: Drag-and-drop upload, visual status indicators
- **Comprehensive Docs**: Complete design system and migration guide

👉 **[View UI Documentation](ui/README.md)** | **[See Before/After](BEFORE_AFTER_COMPARISON.md)** | **[React Migration Guide](REACT_MIGRATION_GUIDE.md)**

---

## 🚀 Features

### Core Capabilities
- **AI-Powered Damage Detection**: Dual-engine system combining GPT-4 Vision (primary) with YOLOv8 (validation)
- **Automated Metadata Extraction**: ISO 6346 compliant container ID extraction with multi-engine OCR
- **Comprehensive Reporting**: Automated PDF, Excel, and JSON reports with annotated images
- **Bounding Box Localization**: Precise damage localization with validated coordinates
- **Cost Estimation**: Intelligent repair cost estimation in INR with detailed breakdowns
- **Safety Assessment**: Automated safety concern identification and compliance checking
- **Modern Web Interface**: Enterprise-grade UI with dark mode and animations

### Technical Highlights
- **Multi-Engine OCR**: EasyOCR + Tesseract with intelligent fallback
- **Advanced Image Processing**: CLAHE enhancement, denoising, morphological operations
- **ISO 6346 Validation**: Container number validation with check digit verification
- **Confidence Scoring**: Multi-layered confidence assessment for quality control
- **PyTorch 2.6 Compatible**: Full compatibility with latest PyTorch versions
- **Custom UI Theme**: Professional dark mode with teal accents and smooth animations

## 📋 Prerequisites

- Python 3.10 or higher
- OpenAI API key (for GPT-4 Vision)
- Tesseract OCR installed on system
- 8GB+ RAM recommended
- GPU optional (CPU inference supported)

## 🔧 Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd ai_cdd2
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **Linux**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`

### 5. Configure Environment
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 6. Setup Models
```bash
python download_models.py
```

This creates base YOLOv8 models. For production use, train custom models on your container dataset and replace:
- `models/yolov8_master_detector.pt` (container ID, data plate detection)
- `models/yolov8_damage_detector.pt` (damage detection)

## 🚀 Quick Start

### Start Backend API
```bash
python start_backend.py
```
Or manually:
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Start Frontend UI
```bash
python start_frontend.py
```
Or manually:
```bash
streamlit run ui/app.py
```

### Access Application
- **Frontend UI**: http://localhost:8501 ✨ *Now with modern dark theme!*
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000

### First Time Users
1. Upload a container image using the drag-and-drop zone
2. Click "🚀 Run AI Inspection" and watch the scanning animation
3. View results with color-coded damage detection
4. Download reports in PDF, Excel, or JSON format

## 📁 Project Structure

```
ai_cdd2/
├── api/                    # FastAPI backend
│   ├── main.py            # API endpoints
│   └── __init__.py
├── core/                   # Core processing modules
│   ├── pipeline.py        # Main inspection pipeline
│   ├── detection.py       # YOLO detection wrapper
│   ├── ocr.py            # OCR engine
│   ├── llm_validator.py  # GPT-4 Vision integration
│   ├── analysis.py       # Damage analysis & grading
│   ├── reporting.py      # Report generation
│   ├── bbox_utils.py     # Bounding box utilities
│   ├── pytorch_compat.py # PyTorch compatibility
│   └── utils.py          # Helper functions
├── ui/                    # Streamlit frontend (v2.0 - Modern UI)
│   ├── app.py            # Redesigned web interface
│   ├── styles.css        # Custom dark theme
│   ├── interactions.js   # Micro-interactions
│   ├── README.md         # UI documentation
│   ├── DESIGN_SYSTEM.md  # Design system guide
│   └── UI_MOCKUPS.md     # Visual mockups
├── configs/               # Configuration files
│   ├── config.yaml       # Main configuration
│   └── api_config.yaml   # API configuration
├── models/                # YOLO model weights
│   ├── yolov8_master_detector.pt
│   ├── yolov8_damage_detector.pt
│   └── README.md
├── data/                  # Data directory
│   ├── outputs/          # Generated reports (gitignored)
│   └── README.md
├── requirements.txt       # Python dependencies
├── download_models.py     # Model setup script
├── start_backend.py       # Backend launcher
├── start_frontend.py      # Frontend launcher
├── README.md              # This file
├── UI_IMPLEMENTATION_SUMMARY.md   # UI overview
├── BEFORE_AFTER_COMPARISON.md     # UI transformation
└── REACT_MIGRATION_GUIDE.md       # React upgrade path
```

## 🔌 API Usage

### Inspect Container
```bash
curl -X POST "http://localhost:8000/inspect" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@container_image.jpg"
```

### Get Report
```bash
curl "http://localhost:8000/report/{report_id}"
```

### Download Artifacts
```bash
curl "http://localhost:8000/download/{report_id}/pdf" -o report.pdf
curl "http://localhost:8000/download/{report_id}/excel" -o report.xlsx
curl "http://localhost:8000/download/{report_id}/image" -o annotated.jpg
```

## ⚙️ Configuration

Edit `configs/config.yaml` to customize:
- Model paths and confidence thresholds
- Damage classification and severity mapping
- Repair cost estimates (INR)
- GPT-4 prompts and parameters
- OCR settings

## 🎯 Model Training

For production deployment, train custom models:

1. **Collect Dataset**: 1000+ annotated container images
2. **Annotation**: Use tools like Roboflow or LabelImg
3. **Train YOLOv8**: Follow `models/README.md` guide
4. **Replace Models**: Place trained weights in `models/` directory
5. **Update Config**: Modify class names in `configs/config.yaml`

## 🐛 Troubleshooting

### PyTorch Compatibility Issues
If you encounter YOLO model loading errors:
```bash
# Remove corrupted models
rm models/*.pt

# Re-download base models
python download_models.py
```

### OCR Not Working
Ensure Tesseract is installed and in PATH:
```bash
tesseract --version
```

### API Connection Errors
Check if backend is running:
```bash
curl http://localhost:8000
```

### Low Confidence Scores
- Ensure good image quality (well-lit, clear, high resolution)
- Train custom models on your specific container types
- Adjust confidence thresholds in `configs/config.yaml`

## 📊 Output Format

### JSON Report Structure
```json
{
  "report_id": "uuid",
  "container_id": "CPIU1811772",
  "condition": "Poor",
  "estimated_cost": 45000,
  "detected_damages": [
    {
      "type": "bent_frame",
      "severity": "major",
      "zone": "door",
      "confidence": 0.92,
      "bbox": [x, y, width, height],
      "location_code": "07",
      "repair_priority": "high"
    }
  ],
  "artifacts": {
    "annotated_image": "path/to/image.jpg",
    "pdf_report": "path/to/report.pdf",
    "excel_report": "path/to/report.xlsx"
  }
}
```

## 🎨 Modern UI Features (v2.0)

### Visual Design
- **Dark Mode Theme**: Professional deep blue background with teal accents
- **Gradient Effects**: Subtle gradients on cards and headers
- **Color-Coded Status**: Instant visual feedback (Green=Good, Red=Critical)
- **Smooth Animations**: Scan lines, hover effects, progress bars
- **Responsive Layout**: Works on mobile, tablet, and desktop

### User Experience
- **Drag-and-Drop Upload**: Easy file upload with visual feedback
- **Animated Scanning**: Laser-like sweep during AI processing
- **Metric Cards**: Beautiful gradient cards with icons
- **Visual Indicators**: Real-time API/AI status with colored dots
- **Expandable Sections**: Collapsible damage details and analysis

### Accessibility
- **WCAG AA Compliant**: 7:1 contrast ratio for text
- **Keyboard Navigation**: Full keyboard support
- **Screen Reader Support**: ARIA labels and semantic HTML
- **Reduced Motion**: Respects user preferences

### Documentation
- **[UI README](ui/README.md)**: Complete UI documentation
- **[Design System](ui/DESIGN_SYSTEM.md)**: Colors, typography, components
- **[UI Mockups](ui/UI_MOCKUPS.md)**: Visual wireframes and layouts
- **[Before/After](BEFORE_AFTER_COMPARISON.md)**: See the transformation
- **[React Migration](REACT_MIGRATION_GUIDE.md)**: Upgrade path to React/Next.js

### Customization
The UI is fully customizable via CSS variables in `ui/styles.css`:
```css
:root {
    --primary-teal: #00C7B7;      /* Change to your brand color */
    --deep-blue: #0F172A;         /* Change background */
}
```

## 🔒 Security Notes

- Never commit `.env` file with API keys
- Use environment variables for sensitive data
- Implement authentication for production deployment
- Sanitize file uploads to prevent malicious files
- Rate limit API endpoints

## 📝 License

This project is proprietary. All rights reserved.

## 🤝 Support

For issues, questions, or feature requests, please contact the development team."# container-damage-detection" 
"# container-damage-detection" 
