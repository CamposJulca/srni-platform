# sinapsis/services.py

from datetime import datetime
from typing import List, Dict, Any

from .loaders import load_json_snapshot
from .schemas import SinapsisProjectSchema
from .repositories import SinapsisSnapshotRepository

from typing import List, Dict
from .repositories import SinapsisSnapshotRepository


class SinapsisProjectService:
    """
    Capa de aplicación para exponer vistas de proyectos Sinapsis.
    """

    def __init__(self, repository: SinapsisSnapshotRepository):
        self.repository = repository

    def list_projects(self) -> List[Dict]:
        return self.repository.list_project_summaries()


class SinapsisSnapshotService:
    """
    Servicio de aplicación para manejo de snapshots Sinapsis.
    """

    def __init__(self, repository: SinapsisSnapshotRepository):
        self.repository = repository

    def ingest_snapshot_from_file(self, path: str) -> int:
        """
        Carga un snapshot desde archivo, valida y persiste.
        Retorna cantidad de proyectos.
        """
        raw_projects = load_json_snapshot(path)

        # Validación estructural (contrato)
        validated = [SinapsisProjectSchema(**p) for p in raw_projects]

        metadata = {
            "source": "SINAPSIS",
            "ingested_at": datetime.utcnow().isoformat(),
            "records": len(validated),
        }

        self.repository.save_snapshot(
            metadata=metadata,
            payload=[p.model_dump() for p in validated],
        )

        return len(validated)
