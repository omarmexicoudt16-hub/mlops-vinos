# Proyecto MLOps — Clasificador de vinos 🍷

Clasifica vinos (3 cultivares) a partir de 4 variables químicas usando el dataset `load_wine` de scikit-learn.

Herramientas: Git/GitHub · DVC · MLflow · Airflow · FastAPI + HTML · Docker · GitHub Actions · Evidently (monitoreo).

## Estructura

```
mlops_vinos/
├── app/main.py                 API FastAPI (/predict, /health, /)
├── templates/index.html        Formulario web
├── src/prepare_data.py         Genera los datasets
├── src/train.py                Entrena 3 modelos + MLflow + champion
├── src/monitor.py              Reporte de drift con Evidently
├── tests/test_api.py           Pruebas pytest
├── airflow/                    docker-compose + DAG
├── .github/workflows/cicd.yml  CI/CD con GitHub Actions
├── Dockerfile
└── requirements.txt
```

## Ejecución rápida (Windows, terminal CMD de VS Code)

```
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python src/prepare_data.py
python src/train.py
python -m pytest -v
python -m uvicorn app.main:app --reload
```

Abre http://127.0.0.1:8000 (formulario) y http://127.0.0.1:8000/docs (documentación).

La guía completa paso a paso (con GitHub, DVC, Docker, Actions, Airflow y monitoreo) está en `GUIA_PASO_A_PASO.md`.
