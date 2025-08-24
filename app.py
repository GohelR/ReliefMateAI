# app.py — ReliefMate AI with Free API Alternatives
import os
import streamlit as st
import json
import time
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List
import hashlib
import requests

# ---------- Config ----------
st.set_page_config(
    page_title="ReliefMate AI", 
    page_icon="🆘", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- FREE API CONFIGURATIONS ----------

# Option 1: Hugging Face (Free with rate limits)
HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY") if "HUGGINGFACE_API_KEY" in st.secrets else os.getenv("HUGGINGFACE_API_KEY")

# Option 2: Cohere (Free tier available)
COHERE_API_KEY = st.secrets.get("COHERE_API_KEY") if "COHERE_API_KEY" in st.secrets else os.getenv("COHERE_API_KEY")

# Option 3: Google Gemini (Free tier)
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")

# Option 4: Ollama (Completely free, runs locally)
OLLAMA_BASE_URL = "http://localhost:11434"

# ---------- API CLIENT CLASSES ----------

class HuggingFaceClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api-inference.huggingface.co/models"
        # Free models available on Hugging Face
        self.model = "microsoft/DialoGPT-medium"  # Good for conversation
        # Alternative: "facebook/blenderbot-400M-distill"
    
    def chat_completion(self, messages, max_tokens=200):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Convert messages to single prompt for DialoGPT
        prompt = ""
        for msg in messages[-5:]:  # Use last 5 messages for context
            if msg["role"] == "user":
                prompt += f"User: {msg['content']}\n"
            elif msg["role"] == "assistant":
                prompt += f"Bot: {msg['content']}\n"
        prompt += "Bot:"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": 0.7,
                "do_sample": True
            }
        }
        
        response = requests.post(
            f"{self.base_url}/{self.model}",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                # Extract only the new response
                if "Bot:" in generated_text:
                    bot_response = generated_text.split("Bot:")[-1].strip()
                    return bot_response
            return "I'm here to help with emergency relief information."
        else:
            raise Exception(f"HuggingFace API error: {response.status_code}")

class CohereClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.cohere.ai/v1"
    
    def chat_completion(self, messages, max_tokens=200):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Convert messages to Cohere format
        conversation_history = []
        for msg in messages[1:]:  # Skip system message
            conversation_history.append({
                "role": "USER" if msg["role"] == "user" else "CHATBOT",
                "message": msg["content"]
            })
        
        payload = {
            "message": messages[-1]["content"] if messages else "Hello",
            "model": "command-light",  # Free tier model
            "max_tokens": max_tokens,
            "temperature": 0.3,
            "chat_history": conversation_history[:-1],  # All except last message
            "preamble": "You are ReliefMate AI, a helpful disaster relief assistant. Provide short, actionable emergency guidance."
        }
        
        response = requests.post(
            f"{self.base_url}/chat",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('text', 'I can help with emergency relief information.')
        else:
            raise Exception(f"Cohere API error: {response.status_code}")

class GeminiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    def chat_completion(self, messages, max_tokens=200):
        headers = {"Content-Type": "application/json"}
        
        # Convert to Gemini format
        contents = []
        for msg in messages[1:]:  # Skip system message
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": 0.3
            },
            "systemInstruction": {
                "parts": [{"text": messages[0]["content"]}]
            }
        }
        
        response = requests.post(
            f"{self.base_url}/models/gemini-pro:generateContent?key={self.api_key}",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            return "I'm ready to assist with emergency relief guidance."
        else:
            raise Exception(f"Gemini API error: {response.status_code}")

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.model = "llama2"  # or "mistral", "codellama"
    
    def chat_completion(self, messages, max_tokens=200):
        # Convert messages to single prompt
        prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt += f"System: {msg['content']}\n"
            elif msg["role"] == "user":
                prompt += f"Human: {msg['content']}\n"
            elif msg["role"] == "assistant":
                prompt += f"Assistant: {msg['content']}\n"
        prompt += "Assistant:"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.3
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'Ollama response received.')
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
        except requests.exceptions.ConnectionError:
            raise Exception("Ollama not running. Install and run: 'ollama serve'")

# ---------- FALLBACK RULE-BASED RESPONSES ----------

class FallbackResponder:
    def __init__(self):
        self.responses = {
            "shelter": {
                "rajkot": """🏠 **Emergency Shelters in Rajkot:**
                
• **Rajkot Civil Hospital** - Near Railway Station
• **Municipal Corporation Relief Centers** - Contact: 0281-2463000  
• **Red Cross Shelter** - University Road
• **Community Centers** in Ghanteshwar, Kalawad Road
                
📞 **Emergency Contacts:**
- GSDMA Helpline: 079-23251900
- Rajkot Collector Office: 0281-2463000""",
                "default": """🏠 **Finding Emergency Shelters:**
                
• Contact local Municipal Corporation
• Visit nearest school/community center
• Check with Red Cross Society
• Call State Disaster Management: 079-23251900"""
            },
            "medical": """🏥 **Medical Emergency Response:**
            
• **Dial 108** - Free ambulance service
• **Nearest Hospital** - Ask locals or call 102
• **First Aid** - Stop bleeding, keep warm, don't move if spine injury
• **Poison Control** - 1066
            
🚨 **Critical Signs:** Unconsciousness, severe bleeding, difficulty breathing""",
            
            "food": """🍽️ **Food & Water Resources:**
            
• **Government Relief Centers** - Contact Collector Office
• **NGO Distribution Points** - Akshaya Patra, Khalsa Aid
• **Community Kitchens** - Religious institutions
• **Water Purification** - Boil for 10 minutes or use purification tablets""",
            
            "missing": """👥 **Missing Person Protocol:**
            
• **File Police Report** - Nearest station immediately
• **Contact Helplines** - Women: 1091, Child: 1098
• **Social Media** - Share photo with last known location
• **Relief Camps** - Check all nearby camps
• **Hospitals** - Contact all medical facilities in area""",
            
            "default": """⚠️ **Emergency Information Hub:**
            
🚨 **Immediate Help:**
- Police: 100 | Fire: 101 | Medical: 108
- National Emergency: 112
- Disaster Helpline: 1078
            
🏥 **For specific help, ask about:**
- Shelters in [city name]
- Medical facilities
- Food distribution
- Missing person procedures"""
        }
    
    def get_response(self, query):
        query_lower = query.lower()
        
        # Location-specific shelter responses
        if "shelter" in query_lower:
            if "rajkot" in query_lower:
                return self.responses["shelter"]["rajkot"]
            else:
                return self.responses["shelter"]["default"]
        
        # Medical emergency
        elif any(word in query_lower for word in ["medical", "hospital", "doctor", "ambulance", "injury"]):
            return self.responses["medical"]
        
        # Food and water
        elif any(word in query_lower for word in ["food", "water", "hungry", "thirsty", "distribution"]):
            return self.responses["food"]
        
        # Missing person
        elif any(word in query_lower for word in ["missing", "lost", "find person", "disappeared"]):
            return self.responses["missing"]
        
        # Default response
        else:
            return self.responses["default"]

# ---------- INITIALIZE CLIENTS ----------

# Initialize clients based on available API keys
clients = []
client_names = []

# Try Gemini (Google) - Free tier available
if GEMINI_API_KEY:
    try:
        gemini_client = GeminiClient(GEMINI_API_KEY)
        clients.append(("Gemini", gemini_client))
        client_names.append("Gemini (Free)")
    except:
        pass

# Try Cohere - Free tier available  
if COHERE_API_KEY:
    try:
        cohere_client = CohereClient(COHERE_API_KEY)
        clients.append(("Cohere", cohere_client))
        client_names.append("Cohere (Free)")
    except:
        pass

# Try Hugging Face - Free tier available
if HUGGINGFACE_API_KEY:
    try:
        hf_client = HuggingFaceClient(HUGGINGFACE_API_KEY)
        clients.append(("HuggingFace", hf_client))
        client_names.append("HuggingFace (Free)")
    except:
        pass

# Try Ollama - Completely free but needs local installation
try:
    ollama_client = OllamaClient()
    # Test connection
    requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
    clients.append(("Ollama", ollama_client))
    client_names.append("Ollama (Local)")
except:
    pass

# Fallback to rule-based responses
fallback_responder = FallbackResponder()

# ---------- API STATUS DISPLAY ----------
api_status = "🔴 No AI APIs configured"
if clients:
    api_status = f"🟢 Using {client_names[0]}"

# Debug API status
if st.checkbox("🔧 Debug API Status", key="debug_api"):
    st.info(f"**Available AI Services:** {', '.join(client_names) if client_names else 'None - Using fallback responses'}")
    
    # Show setup instructions
    with st.expander("📚 Free API Setup Instructions"):
        st.markdown("""
        ### 🆓 Free AI API Options:
        
        **1. Google Gemini (Recommended)**
        - Visit: https://makersuite.google.com/app/apikey
        - Get free API key (generous limits)
        - Add to secrets: `GEMINI_API_KEY = "your-key-here"`
        
        **2. Cohere**  
        - Visit: https://dashboard.cohere.ai/api-keys
        - Free tier: 100 calls/month
        - Add to secrets: `COHERE_API_KEY = "your-key-here"`
        
        **3. Hugging Face**
        - Visit: https://huggingface.co/settings/tokens
        - Free inference API (rate limited)
        - Add to secrets: `HUGGINGFACE_API_KEY = "your-key-here"`
        
        **4. Ollama (Best for Privacy)**
        - Install: `curl -fsSL https://ollama.ai/install.sh | sh`
        - Run: `ollama pull llama2` then `ollama serve`
        - Completely free, runs offline
        
        **5. Fallback Mode**
        - No API needed
        - Pre-programmed emergency responses
        - Always available as backup
        """)

# ---------- AI RESPONSE FUNCTION ----------
def get_ai_response(messages):
    """Get AI response using available free APIs with fallback"""
    
    # Try each available AI client
    for client_name, client in clients:
        try:
            with st.spinner(f"🤖 {client_name} AI processing..."):
                response = client.chat_completion(messages, max_tokens=200)
                return response, client_name
        except Exception as e:
            st.warning(f"⚠️ {client_name} temporarily unavailable: {str(e)[:50]}...")
            continue
    
    # Fallback to rule-based responses
    user_query = messages[-1]["content"] if messages else ""
    fallback_response = fallback_responder.get_response(user_query)
    return fallback_response, "Fallback System"

# ---------- REST OF THE APPLICATION (Same as before) ----------

# Enhanced CSS with Animations
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
    
    .hero { 
        border-radius: 20px; 
        padding: 30px; 
        background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1));
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        animation: slideInDown 0.8s ease-out;
    }
    
    @keyframes slideInDown {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .pill { 
        display: inline-block;
        padding: 8px 16px;
        background: linear-gradient(135deg, #00ff88 0%, #00d4ff 100%);
        border-radius: 25px;
        color: #0a0e27;
        font-weight: 700;
        font-size: 0.85rem;
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
    
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Backend class (same as before)
class ReliefMateBackend:
    def __init__(self):
        self.init_session_state()
    
    def init_session_state(self):
        if "rm_messages" not in st.session_state:
            st.session_state.rm_messages = [
                {"role": "system", "content": "You are ReliefMate AI. Provide short, factual, verifiable, and actionable responses for disaster relief. Ask for location and urgency when needed. Be empathetic but concise."}
            ]
        if "reports" not in st.session_state:
            st.session_state.reports = self.load_sample_data()
        if "analytics" not in st.session_state:
            st.session_state.analytics = {
                "total_interactions": 0,
                "reports_submitted": 0,
                "ai_service": client_names[0] if client_names else "Fallback"
            }
    
    def load_sample_data(self):
        return [
            {
                "id": "r001",
                "type": "Medical",
                "location": "Rajkot Civil Hospital",
                "details": "Need urgent blood donors O+ type",
                "contact": "+91-9876543210",
                "time": (datetime.now() - timedelta(hours=2)).isoformat(),
                "status": "active",
                "priority": "high"
            }
        ]
    
    def add_report(self, report_data):
        report_data["id"] = hashlib.md5(f"{report_data['type']}_{report_data['location']}_{report_data['time']}".encode()).hexdigest()[:8]
        report_data["status"] = "active"
        report_data["priority"] = "medium"
        st.session_state.reports.append(report_data)
        st.session_state.analytics["reports_submitted"] += 1
        return report_data["id"]

backend = ReliefMateBackend()

# Header
st.markdown(
    """
    <div class='hero'>
        <h1 style='margin:0; color: #00d4ff; font-size: 2.5rem; font-weight: 700;'>🆘 ReliefMate AI</h1>
        <p style='margin: 10px 0; color: #8b9dc3; font-size: 1.2rem;'>AI-Powered Disaster Relief Assistant</p>
        <div style='margin-top: 15px;'>
            <span class='pill'>FREE VERSION</span>
            <span class='pill warning' style='margin-left: 10px;'>""" + api_status + """</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3 = st.tabs(["💬 AI Assistant", "📝 Report Incident", "📊 Live Reports"])

# Tab 1: AI Assistant
with tab1:
    st.markdown("### 🤖 Emergency Relief Assistant")
    
    # Display current AI service
    st.info(f"🔧 **Current AI Service:** {api_status}")
    
    # Chat interface
    for msg in st.session_state.rm_messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        elif msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write(msg["content"])
    
    # Chat input
    user_prompt = st.chat_input("Ask about emergency relief, shelters, medical help...")
    
    if user_prompt:
        # Add user message
        st.session_state.rm_messages.append({"role": "user", "content": user_prompt})
        st.session_state.analytics["total_interactions"] += 1
        
        # Get AI response
        assistant_text, service_used = get_ai_response(st.session_state.rm_messages)
        st.session_state.analytics["ai_service"] = service_used
        
        # Add assistant response
        st.session_state.rm_messages.append({"role": "assistant", "content": assistant_text})
        st.rerun()

# Tab 2: Report Form (simplified)
with tab2:
    st.markdown("### 📝 Submit Emergency Report")
    
    with st.form("report_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            report_type = st.selectbox("Type", ["Medical", "Shelter", "Food", "Missing Person", "Other"])
            location = st.text_input("Location *", placeholder="City, landmark...")
        
        with col2:
            contact = st.text_input("Contact", placeholder="+91-XXXXXXXXXX")
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        
        details = st.text_area("Details *", placeholder="Describe the emergency...")
        
        if st.form_submit_button("🚨 Submit Report", type="primary"):
            if location and details:
                report_data = {
                    "type": report_type,
                    "location": location,
                    "details": details,
                    "contact": contact,
                    "time": datetime.now().isoformat(),
                    "priority": priority.lower()
                }
                report_id = backend.add_report(report_data)
                st.success(f"✅ Report submitted! ID: {report_id}")
                st.balloons()
            else:
                st.error("Please fill required fields")

# Tab 3: Reports Display (simplified)
with tab3:
    st.markdown("### 📊 Live Reports")
    
    for report in st.session_state.reports:
        with st.expander(f"🚨 {report['type']} - {report['location']}"):
            st.write(f"**Details:** {report['details']}")
            st.write(f"**Priority:** {report['priority'].title()}")
            st.write(f"**Time:** {report['time'][:19].replace('T', ' ')}")
            if report.get('contact'):
                st.write(f"**Contact:** {report['contact']}")

# Footer
st.markdown("---")
st.markdown("""
**🚨 Emergency Numbers:** Police: 100 | Fire: 101 | Medical: 108 | Emergency: 112
""")

st.markdown(f"""
<div style='text-align: center; color: #8b9dc3; padding: 20px;'>
    <p>ReliefMate AI - Free Version | Current Service: {st.session_state.analytics.get('ai_service', 'Fallback')}</p>
    <p>Total Interactions: {st.session_state.analytics['total_interactions']} | Reports: {st.session_state.analytics['reports_submitted']}</p>
</div>
""", unsafe_allow_html=True)
