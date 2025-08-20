# ReliefMate AI – Disaster Relief Assistant 🌍🚨

ReliefMate AI is an **AI-powered assistant** that helps citizens and responders during disasters with
verified updates, multilingual support, and prioritized request routing.

## ✨ Core Features
- Real-time Q&A chatbot for shelters, hospitals, helplines
- Summarization of long reports into short actionable updates
- Categorization of citizen requests (rescue/medical/food/shelter)
- Instant multilingual translation
- Admin dashboard (planned) for NGOs/Govt

## 🧠 OpenAI Usage
- **Summarization:** Convert long govt/NGO bulletins to concise alerts
- **Classification:** Tag incoming requests (rescue/medical/food/shelter)
- **Conversation:** Natural Q&A for disaster queries
- **Translation:** Break language barriers (planned)

## 🛠 Tech Stack
- **Frontend:** Streamlit (prototype)
- **Backend:** FastAPI (stubbed)
- **AI:** OpenAI API
- **Data:** CSV/JSON feeds (extensible)
- **Deploy:** Streamlit Cloud / Render / Railway

## 🚀 Quickstart
```bash
# 1) Create and activate venv (optional)
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Set API key
cp .env.example .env
# then edit .env and paste your OpenAI API key

# 4) Run Streamlit prototype
streamlit run app/streamlit_app.py

# 5) (Optional) Run FastAPI stub
uvicorn backend.api:app --reload --port 8000
```

## 📁 Structure
```
ReliefMateAI/
 ├─ app/
 │   └─ streamlit_app.py
 ├─ backend/
 │   └─ api.py
 ├─ docs/
 │   ├─ architecture-diagram.png
 │   └─ README_docs.md
 ├─ data/
 │   └─ sample_requests.csv
 ├─ scripts/
 │   └─ deploy_instructions.md
 ├─ .env.example
 ├─ .gitignore
 ├─ requirements.txt
 └─ README.md
```

## 📈 Roadmap
- v0.1: MVP chatbot + request classifier
- v0.2: Multilingual support + live feeds
- v0.3: Admin dashboard with maps & prioritization

---
Made with ❤️ for OpenAI x NxtWave Buildathon.
