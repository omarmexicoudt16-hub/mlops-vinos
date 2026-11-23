from typing import Literal

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
import joblib
import pandas as pd
from pydantic import BaseModel, Field

BASE = Path(__file__).resolve().parent.parent
model = joblib.load(BASE / "models" / "champion.joblib")

app = FastAPI(title="Wine Classifier API")

NAMES = {0: "Cultivar 0", 1: "Cultivar 1", 2: "Cultivar 2"}


class WineInput(BaseModel):
    alcohol: float = Field(ge=10, le=16)
    flavanoids: float = Field(ge=0, le=6)
    color_intensity: float = Field(ge=1, le=14)
    proline: float = Field(ge=200, le=1800)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(wine: WineInput):
    data = pd.DataFrame([wine.model_dump()])
    pred = int(model.predict(data)[0])
    proba = float(model.predict_proba(data)[0].max())
    return {"prediction": pred, "cultivar": NAMES[pred], "confidence": round(proba, 3)}


@app.get("/", response_class=HTMLResponse)
def index():
    return (BASE / "templates" / "index.html").read_text(encoding="utf-8")
