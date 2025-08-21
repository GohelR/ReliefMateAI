
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ReliefMateAI API", version="0.1.0")

class Need(BaseModel):
    name: str | None = None
    location: str
    need: str
    details: str

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/needs")
def submit_need(need: Need):
    # TODO: push to DB / queue for NGO dashboard
    return {"received": need.dict()}
