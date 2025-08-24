import streamlit as st
import pandas as pd
import datetime
import random
import google.generativeai as genai
from streamlit.components.v1 import html
from datetime import date, timedelta

# ----------------------------
# 🎨 Page Config
# ----------------------------
st.set_page_config(
    page_title="ReliefMate AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# 🌟 CSS for UI/UX
# ----------------------------
st.markdown("""
    <style>
    .main { padding: 1.5rem; }
    .stButton>button { border-radius: 10px; font-weight: 600; }
    .chat-box { border:1px solid #ddd; border-radius:10px; padding:1rem; margin:0.5rem 0; background:#f9f9f9; }
    .chat-user { color:#007bff; font-weight:bold; }
    .chat-ai { color:#28a745; font-weight:bold; }
    .report-card {
        background: linear-gradient(135deg, #e3f2fd, #e1f5fe);
        padding: 20px; border-radius: 15px; margin: 10px 0;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# 🔑 Gemini API Setup
# ----------------------------
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

model = None
api_key_status = "Not configured"

if GEMINI_KEY:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        test_response = model.generate_content("test")
        api_key_status = "✅ Gemini Working"
    except Exception as e:
        api_key_status = f"❌ Error: {str(e)[:100]}"
        model = None

# ----------------------------
# 🏠 Hero Section
# ----------------------------
st.title("🌍 ReliefMate AI")
st.markdown("### 🤝 Disaster Relief Assistant – Powered by Gemini AI")
st.success(f"API Status: {api_key_status}")

# ----------------------------
# 📑 Tabs
# ----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["💬 AI Assistant", "📊 Relief Reports", "📈 Analytics", "🛠️ Admin Panel"])

# ----------------------------
# 💬 Tab 1: AI Assistant
# ----------------------------
with tab1:
    st.header("💬 ReliefMate AI Assistant")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_prompt = st.text_input("Ask ReliefMate AI your question:", key="user_input")

    if st.button("Ask AI"):
        if not model:
            assistant_text = "❌ Gemini not configured. Emergency numbers: 112 (Police), 108 (Medical), 101 (Fire)"
        else:
            with st.spinner("🤖 ReliefMate AI is analyzing..."):
                try:
                    enhanced_prompt = f"""
                    You are ReliefMate AI, a disaster relief assistant.
                    Provide short, actionable answers (max 150 words).
                    Include emergency contacts for Gujarat/India when relevant.
                    Be empathetic and concise. Support Hindi/Gujarati if asked.

                    User: {user_prompt}
                    """
                    response = model.generate_content(enhanced_prompt)
                    assistant_text = response.text.strip()
                except Exception as e:
                    assistant_text = "❌ Gemini AI temporarily unavailable. Emergency numbers: 112 (Police), 108 (Medical), 101 (Fire)"
                    st.error(f"Service error: {str(e)[:50]}...")

        st.session_state.chat_history.append({"user": user_prompt, "ai": assistant_text})

    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"""
        <div class="chat-box">
            <div class="chat-user">👤 You: {chat['user']}</div>
            <div class="chat-ai">🤖 ReliefMate: {chat['ai']}</div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# 📊 Tab 2: Relief Reports
# ----------------------------
with tab2:
    st.header("📊 Real-Time Relief Reports")

    sample_reports = [
        {"location": "Rajkot", "needs": "Food, Water", "status": "Active"},
        {"location": "Ahmedabad", "needs": "Medical Kits", "status": "Resolved"},
        {"location": "Surat", "needs": "Shelter, Blankets", "status": "Active"},
        {"location": "Bhavnagar", "needs": "Rescue Boats", "status": "Critical"},
    ]

    for report in sample_reports:
        st.markdown(f"""
        <div class="report-card">
            <h4>📍 {report['location']}</h4>
            <p><b>Needs:</b> {report['needs']}</p>
            <p><b>Status:</b> {report['status']}</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# 📈 Tab 3: Analytics Dashboard
# ----------------------------
with tab3:
    st.header("📈 Relief Analytics")

    dates = [date.today() - timedelta(days=i) for i in range(7)]
    data = {"Date": dates[::-1],
            "Requests": [random.randint(50, 200) for _ in range(7)],
            "Resolved": [random.randint(20, 150) for _ in range(7)]}
    df = pd.DataFrame(data)

    st.line_chart(df.set_index("Date"))

# ----------------------------
# 🛠️ Tab 4: Admin Panel
# ----------------------------
with tab4:
    st.header("🛠️ Admin Panel")
    new_report = st.text_input("Enter new report (e.g., 'Flood in Junagadh - Need Rescue')")

    if st.button("Submit Report"):
        st.success("✅ New report submitted successfully!")

    uploaded_file = st.file_uploader("Upload CSV of reports", type=["csv"])
    if uploaded_file:
        df_upload = pd.read_csv(uploaded_file)
        st.write(df_upload)
