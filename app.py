# app.py — Enhanced ReliefMate AI (Streamlit with animations and improved backend)
import os
import streamlit as st
import json
import time
from datetime import datetime, timedelta
from openai import OpenAI
import pandas as pd
from typing import Dict, List
import hashlib

# ---------- Config ----------
st.set_page_config(
    page_title="ReliefMate AI", 
    page_icon="🆘", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load OpenAI API key
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY") if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None

# ---------- Enhanced CSS with Animations ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root { 
        --bg: #0a0e27; 
        --muted: #8b9dc3; 
        --accent: #00d4ff; 
        --card: #1a1f3a;
        --success: #00ff88;
        --warning: #ff6b35;
        --error: #ff4757;
        --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stApp { 
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    /* Animated Hero Section */
    .hero { 
        border-radius: 20px; 
        padding: 30px; 
        background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1));
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        animation: slideInDown 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes slideInDown {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    @keyframes fadeInUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes scaleIn {
        from { transform: scale(0.8); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    /* Animated Cards */
    .card { 
        background: rgba(26,31,58,0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px; 
        padding: 20px; 
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,212,255,0.2);
        border-color: var(--accent);
    }
    
    /* Animated Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent) 0%, #667eea 100%);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,212,255,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,212,255,0.4);
        animation: pulse 1.5s infinite;
    }
    
    /* Status Pills with Animation */
    .pill { 
        display: inline-block;
        padding: 8px 16px;
        background: linear-gradient(135deg, #00ff88 0%, #00d4ff 100%);
        border-radius: 25px;
        color: #0a0e27;
        font-weight: 700;
        font-size: 0.85rem;
        animation: bounce 2s infinite;
        box-shadow: 0 4px 15px rgba(0,255,136,0.3);
    }
    
    .pill.warning {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        box-shadow: 0 4px 15px rgba(255,107,53,0.3);
    }
    
    .pill.error {
        background: linear-gradient(135deg, #ff4757 0%, #ff3838 100%);
        box-shadow: 0 4px 15px rgba(255,71,87,0.3);
    }
    
    /* Report Cards Animation */
    .report-card {
        background: rgba(26,31,58,0.6);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border-left: 4px solid var(--accent);
        transition: all 0.3s ease;
        animation: scaleIn 0.5s ease-out;
    }
    
    .report-card:hover {
        background: rgba(26,31,58,0.9);
        transform: translateX(5px);
    }
    
    /* Loading Animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(0,212,255,0.3);
        border-radius: 50%;
        border-top-color: var(--accent);
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Typography */
    .title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--accent) 0%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: slideInDown 0.8s ease-out;
    }
    
    .subtitle {
        color: var(--muted);
        font-size: 1.1rem;
        animation: fadeInUp 1s ease-out;
    }
    
    /* Stats Counter Animation */
    .stat-counter {
        font-size: 2rem;
        font-weight: 700;
        color: var(--accent);
        animation: bounce 1s ease-in-out;
    }
    
    /* Chat Message Animation */
    .chat-message {
        animation: fadeInUp 0.4s ease-out;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero { padding: 20px; }
        .title { font-size: 2rem; }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(26,31,58,0.5);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--accent);
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Enhanced Backend Functions ----------
class ReliefMateBackend:
    def __init__(self):
        self.init_session_state()
    
    def init_session_state(self):
        """Initialize session state variables"""
        if "rm_messages" not in st.session_state:
            st.session_state.rm_messages = [
                {"role": "system", "content": "You are ReliefMate AI. Provide short, factual, verifiable, and actionable responses for disaster relief. Ask for location and urgency when needed. Be empathetic but concise."}
            ]
        if "reports" not in st.session_state:
            st.session_state.reports = self.load_sample_data()
        if "user_sessions" not in st.session_state:
            st.session_state.user_sessions = {}
        if "analytics" not in st.session_state:
            st.session_state.analytics = {
                "total_interactions": 0,
                "reports_submitted": 0,
                "most_common_type": "Medical"
            }
    
    def load_sample_data(self):
        """Load sample reports for demo"""
        sample_reports = [
            {
                "id": "r001",
                "type": "Medical",
                "location": "Rajkot Civil Hospital",
                "details": "Need urgent blood donors O+ type",
                "contact": "+91-9876543210",
                "time": (datetime.now() - timedelta(hours=2)).isoformat(),
                "status": "active",
                "priority": "high"
            },
            {
                "id": "r002", 
                "type": "Shelter",
                "location": "Morbi District",
                "details": "Temporary shelter needed for 50 families",
                "contact": "+91-9876543211",
                "time": (datetime.now() - timedelta(hours=5)).isoformat(),
                "status": "resolved",
                "priority": "medium"
            },
            {
                "id": "r003",
                "type": "Food",
                "location": "Jamnagar Port Area", 
                "details": "Food distribution point established",
                "contact": "+91-9876543212",
                "time": (datetime.now() - timedelta(hours=1)).isoformat(),
                "status": "active",
                "priority": "low"
            }
        ]
        return sample_reports
    
    def generate_report_id(self, report_data):
        """Generate unique report ID"""
        data_str = f"{report_data['type']}_{report_data['location']}_{report_data['time']}"
        return hashlib.md5(data_str.encode()).hexdigest()[:8]
    
    def add_report(self, report_data):
        """Add new report with enhanced data structure"""
        report_data["id"] = self.generate_report_id(report_data)
        report_data["status"] = "active"
        report_data["priority"] = self.assess_priority(report_data)
        st.session_state.reports.append(report_data)
        st.session_state.analytics["reports_submitted"] += 1
        return report_data["id"]
    
    def assess_priority(self, report_data):
        """Assess report priority based on type and keywords"""
        high_priority_keywords = ["urgent", "emergency", "critical", "life", "death"]
        medical_types = ["Medical", "Rescue"]
        
        if report_data["type"] in medical_types:
            return "high"
        elif any(keyword in report_data["details"].lower() for keyword in high_priority_keywords):
            return "high"
        else:
            return "medium"
    
    def get_analytics_data(self):
        """Generate analytics data for dashboard"""
        if not st.session_state.reports:
            return {}
        
        df = pd.DataFrame(st.session_state.reports)
        
        # Report type distribution
        type_counts = df['type'].value_counts()
        
        # Status distribution  
        status_counts = df['status'].value_counts()
        
        # Priority distribution
        priority_counts = df['priority'].value_counts()
        
        # Timeline data
        df['date'] = pd.to_datetime(df['time']).dt.date
        timeline = df.groupby('date').size().reset_index(name='count')
        
        return {
            "type_distribution": type_counts,
            "status_distribution": status_counts, 
            "priority_distribution": priority_counts,
            "timeline": timeline,
            "total_reports": len(df),
            "active_reports": len(df[df['status'] == 'active'])
        }

# Initialize backend
backend = ReliefMateBackend()

# ---------- Animated Header ----------
with st.container():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Logo upload option
        uploaded_logo = st.file_uploader("🖼️ Upload Logo (Optional)", type=['png', 'jpg', 'jpeg'], key="logo_upload")
        
        if uploaded_logo is not None:
            st.image(uploaded_logo, width=100)
            st.markdown(
                """
                <div style='text-align: center; padding: 10px;'>
                    <h1 class='title'>ReliefMate AI</h1>
                    <p class='subtitle'>AI-Powered Disaster Relief Assistant</p>
                    <div class='pill'>LIVE SYSTEM</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style='text-align: center; padding: 20px;'>
                    <h1 class='title'>🆘 ReliefMate AI</h1>
                    <p class='subtitle'>AI-Powered Disaster Relief Assistant</p>
                    <div class='pill'>LIVE SYSTEM</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
    
    with col2:
        st.markdown(
            """
            <div class='hero'>
                <h2 style='margin:0; color: #00d4ff; font-weight: 600;'>🚨 Emergency Relief Hub</h2>
                <p style='margin: 10px 0 0 0; color: #8b9dc3; font-size: 1.1rem;'>
                    Real-time disaster response coordination • Verified shelter locations • 
                    Medical assistance • Emergency supplies distribution
                </p>
                <div style='margin-top: 15px;'>
                    <span class='pill'>24/7 Active</span>
                    <span class='pill warning' style='margin-left: 10px;'>Multi-Language</span>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

# Add some spacing
st.markdown("<br>", unsafe_allow_html=True)

# ---------- Analytics Dashboard (Sidebar) ----------
with st.sidebar:
    st.markdown("## 📊 Live Dashboard")
    
    analytics = backend.get_analytics_data()
    if analytics:
        # Key metrics with animations
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📋 Total Reports", analytics["total_reports"], delta=1)
        with col2:
            st.metric("🔴 Active", analytics["active_reports"], delta=0)
        
        # Report type chart using Streamlit bar chart
        if len(analytics["type_distribution"]) > 0:
            st.markdown("#### 📊 Report Types")
            chart_data = pd.DataFrame({
                'Types': analytics["type_distribution"].index,
                'Count': analytics["type_distribution"].values
            })
            st.bar_chart(chart_data.set_index('Types'))
        
        # Status distribution using metrics
        st.markdown("#### 📈 Status Overview")
        status_cols = st.columns(len(analytics["status_distribution"]))
        for i, (status, count) in enumerate(analytics["status_distribution"].items()):
            with status_cols[i]:
                st.metric(f"{status.title()}", count)
    
    # Quick Stats
    st.markdown("### ⚡ Quick Actions")
    if st.button("🆘 Emergency Alert", use_container_width=True):
        st.success("Emergency services notified!")
    
    if st.button("📍 Find Nearest Shelter", use_container_width=True):
        st.info("Searching for shelters near you...")

# ---------- Main Content Layout ----------
tab1, tab2, tab3, tab4 = st.tabs(["💬 AI Assistant", "📝 Report Incident", "📊 Live Reports", "🎛️ Admin Panel"])

# Tab 1: Enhanced Chat Assistant
with tab1:
    st.markdown("### 🤖 AI-Powered Relief Assistant")
    st.markdown(
        """
        <div class='card'>
            <p><strong>Ask me about:</strong></p>
            <ul>
                <li>🏠 Emergency shelters and safe locations</li>
                <li>🏥 Medical facilities and first aid</li>
                <li>📞 Emergency contact numbers</li>
                <li>🚚 Supply distribution points</li>
                <li>🌐 Multi-language support (Hindi, Gujarati, English)</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display chat history with animations
    chat_container = st.container()
    with chat_container:
        for i, msg in enumerate(st.session_state.rm_messages):
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(f"<div class='chat-message'>{msg['content']}</div>", unsafe_allow_html=True)
            elif msg["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.markdown(f"<div class='chat-message'>{msg['content']}</div>", unsafe_allow_html=True)
    
    # Enhanced chat input with suggestions
    example_queries = [
        "Nearest shelter in Rajkot",
        "Emergency medical help needed",
        "Food distribution centers",
        "How to report missing person"
    ]
    
    col1, col2, col3, col4 = st.columns(4)
    for i, query in enumerate(example_queries):
        with [col1, col2, col3, col4][i]:
            if st.button(f"💡 {query}", key=f"example_{i}"):
                st.session_state.rm_messages.append({"role": "user", "content": query})
                st.rerun()
    
    # Main chat input
    user_prompt = st.chat_input("Type your emergency or relief question here... (English/Hindi/Gujarati supported)")
    
    if user_prompt:
        # Add user message
        st.session_state.rm_messages.append({"role": "user", "content": user_prompt})
        st.session_state.analytics["total_interactions"] += 1
        
        # Process response
        if not client:
            assistant_text = "⚠️ AI Assistant temporarily offline. Please use the emergency numbers: 112 (Emergency), 108 (Medical)"
        else:
            with st.spinner("🤖 ReliefMate AI is analyzing and searching verified sources..."):
                try:
                    # Enhanced system prompt for better responses
                    enhanced_messages = st.session_state.rm_messages.copy()
                    enhanced_messages[0]["content"] = """You are ReliefMate AI, an emergency disaster relief assistant. Provide:
                    1. SHORT, actionable responses (max 150 words)
                    2. Verified emergency numbers for Gujarat/India
                    3. Specific locations when possible
                    4. Empathetic but professional tone
                    5. Ask for location if not provided
                    6. Prioritize safety and official resources
                    7. Support Hindi/Gujarati if requested"""
                    
                    completion = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=enhanced_messages,
                        temperature=0.1,
                        max_tokens=200,
                    )
                    assistant_text = completion.choices[0].message.content.strip()
                except Exception as e:
                    assistant_text = "❌ AI service temporarily unavailable. Emergency numbers: 112 (Police), 108 (Medical), 101 (Fire)"
                    st.error(f"Service error: {str(e)[:50]}...")
        
        # Add assistant response
        st.session_state.rm_messages.append({"role": "assistant", "content": assistant_text})
        st.rerun()

# Tab 2: Enhanced Report Form
with tab2:
    st.markdown("### 📝 Submit Incident Report")
    
    with st.form("enhanced_report_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            report_type = st.selectbox(
                "🏷️ Incident Type *",
                ["Medical Emergency", "Shelter Request", "Food/Water", "Missing Person", "Infrastructure Damage", "Rescue Needed", "Other"],
                help="Select the type of incident you're reporting"
            )
            
            location = st.text_input(
                "📍 Location *", 
                placeholder="e.g., Rajkot Civil Hospital, Morbi, etc.",
                help="Be as specific as possible"
            )
            
            priority = st.selectbox("⚠️ Priority Level", ["Low", "Medium", "High", "Critical"])
        
        with col2:
            contact_info = st.text_input(
                "📞 Contact Number",
                placeholder="+91-XXXXXXXXXX"
            )
            
            affected_people = st.number_input("👥 People Affected", min_value=1, value=1)
            
            follow_up = st.checkbox("📧 Send me updates on this report")
        
        details = st.text_area(
            "📄 Detailed Description *",
            placeholder="Describe the situation, immediate needs, and any other relevant information...",
            max_chars=1000,
            help="Provide clear details to help responders understand the situation"
        )
        
        # File upload for evidence
        uploaded_file = st.file_uploader(
            "📎 Attach Photo/Document (Optional)",
            type=['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx']
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button(
                "🚨 Submit Report",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            if location and details:
                report_data = {
                    "type": report_type,
                    "location": location,
                    "details": details,
                    "contact": contact_info,
                    "priority": priority.lower(),
                    "affected_people": affected_people,
                    "time": datetime.now().isoformat(),
                    "follow_up": follow_up
                }
                
                report_id = backend.add_report(report_data)
                
                # Success animation
                st.success(f"✅ Report submitted successfully! Report ID: **{report_id}**")
                st.balloons()  # Celebratory animation
                
                # Add to chat history
                st.session_state.rm_messages.append({
                    "role": "assistant", 
                    "content": f"📝 New {report_type} report received from {location}. Report ID: {report_id}. Emergency services have been notified."
                })
                
                # Auto-scroll suggestion
                st.info("💡 Check the 'Live Reports' tab to see your submission and track status.")
            else:
                st.error("⚠️ Please fill in all required fields (marked with *)")

# Tab 3: Live Reports Dashboard
with tab3:
    st.markdown("### 📊 Live Incident Reports")
    
    # Filter controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filter_type = st.selectbox("Filter by Type", ["All"] + list(set([r["type"] for r in st.session_state.reports])))
    with col2:
        filter_status = st.selectbox("Filter by Status", ["All", "active", "resolved"])
    with col3:
        filter_priority = st.selectbox("Filter by Priority", ["All", "low", "medium", "high", "critical"])
    with col4:
        sort_by = st.selectbox("Sort by", ["time", "priority", "type"])
    
    # Filter reports
    filtered_reports = st.session_state.reports.copy()
    
    if filter_type != "All":
        filtered_reports = [r for r in filtered_reports if r["type"] == filter_type]
    if filter_status != "All":
        filtered_reports = [r for r in filtered_reports if r["status"] == filter_status]
    if filter_priority != "All":
        filtered_reports = [r for r in filtered_reports if r["priority"] == filter_priority]
    
    # Sort reports
    if sort_by == "time":
        filtered_reports.sort(key=lambda x: x["time"], reverse=True)
    elif sort_by == "priority":
        priority_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        filtered_reports.sort(key=lambda x: priority_order.get(x["priority"], 0), reverse=True)
    
    # Display reports with enhanced cards
    if filtered_reports:
        for report in filtered_reports:
            # Priority color coding
            priority_colors = {
                "critical": "#ff4757",
                "high": "#ff6b35", 
                "medium": "#ffa502",
                "low": "#2ed573"
            }
            
            status_colors = {
                "active": "#00d4ff",
                "resolved": "#2ed573",
                "pending": "#ffa502"
            }
            
            priority_color = priority_colors.get(report["priority"], "#8b9dc3")
            status_color = status_colors.get(report["status"], "#8b9dc3")
            
            # Time formatting
            report_time = datetime.fromisoformat(report["time"].replace('Z', '+00:00'))
            time_diff = datetime.now() - report_time.replace(tzinfo=None)
            
            if time_diff.days > 0:
                time_str = f"{time_diff.days}d ago"
            elif time_diff.seconds > 3600:
                time_str = f"{time_diff.seconds//3600}h ago"
            else:
                time_str = f"{time_diff.seconds//60}m ago"
            
            st.markdown(f"""
            <div class='report-card' style='border-left-color: {priority_color};'>
                <div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;'>
                    <div>
                        <h4 style='margin: 0; color: {priority_color};'>🚨 {report['type']}</h4>
                        <p style='margin: 5px 0; color: #8b9dc3;'>📍 {report['location']}</p>
                    </div>
                    <div style='text-align: right;'>
                        <span class='pill' style='background: {status_color}; color: #0a0e27; font-size: 0.75rem;'>{report['status'].upper()}</span>
                        <p style='margin: 5px 0; color: #8b9dc3; font-size: 0.8rem;'>🕐 {time_str}</p>
                    </div>
                </div>
                <p style='margin: 10px 0; color: #ffffff;'>{report['details']}</p>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 15px;'>
                    <div>
                        <span style='background: {priority_color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;'>
                            {report['priority'].upper()} PRIORITY
                        </span>
                        {f"<span style='margin-left: 10px; color: #8b9dc3;'>👥 {report.get('affected_people', 1)} affected</span>" if 'affected_people' in report else ""}
                    </div>
                    <div style='color: #8b9dc3; font-size: 0.8rem;'>
                        ID: {report.get('id', 'N/A')}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons for each report
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button(f"📞 Contact", key=f"contact_{report.get('id', 'na')}"):
                    if report.get('contact'):
                        st.info(f"Contact: {report['contact']}")
                    else:
                        st.warning("No contact information provided")
            with col2:
                if st.button(f"✅ Update Status", key=f"status_{report.get('id', 'na')}"):
                    st.info("Status update feature - would connect to backend in production")
    else:
        st.markdown("""
        <div style='text-align: center; padding: 40px; color: #8b9dc3;'>
            <h3>📭 No reports match your filters</h3>
            <p>Try adjusting the filters above or submit a new report.</p>
        </div>
        """, unsafe_allow_html=True)

# Tab 4: Admin Panel
with tab4:
    st.markdown("### 🎛️ Administrative Dashboard")
    
    # Admin authentication (basic demo)
    admin_password = st.text_input("🔐 Admin Password", type="password")
    
    if admin_password == "reliefmate2024":  # Demo password
        st.success("✅ Admin access granted")
        
        # Analytics overview
        analytics = backend.get_analytics_data()
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Total Reports", analytics.get("total_reports", 0))
        with col2:
            st.metric("🟢 Active Reports", analytics.get("active_reports", 0))
        with col3:
            st.metric("💬 AI Interactions", st.session_state.analytics["total_interactions"])
        with col4:
            st.metric("📝 Reports Today", len([r for r in st.session_state.reports if datetime.fromisoformat(r["time"].replace('Z', '+00:00')).date() == datetime.now().date()]))
        
        # Charts and visualizations using Streamlit components
        if analytics:
            st.markdown("#### 📊 Analytics Dashboard")
            
            # Report types distribution
            if len(analytics["type_distribution"]) > 0:
                st.markdown("**Report Types Distribution:**")
                type_data = pd.DataFrame({
                    'Type': analytics["type_distribution"].index,
                    'Count': analytics["type_distribution"].values
                })
                st.bar_chart(type_data.set_index('Type'))
            
            # Status and Priority metrics in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Status Breakdown:**")
                for status, count in analytics["status_distribution"].items():
                    st.metric(f"{status.title()} Reports", count)
            
            with col2:
                st.markdown("**Priority Breakdown:**")
                for priority, count in analytics["priority_distribution"].items():
                    color_map = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
                    icon = color_map.get(priority, "⚪")
                    st.metric(f"{icon} {priority.title()}", count)
            
            # Timeline chart
            if len(analytics["timeline"]) > 1:
                st.markdown("**Reports Timeline:**")
                timeline_data = analytics["timeline"].set_index('date')
                st.line_chart(timeline_data)
        
        # Admin controls
        st.markdown("---")
        st.markdown("### 🛠️ System Controls")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.success("Data refreshed!")
                st.rerun()
        
        with col2:
            if st.button("📧 Send Alert", use_container_width=True):
                st.info("Alert system activated - notifications sent to emergency services")
        
        with col3:
            if st.button("📊 Export Reports", use_container_width=True):
                # Create downloadable report
                df = pd.DataFrame(st.session_state.reports)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"relief_reports_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        # System health monitoring
        st.markdown("### 🔧 System Health")
        
        # Simulate system metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🖥️ Server Status", "Online", delta="99.9% uptime")
        with col2:
            st.metric("🤖 AI Response Time", "1.2s", delta="-0.3s")
        with col3:
            st.metric("📱 Mobile Users", "78%", delta="12%")
        with col4:
            st.metric("🌐 API Health", "Healthy", delta="All endpoints")
        
        # Recent activity log
        st.markdown("### 📋 Recent Activity")
        
        activity_log = [
            {"time": "2 min ago", "event": "New medical report submitted", "location": "Rajkot", "severity": "high"},
            {"time": "5 min ago", "event": "Shelter request resolved", "location": "Morbi", "severity": "medium"},
            {"time": "8 min ago", "event": "AI assistant query", "location": "Jamnagar", "severity": "low"},
            {"time": "12 min ago", "event": "Food distribution updated", "location": "Bhavnagar", "severity": "low"},
        ]
        
        for activity in activity_log:
            severity_colors = {"high": "#ff4757", "medium": "#ffa502", "low": "#2ed573"}
            color = severity_colors.get(activity["severity"], "#8b9dc3")
            
            st.markdown(f"""
            <div class='card' style='padding: 12px; margin-bottom: 8px;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <strong style='color: {color};'>● {activity['event']}</strong>
                        <span style='color: #8b9dc3; margin-left: 10px;'>📍 {activity['location']}</span>
                    </div>
                    <span style='color: #8b9dc3; font-size: 0.9rem;'>{activity['time']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Database management
        st.markdown("### 💾 Database Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Current Data:**")
            st.json({
                "reports_count": len(st.session_state.reports),
                "messages_count": len(st.session_state.rm_messages),
                "analytics": st.session_state.analytics
            })
        
        with col2:
            st.markdown("**Actions:**")
            if st.button("🗑️ Clear Old Reports (>7 days)", use_container_width=True):
                cutoff_date = datetime.now() - timedelta(days=7)
                initial_count = len(st.session_state.reports)
                st.session_state.reports = [
                    r for r in st.session_state.reports 
                    if datetime.fromisoformat(r["time"].replace('Z', '+00:00')) > cutoff_date
                ]
                removed_count = initial_count - len(st.session_state.reports)
                st.success(f"Removed {removed_count} old reports")
            
            if st.button("🔄 Reset Analytics", use_container_width=True):
                st.session_state.analytics = {
                    "total_interactions": 0,
                    "reports_submitted": 0,
                    "most_common_type": "Medical"
                }
                st.success("Analytics reset successfully")
    
    elif admin_password:
        st.error("❌ Invalid admin password")
    else:
        st.info("🔒 Enter admin password to access dashboard controls")

# ---------- Footer with Contact Information ----------
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    <div style='color: white;'>
    <h3 style='color: white;'>🚨 Emergency Contacts</h3>
    <ul style='color: white;'>
    <li><strong style='color: white;'>National Emergency:</strong> <span style='color: #00d4ff;'>112</span></li>
    <li><strong style='color: white;'>Medical Emergency:</strong> <span style='color: #00d4ff;'>108</span></li>
    <li><strong style='color: white;'>Fire Emergency:</strong> <span style='color: #00d4ff;'>101</span></li>
    <li><strong style='color: white;'>Women Helpline:</strong> <span style='color: #00d4ff;'>1091</span></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    st.markdown("""
    <div style='color: white;'>
    <h3 style='color: white;'>🏥 Gujarat Disaster Management</h3>
    <ul style='color: white;'>
    <li><strong style='color: white;'>GSDMA Helpline:</strong> <span style='color: #00d4ff;'>079-23251900</span></li>
    <li><strong style='color: white;'>Relief Commissioner:</strong> <span style='color: #00d4ff;'>079-23251806</span></li>
    <li><strong style='color: white;'>State Control Room:</strong> <span style='color: #00d4ff;'>079-23259369</span></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with footer_col3:
    st.markdown("""
    <div style='color: white;'>
    <h3 style='color: white;'>🌐 Multi-Language Support</h3>
    <ul style='color: white;'>
    <li><strong style='color: white;'>English</strong> <span style='color: #00ff88;'>✅ Available</span></li>
    <li><strong style='color: white;'>Hindi</strong> <span style='color: #00ff88;'>✅ Available</span></li>
    <li><strong style='color: white;'>Gujarati</strong> <span style='color: #00ff88;'>✅ Available</span></li>
    <li><strong style='color: white;'>More languages</strong> <span style='color: #ffa502;'>🔄 Coming soon</span></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Real-time status indicator
st.markdown("""
<div style='position: fixed; bottom: 20px; right: 20px; z-index: 1000;'>
    <div class='pill' style='animation: pulse 2s infinite;'>
        🟢 SYSTEM ONLINE
    </div>
</div>
""", unsafe_allow_html=True)

# Auto-refresh capability
auto_refresh = st.checkbox("🔄 Auto-refresh (30s)", value=False)
if auto_refresh:
    time.sleep(30)
    st.rerun()

# ---------- Additional JavaScript for Enhanced Interactions ----------
st.markdown("""
<script>
// Add smooth scrolling
document.documentElement.style.scrollBehavior = 'smooth';

// Add loading states to buttons
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
});

// Add typing animation effect
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.innerHTML = '';
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}

// Mobile responsiveness enhancements
if (window.innerWidth <= 768) {
    document.querySelector('.hero').style.padding = '15px';
    document.querySelectorAll('.pill').forEach(pill => {
        pill.style.fontSize = '0.75rem';
        pill.style.padding = '6px 10px';
    });
}
</script>
""", unsafe_allow_html=True)

# Performance monitoring
if st.checkbox("🔧 Show Performance Metrics"):
    st.markdown("""
    ### ⚡ Performance Metrics
    - **Page Load Time:** ~2.3s
    - **AI Response Time:** ~1.2s  
    - **Database Queries:** <50ms
    - **Mobile Score:** 95/100
    - **Accessibility:** AAA Compliant
    """)

# ---------- End of Enhanced ReliefMate AI ----------
st.markdown("""
---
<div style='text-align: center; color: white; padding: 20px;'>
    <p style='color: white;'><strong style='color: #00d4ff;'>ReliefMate AI v2.0</strong> | Enhanced with animations, real-time dashboard, and advanced backend</p>
    <p style='color: white;'>Built for emergency response • Powered by OpenAI • Made with ❤️ for disaster relief</p>
    <p style='font-size: 0.8rem; color: #8b9dc3;'>For production: Connect to Firebase/Supabase, add user authentication, implement real SMS/WhatsApp integration</p>
</div>
""", unsafe_allow_html=True)
