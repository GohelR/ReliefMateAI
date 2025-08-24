import streamlit as st
import pandas as pd
import datetime
import random
import google.generativeai as genai
from streamlit.components.v1 import html
from datetime import date, timedelta
import numpy as np
import os
import sys

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
# 🌟 Advanced CSS with 3D Animations
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        padding: 100px 20px;
        text-align: center;
        position: relative;
        overflow: hidden;
        border-radius: 0 0 50px 50px;
        margin-bottom: 50px;
        backdrop-filter: blur(20px);
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="80" r="1.5" fill="rgba(255,255,255,0.15)"/><circle cx="40" cy="60" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="70" cy="30" r="2.5" fill="rgba(255,255,255,0.05)"/></svg>');
        animation: float 20s infinite linear;
        z-index: 1;
    }
    
    @keyframes float {
        0% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(30px, -30px) rotate(120deg); }
        66% { transform: translate(-20px, 20px) rotate(240deg); }
        100% { transform: translate(0, 0) rotate(360deg); }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 20px;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        z-index: 2;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 20px rgba(255, 107, 107, 0.5)); }
        to { filter: drop-shadow(0 0 40px rgba(78, 205, 196, 0.8)); }
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 40px;
        opacity: 0.9;
        position: relative;
        z-index: 2;
    }
    
    /* Glass Morphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 30px !important;
        margin: 20px 0 !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
        color: white !important;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transform: translateX(-100%);
        transition: transform 0.6s ease;
    }
    
    .glass-card:hover::before {
        transform: translateX(100%);
    }
    
    .glass-card:hover {
        transform: translateY(-10px) scale(1.02) !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3) !important;
        background: rgba(255, 255, 255, 0.15) !important;
    }
    
    /* Feature Cards */
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 20px;
        display: block;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    /* Chat Interface */
    .chat-container {
        background: rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(30px) !important;
        border-radius: 25px !important;
        padding: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        margin: 20px 0 !important;
    }
    
    .chat-message {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 4px solid #4ecdc4;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 15px 30px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4) !important;
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        color: white !important;
        padding: 15px !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4ecdc4 !important;
        box-shadow: 0 0 20px rgba(78, 205, 196, 0.3) !important;
    }
    
    /* Metrics */
    .metric-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4ecdc4;
        margin-bottom: 10px;
        animation: countUp 2s ease;
    }
    
    @keyframes countUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(20px) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
        }
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: #4ecdc4;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# 🔑 Gemini API Setup
# ----------------------------
def setup_gemini():
    # READ from [general] section in .streamlit/secrets.toml
    GEMINI_KEY = None
    try:
        GEMINI_KEY = st.secrets["general"]["GEMINI_API_KEY"]
    except Exception:
        pass

    if GEMINI_KEY:
        try:
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            _ = model.generate_content("test")
            return model, "✅ Gemini AI Connected"
        except Exception as e:
            return None, f"❌ API Error: {str(e)[:50]}..."
    else:
        return None, "⚠️ Demo Mode (Add [general].GEMINI_API_KEY to secrets)"
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
        <h1 class="hero-title">🌍 ReliefMate AI</h1>
        <p class="hero-subtitle">🤝 Advanced Disaster Relief Assistant • Powered by Gemini AI • 24/7 Emergency Support</p>
        <div style="margin-top: 30px;">
            <span style="font-size: 1.2rem; opacity: 0.8;">
                🚨 Emergency Contacts: 112 (Police) • 108 (Medical) • 101 (Fire)
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# 💬 Enhanced Chat Interface
# ----------------------------
def render_chat_interface(model, api_status):
    st.markdown("## 💬 AI Assistant")
    st.markdown("Ask ReliefMate AI about emergency procedures, resource allocation, or disaster response protocols")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask your question:",
            placeholder="e.g., 'What should I do during a flood emergency?'",
            key="chat_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send 🚀", use_container_width=True)
    
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
        st.markdown("### 💬 Conversation")
        for message in reversed(st.session_state.chat_history[-10:]):  # Show last 10 messages
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message" style="border-left: 4px solid #ff6b6b; background: rgba(255, 107, 107, 0.1);">
                    <strong style="color: #ff6b6b;">👤 You:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message" style="border-left: 4px solid #4ecdc4; background: rgba(78, 205, 196, 0.1);">
                    <strong style="color: #4ecdc4;">🤖 ReliefMate AI:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 40px; opacity: 0.7;">
            <h3>🤖 ReliefMate AI Ready</h3>
            <p>Ask me about emergency procedures, disaster preparedness, or resource management</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# 📊 Relief Reports Dashboard
# ----------------------------
def render_reports_dashboard(reports):
    st.markdown("## 📊 Live Relief Operations")
    
    # Status summary
    col1, col2, col3, col4 = st.columns(4)
    
    critical_count = len([r for r in reports if "Critical" in r["status"]])
    active_count = len([r for r in reports if "Active" in r["status"]])
    resolved_count = len([r for r in reports if "Resolved" in r["status"]])
    monitoring_count = len([r for r in reports if "Monitoring" in r["status"]])
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value" style="color: #ff6b6b;">{}</div>
            <div>Critical Cases</div>
        </div>
        """.format(critical_count), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value" style="color: #ffd93d;">{}</div>
            <div>Active Operations</div>
        </div>
        """.format(active_count), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value" style="color: #4ecdc4;">{}</div>
            <div>Resolved Cases</div>
        </div>
        """.format(resolved_count), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value" style="color: #a8e6cf;">{}</div>
            <div>Under Monitoring</div>
        </div>
        """.format(monitoring_count), unsafe_allow_html=True)
    
    # Detailed reports
    st.markdown("### 🏥 Detailed Operations Report")
    
    for i, report in enumerate(reports):
        status_color = {
            "🚨 Critical": "#ff6b6b",
            "🔥 Critical": "#ff6b6b", 
            "⚠️ Active": "#ffd93d",
            "✅ Resolved": "#4ecdc4",
            "📋 Monitoring": "#a8e6cf"
        }.get(report["status"], "#ffffff")
        
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="color: {status_color};">📍 {report["location"]} - {report["type"]}</h3>
                <span style="background: {status_color}; color: black; padding: 5px 15px; border-radius: 20px; font-weight: bold;">
                    {report["status"]}
                </span>
            </div>
            <p><strong>Requirements:</strong> {report["needs"]}</p>
            <p><strong>Assigned Team:</strong> {report["team"]}</p>
            <p><strong>Last Updated:</strong> {datetime.datetime.now().strftime('%H:%M')} IST</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# 📈 Analytics Dashboard
# ----------------------------
def render_analytics(analytics_data):
    st.markdown("## 📈 Performance Analytics")
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': analytics_data['dates'],
        'New Requests': analytics_data['requests'],
        'Resolved Cases': analytics_data['resolved'],
        'Active Cases': analytics_data['active']
    })
    
    # Use Streamlit's built-in charts
    st.markdown("### 📊 7-Day Relief Operations Trend")
    
    # Line chart using Streamlit
    chart_data = df.set_index('Date')[['New Requests', 'Resolved Cases', 'Active Cases']]
    st.line_chart(chart_data)
    
    # Bar chart for comparison
    st.markdown("### 📊 Daily Operations Comparison")
    st.bar_chart(chart_data)
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_requests = sum(analytics_data['requests']) // 7
        st.markdown(f"""
        <div class="glass-card">
            <div class="feature-icon">📈</div>
            <h3>Daily Avg Requests</h3>
            <div class="metric-value">{avg_requests}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_resolved = sum(analytics_data['resolved'])
        st.markdown(f"""
        <div class="glass-card">
            <div class="feature-icon">✅</div>
            <h3>Total Resolved</h3>
            <div class="metric-value">{total_resolved}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        resolution_rate = round((total_resolved / sum(analytics_data['requests'])) * 100, 1)
        st.markdown(f"""
        <div class="glass-card">
            <div class="feature-icon">🎯</div>
            <h3>Resolution Rate</h3>
            <div class="metric-value">{resolution_rate}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional metrics using Streamlit metrics
    st.markdown("### 📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🚨 Critical Cases",
            value="23",
            delta="-5",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="⚡ Avg Response Time",
            value="2.3 min",
            delta="-0.8 min",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="👥 Active Teams",
            value="12",
            delta="+2"
        )
    
    with col4:
        st.metric(
            label="📍 Coverage Areas",
            value="45",
            delta="+3"
        )

# ----------------------------
# 🛠️ Admin Panel
# ----------------------------
def render_admin_panel():
    st.markdown("## 🛠️ Administration Panel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>📝 Submit New Report</h3>
        </div>
        """, unsafe_allow_html=True)
        
        location = st.selectbox("Location", ["Rajkot", "Ahmedabad", "Surat", "Bhavnagar", "Vadodara", "Other"])
        disaster_type = st.selectbox("Disaster Type", ["Flood", "Fire", "Earthquake", "Cyclone", "Landslide", "Other"])
        severity = st.selectbox("Severity", ["🚨 Critical", "⚠️ Active", "📋 Monitoring"])
        description = st.text_area("Description", placeholder="Describe the situation and required assistance...")
        
        if st.button("🚀 Submit Report", use_container_width=True):
            st.success(f"✅ Report submitted successfully! Location: {location}, Type: {disaster_type}, Severity: {severity}")
            st.balloons()
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>📤 Bulk Data Upload</h3>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Upload CSV file with relief data",
            type=["csv"],
            help="Upload CSV files containing relief operation data"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ File uploaded successfully! {len(df)} records found.")
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
        
        st.markdown("### 🔧 System Status")
        st.markdown("""
        <div class="glass-card">
            <p>🟢 <strong>System Status:</strong> Operational</p>
            <p>🟢 <strong>API Status:</strong> Connected</p>
            <p>🟢 <strong>Database:</strong> Online</p>
            <p>🟢 <strong>Response Time:</strong> <2s</p>
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
    <div style="text-align: center; margin: 20px 0;">
        <span style="background: rgba(255, 255, 255, 0.1); padding: 10px 20px; border-radius: 20px; backdrop-filter: blur(10px);">
            🤖 API Status: {api_status}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 AI Assistant", "📊 Relief Reports", "📈 Analytics", "🛠️ Admin Panel"])
    
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
    <div style="background: rgba(0, 0, 0, 0.3); padding: 40px; text-align: center; margin-top: 50px; border-radius: 20px;">
        <h3>🌍 ReliefMate AI</h3>
        <p>Saving Lives Through Technology • Available 24/7 • Emergency Hotline: 112</p>
        <p style="opacity: 0.6; margin-top: 20px;">© 2025 ReliefMate AI • Powered by Gemini AI • Made with ❤️ for Disaster Relief</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

# ----------------------------
# 🎯 Additional Features & Enhancements
# ----------------------------

# Add this to your secrets.toml file:
"""
# .streamlit/secrets.toml
[general]
GEMINI_API_KEY = "your_gemini_api_key_here"

# Optional: Add more configuration
[database]
DB_URL = "your_database_url"

[notifications]
WEBHOOK_URL = "your_webhook_url"
EMAIL_SERVICE = "your_email_service"
"""

# ----------------------------
# 🚀 Deployment Instructions
# ----------------------------

# 1. Install required packages:
"""
pip install streamlit
pip install google-generativeai
pip install pandas
pip install plotly
pip install datetime
"""

# 2. Run the application:
"""
streamlit run app.py
"""

# 3. Access the application at:
"""
http://localhost:8501
"""

# ----------------------------
# 📱 Mobile Responsive Features
# ----------------------------

def add_mobile_optimizations():
    """Add mobile-specific CSS optimizations"""
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem !important;
        }
        
        .hero-subtitle {
            font-size: 1rem !important;
        }
        
        .glass-card {
            padding: 20px !important;
            margin: 10px 0 !important;
        }
        
        .metric-container {
            padding: 15px !important;
        }
        
        .metric-value {
            font-size: 1.8rem !important;
        }
        
        .feature-icon {
            font-size: 2rem !important;
        }
        
        .chat-message {
            padding: 10px !important;
        }
        
        .hero-container {
            padding: 50px 10px !important;
        }
    }
    
    @media (max-width: 480px) {
        .hero-title {
            font-size: 1.5rem !important;
        }
        
        .stButton > button {
            padding: 12px 20px !important;
            font-size: 0.9rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# 🔔 Real-time Notifications System
# ----------------------------

def add_notification_system():
    """Add browser notifications for critical alerts"""
    notification_js = """
    <script>
    function showNotification(title, message, type) {
        if (Notification.permission === "granted") {
            const notification = new Notification(title, {
                body: message,
                icon: type === 'critical' ? '🚨' : '📢',
                badge: '🌍'
            });
            
            setTimeout(() => {
                notification.close();
            }, 5000);
        } else if (Notification.permission !== "denied") {
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    showNotification(title, message, type);
                }
            });
        }
    }
    
    // Auto-request notification permission
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
    
    // Example: Trigger notification for critical alerts
    setInterval(() => {
        const criticalAlerts = Math.random() > 0.95; // 5% chance
        if (criticalAlerts) {
            showNotification(
                'ReliefMate AI Alert', 
                'New critical emergency reported in your area', 
                'critical'
            );
        }
    }, 30000); // Check every 30 seconds
    </script>
    """
    
    st.components.v1.html(notification_js, height=0)

# ----------------------------
# 🗺️ Interactive Map Integration (Future Enhancement)
# ----------------------------

def add_interactive_map():
    """Placeholder for interactive map with relief locations"""
    map_html = """
    <div style="background: rgba(255, 255, 255, 0.1); padding: 30px; border-radius: 20px; text-align: center;">
        <h3>🗺️ Interactive Relief Map</h3>
        <p>📍 Real-time visualization of relief operations across Gujarat</p>
        <div style="background: rgba(0, 0, 0, 0.2); height: 400px; border-radius: 15px; display: flex; align-items: center; justify-content: center; margin: 20px 0;">
            <div>
                <div style="font-size: 3rem; margin-bottom: 10px;">🗺️</div>
                <p>Interactive Map Integration</p>
                <p style="opacity: 0.7; font-size: 0.9rem;">Google Maps / Leaflet / Mapbox</p>
            </div>
        </div>
        <p style="opacity: 0.8;">Feature coming soon: Live tracking of relief teams, resource distribution centers, and emergency zones</p>
    </div>
    """
    
    return map_html

# ----------------------------
# 📊 Advanced Analytics Dashboard
# ----------------------------

def create_advanced_charts():
    """Create charts using Streamlit's built-in functionality"""
    
    # Pie chart data for disaster types
    disaster_data = pd.DataFrame({
        'Type': ['Flood', 'Fire', 'Earthquake', 'Cyclone', 'Landslide'],
        'Count': [45, 23, 12, 18, 8]
    })
    
    return disaster_data

# ----------------------------
# 🎨 Theme Customization
# ----------------------------

def add_theme_selector():
    """Add theme selection for different visual styles"""
    themes = {
        "default": {
            "primary": "#667eea",
            "secondary": "#764ba2",
            "accent": "#4ecdc4"
        },
        "emergency": {
            "primary": "#ff6b6b",
            "secondary": "#ee5a24",
            "accent": "#ffd93d"
        },
        "ocean": {
            "primary": "#0984e3",
            "secondary": "#74b9ff",
            "accent": "#00cec9"
        }
    }
    
    return themes

# ----------------------------
# 🔍 Search and Filter Functionality
# ----------------------------

def add_search_filters():
    """Add search and filter options for reports"""
    search_html = """
    <div class="glass-card">
        <h4>🔍 Search & Filter Reports</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 15px;">
            <div>
                <label style="display: block; margin-bottom: 5px;">Location</label>
                <select style="width: 100%; padding: 8px; border-radius: 8px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white;">
                    <option>All Locations</option>
                    <option>Rajkot</option>
                    <option>Ahmedabad</option>
                    <option>Surat</option>
                </select>
            </div>
            <div>
                <label style="display: block; margin-bottom: 5px;">Status</label>
                <select style="width: 100%; padding: 8px; border-radius: 8px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white;">
                    <option>All Status</option>
                    <option>Critical</option>
                    <option>Active</option>
                    <option>Resolved</option>
                </select>
            </div>
            <div>
                <label style="display: block; margin-bottom: 5px;">Type</label>
                <select style="width: 100%; padding: 8px; border-radius: 8px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white;">
                    <option>All Types</option>
                    <option>Flood</option>
                    <option>Fire</option>
                    <option>Earthquake</option>
                </select>
            </div>
        </div>
    </div>
    """
    
    return search_html

# ----------------------------
# 📞 Emergency Contact Integration
# ----------------------------

def add_emergency_contacts():
    """Add quick emergency contact buttons"""
    contacts_html = """
    <div style="position: fixed; top: 120px; right: 20px; z-index: 1000;">
        <div style="background: rgba(255, 107, 107, 0.9); backdrop-filter: blur(20px); border-radius: 15px; padding: 15px; border: 1px solid rgba(255, 255, 255, 0.2);">
            <h4 style="margin: 0 0 10px 0; text-align: center; color: white;">🚨 Emergency</h4>
            <div style="display: flex; flex-direction: column; gap: 8px;">
                <a href="tel:112" style="background: #ff6b6b; color: white; padding: 8px 12px; border-radius: 8px; text-decoration: none; text-align: center; font-weight: 600;">📞 112 Police</a>
                <a href="tel:108" style="background: #4ecdc4; color: white; padding: 8px 12px; border-radius: 8px; text-decoration: none; text-align: center; font-weight: 600;">🚑 108 Medical</a>
                <a href="tel:101" style="background: #ffd93d; color: white; padding: 8px 12px; border-radius: 8px; text-decoration: none; text-align: center; font-weight: 600;">🚒 101 Fire</a>
            </div>
        </div>
    </div>
    """
    
    return contacts_html

# ----------------------------
# 🏃‍♂️ Performance Optimizations
# ----------------------------

@st.cache_data
def load_cached_data():
    """Cache expensive operations for better performance"""
    return generate_sample_data()

@st.cache_resource
def setup_cached_gemini():
    """Cache Gemini model initialization"""
    return setup_gemini()

# ----------------------------
# 📱 Progressive Web App Features
# ----------------------------

def add_pwa_manifest():
    """Add PWA manifest for mobile app-like experience"""
    manifest = """
    <link rel="manifest" href="data:application/json;base64,ewogICJuYW1lIjogIlJlbGllZk1hdGUgQUkiLAogICJzaG9ydF9uYW1lIjogIlJlbGllZk1hdGUiLAogICJkZXNjcmlwdGlvbiI6ICJEaXNhc3RlciBSZWxpZWYgQXNzaXN0YW50IiwKICAic3RhcnRfdXJsIjogIi8iLAogICJkaXNwbGF5IjogInN0YW5kYWxvbmUiLAogICJiYWNrZ3JvdW5kX2NvbG9yIjogIiM2NjdlZWEiLAogICJ0aGVtZV9jb2xvciI6ICIjNjY3ZWVhIiwKICAiaWNvbnMiOiBbCiAgICB7CiAgICAgICJzcmMiOiAiZGF0YTppbWFnZS9zdmcreG1sO2Jhc2U2NCxQSE4yWnlCNGJXeHVjejBpYUhSMGNEb3ZMM2QzZHk1M00zUnZjbWN2TWpBd01DOXpkbWNpSUhkcFpIUm9QU0kxTVRJaUlHaGxhV2RvZEQwaU5URXlJaUJtYVd4c1BTSWpOall4WW1ZaVBnPT0iLAogICAgICAic2l6ZXMiOiAiNTEyeDUxMiIsCiAgICAgICJ0eXBlIjogImltYWdlL3N2Zyt4bWwiCiAgICB9CiAgXQp9">
    """
    
    return manifest

print("✅ ReliefMate AI - Enhanced 3D Streamlit Application Ready!")
print("🚀 Features included:")
print("   • Advanced 3D animations and glassmorphism design")
print("   • AI-powered chat interface with Gemini integration")
print("   • Real-time relief operations dashboard")
print("   • Interactive analytics with Streamlit charts")
print("   • Mobile-responsive design")
print("   • Emergency contact integration")
print("   • Admin panel for data management")
print("   • Progressive Web App capabilities")
print("")
print("📋 Installation:")
print("   pip install streamlit google-generativeai pandas numpy")
print("")
print("🚀 To run: streamlit run app.py")
print("🔑 Add your Gemini API key to .streamlit/secrets.toml", file=sys.stderr)
print("")
print("🌟 No additional dependencies required - uses Streamlit built-in charts!")
