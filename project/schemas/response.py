from pydantic import BaseModel


class PredictionResponse(BaseModel):
    risk_label: int
    confidence: float
    probabilities: list[float]
