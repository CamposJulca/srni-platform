# backend/rni_web/src/sinapsis/client.py

import os
import requests
from typing import List

from .schemas import SinapsisProjectSchema


class SinapsisClient:
    """
    Cliente HTTP para la API de Sinapsis.
    Capa de infraestructura (no contiene lógica de negocio).
    """

    def __init__(self):
        self.base_url = os.getenv("SINAPSIS_BASE_URL")
        self.api_key = os.getenv("SINAPSIS_API_KEY")

        if not self.base_url or not self.api_key:
            raise RuntimeError(
                "SINAPSIS_BASE_URL y SINAPSIS_API_KEY deben estar definidos en el entorno"
            )

        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def fetch_projects_raw(self) -> list:
        """
        Retorna el JSON crudo de proyectos desde Sinapsis.
        """
        url = f"{self.base_url}/api/management/projects/detailed"

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30,
            verify=False,  # Equivalente a curl -k
        )

        response.raise_for_status()
        return response.json()

    def fetch_projects_validated(self) -> List[SinapsisProjectSchema]:
        """
        Retorna los proyectos validados contra el schema Pydantic.
        """
        raw_projects = self.fetch_projects_raw()
        return [SinapsisProjectSchema(**p) for p in raw_projects]
