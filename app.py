import streamlit as st
import pandas as pd
import datetime
import random
import google.generativeai as genai
from datetime import date, timedelta
import numpy as np
import os

# ----------------------------
# 🎨 Page Config
# ----------------------------
st.set_page_config(
    page_title="ReliefMate AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------
# 🎨 Professional Government-Grade CSS
# ----------------------------
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        padding: 0 !important;
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        color: #334155;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    }
    
    /* Header Section - Professional & Clean */
    .hero-container {
        background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%);
        padding: 40px 40px 32px 40px;
        text-align: left;
        border-bottom: 2px solid #06b6d4;
        margin-bottom: 48px;
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 10px;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .hero-subtitle {
        font-size: 1rem;
        margin-bottom: 16px;
        color: #e0f2fe;
        font-weight: 400;
    }
    
    .status-badge {
        display: inline-block;
        background: rgba(236, 253, 245, 0.9);
        color: #059669;
        padding: 6px 16px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #a7f3d0;
    }
    
    .emergency-info {
        margin-top: 16px;
        padding: 12px 16px;
        background: rgba(0, 0, 0, 0.15);
        border-radius: 8px;
        border-left: 3px solid #fbbf24;
    }
    
    /* Professional Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 24px !important;
        margin: 20px 0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
        color: #334155 !important;
        transition: all 0.2s ease !important;
    }
    
    .glass-card:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Chat Interface */
    .chat-container {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 10px !important;
        padding: 24px !important;
        border: 1px solid #e2e8f0 !important;
        margin: 24px 0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
    }
    
    .chat-message {
        background: #f8fafc;
        padding: 14px 16px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 3px solid #06b6d4;
    }
    
    .chat-message strong {
        color: #0f172a;
    }
    
    /* Professional Buttons */
    .stButton > button {
        background: #0891b2 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08) !important;
    }
    
    .stButton > button:hover {
        background: #0e7490 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Text Input */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        color: #1e293b !important;
        padding: 12px !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #06b6d4 !important;
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1) !important;
    }
    
    .stSelectbox > div > div {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }
    
    /* Metrics */
    .metric-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        transition: all 0.2s ease;
    }
    
    .metric-container:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 6px;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 500;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
        border-bottom: none;
        padding-bottom: 0;
        margin-bottom: 32px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f1f5f9;
        border-radius: 20px;
        color: #64748b;
        padding: 10px 24px;
        font-weight: 600;
        border: 1px solid #e2e8f0;
        font-size: 0.95rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: #0891b2 !important;
        color: white !important;
        border: 1px solid #0891b2 !important;
        box-shadow: 0 2px 4px rgba(8, 145, 178, 0.2) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Improved spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
    }
    
    h2 {
        margin-bottom: 8px;
    }
    
    p, label {
        color: #475569;
    }
    
    /* Status badges */
    .status-critical {
        background: #fef2f2;
        color: #dc2626;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #fecaca;
    }
    
    .status-active {
        background: #fef3c7;
        color: #d97706;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #fde68a;
    }
    
    .status-resolved {
        background: #ecfdf5;
        color: #059669;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #a7f3d0;
    }
    
    .status-monitoring {
        background: #eff6ff;
        color: #2563eb;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #bfdbfe;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.8rem;
        }
        .hero-subtitle {
            font-size: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# 🔑 Gemini API Setup - FIXED VERSION
# ----------------------------
def setup_gemini():
    # Correct way to read from Streamlit secrets
    try:
        GEMINI_KEY = st.secrets["general"]["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        GEMINI_KEY = None
        st.warning("Gemini API key not found in secrets.toml")
    
    if GEMINI_KEY and GEMINI_KEY != "your_actual_gemini_api_key_here":
        try:
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            return model, "✅ Gemini AI Connected"
        except Exception as e:
            return None, f"❌ API Error: {str(e)[:50]}..."
    else:
        return None, "⚠️ Demo Mode (Add real GEMINI_API_KEY to secrets)"

# ----------------------------
# 📊 Sample Data Generation
# ----------------------------
def generate_sample_data():
    # Relief Reports
    reports = [
        {"location": "Rajkot", "type": "Flood", "status": "🚨 Critical", "needs": "Food, Water, Medical Supplies", "team": "Team A"},
        {"location": "Ahmedabad", "type": "Earthquake", "status": "✅ Resolved", "needs": "Search & Rescue Complete", "team": "Team B"},
        {"location": "Surat", "type": "Cyclone", "status": "⚠️ Active", "needs": "Evacuation, Shelter", "team": "Team C"},
        {"location": "Bhavnagar", "type": "Fire", "status": "🔥 Critical", "needs": "Fire Brigade, Medical Aid", "team": "Team D"},
        {"location": "Vadodara", "type": "Landslide", "status": "📋 Monitoring", "needs": "Geological Survey", "team": "Team E"}
    ]
    
    # Analytics Data
    dates = [date.today() - timedelta(days=i) for i in range(7, 0, -1)]
    analytics = {
        "dates": dates,
        "requests": [random.randint(50, 200) for _ in range(7)],
        "resolved": [random.randint(20, 150) for _ in range(7)],
        "active": [random.randint(10, 80) for _ in range(7)]
    }
    
    return reports, analytics

# ----------------------------
# 🏠 Hero Section
# ----------------------------
def render_hero():
    st.markdown("""
    <div class="hero-container">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <h1 class="hero-title">
                    <span style="font-size: 1.8rem;">🌍</span> ReliefMate AI
                </h1>
                <p class="hero-subtitle">Advanced Disaster Relief Management System</p>
                <span class="status-badge">System Operational</span>
            </div>
        </div>
        <div class="emergency-info" style="margin-top: 16px;">
            <strong style="color: #fbbf24;">Emergency Hotlines:</strong>
            <span style="color: #e5e7eb; margin-left: 16px;">
                Police: 112  |  Medical: 108  |  Fire: 101
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# 💬 Enhanced Chat Interface
# ----------------------------
def render_chat_interface(model, api_status):
    st.markdown("## AI Assistant")
    st.markdown('<p style="color: #64748b; margin-bottom: 32px;">Get instant guidance on emergency procedures, resource allocation, and disaster response protocols</p>', unsafe_allow_html=True)
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # System Ready indicator
    st.markdown("""
    <div style="text-align: center; margin-bottom: 24px;">
        <span style="background: #ecfdf5; color: #059669; padding: 6px 16px; border-radius: 16px; font-size: 0.85rem; font-weight: 600; border: 1px solid #a7f3d0;">
            ● System Ready
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Centered chat input container
    st.markdown('<div style="max-width: 800px; margin: 0 auto;">', unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask your question:",
            placeholder="e.g., 'What should I do during a flood emergency?'",
            key="chat_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process message
    if send_button and user_input.strip():
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Generate AI response
        if model:
            with st.spinner("🤖 ReliefMate AI is analyzing..."):
                try:
                    enhanced_prompt = f"""
                    You are ReliefMate AI, a disaster relief assistant for Gujarat, India.
                    Provide helpful, actionable advice in 100-150 words.
                    Include relevant emergency contacts when appropriate.
                    Be empathetic, clear, and focus on immediate safety.
                    
                    User Question: {user_input}
                    """
                    response = model.generate_content(enhanced_prompt)
                    ai_response = response.text.strip()
                except Exception as e:
                    ai_response = f"❌ Service temporarily unavailable. For immediate help: 112 (Police), 108 (Medical), 101 (Fire). Error: {str(e)[:50]}..."
        else:
            # Demo responses for when API is not available
            demo_responses = [
                "🚨 **Emergency Protocol**: For immediate danger, call 112 (Police), 108 (Ambulance), or 101 (Fire). Stay calm, move to safety, and follow official evacuation routes. Keep emergency kit ready with water, food, medicine, and important documents.",
                "🌊 **Flood Safety**: Move to higher ground immediately. Never walk or drive through flood water. Stay informed via official radio/TV channels. If trapped, signal for help from highest available point. Emergency services: 108 for rescue operations.",
                "🔥 **Fire Emergency**: GET OUT, STAY OUT, CALL 101. Crawl low under smoke. Close doors behind you. Meet at designated family meeting spot. Don't use elevators. If clothes catch fire: Stop, Drop, Roll.",
                "🏥 **Medical Emergency**: Call 108 immediately. Check for breathing and pulse. Apply pressure to bleeding wounds. Keep victim warm and conscious. Don't move someone with potential spinal injury unless in immediate danger.",
                "📋 **Emergency Kit**: Include water (1 gallon per person per day), non-perishable food, flashlight, radio, first aid kit, medications, documents, cash, and phone chargers. Update kit every 6 months."
            ]
            ai_response = random.choice(demo_responses)
        
        # Add AI response to history
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown('<div style="max-width: 900px; margin: 24px auto;">', unsafe_allow_html=True)
        st.markdown("### Conversation History")
        for message in reversed(st.session_state.chat_history[-10:]):  # Show last 10 messages
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message" style="border-left: 3px solid #dc2626; background: #fef2f2;">
                    <strong style="color: #dc2626;">You:</strong><br>
                    <span style="color: #334155;">{message["content"]}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message" style="border-left: 3px solid #06b6d4; background: #ecfeff;">
                    <strong style="color: #0891b2;">ReliefMate AI:</strong><br>
                    <span style="color: #334155;">{message["content"]}</span>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 60px 40px; background: white; border-radius: 10px; margin: 24px auto; max-width: 600px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);">
            <div style="font-size: 3rem; margin-bottom: 16px;">💬</div>
            <h3 style="color: #0f172a; margin-bottom: 12px;">Assistant Ready</h3>
            <p style="color: #64748b;">Ask me about emergency procedures, disaster preparedness, or resource management</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# 📊 Relief Reports Dashboard
# ----------------------------
def render_reports_dashboard(reports):
    st.markdown("## Live Relief Operations")
    st.markdown('<p style="color: #64748b; margin-bottom: 32px;">Real-time monitoring of active disaster response operations</p>', unsafe_allow_html=True)
    
    # Status summary
    col1, col2, col3, col4 = st.columns(4)
    
    critical_count = len([r for r in reports if "Critical" in r["status"]])
    active_count = len([r for r in reports if "Active" in r["status"]])
    resolved_count = len([r for r in reports if "Resolved" in r["status"]])
    monitoring_count = len([r for r in reports if "Monitoring" in r["status"]])
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value" style="color: #dc2626;">{}</div>
            <div class="metric-label">Critical Cases</div>
        </div>
        """.format(critical_count), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value" style="color: #d97706;">{}</div>
            <div class="metric-label">Active Operations</div>
        </div>
        """.format(active_count), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value" style="color: #059669;">{}</div>
            <div class="metric-label">Resolved Cases</div>
        </div>
        """.format(resolved_count), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value" style="color: #2563eb;">{}</div>
            <div class="metric-label">Under Monitoring</div>
        </div>
        """.format(monitoring_count), unsafe_allow_html=True)
    
    # Detailed reports
    st.markdown("### Operations Report")
    st.markdown("")  # spacing
    
    for i, report in enumerate(reports):
        # Determine status styling
        if "Critical" in report["status"]:
            status_bg = "#fef2f2"
            status_color = "#dc2626"
            status_border = "#fecaca"
            icon = "🚨"
        elif "Active" in report["status"]:
            status_bg = "#fef3c7"
            status_color = "#d97706"
            status_border = "#fde68a"
            icon = "⚠️"
        elif "Resolved" in report["status"]:
            status_bg = "#ecfdf5"
            status_color = "#059669"
            status_border = "#a7f3d0"
            icon = "✅"
        else:  # Monitoring
            status_bg = "#eff6ff"
            status_color = "#2563eb"
            status_border = "#bfdbfe"
            icon = "📋"
        
        disaster_icons = {
            "Flood": "🌊",
            "Fire": "🔥",
            "Earthquake": "🌍",
            "Cyclone": "🌀",
            "Landslide": "⛰️"
        }
        disaster_icon = disaster_icons.get(report["type"], "⚠️")
        
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 12px;">
                <h3 style="color: #0f172a; margin: 0; display: flex; align-items: center; gap: 8px;">
                    {disaster_icon} {report["location"]} • {report["type"]}
                </h3>
                <span style="background: {status_bg}; color: {status_color}; padding: 6px 14px; border-radius: 12px; font-weight: 600; font-size: 0.85rem; border: 1px solid {status_border};">
                    {report["status"].replace("🚨 ", "").replace("🔥 ", "").replace("⚠️ ", "").replace("✅ ", "").replace("📋 ", "")}
                </span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px; color: #475569;">
                <p style="margin: 0;"><strong style="color: #334155;">Requirements:</strong> {report["needs"]}</p>
                <p style="margin: 0; color: #64748b;"><strong style="color: #334155;">Team:</strong> {report["team"]}</p>
                <p style="margin: 0; color: #94a3b8; font-size: 0.85rem;">Updated: {datetime.datetime.now().strftime('%H:%M')} IST</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# 📈 Analytics Dashboard
# ----------------------------
def render_analytics(analytics_data):
    st.markdown("## Performance Analytics")
    st.markdown('<p style="color: #64748b; margin-bottom: 32px;">Data-driven insights for operational efficiency</p>', unsafe_allow_html=True)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': analytics_data['dates'],
        'New Requests': analytics_data['requests'],
        'Resolved Cases': analytics_data['resolved'],
        'Active Cases': analytics_data['active']
    })
    
    # Charts with better styling
    st.markdown("### 7-Day Operations Trend")
    st.markdown('<div style="background: white; padding: 24px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08); margin-bottom: 32px;">', unsafe_allow_html=True)
    
    # Line chart using Streamlit
    chart_data = df.set_index('Date')[['New Requests', 'Resolved Cases', 'Active Cases']]
    st.line_chart(chart_data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bar chart for comparison
    st.markdown("### Daily Comparison")
    st.markdown('<div style="background: white; padding: 24px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08); margin-bottom: 32px;">', unsafe_allow_html=True)
    st.bar_chart(chart_data, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Summary statistics
    st.markdown("### Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_requests = sum(analytics_data['requests']) // 7
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 8px;">📈</div>
            <div class="metric-value">{avg_requests}</div>
            <div class="metric-label">Avg Daily Requests</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_resolved = sum(analytics_data['resolved'])
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 8px;">✅</div>
            <div class="metric-value">{total_resolved}</div>
            <div class="metric-label">Total Resolved</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        resolution_rate = round((total_resolved / sum(analytics_data['requests'])) * 100, 1)
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 8px;">🎯</div>
            <div class="metric-value">{resolution_rate}%</div>
            <div class="metric-label">Resolution Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional metrics using Streamlit metrics
    st.markdown("### Key Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Critical Cases",
            value="23",
            delta="-5",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="Avg Response Time",
            value="2.3 min",
            delta="-0.8 min",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Active Teams",
            value="12",
            delta="+2"
        )
    
    with col4:
        st.metric(
            label="Coverage Areas",
            value="45",
            delta="+3"
        )

# ----------------------------
# 🛠️ Admin Panel
# ----------------------------
def render_admin_panel():
    st.markdown("## Administration Panel")
    st.markdown('<p style="color: #64748b; margin-bottom: 32px;">Manage relief operations and system configuration</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-bottom: 20px;">Submit New Report</h3>
        </div>
        """, unsafe_allow_html=True)
        
        location = st.selectbox("Location", ["Rajkot", "Ahmedabad", "Surat", "Bhavnagar", "Vadodara", "Other"])
        disaster_type = st.selectbox("Disaster Type", ["Flood", "Fire", "Earthquake", "Cyclone", "Landslide", "Other"])
        severity = st.selectbox("Severity Level", ["Critical", "Active", "Monitoring"])
        description = st.text_area("Description", placeholder="Describe the situation and required assistance...", height=120)
        
        if st.button("Submit Report", use_container_width=True):
            st.success(f"✅ Report submitted successfully! Location: {location}, Type: {disaster_type}, Severity: {severity}")
            st.balloons()
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-bottom: 20px;">Bulk Data Upload</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 8px; padding: 30px; text-align: center; margin-bottom: 20px;">
            <div style="font-size: 2rem; margin-bottom: 12px; color: #64748b;">📁</div>
            <p style="color: #64748b; margin: 0;">Drop CSV file or click to browse</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Upload CSV file with relief data",
            type=["csv"],
            help="Upload CSV files containing relief operation data",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ File uploaded successfully! {len(df)} records found.")
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
    
    # System Status Section
    st.markdown("### System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 8px;">🟢</div>
            <p style="margin: 0; font-weight: 600; color: #059669;">Operational</p>
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">System Status</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 8px;">🟢</div>
            <p style="margin: 0; font-weight: 600; color: #059669;">Connected</p>
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">API Status</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 8px;">🟢</div>
            <p style="margin: 0; font-weight: 600; color: #059669;">Online</p>
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">Database</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 8px;">⚡</div>
            <p style="margin: 0; font-weight: 600; color: #0ea5e9;">&lt;2s</p>
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">Response Time</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# 🚀 Main Application
# ----------------------------
def main():
    # Inject custom CSS
    inject_custom_css()
    
    # Setup Gemini
    model, api_status = setup_gemini()
    
    # Generate sample data
    reports, analytics_data = generate_sample_data()
    
    # Hero Section
    render_hero()
    
    # Status indicator
    st.markdown(f"""
    <div style="text-align: center; margin: 24px 0 32px 0;">
        <span style="background: rgba(255, 255, 255, 0.98); padding: 8px 20px; border-radius: 8px; border: 1px solid #e2e8f0; color: #475569; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08); font-size: 0.9rem;">
            API Status: {api_status}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["AI Assistant", "Relief Reports", "Analytics", "Admin Panel"])
    
    with tab1:
        render_chat_interface(model, api_status)
    
    with tab2:
        render_reports_dashboard(reports)
    
    with tab3:
        render_analytics(analytics_data)
    
    with tab4:
        render_admin_panel()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 60px; padding: 24px; border-top: 1px solid #e2e8f0;">
        <p style="color: #94a3b8; margin: 0; font-size: 0.875rem;">
            © 2025 ReliefMate AI • Emergency Hotline: 112 (Police) | 108 (Medical) | 101 (Fire)
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
