# routes.py

from fastapi import APIRouter, Depends
from controllers.todo_controllers import PredictionController
from models import Prediction_Input, Prediction_Output
from typing import List


prediction_router = APIRouter()
prediction_controller = PredictionController()

@prediction_router.get("/predictions", response_model=List[Prediction_Output])
def get_predictions():
    return prediction_controller.get_predictions()

@prediction_router.get("/predictions/{prediction_id}", response_model=Prediction_Output)
def get_prediction(prediction_id: int):
    return prediction_controller.get_prediction(prediction_id)

@prediction_router.post("/predictions", response_model=Prediction_Output)
def create_prediction(input_data: Prediction_Input):
    return prediction_controller.create_prediction(input_data)

@prediction_router.delete("/predictions/{prediction_id}")
def delete_prediction(prediction_id: int):
    return prediction_controller.delete_prediction(prediction_id)
