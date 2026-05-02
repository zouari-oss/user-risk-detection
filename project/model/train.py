from pathlib import Path
from data_visualize import DataVisualizer
from risk_model import RiskModel


def main():
    DataVisualizer(
        "../dataset/session_risk_dataset.csv",
        output_dir="../../res/img",
        show=False,
    ).run_all()

    RiskModel().train(
        "../dataset/session_risk_dataset.csv",
        Path("plot_feature_importance.png"),
        Path("plot_decision_tree.png"),
    ).save()


if __name__ == "__main__":
    main()
