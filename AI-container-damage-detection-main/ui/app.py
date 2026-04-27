# ui/app.py
import streamlit as st
import requests
import json
import pandas as pd
import sys
import base64
from pathlib import Path
sys.path.append('.')
from core.utils import format_currency_inr

# Page Configuration
st.set_page_config(
    layout="wide",
    page_title="CONTAINER INSPECTION AI | Enterprise Damage Detection",
    page_icon="📦",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css():
    css_file = Path(__file__).parent / "styles.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning("Custom CSS file not found. Using default styling.")

load_css()

# Custom JavaScript for animations
st.markdown("""
<script>
// Number counter animation
function animateValue(id, start, end, duration) {
    const obj = document.getElementById(id);
    if (!obj) return;
    const range = end - start;
    const increment = end > start ? 1 : -1;
    const stepTime = Math.abs(Math.floor(duration / range));
    let current = start;
    const timer = setInterval(function() {
        current += increment;
        obj.innerHTML = current;
        if (current == end) {
            clearInterval(timer);
        }
    }, stepTime);
}

// Add scan line animation to images
function addScanAnimation() {
    const images = document.querySelectorAll('[data-testid="stImage"]');
    images.forEach(img => {
        if (!img.classList.contains('scanning-indicator')) {
            img.classList.add('scanning-indicator');
        }
    });
}

// Run on page load
window.addEventListener('load', function() {
    addScanAnimation();
});
</script>
""", unsafe_allow_html=True)

# Hero Header with Gradient
st.markdown("""
<div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
    <h1 class="hero-title" style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">
        🚢 Container Inspection AI
    </h1>
    <p style="color: #CBD5E1; font-size: 1.1rem; font-weight: 400;">
        Enterprise-Grade Damage Detection • AI-Powered Analysis • Instant Reports
    </p>
</div>
""", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000"

if 'report' not in st.session_state:
    st.session_state.report = None

# Sidebar Navigation
with st.sidebar:
    # Logo/Branding
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📦</div>
        <div style="color: #00C7B7; font-weight: 700; font-size: 1.1rem; letter-spacing: 0.05em;">
            INSPECTION AI
        </div>
        <div style="color: #94A3B8; font-size: 0.75rem; margin-top: 0.25rem;">
            v2.0 Enterprise
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation Menu
    st.markdown("### 🎯 Navigation")
    nav_option = st.radio(
        "Select Module",
        ["🏠 Home", "🔍 Detection", "📊 Reports", "📈 Analytics", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Upload Section
    st.markdown("### 📤 Upload Container Image")
    uploaded_file = st.file_uploader(
        "Drag and drop or click to browse",
        type=["jpg", "png", "jpeg"],
        help="Supported formats: JPG, PNG, JPEG (Max 10MB)"
    )
    
    # Inspection Button with Icon
    analyze_button = st.button(
        "🚀 Run AI Inspection",
        use_container_width=True,
        type="primary"
    )
    
    st.markdown("---")
    
    # Enhanced Color Legend
    st.markdown("### Detection Legend")
    st.markdown("""
    <div class="legend-box">
        <div style='margin: 8px 0; display: flex; align-items: center;'>
            <span style='display: inline-block; width: 20px; height: 20px; background: #EF4444; 
                         border-radius: 4px; margin-right: 10px;'></span>
            <span style='color: #F8FAFC; font-weight: 500;'>Damage Detection</span>
        </div>
        <div style='margin: 8px 0; display: flex; align-items: center;'>
            <span style='display: inline-block; width: 20px; height: 20px; background: #10B981; 
                         border-radius: 4px; margin-right: 10px;'></span>
            <span style='color: #F8FAFC; font-weight: 500;'>Container ID</span>
        </div>
        <div style='margin: 8px 0; display: flex; align-items: center;'>
            <span style='display: inline-block; width: 20px; height: 20px; background: #06B6D4; 
                         border-radius: 4px; margin-right: 10px;'></span>
            <span style='color: #F8FAFC; font-weight: 500;'>Data Plate</span>
        </div>
        <div style='margin: 8px 0; display: flex; align-items: center;'>
            <span style='display: inline-block; width: 20px; height: 20px; background: #FFD700; 
                         border-radius: 4px; margin-right: 10px;'></span>
            <span style='color: #F8FAFC; font-weight: 500;'>Location Codes</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System Status
    st.markdown("### System Status")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 0.5rem; background: rgba(16, 185, 129, 0.1); 
                    border-radius: 8px; border: 1px solid #10B981;'>
            <div style='color: #10B981; font-size: 1.5rem;'>●</div>
            <div style='color: #10B981; font-size: 0.75rem; font-weight: 600;'>API</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 0.5rem; background: rgba(16, 185, 129, 0.1); 
                    border-radius: 8px; border: 1px solid #10B981;'>
            <div style='color: #10B981; font-size: 1.5rem;'>●</div>
            <div style='color: #10B981; font-size: 0.75rem; font-weight: 600;'>AI</div>
        </div>
        """, unsafe_allow_html=True)

# Analysis Trigger
if analyze_button and uploaded_file:
    # Custom loading animation
    with st.spinner(""):
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: rgba(0, 199, 183, 0.05); 
                    border-radius: 16px; border: 1px solid #00C7B7; margin: 2rem 0;">
            <div style="font-size: 3rem; margin-bottom: 1rem; animation: radarPulse 2s infinite;">🔍</div>
            <h3 style="color: #00C7B7; margin-bottom: 0.5rem;">AI Scanning in Progress...</h3>
            <p style="color: #CBD5E1; font-size: 0.9rem;">Analyzing container with AI Vision</p>
            <div style="width: 100%; height: 4px; background: #1E293B; border-radius: 2px; 
                        margin-top: 1rem; overflow: hidden;">
                <div style="width: 100%; height: 100%; background: linear-gradient(90deg, #00C7B7, #1FFFE8); 
                            animation: scanLine 2s infinite;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        try:
            response = requests.post(f"{API_URL}/inspect", files=files)
            if response.status_code == 200:
                st.session_state.report = response.json()
                # Success animation
                st.markdown("""
                <div style="text-align: center; padding: 1.5rem; background: rgba(16, 185, 129, 0.1); 
                            border-radius: 16px; border: 1px solid #10B981; margin: 1rem 0;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">✅</div>
                    <h3 style="color: #10B981; margin: 0;">Analysis Complete!</h3>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"❌ API Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection Error: Could not connect to the backend. Please ensure the API server is running.")

# Display Results
if st.session_state.report:
    report = st.session_state.report
    # Handle backend error responses gracefully
    if "error" in report and "report_id" not in report:
        st.error(f"API Error: {report.get('error')}")
    elif report.get("status") == "Unclear – Needs Manual Review":
        st.markdown("""
        <div style="padding: 1.5rem; background: rgba(245, 158, 11, 0.1); border-radius: 16px; 
                    border-left: 4px solid #F59E0B; margin: 2rem 0;">
            <h3 style="color: #F59E0B; margin-bottom: 0.5rem;">⚠️ Manual Review Required</h3>
            <p style="color: #CBD5E1;">AI Confidence: {:.0%}</p>
            <p style="color: #94A3B8; font-size: 0.9rem;">
                The AI was not confident enough to provide an automated report. 
                Please have a human inspector review this case.
            </p>
        </div>
        """.format(report['confidence']), unsafe_allow_html=True)
    else:
        if 'report_id' not in report:
            st.error("API Error: Missing report_id in response.")
            st.json(report)
            st.stop()
        report_id = report['report_id']
        
        # Results Header with Container ID
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #334155 0%, #1E293B 100%); 
                    border-radius: 16px; border: 1px solid #00C7B7; margin-bottom: 2rem;">
            <div style="color: #94A3B8; font-size: 0.875rem; text-transform: uppercase; 
                        letter-spacing: 0.1em; margin-bottom: 0.5rem;">Inspection Results</div>
            <h2 style="color: #00C7B7; font-size: 2rem; margin: 0; font-weight: 700;">
                {report.get('container_id', 'N/A')}
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Main Content: Image + Metrics
        col1, col2 = st.columns([2, 1], gap="large")
        
        with col1:
            st.markdown("### 🖼️ Annotated Detection")
            # Use server-side file reading to avoid browser trying to load
            # a local file path like file:///E:/... which is blocked by browsers.
            annotated_image_path = report.get('artifacts', {}).get('annotated_image')
            if annotated_image_path and Path(annotated_image_path).exists():
                try:
                    with open(annotated_image_path, 'rb') as img_f:
                        image_bytes = img_f.read()
                    st.image(image_bytes, use_column_width=True)
                except Exception:
                    # Fallback to Streamlit's default behavior if something goes wrong
                    st.image(annotated_image_path, use_column_width=True)
            else:
                st.warning("Annotated image not found on server.")
        
        with col2:
            st.markdown("### 📊 Key Metrics")
            
            # Condition with color coding
            condition = report['condition']
            condition_colors = {
                'Excellent': '#10B981',
                'Good': '#34D399',
                'Fair': '#F59E0B',
                'Poor': '#FB923C',
                'Critical': '#EF4444'
            }
            condition_color = condition_colors.get(condition, '#94A3B8')
            
            st.markdown(f"""
            <div style="padding: 1.5rem; background: linear-gradient(135deg, #334155 0%, #1E293B 100%); 
                        border-radius: 16px; border: 1px solid {condition_color}; margin-bottom: 1rem; 
                        text-align: center;">
                <div style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; 
                            letter-spacing: 0.1em; margin-bottom: 0.5rem;">Overall Condition</div>
                <div style="color: {condition_color}; font-size: 2rem; font-weight: 700; 
                            text-shadow: 0 0 20px {condition_color}40;">{condition}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Confidence Score
            confidence = report['confidence']
            confidence_color = '#10B981' if confidence > 0.8 else '#F59E0B' if confidence > 0.5 else '#EF4444'
            st.markdown(f"""
            <div style="padding: 1rem; background: rgba(0, 199, 183, 0.05); border-radius: 12px; 
                        border: 1px solid {confidence_color}; margin-bottom: 1rem;">
                <div style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; 
                            letter-spacing: 0.1em; margin-bottom: 0.5rem;">AI Confidence</div>
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="color: {confidence_color}; font-size: 1.5rem; font-weight: 700;">
                        {confidence:.0%}
                    </div>
                    <div style="width: 60%; height: 8px; background: #1E293B; border-radius: 4px; overflow: hidden;">
                        <div style="width: {confidence*100}%; height: 100%; background: {confidence_color}; 
                                    transition: width 1s ease-out;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Discard Status
            if report.get('discard_status'):
                discard_info = report['discard_status']
                if discard_info.get('should_discard'):
                    st.markdown(f"""
                    <div style="padding: 1rem; background: rgba(239, 68, 68, 0.1); border-radius: 12px; 
                                border: 1px solid #EF4444; margin-bottom: 1rem;">
                        <div style="color: #EF4444; font-weight: 600; margin-bottom: 0.25rem;">⚠️ DISCARD RECOMMENDED</div>
                        <div style="color: #CBD5E1; font-size: 0.875rem;">{discard_info.get('reason', 'Not reusable')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="padding: 1rem; background: rgba(16, 185, 129, 0.1); border-radius: 12px; 
                                border: 1px solid #10B981; margin-bottom: 1rem;">
                        <div style="color: #10B981; font-weight: 600; margin-bottom: 0.25rem;">✓ REUSABLE</div>
                        <div style="color: #CBD5E1; font-size: 0.875rem;">{discard_info.get('reason', 'Container can be repaired')}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Download Section
            st.markdown("### 📥 Download Reports")
            st.download_button(
                "📄 PDF Report",
                data=open(report['artifacts']['pdf_report'], 'rb').read(),
                file_name=f"{report_id}.pdf",
                use_container_width=True
            )
            st.download_button(
                "📊 Excel Report",
                data=open(report['artifacts']['excel_report'], 'rb').read(),
                file_name=f"{report_id}.xlsx",
                use_container_width=True
            )
            st.download_button(
                "📋 JSON Data",
                data=json.dumps(report, indent=2),
                file_name=f"{report_id}.json",
                use_container_width=True
            )

        # Enhanced AI Analysis Display
        if 'gpt5_analysis' in report:
            st.markdown("---")
            st.markdown("## 🤖 AI Vision Analysis")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                integrity = report.get('structural_integrity', 'Unknown')
                integrity_color = '#10B981' if integrity == 'Sound' else '#F59E0B' if integrity == 'Compromised' else '#EF4444'
                st.markdown(f"""
                <div style="padding: 1rem; background: linear-gradient(135deg, #334155 0%, #1E293B 100%); 
                            border-radius: 12px; border: 1px solid {integrity_color}; text-align: center;">
                    <div style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; 
                                letter-spacing: 0.1em; margin-bottom: 0.5rem;">Structural Integrity</div>
                    <div style="color: {integrity_color}; font-size: 1.25rem; font-weight: 600;">{integrity}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                gpt_confidence = report['gpt5_analysis'].get('confidence_score', 0)
                st.markdown(f"""
                <div style="padding: 1rem; background: linear-gradient(135deg, #334155 0%, #1E293B 100%); 
                            border-radius: 12px; border: 1px solid #00C7B7; text-align: center;">
                    <div style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; 
                                letter-spacing: 0.1em; margin-bottom: 0.5rem;">AI Confidence</div>
                    <div style="color: #00C7B7; font-size: 1.25rem; font-weight: 600;">{gpt_confidence:.0%}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if report.get('safety_concerns'):
                    concern_count = len(report['safety_concerns'])
                    st.markdown(f"""
                    <div style="padding: 1rem; background: linear-gradient(135deg, #334155 0%, #1E293B 100%); 
                                border-radius: 12px; border: 1px solid #EF4444; text-align: center;">
                        <div style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; 
                                    letter-spacing: 0.1em; margin-bottom: 0.5rem;">Safety Concerns</div>
                        <div style="color: #EF4444; font-size: 1.25rem; font-weight: 600;">⚠️ {concern_count}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="padding: 1rem; background: linear-gradient(135deg, #334155 0%, #1E293B 100%); 
                                border-radius: 12px; border: 1px solid #10B981; text-align: center;">
                        <div style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; 
                                    letter-spacing: 0.1em; margin-bottom: 0.5rem;">Safety Status</div>
                        <div style="color: #10B981; font-size: 1.25rem; font-weight: 600;">✓ Clear</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Safety Concerns & Maintenance
        col1, col2 = st.columns(2)
        
        with col1:
            if report.get('safety_concerns'):
                with st.expander("🚨 Safety Concerns", expanded=True):
                    for idx, concern in enumerate(report['safety_concerns'], 1):
                        st.markdown(f"""
                        <div style="padding: 0.75rem; background: rgba(239, 68, 68, 0.05); 
                                    border-left: 3px solid #EF4444; margin-bottom: 0.5rem; border-radius: 4px;">
                            <span style="color: #EF4444; font-weight: 600;">{idx}.</span>
                            <span style="color: #CBD5E1; margin-left: 0.5rem;">{concern}</span>
                        </div>
                        """, unsafe_allow_html=True)
        
        with col2:
            if report.get('maintenance_recommendations'):
                with st.expander("🔧 Maintenance Recommendations", expanded=True):
                    for idx, rec in enumerate(report['maintenance_recommendations'], 1):
                        st.markdown(f"""
                        <div style="padding: 0.75rem; background: rgba(0, 199, 183, 0.05); 
                                    border-left: 3px solid #00C7B7; margin-bottom: 0.5rem; border-radius: 4px;">
                            <span style="color: #00C7B7; font-weight: 600;">{idx}.</span>
                            <span style="color: #CBD5E1; margin-left: 0.5rem;">{rec}</span>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Container Information
        st.markdown("---")
        st.markdown("## 📦 Container Metadata")
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.write(f"**Container ID:** {report.get('container_id', 'N/A')}")
            st.write(f"**Container Type:** {report.get('container_type', 'N/A')}")
            st.write(f"**Owner Code:** {report.get('container_owner', 'N/A')}")
        with info_col2:
            st.write(f"**Size/Type Code:** {report.get('size_type_code', 'N/A')}")
            st.write(f"**Equipment Category:** {report.get('equipment_category', 'N/A')}")
            st.write(f"**Structural Integrity:** {report.get('structural_integrity', 'Unknown')}")
        with info_col3:
            if report.get('container_details') and report['container_details'].get('data_plate_info'):
                data_plate = report['container_details']['data_plate_info']
                st.write(f"**Max Gross:** {data_plate.get('max_gross', 'N/A')}")
                st.write(f"**Tare Weight:** {data_plate.get('tare', 'N/A')}")
                if data_plate.get('manufacture_date'):
                    st.write(f"**Mfg Date:** {data_plate.get('manufacture_date', 'N/A')}")
        
        st.markdown("---")
        st.markdown("## 🔍 Damage Analysis")
        
        if not report['detected_damages']:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: rgba(16, 185, 129, 0.05); 
                        border-radius: 16px; border: 1px solid #10B981;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
                <h3 style="color: #10B981; margin-bottom: 0.5rem;">No Damage Detected</h3>
                <p style="color: #CBD5E1; font-size: 0.9rem;">Container appears to be in excellent condition</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            damage_df = pd.DataFrame(report['detected_damages'])
            # Enhanced columns for AI analysis with location codes
            display_columns = ['type', 'severity', 'zone', 'location_code', 'code_mode', 'confidence', 'repair_priority']
            if 'description' in damage_df.columns:
                display_columns.append('description')
            
            # Filter to only existing columns
            display_columns = [col for col in display_columns if col in damage_df.columns]
            st.dataframe(damage_df[display_columns], use_container_width=True)
            
            # Show detailed damage information
            for idx, damage in enumerate(report['detected_damages']):
                with st.expander(f"Damage {idx+1}: {damage.get('type', 'Unknown')} - {damage.get('severity', 'Unknown')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Zone:** {damage.get('zone', 'Unknown')}")
                        st.write(f"**Location Code:** {damage.get('location_code', 'N/A')} ({damage.get('code_mode', 'N/A')})")
                        st.write(f"**Confidence:** {damage.get('confidence', 0):.0%}")
                        # Source field hidden for production
                    with col2:
                        st.write(f"**Repair Priority:** {damage.get('repair_priority', 'Unknown')}")
                        if 'repair_recommendation' in damage:
                            st.write(f"**Recommendation:** {damage['repair_recommendation']}")
                    if 'description' in damage and damage['description']:
                        st.write(f"**Description:** {damage['description']}")
        
        # Enhanced Analysis Details
        if 'enhanced_analysis' in report and report['enhanced_analysis']:
            st.markdown("---")
            with st.expander("🔬 Enhanced AI Analysis", expanded=False):
                enhanced = report['enhanced_analysis']
                
                if 'repair_recommendations' in enhanced:
                    st.markdown("#### 🛠️ Repair Recommendations")
                    for idx, rec in enumerate(enhanced['repair_recommendations'], 1):
                        st.markdown(f"""
                        <div style="padding: 0.75rem; background: rgba(0, 199, 183, 0.05); 
                                    border-left: 3px solid #00C7B7; margin-bottom: 0.5rem; border-radius: 4px;">
                            <span style="color: #00C7B7; font-weight: 600;">{idx}.</span>
                            <span style="color: #CBD5E1; margin-left: 0.5rem;">{rec}</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                if 'cost_breakdown' in enhanced:
                    st.markdown("#### 💰 Cost Breakdown")
                    st.json(enhanced['cost_breakdown'])
                
                col1, col2 = st.columns(2)
                with col1:
                    if 'safety_assessment' in enhanced:
                        st.markdown("#### 🛡️ Safety Assessment")
                        st.info(enhanced['safety_assessment'])
                
                with col2:
                    if 'compliance_status' in enhanced:
                        st.markdown("#### ✅ Compliance Status")
                        st.success(enhanced['compliance_status'])