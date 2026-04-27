# Data Directory

This directory contains input and output data for the container inspection system.

## Directory Structure

- `input/` - Place your container images here for inspection
- `outputs/` - Generated reports, annotated images, and analysis results are saved here

## Supported Image Formats

- JPG/JPEG
- PNG
- Other formats supported by OpenCV

## Output Files

The system generates several output files for each inspection:
- `{report_id}.json` - Complete inspection data in JSON format
- `{report_id}_annotated.jpg` - Image with damage and metadata annotations
- `{report_id}.pdf` - Professional PDF report
- `{report_id}.xlsx` - Excel spreadsheet with detailed data
