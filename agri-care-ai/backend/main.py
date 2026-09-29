from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import Base, engine
from models.models import Crop, GrowthStage, PestDisease, Treatment, Source, ProductPrice
from routes.crops import router as crops_router
from routes.advice import router as advice_router
from routes.chat import router as chat_router
app = FastAPI(title="AI Crop Care Advisor API")

Base.metadata.create_all(bind=engine)
app.include_router(crops_router)
app.include_router(advice_router)
app.include_router(chat_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Backend is alive"}