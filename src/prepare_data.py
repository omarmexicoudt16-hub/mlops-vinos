"""Genera data/wine.csv, data/reference.csv y data/current.csv."""
from pathlib import Path

from sklearn.datasets import load_wine

FEATURES = ["alcohol", "flavanoids", "color_intensity", "proline"]


def main():
    Path("data").mkdir(exist_ok=True)
    df = load_wine(as_frame=True).frame[FEATURES + ["target"]]
    df.to_csv("data/wine.csv", index=False)

    # Datos para monitoreo: referencia (original) y actuales (con cambios)
    reference = df[FEATURES].sample(frac=0.5, random_state=1)
    current = df[FEATURES].sample(frac=0.5, random_state=2).copy()
    current["alcohol"] = current["alcohol"] + 1.5          # drift simulado
    current["proline"] = current["proline"] * 1.4           # drift simulado
    reference.to_csv("data/reference.csv", index=False)
    current.to_csv("data/current.csv", index=False)
    print("Datos generados en data/:", df.shape)


if __name__ == "__main__":
    main()
