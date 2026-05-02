import numpy as np
import pandas as pd

from model.risk_model import RiskModel


class PredictorService:
    def __init__(self) -> None:
        self.model: RiskModel = RiskModel().load()

    def predict(self, input_dict: dict) -> tuple[int, float, np.ndarray]:
        X = pd.DataFrame([input_dict])[self.model.feature_names]

        proba = self.model.model.predict_proba(X)[0]  # [p0, p1, p2]
        pred = int(proba.argmax())
        confidence = float(proba[pred])

        return pred, confidence, proba
