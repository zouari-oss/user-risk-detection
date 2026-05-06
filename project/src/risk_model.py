"""
Module: risk_model.py

Main user risk model train/prediction class

Author: @ZouariOmar (zouariomar20@gmail.com)
Date: 2026-05-01
License: GPL-3.0
Version: 0.1
"""

from pathlib import Path
from typing import Optional, Self, Tuple

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    precision_recall_curve,
)
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


class RiskModel:
    def __init__(
        self: Self,
        model_path: Path = Path(__file__).resolve().parent / "model/risk_model.pkl",
    ) -> None:
        self.model_path = model_path
        self.target_label = "risk_label"
        self.feature_names = None
        self.threshold = 0.5

        self.model = XGBClassifier(
            n_estimators=400,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="mlogloss",
            objective="multi:softprob",
        )

    # ==========================
    # === Train & Prediction ===
    # ==========================

    def train(
        self: Self,
        data_path: str,
        plot_feature_importance_path: Optional[Path] = None,
        plot_decision_tree_path: Optional[Path] = None,
    ) -> Self:

        df = pd.read_csv(data_path)

        X = df.drop(self.target_label, axis=1)
        y = df[self.target_label]

        self.feature_names = list(X.columns)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        self.model.fit(X_train, y_train)

        # ==========================
        # MULTICLASS EVALUATION
        # ==========================
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)

        # TRAIN ACCURACY
        y_train_pred = self.model.predict(X_train)
        train_acc = accuracy_score(y_train, y_train_pred)

        print("""
        =============================
        === CLASSIFICATION REPORT ===
        =============================""")
        print(classification_report(y_test, y_pred))

        print(f"[INFO] Training Accuracy: {train_acc:.4f}")
        print(f"[INFO] Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")

        # ==========================
        # FRAUD ANALYSIS (CLASS 2)
        # ==========================
        fraud_proba = y_proba[:, 2]

        y_test_fraud = np.array(y_test == 2, dtype=np.int32)

        precision, recall, thresholds = precision_recall_curve(
            y_test_fraud, fraud_proba
        )

        # FIX: Avoid edge mismatch safely
        f1 = (2 * precision * recall) / (precision + recall + 1e-9)

        if len(thresholds) > 0:
            best_idx = np.argmax(f1[:-1])
            self.threshold = thresholds[best_idx]
            print(f"[INFO] Fraud threshold tuned to: {self.threshold:.4f}")

        print("[INFO] Multiclass model trained successfully")
        # ==========================
        # PLOTS
        # ==========================
        if plot_feature_importance_path is not None:
            self._save_plot_feature_importance(plot_feature_importance_path)

        if plot_decision_tree_path is not None:
            self._save__plot_xgboost_decision_tree(plot_decision_tree_path)

        return self

    def predict(self: Self, input_dict: dict) -> Tuple[int, float]:
        X = pd.DataFrame([input_dict])[self.feature_names]
        proba = self.model.predict_proba(X)[0]  # [p0, p1, p2]
        pred = int(proba.argmax())
        confidence = float(proba[pred])

        return pred, confidence

    # ===========================
    # === !Train & Prediction ===
    # ===========================

    # ==============
    # === Plots ===
    # ==============

    def _save_plot_feature_importance(
        self: Self, plot_feature_importance: Path
    ) -> None:
        ax = plt.subplots(figsize=(12, 8))[1]
        xgb.plot_importance(self.model, ax=ax)

        ax.set_title("Feature Importance")
        plt.tight_layout()
        plt.savefig(
            Path("../../res/img/model/") / plot_feature_importance,
            dpi=200,
            bbox_inches="tight",
        )
        plt.close()

    def _save__plot_xgboost_decision_tree(self: Self, plot_decision_tree: Path) -> None:
        ax = plt.subplots(figsize=(24, 12))[1]
        xgb.plot_tree(self.model, tree_idx=0, ax=ax)

        ax.set_title("Decision Tree")
        plt.tight_layout()
        plt.savefig(
            Path("../../res/img/model/") / plot_decision_tree,
            dpi=200,
            bbox_inches="tight",
        )
        plt.close()

    # ==============
    # === !Plots ===
    # ==============

    def save(self: Self) -> None:
        joblib.dump(
            {"model": self.model, "features": self.feature_names}, self.model_path
        )

    def load(self: Self) -> Self:
        data = joblib.load(self.model_path)
        self.model = data["model"]
        self.feature_names = data["features"]
        return self
