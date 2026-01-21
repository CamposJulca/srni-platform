# src/sinapsis/repositories.py

from typing import Any, Dict, List
import os
from pymongo import MongoClient
from bson import ObjectId


class SinapsisSnapshotRepository:
    """
    Interfaz de persistencia para snapshots de Sinapsis.
    """

    def save_snapshot(self, metadata: Dict[str, Any], payload: List[Dict[str, Any]]) -> None:
        raise NotImplementedError

    def list_snapshots(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def get_snapshot(self, snapshot_id: str) -> List[Dict[str, Any]]:
        raise NotImplementedError


class MongoSinapsisSnapshotRepository(SinapsisSnapshotRepository):
    """
    Implementación MongoDB para snapshots de Sinapsis.
    Capa de infraestructura (sin dependencia directa de Django).
    """

    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        mongo_db = os.getenv("MONGO_DB", "sinapsis")
        mongo_collection = os.getenv("MONGO_COLLECTION", "projects_snapshots")

        if not mongo_uri:
            raise RuntimeError("MONGO_URI no configurado")

        self.client = MongoClient(mongo_uri)
        self.db = self.client[mongo_db]
        self.collection = self.db[mongo_collection]

    # =====================================================
    # Persistencia de snapshots completos
    # =====================================================

    def save_snapshot(self, metadata: Dict[str, Any], payload: List[Dict[str, Any]]) -> None:
        document = {
            "metadata": metadata,
            "payload": payload,
        }
        self.collection.insert_one(document)

    def list_snapshots(self) -> List[Dict[str, Any]]:
        return list(self.collection.find({}, {"payload": 0}))

    def get_snapshot(self, snapshot_id: str) -> List[Dict[str, Any]]:
        doc = self.collection.find_one({"_id": ObjectId(snapshot_id)})
        return doc["payload"] if doc else []

    # =====================================================
    # 🔵 NUEVO MÉTODO — VISTA NORMALIZADA PARA API
    # =====================================================

    def list_project_summaries(self) -> List[Dict[str, Any]]:
        """
        Devuelve una vista plana de proyectos a partir de los snapshots.
        Pensado para consumo por API / dashboards.
        """

        cursor = self.collection.find(
            {},
            {
                "_id": 1,
                "payload.name": 1,
                "payload.status": 1,
                "payload.lifecycle_stage": 1,
                "payload.tech_domain": 1,
                "payload.risk_level": 1,
                "payload.initiative_level": 1,
            }
        )

        projects: List[Dict[str, Any]] = []

        for snapshot in cursor:
            snapshot_id = str(snapshot["_id"])

            for project in snapshot.get("payload", []):
                projects.append({
                    "snapshot_id": snapshot_id,
                    "name": project.get("name"),
                    "status": project.get("status"),
                    "lifecycle_stage": project.get("lifecycle_stage"),
                    "tech_domain": project.get("tech_domain"),
                    "risk_level": project.get("risk_level"),
                    "initiative_level": project.get("initiative_level"),
                })

        return projects
