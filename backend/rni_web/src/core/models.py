# Compatibilidad (legacy):
# Mantiene imports viejos funcionando, pero el dominio vive en apps.colaboradores
from apps.colaboradores.models import ColaboradorCore, ContratoCore, ColaboradorContrato

__all__ = ["ColaboradorCore", "ContratoCore", "ColaboradorContrato"]
