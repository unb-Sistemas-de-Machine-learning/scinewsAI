import os
from typing import Optional, Dict, Any

import mlflow

from src.config import get_settings


def setup_mlflow() -> bool:
    """
    Initializes MLflow tracking if MLFLOW_TRACKING_URI is set.
    Returns True when tracking is enabled, False otherwise.
    """
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    if not tracking_uri:
        return False

    mlflow.set_tracking_uri(tracking_uri)
    experiment_name = os.getenv("MLFLOW_EXPERIMENT_NAME", "ai-translator")
    mlflow.set_experiment(experiment_name)
    return True


def log_common_params(extra: Optional[Dict[str, Any]] = None) -> None:
    """
    Logs common model/pipeline parameters from settings and any extra provided.
    """
    settings = get_settings()

    params = {
        "llm_provider": settings.LLM_PROVIDER.value,
        "openai_model": getattr(settings, "OPENAI_MODEL", None),
        "anthropic_model": getattr(settings, "ANTHROPIC_MODEL", None),
        "ollama_model": getattr(settings, "OLLAMA_MODEL", None),
        "chroma_dir": settings.CHROMA_PERSIST_DIRECTORY,
    }

    if extra:
        params.update(extra)

    # Filter out None values to keep the run clean
    filtered = {k: v for k, v in params.items() if v is not None}
    mlflow.log_params(filtered)
