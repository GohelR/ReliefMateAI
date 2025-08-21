
import os
import streamlit as st
from dotenv import load_dotenv
from typing import Dict

# Optional: Use OpenAI if available
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

load_dotenv()
st.set_page_config(page_title="ReliefMate AI", page_icon="🚨", layout="centered")

st.title("ReliefMate AI – Disaster Relief Assistant 🚨")
st.write("Ask about shelters, hospitals, helplines, or submit a need. (Prototype)")

api_key = os.getenv("OPENAI_API_KEY", "")
if not api_key:
    st.info("Set your OpenAI API key in `.env` to enable AI responses.")

# Simple in-memory "db"
if "requests" not in st.session_state:
    st.session_state.requests = []

tab1, tab2 = st.tabs(["Chat", "Report a Need"])

with tab1:
    user_q = st.text_input("Your question")
    if st.button("Ask") and user_q:
        # Fallback answer
        answer = "This is a demo response. Provide verified info, nearest shelters, and helplines here."
        # If OpenAI configured, generate a better reply
        if api_key and OpenAI is not None:
            client = OpenAI(api_key=api_key)
            try:
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role":"system","content":"You are a concise disaster relief assistant. Prefer verified, safety-first guidance."},
                        {"role":"user","content":user_q}
                    ],
                    temperature=0.3
                )
                answer = resp.choices[0].message.content
            except Exception as e:
                answer = f"AI error: {e}"
        st.success(answer)

with tab2:
    with st.form("need_form"):
        name = st.text_input("Your name (optional)")
        location = st.text_input("Location (City/Area)")
        need = st.selectbox("Type of need", ["Rescue","Medical","Food","Shelter","Other"])
        details = st.text_area("Details (what help is needed?)")
        submitted = st.form_submit_button("Submit need")
    if submitted:
        item = {"name": name, "location": location, "need": need, "details": details}
        st.session_state.requests.append(item)
        st.success("Submitted. Stay safe. Volunteers will prioritize requests in the dashboard (planned).")

    if st.checkbox("Show submitted needs (demo)"):
        st.table(st.session_state.requests)
