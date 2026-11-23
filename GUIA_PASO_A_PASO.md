# Guía paso a paso (con tu proyecto de vinos)

Tiempo estimado: 2–3 horas la primera vez. Haz una **captura de pantalla** en cada paso marcado con 📸 (las necesitas para el PDF).

---

## PARTE 0 — Instalar lo necesario (una sola vez)

| Programa | Dónde descargarlo | Cómo |
|---|---|---|
| **Python 3.11 o 3.12** | https://www.python.org/downloads/ | Descarga el instalador de Windows. **Marca la casilla "Add Python to PATH"** antes de instalar. |
| **Git** | https://git-scm.com/download/win | Instalador → "Next" en todo. |
| **VS Code** | https://code.visualstudio.com | Instalador → "Next" en todo. |
| **Docker Desktop** | https://www.docker.com/products/docker-desktop | Instala, reinicia la PC y **ábrelo** (debe decir "Engine running"). |
| **Cuenta de GitHub** | https://github.com/signup | Crea tu cuenta gratis. |

Comprueba en una terminal (CMD): `python --version`, `git --version`, `docker --version`. Los tres deben mostrar una versión.

> Se recomienda Python 3.11 o 3.12.

Configura Git una vez (con tus datos):
```
git config --global user.name "Tu Nombre"
git config --global user.email "tu@correo.com"
```

---

## PARTE 1 — Preparar el proyecto

1. Descarga y **descomprime** `mlops_vinos.zip` (por ejemplo en Documentos).
2. Abre VS Code → **File → Open Folder** → elige la carpeta `mlops_vinos`.
3. Abre la terminal: **Terminal → New Terminal**. Si dice PowerShell, cambia a **Command Prompt** (flecha junto al "+").
4. Ejecuta:
```
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python src/prepare_data.py
```
(La instalación tarda unos minutos.)

---

## PARTE 2 — Git y GitHub 📸

1. En GitHub: **New repository** → nombre `wine-mlops` → **Public** → **no** marques README/.gitignore → *Create repository*.
2. En la terminal (cambia `TU_USUARIO`):
```
git init -b main
git add .
git commit -m "Proyecto inicial"
git remote add origin https://github.com/TU_USUARIO/wine-mlops.git
git push -u origin main
```
(Te pedirá iniciar sesión en el navegador.)
📸 Captura: el repositorio en GitHub con los archivos. Y `git log --oneline`.

Extra (rápido, para mostrar ramas): 
```
git switch -c feature/readme
```
Edita algo en README.md, luego:
```
git add . & git commit -m "Mejorar README" & git push -u origin feature/readme
```
En GitHub crea el **Pull Request** y haz **Merge**. 📸 Captura del PR. Luego: `git switch main` y `git pull`.

---

## PARTE 3 — DVC (versionar datos) 📸

```
dvc init
dvc add data/wine.csv
git add data/wine.csv.dvc data/.gitignore .dvc .dvcignore
git commit -m "Versionar dataset con DVC"
mkdir ..\dvc_storage
dvc remote add -d storage ..\dvc_storage
git add .dvc/config
git commit -m "Configurar remoto DVC"
dvc push
git push
```
📸 Captura: salida de `dvc add`, el archivo `data/wine.csv.dvc` abierto y la carpeta `dvc_storage`.

---

## PARTE 4 — MLflow (entrenar y comparar modelos) 📸

1. Entrena (ya hace todo: 3 modelos, métricas y alias `champion`):
```
python src/train.py
```
📸 Captura de la salida (accuracy y F1 de cada modelo).

2. Abre la interfaz **en otra terminal** (Terminal → New Terminal, activa el entorno otra vez con `.venv\Scripts\activate.bat`):
```
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
3. Abre http://127.0.0.1:5000 → experimento **Wine_Classification**.
📸 Captura 1: los 3 runs. 📸 Captura 2: selecciona los 3 y pulsa **Compare**. 📸 Captura 3: pestaña **Models** → `WineClassifier` con el alias `champion`.

Luego guarda en Git:
```
git add models/champion.joblib
git commit -m "Modelo champion"
git push
```

---

## PARTE 5 — FastAPI + página web 📸

```
python -m uvicorn app.main:app --reload
```
- http://127.0.0.1:8000 → formulario: pulsa **Predecir**. 📸
- http://127.0.0.1:8000/docs → prueba `/predict`. 📸
- http://127.0.0.1:8000/health → `{"status":"ok"}`. 📸
- Error 422: en `/docs` envía `alcohol: -5`. 📸

Detén el servidor con `Ctrl + C`.

---

## PARTE 6 — Pruebas y CI/CD con GitHub Actions 📸

1. Local: `python -m pytest -v` → deben pasar 3 pruebas. 📸
2. Ya hiciste `git push`: en GitHub abre la pestaña **Actions** → el workflow **Wine CI CD** debe salir con ✅. 📸
3. Fallo intencional (opcional, muy buena evidencia): en `tests/test_api.py` cambia `assert r.status_code == 200` (en `test_health`) por `404`, haz commit y push → ❌ en rojo 📸. Corrígelo, push de nuevo → ✅.
4. La imagen Docker se publica en GitHub: tu perfil → **Packages**. 📸

---

## PARTE 7 — Docker 📸

Con Docker Desktop abierto:
```
docker build -t wine-api:v1 .
docker images
docker run -d --name wine-api -p 8000:8000 wine-api:v1
docker ps
```
Abre http://localhost:8000 y haz una predicción. 📸 (`docker images`, `docker ps` y la web).

Para detenerlo: `docker stop wine-api` y `docker rm wine-api`.

---

## PARTE 8 — Airflow 📸

Requiere Docker Desktop abierto. En la terminal:
```
cd airflow
docker compose up -d
docker compose logs airflow
```
- Espera 2–3 minutos y busca en los logs la línea con la **contraseña** del usuario `admin`.
- Abre http://localhost:8080, entra con `admin` y esa contraseña.
- Busca el DAG **wine_training_pipeline**, actívalo y pulsa ▶ **Trigger**.
📸 Captura del DAG con las 3 tareas en verde (Graph).

Para apagarlo: `docker compose down`, y luego `cd ..`.

> Nota: Airflow descarga bastante la primera vez. Si algo falla, captura los logs: igual demuestra el flujo. Esta parte no pude probarla aquí porque necesita Docker.

---

## PARTE 9 — Monitoreo con Evidently 📸

```
python src/monitor.py
```
Abre `reports/data_drift.html` en el navegador (doble clic). Verás que `alcohol` y `proline` cambiaron (drift simulado). 📸
Interpretación para el PDF: los datos nuevos tienen más alcohol y más prolina que los de referencia → *data drift*; habría que revisar si el modelo sigue funcionando bien con etiquetas reales antes de reentrenar.

---

## PARTE 10 — Entregables

1. **PDF** (10–15 páginas): una sección por herramienta (Introducción, Git/GitHub, DVC, MLflow, FastAPI, Docker, Actions, Airflow, Monitoreo, Conclusiones), con tus capturas y 1–2 párrafos explicando qué hace cada una. Ya tienes la estructura en `PLANTILLA_REPORTE.md`; puedes pegarla en Word o Google Docs.
2. **Enlace de GitHub**: `https://github.com/TU_USUARIO/wine-mlops`.
3. **ZIP**: borra la carpeta `.venv`, luego clic derecho sobre `mlops_vinos` → *Comprimir/Enviar a → Carpeta comprimida*.
4. **Demo en clase** — ten abiertos antes de empezar: Docker Desktop con el contenedor corriendo (http://localhost:8000), MLflow UI (puerto 5000), tu repositorio en GitHub (Actions), el DAG de Airflow y `data_drift.html`.

### Frases para explicar al profesor
- **Git/GitHub**: versiona y comparte el código.
- **DVC**: versiona el dataset sin subirlo a Git.
- **MLflow**: guarda experimentos y elige el mejor modelo (champion).
- **Airflow**: automatiza validar → entrenar → verificar.
- **FastAPI**: convierte el modelo en un servicio web.
- **Docker**: empaqueta la app para correrla en cualquier PC.
- **GitHub Actions**: prueba y publica la imagen automáticamente en cada push.
- **Evidently**: detecta si los datos nuevos cambiaron respecto a los de entrenamiento.
