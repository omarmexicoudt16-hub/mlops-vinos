"""DAG de Airflow: validar datos -> entrenar -> verificar modelo."""
from datetime import datetime
from pathlib import Path
import subprocess

from airflow import DAG

try:  # Airflow 3
    from airflow.providers.standard.operators.python import PythonOperator
except ImportError:  # Airflow 2
    from airflow.operators.python import PythonOperator

PROJECT = "/opt/airflow/project"


def validar_datos():
    if not Path(f"{PROJECT}/data/wine.csv").exists():
        raise FileNotFoundError("Falta data/wine.csv")
    print("Dataset encontrado")


def entrenar_modelos():
    subprocess.run(["python", "src/train.py"], cwd=PROJECT, check=True)


def verificar_modelo():
    if not Path(f"{PROJECT}/models/champion.joblib").exists():
        raise FileNotFoundError("No se generó el champion")
    print("Champion generado correctamente")


with DAG(
    dag_id="wine_training_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    t1 = PythonOperator(task_id="validar_datos", python_callable=validar_datos)
    t2 = PythonOperator(task_id="entrenar_modelos", python_callable=entrenar_modelos)
    t3 = PythonOperator(task_id="verificar_modelo", python_callable=verificar_modelo)
    t1 >> t2 >> t3
