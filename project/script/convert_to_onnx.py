from pathlib import Path

import joblib
from onnxmltools.convert import convert_xgboost
from onnxmltools.convert.common.data_types import FloatTensorType


class ConvertToOnnx:
    def __init__(
        self, BASE_PATH: Path = Path(__file__).resolve().parent.parent
    ) -> None:
        self.risk_pkl_model_path = BASE_PATH / "model/risk_model.pkl"
        self.risk_onnx_model_path = BASE_PATH / "model/risk_model.onnx"

    def main(self) -> None:
        data = joblib.load(self.risk_pkl_model_path)
        model, features = data["model"], data["features"]

        # convert to booster
        booster = model.get_booster()
        booster.feature_names = list(features)

        assert booster.feature_names == list(features)

        # convert to onnx
        onnx_model = convert_xgboost(
            booster,
            initial_types=[
                ("input", FloatTensorType([None, len(features)]))
            ],  # define input
            target_opset=15,
        )

        with open(self.risk_onnx_model_path, "wb") as f:
            f.write(onnx_model.SerializeToString())


if __name__ == "__main__":
    ConvertToOnnx()
