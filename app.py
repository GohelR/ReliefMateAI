# app.py — Polished ReliefMate AI (Streamlit) with OpenAI chat
import os
import streamlit as st
from datetime import datetime
import openai

# ---------- Config ----------
st.set_page_config(page_title="ReliefMate AI", page_icon="🆘", layout="wide")

# Load key safely (Streamlit secrets > env var)
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY") if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY

# ---------- Small CSS for nicer UI ----------
st.markdown(
    """
    <style>
    :root { --bg: #071024; --muted: #9fb7d9; --accent: #06b6d4; --card: #0b1220; }
    .page-bg { background: linear-gradient(180deg, rgba(2,6,23,1) 0%, rgba(7,16,36,1) 100%); padding: 18px 0; }
    .hero { border-radius: 12px; padding: 18px; background: linear-gradient(90deg, rgba(2,6,23,0.6), rgba(4,20,40,0.6)); box-shadow: 0 6px 18px rgba(2,6,23,0.6); }
    .muted { color: var(--muted); }
    .card { background: var(--card); border-radius: 10px; padding: 12px; }
    .small { font-size: 0.9rem; color: var(--muted); }
    .pill { display:inline-block;padding:6px 10px;background:#062634;border-radius:999px;color:#9ff3ff;font-weight:600;font-size:0.9rem; }
    .report-row { display:flex; gap:8px; align-items:center; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.03); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header / Hero ----------
with st.container():
    c1, c2 = st.columns([1.2, 3])
    with c1:
        st.markdown("<h2 style='margin:0'>🆘 ReliefMate AI</h2>", unsafe_allow_html=True)
        st.markdown("<div class='small'>AI-powered Disaster Relief Assistant</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='hero'><strong style='font-size:1.05rem'>Verified relief info — shelters, medical aid & helplines</strong><div class='muted' style='margin-top:6px'>Fast, simple and multi-lingual assistance for people and volunteers during crises.</div></div>", unsafe_allow_html=True)

st.markdown("")  # spacer

# ---------- Layout: columns ----------
left, right = st.columns([2.2, 1])

# ---------- Left: Chat + History ----------
with left:
    st.markdown("## 💬 Chat Assistant")
    st.markdown("<div class='card'>Ask ReliefMate for shelters, helplines or submit a short report.</div>", unsafe_allow_html=True)

    # Session state to keep conversation
    if "rm_messages" not in st.session_state:
        st.session_state.rm_messages = [
            {"role": "system", "content": "You are ReliefMate AI. Provide short, factual, verifiable, and actionable responses for disaster relief. Ask for location and urgency when needed."}
        ]
    if "reports" not in st.session_state:
        st.session_state.reports = []

    # Show chat history (user vs assistant)
    for msg in st.session_state.rm_messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        elif msg["role"] == "assistant":
            st.chat_message("assistant").write(msg["content"])

    # Chat input (Streamlit chat UI)
    user_prompt = st.chat_input("Ask about shelters, medical help, or type 'report' to submit an incident.")
    if user_prompt:
        st.session_state.rm_messages.append({"role": "user", "content": user_prompt})
        st.chat_message("user").write(user_prompt)

        # Quick local commands: 'report' opens report form message
        if user_prompt.strip().lower().startswith("report"):
            st.chat_message("assistant").write("You can use the 'Report an incident' form on the right to submit details quickly.")
        else:
            if not OPENAI_KEY:
                st.chat_message("assistant").write("Chatbot is offline — OpenAI key not configured. Use Resources or Report form for help.")
            else:
                # Call OpenAI (chat completion)
                with st.spinner("ReliefMate checking verified sources..."):
                    try:
                        completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=st.session_state.rm_messages,
                            temperature=0.15,
                            max_tokens=300,
                        )
                        assistant_text = completion.choices[0].message.content.strip()
                    except Exception as e:
                        assistant_text = "Sorry — AI service failed. Please try again later."
                        st.error(f"OpenAI error: {e}")
                st.session_state.rm_messages.append({"role": "assistant", "content": assistant_text})
                st.chat_message("assistant").write(assistant_text)

    st.markdown("---")
    # Show recent reports (demo)
    st.markdown("### 📌 Recent Reports (demo)")
    if st.session_state.reports:
        for r in reversed(st.session_state.reports[-6:]):
            st.markdown(f"<div class='report-row'><div><strong>{r['type']}</strong> • <span class='small'>{r['location']}</span><div class='small'>{r['details'][:90]}</div></div><div class='small'>{r['time'][:19]}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='small'>No reports yet — submit one from the right column.</div>", unsafe_allow_html=True)

# ---------- Right: Quick actions, Resources, Report form ----------
with right:
    st.markdown("## ⚡ Quick Actions")
    if st.button("Example: Nearest shelter (Rajkot)"):
        st.experimental_set_query_params(action="example_find_shelter")
        st.info("Try: 'Nearest shelter in Rajkot' in the chat input.")

    st.markdown("## 📍 Verified Resources")
    st.markdown("<div class='card'><div class='small'>Official Helplines</div><ul><li>National Emergency: 112</li><li>Medical Helpline: 108</li></ul></div>", unsafe_allow_html=True)
    st.markdown("## 📝 Report an incident")
    with st.form("report_form", clear_on_submit=True):
        r_type = st.selectbox("Type", ("Medical", "Shelter", "Food", "Rescue", "Other"))
        r_loc = st.text_input("Location (village/ward/area)")
        r_details = st.text_area("Details (brief)", max_chars=500)
        r_contact = st.text_input("Contact number (optional)")
        submitted = st.form_submit_button("Submit report")
        if submitted:
            entry = {
                "type": r_type,
                "location": r_loc or "Unspecified",
                "details": r_details or "",
                "contact": r_contact or "",
                "time": datetime.utcnow().isoformat(),
            }
            st.session_state.reports.append(entry)
            st.success("Report submitted! Volunteers/NGOs (demo) can see it in Recent Reports.")
            # auto-add to chat history for traceability
            st.session_state.rm_messages.append({"role": "assistant", "content": f"New report saved: {r_type} at {entry['location']}. Thank you."})

    st.markdown("## ⚙️ Admin (Demo)")
    st.markdown("<div class='small'>Open reports: <strong>" + str(len(st.session_state.reports)) + "</strong></div>", unsafe_allow_html=True)
    if st.checkbox("Show raw reports (debug)"):
        st.json(st.session_state.reports)

st.markdown("---")
st.caption("Tip: For real deployments connect reports to a DB (Firebase/Firestore/Firestore), and set up verification flows and NGO dashboard. OpenAI usage costs money; keep replies short (low tokens).")
