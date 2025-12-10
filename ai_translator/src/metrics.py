import os
from typing import Dict, List, Optional

import mlflow
import textstat


def log_basic_metrics(answer: str, contexts: List[str], reference: Optional[str] = None) -> None:
    """
    Logs lightweight metrics (lengths, readability) and, if a reference is provided,
    ROUGE-L. Heavy metrics are wrapped in try/except to avoid breaking the run.
    """
    mlflow.log_metric("summary_length", len(answer or ""))
    mlflow.log_metric("context_count", len(contexts))
    mlflow.log_metric("context_total_length", sum(len(c) for c in contexts))

    try:
        flesch = textstat.flesch_reading_ease(answer or "")
        mlflow.log_metric("flesch_reading_ease", flesch)
    except Exception:
        pass

    if reference:
        _log_reference_metrics(answer, reference)


def _log_reference_metrics(answer: str, reference: str) -> None:
    """
    Computes ROUGE-L if the libraries are available.
    """
    try:
        import evaluate

        rouge = evaluate.load("rouge")
        rouge_res = rouge.compute(predictions=[answer], references=[reference])
        if "rougeL" in rouge_res:
            mlflow.log_metric("rougeL", rouge_res["rougeL"])
    except Exception:
        pass


def maybe_load_reference(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None
