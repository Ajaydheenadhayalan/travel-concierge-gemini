from fastapi import FastAPI
from .coordinator import router
app = FastAPI(title="Travel Concierge Agent (Gemini)")
app.include_router(router, prefix="/api")
@app.get("/")
def health(): return {"ok": True}
