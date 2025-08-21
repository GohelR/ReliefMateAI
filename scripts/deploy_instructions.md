# Deployment (Prototype)

- Streamlit: `streamlit run app/streamlit_app.py`
- FastAPI (dev): `uvicorn backend.api:app --reload --port 8000`

For cloud:
- Streamlit Cloud for frontend
- Render/Railway for FastAPI backend
- Set `OPENAI_API_KEY` as environment variable
