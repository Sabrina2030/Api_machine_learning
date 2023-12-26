from fastapi import FastAPI
from routes import prediction_router

app = FastAPI()

app.include_router(prediction_router, prefix="/api/predictions")
