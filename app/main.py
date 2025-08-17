# app/main.py
from fastapi import FastAPI
from app.controllers.progress_controller import router as progress_router

app = FastAPI(title="Progress Service")
app.include_router(progress_router)

# Chạy: uvicorn app.main:app --reload
