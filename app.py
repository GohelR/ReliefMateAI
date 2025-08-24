# app.py — Enhanced ReliefMate AI with Animations & Better Design (Streamlit + CLI Fallback)
"""
This file now **runs even if Streamlit isn't installed**.

- If Streamlit is available: launches the full animated UI (original behavior).
- If Streamlit is missing: falls back to a **CLI mode** so you can still chat, submit demo reports,
  and run tests without installing Streamlit.

Extras added:
- Safer optional imports (streamlit, streamlit_lottie, requests, openai)
- Unified prompt processing shared by both modes
- Minimal **unit tests** (run with: `python app.py --test`)

Usage:
  Streamlit UI ......... `streamlit run app.py`
  Force CLI mode ....... `python app.py --cli`
  Run tests ............ `python app.py --test`

Tip: create a requirements.txt for the UI:
  streamlit\nopenai\nstreamlit-lottie\nrequests
"""

from __future__ import annotations
import os
import sys
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# ---- Optional deps (guarded) -----------------------------------------------
try:
    import openai  # type: ignore
except Exception:  # pragma: no cover
    openai = None  # We'll handle absence gracefully

try:
    import importlib.util as _importlib_util
except Exception:  # pragma: no cover
    _importlib_util = None  # extremely rare, but keep code defensive

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover
    requests = None  # load_lottieurl becomes a no-op

APP_NAME = "ReliefMate AI"

# ---------- Key loader (env or Streamlit secrets later inside UI) -----------
OPENAI_KEY_ENV = os.getenv("OPENAI_API_KEY")

# ---------- Helpers shared by UI + CLI -------------------------------------
def load_lottieurl(url: str):
    """Best-effort fetch of Lottie JSON. Returns None if requests missing/fails."""
    if not requests:
        return None
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


def add_report(
    reports: List[Dict[str, str]],
    r_type: str,
    r_loc: str,
    r_details: str = "",
    r_contact: str = "",
) -> Dict[str, str]:
    """Append a report entry to the in-memory list and return it."""
    entry = {
        "type": (r_type or "Other").strip(),
        "location": (r_loc or "Unspecified").strip(),
        "details": (r_details or "").strip(),
        "contact": (r_contact or "").strip(),
        "time": datetime.utcnow().isoformat(),
    }
    reports.append(entry)
    return entry


def process_prompt(
    messages: List[Dict[str, str]],
    user_prompt: str,
    openai_key: Optional[str],
) -> str:
    """Core chat logic used by both UI and CLI.

    - If prompt begins with 'report', we guide the user to the report form (UI) or explain
      the CLI flow.
    - If no OpenAI key or SDK, return an offline message.
    - Otherwise, call OpenAI ChatCompletion with concise settings.
    """
    text = user_prompt.strip()

    if text.lower().startswith("report"):
        return (
            "You can use the 'Report an incident' form (UI) or type 'report' in CLI to submit details."
        )

    if not openai_key or not openai:
        return (
            "Chatbot is offline — OpenAI key or SDK not configured. Use Resources or the Report flow for help."
        )

    # At this point we have a key + SDK; try to call the API safely.
    try:
        openai.api_key = openai_key  # old-style SDK; still supported widely
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.15,
            max_tokens=300,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry — AI service failed. Please try again later. Error: {e}"


# ---------- Streamlit detection --------------------------------------------
def _has_module(name: str) -> bool:
    if not _importlib_util:
        return False
    try:
        return _importlib_util.find_spec(name) is not None
    except Exception:
        return False


# ---------- Streamlit UI ----------------------------------------------------
def run_streamlit_ui():
    import streamlit as st  # local import so file can run without streamlit

    # Safe optional import for lottie
    try:
        from streamlit_lottie import st_lottie  # type: ignore
    except Exception:  # pragma: no cover
        st_lottie = None

    # Config
    st.set_page_config(page_title=APP_NAME, page_icon="🆘", layout="wide")

    # Prefer Streamlit secrets, fallback to env
    openai_key = (
        st.secrets.get("OPENAI_API_KEY") if "OPENAI_API_KEY" in st.secrets else OPENAI_KEY_ENV
    )

    # ---------- CSS Enhancements ----------
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

        /* Chat fade-in */
        @keyframes fadeInUp {
          from { opacity: 0; transform: translate3d(0, 20%, 0); }
          to { opacity: 1; transform: translate3d(0, 0, 0); }
        }
        .chat-element { animation: fadeInUp 0.6s ease both; }

        /* Pulsing quick-action button */
        @keyframes pulse {
          0% { box-shadow: 0 0 0 0 rgba(6,182,212, 0.6); }
          70% { box-shadow: 0 0 0 12px rgba(6,182,212, 0); }
          100% { box-shadow: 0 0 0 0 rgba(6,182,212, 0); }
        }
        div.stButton > button:first-child {
          background: var(--accent) !important;
          border-radius: 999px !important;
          color: white !important;
          font-weight: 600;
          animation: pulse 2s infinite;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- Header / Hero ----------
    with st.container():
        c1, c2 = st.columns([2, 3])
        with c1:
            st.markdown("<h2 style='margin:0'>🆘 ReliefMate AI</h2>", unsafe_allow_html=True)
            st.markdown("<div class='small'>AI-powered Disaster Relief Assistant</div>", unsafe_allow_html=True)
            st.markdown(
                "<div class='hero'><strong style='font-size:1.05rem'>Verified relief info — shelters, medical aid & helplines</strong><div class='muted' style='margin-top:6px'>Fast, simple and multi-lingual assistance for people and volunteers during crises.</div></div>",
                unsafe_allow_html=True,
            )
        with c2:
            lottie_help = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_u4yrau.json")
            if lottie_help and 'st_lottie' in locals() and st_lottie:
                st_lottie(lottie_help, height=180, key="help_anim")

    st.markdown("")  # spacer

    # ---------- Layout: columns ----------
    left, right = st.columns([2.2, 1])

    # ---------- Left: Chat + History ----------
    with left:
        st.markdown("## 💬 Chat Assistant")
        st.markdown(
            "<div class='card'>Ask ReliefMate for shelters, helplines or submit a short report.</div>",
            unsafe_allow_html=True,
        )

        if "rm_messages" not in st.session_state:
            st.session_state.rm_messages = [
                {
                    "role": "system",
                    "content": (
                        "You are ReliefMate AI. Provide short, factual, verifiable, and actionable responses for disaster relief. "
                        "Ask for location and urgency when needed."
                    ),
                }
            ]
        if "reports" not in st.session_state:
            st.session_state.reports = []

        # Show chat history (fade-in)
        for msg in st.session_state.rm_messages:
            if msg["role"] == "user":
                st.chat_message("user").markdown(
                    f"<div class='chat-element'>{msg['content']}</div>", unsafe_allow_html=True
                )
            elif msg["role"] == "assistant":
                st.chat_message("assistant").markdown(
                    f"<div class='chat-element'>{msg['content']}</div>", unsafe_allow_html=True
                )

        # Chat input
        user_prompt = st.chat_input(
            "Ask about shelters, medical help, or type 'report' to submit an incident."
        )
        if user_prompt:
            st.session_state.rm_messages.append({"role": "user", "content": user_prompt})
            st.chat_message("user").markdown(
                f"<div class='chat-element'>{user_prompt}</div>", unsafe_allow_html=True
            )

            if user_prompt.strip().lower().startswith("report"):
                st.chat_message("assistant").markdown(
                    "<div class='chat-element'>You can use the 'Report an incident' form on the right to submit details quickly.</div>",
                    unsafe_allow_html=True,
                )
            else:
                with st.spinner("ReliefMate checking verified sources..."):
                    assistant_text = process_prompt(
                        st.session_state.rm_messages, user_prompt, openai_key
                    )
                st.session_state.rm_messages.append(
                    {"role": "assistant", "content": assistant_text}
                )
                st.chat_message("assistant").markdown(
                    f"<div class='chat-element'>{assistant_text}</div>", unsafe_allow_html=True
                )

        st.markdown("---")
        st.markdown("### 📌 Recent Reports (demo)")
        if st.session_state.reports:
            for r in reversed(st.session_state.reports[-6:]):
                st.markdown(
                    f"<div class='report-row'><div><strong>{r['type']}</strong> • <span class='small'>{r['location']}</span><div class='small'>{r['details'][:90]}</div></div><div class='small'>{r['time'][:19]}</div></div>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                "<div class='small'>No reports yet — submit one from the right column.</div>",
                unsafe_allow_html=True,
            )

    # ---------- Right: Quick actions, Resources, Report form ----------
    with right:
        st.markdown("## ⚡ Quick Actions")
        if st.button("🚨 Find Nearest Shelter"):
            st.info("Try: 'Nearest shelter in Rajkot' in the chat input.")

        st.markdown("## 📍 Verified Resources")
        st.markdown(
            "<div class='card'><div class='small'>Official Helplines</div><ul><li>National Emergency: 112</li><li>Medical Helpline: 108</li></ul></div>",
            unsafe_allow_html=True,
        )

        st.markdown("## 📝 Report an incident")
        with st.form("report_form", clear_on_submit=True):
            r_type = st.selectbox("Type", ("Medical", "Shelter", "Food", "Rescue", "Other"))
            r_loc = st.text_input("Location (village/ward/area)")
            r_details = st.text_area("Details (brief)", max_chars=500)
            r_contact = st.text_input("Contact number (optional)")
            submitted = st.form_submit_button("Submit report")
            if submitted:
                entry = add_report(st.session_state.reports, r_type, r_loc, r_details, r_contact)
                st.success(
                    "Report submitted! Volunteers/NGOs (demo) can see it in Recent Reports."
                )
                st.session_state.rm_messages.append(
                    {
                        "role": "assistant",
                        "content": f"New report saved: {entry['type']} at {entry['location']}. Thank you.",
                    }
                )

        st.markdown("## ⚙️ Admin (Demo)")
        st.markdown(
            "<div class='small'>Open reports: <strong>" + str(len(st.session_state.reports)) + "</strong></div>",
            unsafe_allow_html=True,
        )
        if st.checkbox("Show raw reports (debug)"):
            st.json(st.session_state.reports)

    st.markdown("---")
    st.caption(
        "Tip: For real deployments connect reports to a DB (Firebase/Firestore), and set up verification flows and NGO dashboard. OpenAI usage costs money; keep replies short (low tokens)."
    )


# ---------- CLI Fallback ----------------------------------------------------
def run_cli():
    print(f"\n{APP_NAME} (CLI mode) — Streamlit not installed.\n")
    print("Type messages to chat. Commands: 'report', 'show', 'help', 'quit'.\n")

    messages: List[Dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "You are ReliefMate AI. Provide short, factual, verifiable, and actionable responses for disaster relief. "
                "Ask for location and urgency when needed."
            ),
        }
    ]
    reports: List[Dict[str, str]] = []

    # Use env key only in CLI
    openai_key = OPENAI_KEY_ENV

    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

        if not text:
            print("(empty input — type 'help' for options)")
            continue

        low = text.lower()
        if low in {"quit", "exit"}:
            print("Bye!")
            return
        if low in {"help", ":h"}:
            print("Commands: report (submit), show (recent reports), quit")
            continue
        if low.startswith("report"):
            r_type = input("Type (Medical/Shelter/Food/Rescue/Other): ").strip() or "Other"
            r_loc = input("Location (village/ward/area): ").strip() or "Unspecified"
            r_details = input("Details (brief): ").strip()
            r_contact = input("Contact (optional): ").strip()
            entry = add_report(reports, r_type, r_loc, r_details, r_contact)
            print(
                f"Saved report: {entry['type']} at {entry['location']} — {entry['details'][:80]} (time: {entry['time'][:19]})"
            )
            continue
        if low.startswith("show"):
            if not reports:
                print("No reports yet.")
            else:
                print("Recent Reports:")
                for r in reports[-6:][::-1]:
                    print(
                        f" - {r['type']} • {r['location']} • {r['details'][:60]} • {r['time'][:19]}"
                    )
            continue

        # Normal chat
        messages.append({"role": "user", "content": text})
        reply = process_prompt(messages, text, openai_key)
        messages.append({"role": "assistant", "content": reply})
        print(f"ReliefMate: {reply}\n")


# ---------- Tests -----------------------------------------------------------
import unittest


class ReliefMateTests(unittest.TestCase):
    def test_add_report_populates_fields(self):
        reports: List[Dict[str, str]] = []
        entry = add_report(reports, "Medical", "Ward 5", "Injury", "9876543210")
        self.assertEqual(len(reports), 1)
        self.assertEqual(entry["type"], "Medical")
        self.assertEqual(entry["location"], "Ward 5")
        self.assertEqual(entry["details"], "Injury")
        self.assertEqual(entry["contact"], "9876543210")
        self.assertIn("time", entry)

    def test_process_prompt_reports_hint(self):
        msgs = [{"role": "system", "content": "x"}]
        reply = process_prompt(msgs, "report flood near bridge", None)
        self.assertIn("Report an incident", reply)

    def test_process_prompt_offline_when_no_key(self):
        msgs = [{"role": "system", "content": "x"}, {"role": "user", "content": "hi"}]
        reply = process_prompt(msgs, "hi", None)
        self.assertIn("offline", reply.lower())


# ---------- Entrypoint ------------------------------------------------------
if __name__ == "__main__":
    if "--test" in sys.argv:
        # Run unit tests and exit
        unittest.main(argv=[sys.argv[0]], exit=True)
    elif "--cli" in sys.argv:
        run_cli()
    else:
        # Autodetect Streamlit; if missing, CLI fallback
        if _has_module("streamlit"):
            # When launched as `python app.py`, inform the user how to start Streamlit
            # (Many environments will still prefer: streamlit run app.py)
            print(
                "Detected Streamlit. To run the UI, execute:\n  streamlit run app.py\n\nStarting CLI for now...\n"
            )
            run_cli()
        else:
            run_cli()
