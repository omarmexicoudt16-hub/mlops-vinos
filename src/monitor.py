"""Compara datos de referencia vs actuales con Evidently y genera un reporte HTML."""
from pathlib import Path

import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

reference = pd.read_csv("data/reference.csv")
current = pd.read_csv("data/current.csv")

report = Report([DataDriftPreset()])
result = report.run(reference_data=reference, current_data=current)

Path("reports").mkdir(exist_ok=True)
result.save_html("reports/data_drift.html")
print("Reporte guardado en reports/data_drift.html")
