import os
from typing import Self
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class DataVisualizer:
    def __init__(
        self,
        data_path: str,
        output_dir: str = "plots",
        show: bool = False,
    ) -> None:
        self.data_path = data_path
        self.df: pd.DataFrame = pd.read_csv(data_path)
        self.output_dir = output_dir
        self.show = show

        # Directories
        self.dataset_dir = os.path.join(self.output_dir, "dataset")
        self.feature_dir = os.path.join(self.output_dir, "feature_vs_target")

        os.makedirs(self.dataset_dir, exist_ok=True)
        os.makedirs(self.feature_dir, exist_ok=True)

        sns.set_theme(style="whitegrid")

    # ==========================
    # INTERNAL SAVE METHOD
    # ==========================
    def _save(self, relative_path: str) -> str:
        full_path = os.path.join(self.output_dir, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        plt.savefig(full_path, dpi=300, bbox_inches="tight")

        if self.show:
            plt.show()

        plt.close("all")
        return full_path

    # ==========================
    # CLASS DISTRIBUTION
    # ==========================
    def plot_class_distribution(self) -> str:
        plt.figure(figsize=(6, 4))
        sns.countplot(x="risk_label", data=self.df)
        plt.title("Class Distribution")
        return self._save("dataset/class_distribution.png")

    # ==========================
    # FEATURE DISTRIBUTIONS
    # ==========================
    def plot_feature_distributions(self) -> str:
        self.df.hist(figsize=(12, 10), bins=30)
        plt.suptitle("Feature Distributions")
        return self._save("dataset/feature_distributions.png")

    # ==========================
    # CORRELATION MATRIX
    # ==========================
    def plot_correlation(self) -> str:
        plt.figure(figsize=(10, 6))
        corr = self.df.corr(numeric_only=True)
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Matrix")
        return self._save("dataset/correlation_matrix.png")

    # ==========================
    # FEATURE VS TARGET
    # ==========================
    def plot_feature_vs_target(self) -> list[str]:
        paths = []
        features = self.df.columns.drop("risk_label")

        for col in features:
            plt.figure(figsize=(6, 4))
            sns.boxplot(x="risk_label", y=col, data=self.df)
            plt.title(f"{col} vs Risk")
            paths.append(self._save(f"feature_vs_target/{col}_vs_risk.png"))

        return paths

    # ==========================
    # RUN ALL
    # ==========================
    def run_all(self: Self) -> dict:
        return {
            "class_distribution": self.plot_class_distribution(),
            "feature_distributions": self.plot_feature_distributions(),
            "correlation": self.plot_correlation(),
            "feature_vs_target": self.plot_feature_vs_target(),
        }
