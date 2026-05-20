"""Entidad Producto - Catálogo de productos."""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime


@dataclass
class Producto:
    """
    Entidad de negocio Producto.
    Representa items del catálogo con estructura flexible.
    """
    id: UUID
    codigo: str
    nombre: str
    precio: float
    stock: int
    categoria: str
    fecha_creacion: datetime
    metadata: Dict[str, Any]
    activo: bool = True
    
    def obtener_precio_unitario(self) -> float:
        """Retorna el precio unitario del producto."""
        return self.precio
    
    def tiene_stock_disponible(self, cantidad: int) -> bool:
        """Verifica si hay stock suficiente."""
        return self.stock >= cantidad
    
    def descontar_stock(self, cantidad: int) -> None:
        """Descuenta stock del producto."""
        if not self.tiene_stock_disponible(cantidad):
            raise ValueError(f"Stock insuficiente. Disponible: {self.stock}, Solicitado: {cantidad}")
        self.stock -= cantidad
    
    def validar(self) -> bool:
        """Valida reglas de negocio básicas."""
        if not self.codigo or len(self.codigo.strip()) == 0:
            raise ValueError("El código de producto no puede estar vacío")
        if not self.nombre or len(self.nombre.strip()) == 0:
            raise ValueError("El nombre del producto no puede estar vacío")
        if self.precio <= 0:
            raise ValueError("El precio debe ser mayor a cero")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")
        return True
