from __future__ import annotations
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

"""
API FastAPI de prédiction de churn pour le lab MLOps.

Ce service :
- charge dynamiquement le modèle courant indiqué dans `registry/current_model.txt` ;
- expose un endpoint `/health` pour vérifier l'état de l'API et du modèle ;
- expose un endpoint `/predict` pour faire une prédiction de churn à partir
  de features simples (tenure, plaintes, durée de session, type d’abonnement,
  région) ;
- journalise chaque requête de prédiction dans `logs/predictions.log` au
  format JSON (une ligne par prédiction).

Cette API illustre une étape "Serve" dans un pipeline MLOps minimal :
un modèle versionné est promu côté registry, puis utilisé par un service
d’inférence léger.
"""

import json
import time
import uuid
from pathlib import Path
from typing import Any, Optional

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Constantes de chemin
# ---------------------------------------------------------------------------

ROOT: Path = Path(__file__).resolve().parents[1]
MODELS_DIR: Path = ROOT / "models"
REGISTRY_DIR: Path = ROOT / "registry"
CURRENT_MODEL_PATH: Path = REGISTRY_DIR / "current_model.txt"
LOG_PATH: Path = ROOT / "logs" / "predictions.log"
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
MODEL_NAME = "churn_model"
ALIAS = "production"
MODEL_URI = f"models:/{MODEL_NAME}@{ALIAS}"

# ---------------------------------------------------------------------------
# Application FastAPI
# ---------------------------------------------------------------------------

app = FastAPI(title="MLOps Lab 01 - Churn API")

# ---------------------------------------------------------------------------
# Schéma d'entrée (Pydantic)
# ---------------------------------------------------------------------------

class PredictRequest(BaseModel):
    tenure_months: int = Field(..., ge=0, le=200)
    num_complaints: int = Field(..., ge=0, le=50)
    avg_session_minutes: float = Field(..., ge=0.0, le=500.0)
    plan_type: str
    region: str
    request_id: Optional[str] = None

# ---------------------------------------------------------------------------
# Cache de modèle en mémoire
# ---------------------------------------------------------------------------

_model_cache: dict[str, Any] = {"name": None, "model": None}

# ---------------------------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------------------------

# def get_current_model_name() -> str:
#     if not CURRENT_MODEL_PATH.exists():
#         raise FileNotFoundError(
#             "Aucun modèle courant. Lancer train.py (avec gate) d'abord."
#         )
#     name = CURRENT_MODEL_PATH.read_text(encoding="utf-8").strip()
#     if not name:
#         raise FileNotFoundError(
#             "Fichier current_model.txt vide. Aucun modèle activé."
#         )
#     return name

def get_current_model_name() -> str:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient()
    mv = client.get_model_version_by_alias(MODEL_NAME, ALIAS)
    return f"{MODEL_NAME}@{ALIAS} (v{mv.version})"

# def load_model_if_needed() -> tuple[str, Any]:
#     name = get_current_model_name()
#     if _model_cache["name"] == name and _model_cache["model"] is not None:
#         return name, _model_cache["model"]
#     path = MODELS_DIR / name
#     if not path.exists():
#         raise FileNotFoundError(f"Modèle introuvable sur disque : {path}")
#     model = joblib.load(path)
#     _model_cache["name"] = name
#     _model_cache["model"] = model
#     return name, model

def load_model_if_needed() -> tuple[str, Any]:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    # Cache key = model URI (alias), not local filename
    cache_key = MODEL_URI

    if _model_cache["name"] == cache_key and _model_cache["model"] is not None:
        return cache_key, _model_cache["model"]

    model = mlflow.sklearn.load_model(MODEL_URI)

    _model_cache["name"] = cache_key
    _model_cache["model"] = model
    return cache_key, model

def log_prediction(payload: dict[str, Any]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(payload, ensure_ascii=False) + "\n")

# ---------------------------------------------------------------------------
# Endpoints FastAPI
# ---------------------------------------------------------------------------

@app.get("/health")
def health() -> dict[str, Any]:
    """
    Endpoint de santé de l'API.


    Vérifie simplement qu'un modèle courant est bien configuré.


    Retour
    ------
    dict
        - status : "ok" ou "error"
        - current_model : nom du modèle courant (si OK)
        - detail : message d'erreur (si error)
    """
    try:
        model_name = get_current_model_name()
        return {"status": "ok", "current_model": model_name}
    except Exception as exc:  # pragma: no cover - simple endpoint de debug
        return {"status": "error", "detail": str(exc)}

@app.get("/startup")
def startup() -> dict[str, Any]:
    """
    Endpoint utilisé par Kubernetes startupProbe.

    L'application est considérée comme démarrée UNIQUEMENT si :
    - le registry existe,
    - le fichier current_model.txt existe,
    - le fichier n'est pas vide.
    """
    if not REGISTRY_DIR.exists():
        raise HTTPException(
            status_code=503,
            detail="Registry non monté (PVC absent ou incorrect).",
        )

    if not CURRENT_MODEL_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail="Aucun modèle courant. Lancer train.py (avec gate) d'abord.",
        )

    name = CURRENT_MODEL_PATH.read_text(encoding="utf-8").strip()
    if not name:
        raise HTTPException(
            status_code=503,
            detail="current_model.txt vide.",
        )

    return {
        "status": "ok",
        "current_model": name,
    }


@app.get("/ready")
def ready() -> dict[str, Any]:
    try:
        model_name = get_current_model_name()
        return {"status": "ready", "current_model": model_name}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc))

@app.post("/predict")
def predict(req: PredictRequest) -> dict[str, Any]:
    try:
        model_name, model = load_model_if_needed()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    features = {
        "tenure_months": req.tenure_months,
        "num_complaints": req.num_complaints,
        "avg_session_minutes": req.avg_session_minutes,
        "plan_type": req.plan_type.strip().lower(),
        "region": req.region.strip().upper(),
    }

    X_df = pd.DataFrame([features])

    start = time.perf_counter()
    try:
        proba = float(model.predict_proba(X_df)[0][1])
        pred = int(proba >= 0.5)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Erreur de prédiction : {exc}",
        ) from exc
    latency_ms = (time.perf_counter() - start) * 1000.0

    # --- Gestion du request_id    ---
    if not req.request_id:
        req.request_id = str(uuid.uuid4())

    out: dict[str, Any] = {
        "request_id": req.request_id,
        "model_version": model_name,
        "prediction": pred,
        "probability": round(proba, 6),
        "latency_ms": round(latency_ms, 3),
        "features": features,
        "ts": int(time.time()),
    }

    log_prediction(out)
    return out
