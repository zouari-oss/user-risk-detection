from fastapi import APIRouter
from schemas.request import SessionRequest
from schemas.response import PredictionResponse
from services.predictor import PredictorService

router = APIRouter()
predictor = PredictorService()


@router.post("/predict", response_model=PredictionResponse)
def predict(data: SessionRequest) -> PredictionResponse:
    pred, confidence, probs = predictor.predict(data.model_dump())

    return PredictionResponse(
        risk_label=pred, confidence=confidence, probabilities=probs.tolist()
    )
