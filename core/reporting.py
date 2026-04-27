# core/reporting.py
import pandas as pd
try:
    from fpdf import FPDF
except ModuleNotFoundError:
    FPDF = None
from pathlib import Path
import json
from datetime import datetime

def generate_reports(report_data: dict, annotated_image_path: str, output_dir: Path):
    """Generate enhanced Excel and PDF reports. Uses ASCII-only characters for PDF compatibility."""
    # Ensure strings are compatible with FPDF core fonts (latin-1)
    def _safe(text: str) -> str:
        if text is None:
            return ""
        try:
            text.encode("latin-1")
            return text
        except Exception:
            return text.encode("latin-1", "ignore").decode("latin-1")

    report_id = report_data['report_id']
    base_path = output_dir / report_id

    # Excel Report
    excel_path = base_path.with_suffix('.xlsx')
    damage_df = pd.DataFrame(report_data['detected_damages'])

    currency = report_data.get('currency', 'INR')
    discard_status = report_data.get('discard_status', {})
    
    summary_data = {
        "Container ID": report_data['container_id'],
        "Container Type": report_data.get('container_type', 'N/A'),
        "Container Owner": report_data.get('container_owner', 'N/A'),
        "Overall Condition": report_data['condition'],
        "Structural Integrity": report_data.get('structural_integrity', 'Unknown'),
        f"Total Estimated Cost ({currency})": report_data['estimated_cost'],
        "Reusable": "Yes" if discard_status.get('reusable', True) else "No",
        "Discard Reason": discard_status.get('reason', 'N/A'),
        "Confidence": f"{report_data['confidence']:.0%}",
        "GPT-5 Confidence": f"{report_data.get('gpt5_analysis', {}).get('confidence_score', 0):.0%}" if 'gpt5_analysis' in report_data else "N/A",
        "Safety Concerns Count": len(report_data.get('safety_concerns', [])),
        "Maintenance Recommendations Count": len(report_data.get('maintenance_recommendations', []))
    }
    summary_df = pd.DataFrame([summary_data])
    
    # Extract location codes if available
    location_codes_data = []
    if 'container_details' in report_data and report_data['container_details']:
        container_details = report_data['container_details']
        if 'location_codes' in container_details:
            for loc_code in container_details['location_codes']:
                location_codes_data.append({
                    'Code': loc_code.get('code', 'N/A'),
                    'Type': loc_code.get('type', 'N/A'),
                    'Text Content': loc_code.get('text_content', 'N/A')
                })
    location_codes_df = pd.DataFrame(location_codes_data) if location_codes_data else None

    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        summary_df.to_excel(writer, sheet_name="Inspection Summary", index=False)
        if not damage_df.empty:
            damage_df.to_excel(writer, sheet_name="Damage Details", index=False)
        if location_codes_df is not None and not location_codes_df.empty:
            location_codes_df.to_excel(writer, sheet_name="Location Codes", index=False)
        if 'gpt5_analysis' in report_data:
            gpt5_data = report_data['gpt5_analysis']
            gpt5_summary = {
                'Metric': ['Overall Condition', 'Structural Integrity', 'Confidence Score', 'Safety Concerns Count'],
                'Value': [
                    gpt5_data.get('overall_condition', 'Unknown'),
                    gpt5_data.get('structural_integrity', 'Unknown'),
                    f"{gpt5_data.get('confidence_score', 0):.0%}",
                    len(gpt5_data.get('safety_concerns', []))
                ]
            }
            pd.DataFrame(gpt5_summary).to_excel(writer, sheet_name="GPT5_Analysis", index=False)
        if report_data.get('safety_concerns'):
            pd.DataFrame({'Safety Concern': report_data['safety_concerns']}).to_excel(writer, sheet_name="Safety_Concerns", index=False)
        if report_data.get('maintenance_recommendations'):
            pd.DataFrame({'Recommendation': report_data['maintenance_recommendations']}).to_excel(writer, sheet_name="Maintenance", index=False)
        if 'enhanced_analysis' in report_data and report_data['enhanced_analysis']:
            enhanced = report_data['enhanced_analysis']
            enhanced_data = []
            if 'safety_assessment' in enhanced:
                enhanced_data.append({'Field': 'Safety Assessment', 'Value': enhanced['safety_assessment']})
            if 'compliance_status' in enhanced:
                enhanced_data.append({'Field': 'Compliance Status', 'Value': enhanced['compliance_status']})
            if enhanced_data:
                pd.DataFrame(enhanced_data).to_excel(writer, sheet_name="Enhanced_Analysis", index=False)

    # PDF Report
    pdf_path = base_path.with_suffix('.pdf')
    if FPDF is None:
        return {"pdf_report": None, "excel_report": str(excel_path)}

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, _safe(f"Container Inspection Report (GPT-5 Enhanced): {report_data['container_id']}"), 0, 1, 'C')
    pdf.ln(5)

    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, _safe(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), 0, 1, 'C')
    pdf.ln(5)

    # Annotated image
    pdf.image(annotated_image_path, x=10, y=40, w=190)
    pdf.ln(155)

    # Basic information table
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(95, 10, _safe("Container ID:"), 1)
    pdf.set_font("Arial", '', 12)
    pdf.cell(95, 10, _safe(report_data['container_id']), 1, 1)

    if 'container_type' in report_data:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(95, 10, _safe("Container Type:"), 1)
        pdf.set_font("Arial", '', 12)
        pdf.cell(95, 10, _safe(report_data.get('container_type', 'N/A')), 1, 1)
    
    if 'container_owner' in report_data:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(95, 10, _safe("Owner Code:"), 1)
        pdf.set_font("Arial", '', 12)
        pdf.cell(95, 10, _safe(report_data.get('container_owner', 'N/A')), 1, 1)
    
    if 'size_type_code' in report_data:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(95, 10, _safe("Size/Type Code:"), 1)
        pdf.set_font("Arial", '', 12)
        pdf.cell(95, 10, _safe(report_data.get('size_type_code', 'N/A')), 1, 1)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(95, 10, _safe("Overall Condition:"), 1)
    pdf.set_font("Arial", '', 12)
    pdf.cell(95, 10, _safe(report_data['condition']), 1, 1)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(95, 10, _safe("Structural Integrity:"), 1)
    pdf.set_font("Arial", '', 12)
    pdf.cell(95, 10, _safe(report_data.get('structural_integrity', 'Unknown')), 1, 1)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(95, 10, _safe("Total Estimated Repair Cost:"), 1)
    pdf.set_font("Arial", '', 12)
    currency_symbol = "Rs." if currency == 'INR' else "$"
    pdf.cell(95, 10, _safe(f"{currency_symbol}{report_data['estimated_cost']:.2f} {currency}"), 1, 1)
    
    # Discard status
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(95, 10, _safe("Reusable Status:"), 1)
    pdf.set_font("Arial", '', 12)
    reusable_text = "Yes" if discard_status.get('reusable', True) else "No - DISCARD"
    pdf.cell(95, 10, _safe(reusable_text), 1, 1)
    
    if not discard_status.get('reusable', True):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(95, 10, _safe("Discard Reason:"), 1)
        pdf.set_font("Arial", '', 12)
        pdf.cell(95, 10, _safe(discard_status.get('reason', 'N/A')), 1, 1)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(95, 10, _safe("Confidence Score:"), 1)
    pdf.set_font("Arial", '', 12)
    pdf.cell(95, 10, _safe(f"{report_data['confidence']:.0%}"), 1, 1)

    # Location Codes section
    if 'container_details' in report_data and report_data['container_details']:
        container_details = report_data['container_details']
        if 'location_codes' in container_details and container_details['location_codes']:
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, _safe("Location Codes & Markings"), 0, 1)
            pdf.set_font("Arial", '', 10)
            for loc_code in container_details['location_codes']:
                code_text = f"- {loc_code.get('type', 'N/A')}: {loc_code.get('code', 'N/A')}"
                if loc_code.get('text_content'):
                    code_text += f" ({loc_code['text_content']})"
                pdf.cell(0, 8, _safe(code_text), 0, 1)
        
        # Data plate information
        if 'data_plate_info' in container_details and container_details['data_plate_info']:
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, _safe("Data Plate Information"), 0, 1)
            pdf.set_font("Arial", '', 10)
            data_info = container_details['data_plate_info']
            if data_info.get('max_gross'):
                pdf.cell(0, 8, _safe(f"- Max Gross Weight: {data_info['max_gross']}"), 0, 1)
            if data_info.get('tare'):
                pdf.cell(0, 8, _safe(f"- Tare Weight: {data_info['tare']}"), 0, 1)
            if data_info.get('other_specs'):
                pdf.cell(0, 8, _safe(f"- Other Specs: {data_info['other_specs']}"), 0, 1)
    
    # GPT-5 Analysis section
    if 'gpt5_analysis' in report_data:
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, _safe("GPT-5 Vision Analysis"), 0, 1)
        pdf.set_font("Arial", '', 10)
        gpt5_data = report_data['gpt5_analysis']
        pdf.cell(0, 8, _safe(f"GPT-5 Confidence: {gpt5_data.get('confidence_score', 0):.0%}"), 0, 1)
        pdf.cell(0, 8, _safe(f"Structural Integrity: {gpt5_data.get('structural_integrity', 'Unknown')}"), 0, 1)

    # Safety Concerns
    if report_data.get('safety_concerns'):
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, _safe("Safety Concerns:"), 0, 1)
        pdf.set_font("Arial", '', 10)
        for concern in report_data['safety_concerns']:
            pdf.cell(0, 8, _safe(f"- {concern}"), 0, 1)

    # Maintenance Recommendations
    if report_data.get('maintenance_recommendations'):
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, _safe("Maintenance Recommendations:"), 0, 1)
        pdf.set_font("Arial", '', 10)
        for rec in report_data['maintenance_recommendations']:
            pdf.cell(0, 8, _safe(f"- {rec}"), 0, 1)

    # Damage details
    if report_data['detected_damages']:
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, _safe("Detected Damages:"), 0, 1)
        pdf.set_font("Arial", '', 10)
        for i, damage in enumerate(report_data['detected_damages'], 1):
            damage_text = f"{i}. {damage['type']} - {damage['severity']} (Zone: {damage['zone']})"
            if 'repair_priority' in damage:
                damage_text += f" [Priority: {damage['repair_priority']}]"
            pdf.cell(0, 8, _safe(damage_text), 0, 1)

            if 'description' in damage and damage['description']:
                pdf.set_font("Arial", '', 9)
                pdf.cell(0, 6, _safe(f"   Description: {damage['description']}"), 0, 1)
                pdf.set_font("Arial", '', 10)

            if 'repair_recommendation' in damage:
                pdf.set_font("Arial", '', 9)
                pdf.cell(0, 6, _safe(f"   Recommendation: {damage['repair_recommendation']}"), 0, 1)
                pdf.set_font("Arial", '', 10)
    else:
        pdf.ln(10)
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 8, _safe("No damages detected."), 0, 1)

    pdf.output(pdf_path)

    return {"pdf_report": str(pdf_path), "excel_report": str(excel_path)}