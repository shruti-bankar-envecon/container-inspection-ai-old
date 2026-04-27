# api/main.py
import io
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path

from core.pipeline import InspectionPipeline

app = FastAPI(
    title="CONTAINER INSPECTION API",
    description="Advanced container damage detection and analysis using GPT-5 Vision and traditional computer vision",
    version="2.0.0"
)
pipeline = InspectionPipeline()
REPORTS_DB = {} # Simple in-memory cache for reports

@app.post("/inspect", tags=["Inspection"])
async def inspect_container(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
    
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    report = pipeline.run(img)
    if 'report_id' in report:
        REPORTS_DB[report['report_id']] = report
    return JSONResponse(content=report)

@app.get("/report/{report_id}", tags=["Reports"])
def get_report(report_id: str):
    report = REPORTS_DB.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")
    return JSONResponse(content=report)

@app.get("/download/{report_id}/{file_type}", tags=["Reports"])
def download_artifact(report_id: str, file_type: str):
    report = REPORTS_DB.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    key_map = {"image": "annotated_image", "pdf": "pdf_report", "excel": "excel_report"}
    file_path = report.get('artifacts', {}).get(key_map.get(file_type))

    if file_path and Path(file_path).exists():
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Artifact file not found")