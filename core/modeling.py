# -*- coding: utf-8 -*-
"""
core/modeling.py
Pipeline formulation, multi-model cross-validation arena, and model explainability.
Complies with section 5: imblearn/sklearn pipelines, stratified CV, zero leakage.
"""
from __future__ import annotations
import time
import numpy as np
import pandas as pd
from typing import Any

from sklearn.base import BaseEstimator
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.metrics import (
    f1_score,
    balanced_accuracy_score,
    recall_score,
    roc_auc_score,
    matthews_corrcoef,
    confusion_matrix,
    roc_curve,
    precision_recall_curve,
    classification_report,
)
from sklearn.inspection import permutation_importance

try:
    from imblearn.pipeline import Pipeline as ImbPipeline
    from imblearn.over_sampling import SMOTE
    HAS_IMBLEARN = True
except ImportError:
    from sklearn.pipeline import Pipeline as ImbPipeline
    HAS_IMBLEARN = False
    SMOTE = None

from core.config import RANDOM_SEED


def get_model_catalog(use_class_weight: bool = True) -> dict[str, BaseEstimator]:
    """Returns the catalog of candidate classification algorithms."""
    cw = "balanced" if use_class_weight else None
    return {
        "Majority Baseline": DummyClassifier(strategy="most_frequent"),
        "Logistic Regression": LogisticRegression(
            C=1.0, penalty="l2", class_weight=cw, solver="lbfgs", random_state=RANDOM_SEED, max_iter=500
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=4, min_samples_leaf=3, class_weight=cw, random_state=RANDOM_SEED
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, max_depth=5, min_samples_leaf=2, class_weight=cw, random_state=RANDOM_SEED, n_jobs=-1
        ),
        "Support Vector Machine (RBF)": SVC(
            kernel="rbf", C=1.5, probability=True, class_weight=cw, random_state=RANDOM_SEED
        ),
        "K-Nearest Neighbors (KNN)": KNeighborsClassifier(
            n_neighbors=5, weights="distance"
        ),
        "Gaussian Naive Bayes": GaussianNB(),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=75, learning_rate=0.08, max_depth=3, random_state=RANDOM_SEED
        ),
    }


def build_pipeline(
    model: BaseEstimator, imbalance_method: str = "class_weight"
) -> ImbPipeline:
    """
    Constructs an imblearn/sklearn Pipeline preventing any test-fold data leakage.
    Scales features with StandardScaler and applies SMOTE (if selected and available).
    """
    steps = [("scaler", StandardScaler())]

    if imbalance_method == "smote" and HAS_IMBLEARN and SMOTE is not None:
        # Resampling is executed strictly inside training folds only
        steps.append(("resampler", SMOTE(random_state=RANDOM_SEED, k_neighbors=3)))

    steps.append(("classifier", model))
    return ImbPipeline(steps)


def evaluate_model_cv(
    pipeline: ImbPipeline,
    X: pd.DataFrame,
    y: pd.Series,
    n_splits: int = 5,
) -> dict[str, Any]:
    """
    Runs Stratified K-Fold Cross Validation and computes robust metrics:
    F1-Macro, Balanced Accuracy, Recall (At-Risk), ROC-AUC, and MCC.
    """
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_SEED)

    scoring = {
        "f1_macro": "f1_macro",
        "balanced_accuracy": "balanced_accuracy",
        "recall_at_risk": "recall",
        "roc_auc": "roc_auc",
    }

    t0 = time.time()
    cv_res = cross_validate(
        pipeline,
        X,
        y,
        cv=cv,
        scoring=scoring,
        return_train_score=False,
        n_jobs=-1,
    )
    elapsed = time.time() - t0

    # Custom computation for MCC across folds
    mcc_scores = []
    for train_idx, val_idx in cv.split(X, y):
        X_tr, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_tr, y_val = y.iloc[train_idx], y.iloc[val_idx]
        fitted_pipe = pipeline.fit(X_tr, y_tr)
        preds = fitted_pipe.predict(X_val)
        mcc_scores.append(matthews_corrcoef(y_val, preds))

    return {
        "f1_macro_mean": np.mean(cv_res["test_f1_macro"]),
        "f1_macro_std": np.std(cv_res["test_f1_macro"]),
        "bal_acc_mean": np.mean(cv_res["test_balanced_accuracy"]),
        "bal_acc_std": np.std(cv_res["test_balanced_accuracy"]),
        "recall_mean": np.mean(cv_res["test_recall_at_risk"]),
        "recall_std": np.std(cv_res["test_recall_at_risk"]),
        "roc_auc_mean": np.mean(cv_res["test_roc_auc"]),
        "roc_auc_std": np.std(cv_res["test_roc_auc"]),
        "mcc_mean": np.mean(mcc_scores),
        "mcc_std": np.std(mcc_scores),
        "fit_time_sec": round(elapsed, 2),
    }


def train_benchmark_arena(
    X: pd.DataFrame,
    y: pd.Series,
    imbalance_method: str = "class_weight",
    n_splits: int = 5,
) -> pd.DataFrame:
    """
    Trains all candidate algorithms and returns a sortable leaderboard DataFrame.
    """
    models = get_model_catalog(use_class_weight=(imbalance_method == "class_weight"))
    records = []

    for name, model in models.items():
        pipe = build_pipeline(model, imbalance_method=imbalance_method)
        eval_dict = evaluate_model_cv(pipe, X, y, n_splits=n_splits)

        records.append({
            "Algoritma Model": name,
            "F1-Macro (Mean ± Std)": f"{eval_dict['f1_macro_mean']:.3f} ± {eval_dict['f1_macro_std']:.3f}",
            "Balanced Acc": round(eval_dict['bal_acc_mean'], 3),
            "Recall At-Risk": round(eval_dict['recall_mean'], 3),
            "ROC-AUC": round(eval_dict['roc_auc_mean'], 3),
            "MCC": round(eval_dict['mcc_mean'], 3),
            "Waktu Fit (s)": eval_dict["fit_time_sec"],
            "_raw_f1": eval_dict["f1_macro_mean"],
            "_raw_roc_auc": eval_dict["roc_auc_mean"],
            "_raw_recall": eval_dict["recall_mean"],
        })

    leaderboard = pd.DataFrame(records)
    leaderboard = leaderboard.sort_values(by="_raw_f1", ascending=False).reset_index(drop=True)
    return leaderboard


def get_trained_evaluation_artifacts(
    model_name: str,
    X: pd.DataFrame,
    y: pd.Series,
    imbalance_method: str = "class_weight",
    test_size: float = 0.25,
) -> dict[str, Any]:
    """
    Fits selected model on train/test split to compute granular diagnostic artifacts:
    Confusion Matrix, ROC Curve, PR Curve, Classification Report, and Permutation Importance.
    """
    models = get_model_catalog(use_class_weight=(imbalance_method == "class_weight"))
    raw_model = models.get(model_name, models["Random Forest"])
    pipeline = build_pipeline(raw_model, imbalance_method=imbalance_method)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=RANDOM_SEED
    )

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    # Probabilities for curves
    if hasattr(pipeline, "predict_proba"):
        y_prob = pipeline.predict_proba(X_test)[:, 1]
    elif hasattr(pipeline, "decision_function"):
        y_prob = pipeline.decision_function(X_test)
    else:
        y_prob = y_pred

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    cm_norm = confusion_matrix(y_test, y_pred, normalize="true")

    # ROC & PR curves
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    precision_curve, recall_curve, _ = precision_recall_curve(y_test, y_prob)
    roc_score = roc_auc_score(y_test, y_prob)

    # Classification report dict
    report = classification_report(
        y_test, y_pred, target_names=["Good Standing", "At-Risk"], output_dict=True
    )

    # Permutation importance
    perm = permutation_importance(
        pipeline, X_test, y_test, n_repeats=10, random_state=RANDOM_SEED, scoring="f1_macro"
    )
    importance_df = pd.DataFrame({
        "Fitur": X.columns,
        "Importance (Mean)": np.round(perm.importances_mean, 4),
        "Importance (Std)": np.round(perm.importances_std, 4),
    }).sort_values(by="Importance (Mean)", ascending=False).reset_index(drop=True)

    return {
        "pipeline": pipeline,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "y_pred": y_pred,
        "y_prob": y_prob,
        "cm": cm,
        "cm_norm": cm_norm,
        "fpr": fpr,
        "tpr": tpr,
        "roc_auc": roc_score,
        "precision_curve": precision_curve,
        "recall_curve": recall_curve,
        "report": report,
        "importance_df": importance_df,
    }
