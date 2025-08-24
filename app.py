# ---------------- Gemini AI Setup ----------------
import os
import streamlit as st
import google.generativeai as genai

def get_gemini_api_key():
    """Get Gemini API key from Streamlit secrets or environment variable."""
    try:
        if "general" in st.secrets and "GEMINI_API_KEY" in st.secrets["general"]:
            return st.secrets["general"]["GEMINI_API_KEY"]
    except Exception:
        pass  # st.secrets might not be available yet

    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        return env_key

    return None

def setup_gemini():
    """Configure Gemini AI if key exists, else run in demo mode."""
    api_key = get_gemini_api_key()
    if not api_key:
        st.warning("⚠️ Gemini API key not found. Running in demo mode.")
        return None, "⚠️ Demo Mode (no GEMINI_API_KEY)"
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        return model, "✅ Gemini AI Connected"
    except Exception as e:
        return None, f"❌ API Error: {str(e)[:80]}"
