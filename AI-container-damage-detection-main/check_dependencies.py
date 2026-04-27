#!/usr/bin/env python3
"""
Dependency Check Script for Container Inspection AI
Checks if all required dependencies are properly installed.
"""
import sys

def check_dependency(name, import_name=None):
    """Check if a dependency can be imported."""
    if import_name is None:
        import_name = name
    
    try:
        __import__(import_name)
        print(f"[OK] {name}")
        return True
    except ImportError as e:
        print(f"[FAIL] {name}: {e}")
        return False
    except Exception as e:
        print(f"[WARN] {name}: {e}")
        return False

def main():
    print("=" * 60)
    print("Container Inspection AI - Dependency Check")
    print("=" * 60)
    print()
    
    dependencies = [
        ("cv2 (OpenCV)", "cv2"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("streamlit", "streamlit"),
        ("PIL (Pillow)", "PIL"),
        ("yaml", "yaml"),
        ("openai", "openai"),
        ("scikit-image", "skimage"),
        ("shapely", "shapely"),
        ("easyocr", "easyocr"),
        ("pytesseract", "pytesseract"),
    ]
    
    results = []
    for name, import_name in dependencies:
        results.append(check_dependency(name, import_name))
    
    print()
    print("=" * 60)
    print("PyTorch Check (Critical for AI features)")
    print("=" * 60)
    
    torch_ok = check_dependency("torch", "torch")
    
    if not torch_ok:
        print()
        print("[WARNING] PyTorch DLL Loading Error Detected!")
        print()
        print("This is a common Windows issue. To fix it:")
        print()
        print("1. Download and install Microsoft Visual C++ Redistributables:")
        print("   https://aka.ms/vs/17/release/vc_redist.x64.exe")
        print()
        print("2. After installation, restart your terminal/IDE")
        print()
        print("3. Try running the project again")
        print()
        print("Alternative: If the above doesn't work, try:")
        print("   pip uninstall torch torchvision")
        print("   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu")
        print()
    
    if torch_ok:
        try:
            import torch
            print(f"   PyTorch version: {torch.__version__}")
            print(f"   CUDA available: {torch.cuda.is_available()}")
        except:
            pass
    
    print()
    print("=" * 60)
    print("Ultralytics Check (Required for YOLO models)")
    print("=" * 60)
    
    ultralytics_ok = check_dependency("ultralytics", "ultralytics")
    
    if not ultralytics_ok and torch_ok:
        print("   Note: Ultralytics requires PyTorch to be working")
    
    print()
    print("=" * 60)
    
    all_basic = all(results)
    
    if all_basic and torch_ok and ultralytics_ok:
        print("[SUCCESS] All dependencies are installed and working!")
        return 0
    elif all_basic:
        print("[WARNING] Basic dependencies OK, but PyTorch/Ultralytics has issues")
        print("   The API may start but AI features won't work")
        return 1
    else:
        print("[ERROR] Some dependencies are missing")
        return 2

if __name__ == "__main__":
    sys.exit(main())
