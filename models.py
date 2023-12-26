from pydantic import BaseModel
from typing import List

class Prediction_Input(BaseModel):
    id: int
    text_input: List[float]

class Prediction_Output(BaseModel):
    id: int
    text_input: List[float]
    pred: float