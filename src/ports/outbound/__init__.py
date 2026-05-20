"""Outbound Ports - External resource contracts."""
from .repositories import (
    PersonaRepositoryPort,
    ProductoRepositoryPort,
    FacturaRepositoryPort,
    RecomendacionRepositoryPort
)

__all__ = [
    "PersonaRepositoryPort",
    "ProductoRepositoryPort",
    "FacturaRepositoryPort",
    "RecomendacionRepositoryPort"
]
