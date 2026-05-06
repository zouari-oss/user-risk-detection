from pathlib import Path

from data_visualize import DataVisualizer
from risk_model import RiskModel


class Train:
    def __init__(
        self, BASE_PATH: Path = Path(__file__).resolve().parent.parent
    ) -> None:
        self.session_risk_dataset_path = str(
            BASE_PATH / "dataset/session_risk_dataset.csv"
        )
        self.data_visualize_out = str(BASE_PATH / "../res/img")

    def main(self):
        DataVisualizer(
            self.session_risk_dataset_path,
            output_dir=self.data_visualize_out,
            show=False,
        ).run_all()

        RiskModel().train(
            self.session_risk_dataset_path,
            Path("plot_feature_importance.png"),
            Path("plot_decision_tree.png"),
        ).save()


if __name__ == "__main__":
    Train()
