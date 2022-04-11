from pathlib import Path

BASE_PATH = Path(__file__).parent.parent.parent.parent

TEMPLATE_WORKER_PATH = (BASE_PATH / "worker/" / "workerTemplate.js").resolve()

RESOLVED_WORKER_PATH = (BASE_PATH / "worker/" / "resolvedWorker.js").resolve()
