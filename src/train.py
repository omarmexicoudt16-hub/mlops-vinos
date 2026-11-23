"""Entrena 3 modelos, los registra en MLflow y guarda el mejor como 'champion'."""
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow import MlflowClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

FEATURES = ["alcohol", "flavanoids", "color_intensity", "proline"]
MODEL_NAME = "WineClassifier"
TRACKING_URI = "sqlite:///mlflow.db"


def main():
    df = pd.read_csv("data/wine.csv")
    X, y = df[FEATURES], df["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    candidates = {
        "LogisticRegression": (
            make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=1000)),
            {"C": 1.0, "max_iter": 1000},
        ),
        "RandomForest": (
            RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42),
            {"n_estimators": 100, "max_depth": 5},
        ),
        "SVM": (
            make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1.0, probability=True)),
            {"kernel": "rbf", "C": 1.0},
        ),
    }

    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment("Wine_Classification")

    best = {"f1": -1, "run_id": None, "name": None, "model": None}
    for name, (model, params) in candidates.items():
        with mlflow.start_run(run_name=name) as run:
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            acc = accuracy_score(y_test, pred)
            f1 = f1_score(y_test, pred, average="macro")
            mlflow.log_param("modelo", name)
            mlflow.log_params(params)
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("f1_macro", f1)
            mlflow.sklearn.log_model(model, name="model", serialization_format="cloudpickle")
            print(f"{name}: accuracy={acc:.3f} f1_macro={f1:.3f}")
            if f1 > best["f1"]:
                best = {"f1": f1, "run_id": run.info.run_id, "name": name, "model": model}

    # Registrar al mejor y asignarle el alias "champion"
    version = mlflow.register_model(f"runs:/{best['run_id']}/model", MODEL_NAME)
    MlflowClient().set_registered_model_alias(MODEL_NAME, "champion", version.version)
    print(f"Champion: {best['name']} (F1={best['f1']:.3f}), versión {version.version}")

    Path("models").mkdir(exist_ok=True)
    joblib.dump(best["model"], "models/champion.joblib")
    print("Modelo guardado en models/champion.joblib")


if __name__ == "__main__":
    main()
