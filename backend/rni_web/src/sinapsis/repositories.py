# src/sinapsis/repositories.py

from typing import Any, Dict, List
import os
from pymongo import MongoClient


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

    def save_snapshot(self, metadata: Dict[str, Any], payload: List[Dict[str, Any]]) -> None:
        document = {
            "metadata": metadata,
            "payload": payload,
        }
        self.collection.insert_one(document)

    def list_snapshots(self) -> List[Dict[str, Any]]:
        return list(self.collection.find({}, {"payload": 0}))

    def get_snapshot(self, snapshot_id: str) -> List[Dict[str, Any]]:
        doc = self.collection.find_one({"_id": snapshot_id})
        return doc["payload"] if doc else []
