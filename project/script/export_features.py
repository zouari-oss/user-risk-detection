import json
from pathlib import Path

import joblib


class Export_Features:
    def __init__(
        self, BASE_PATH: Path = Path(__file__).resolve().parent.parent
    ) -> None:
        self.features_json_out = BASE_PATH / "meta/features.json"
        self.risk_pkl_model_path = BASE_PATH / "model/risk_model.pkl"

    def main(self) -> None:
        # load your trained model bundle
        data = joblib.load(self.risk_pkl_model_path)

        features = data["features"]

        # save as JSON
        with open(self.features_json_out, "w") as f:
            json.dump(features, f, indent=2)

        print(f"`{self.features_json_out}` saved")


if __name__ == "__main__":
    Export_Features()
