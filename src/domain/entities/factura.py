"""Entidades de Facturación - Factura y DetalleFactura."""

from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal


@dataclass
class DetalleFactura:
    """
    Entidad de negocio DetalleFactura.
    Representa un item en la factura.
    """
    id: Optional[UUID] = None
    factura_id: Optional[UUID] = None
    producto_id: UUID = None
    cantidad: int = 0
    precio_unitario: float = 0.0
    subtotal: float = 0.0
    
    def calcular_subtotal(self) -> float:
        """Calcula el subtotal del detalle."""
        return self.cantidad * self.precio_unitario
    
    def validar(self) -> bool:
        """Valida reglas de negocio básicas."""
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        if self.precio_unitario <= 0:
            raise ValueError("El precio unitario debe ser mayor a cero")
        return True


@dataclass
class Factura:
    """
    Entidad de negocio Factura.
    Representa una transacción comercial completa.
    """
    id: Optional[UUID] = None
    numero: str = ""
    fecha: datetime = None
    cliente_id: UUID = None
    detalles: List[DetalleFactura] = field(default_factory=list)
    total: float = 0.0
    estado: str = "pendiente"
    
    def agregar_detalle(self, detalle: DetalleFactura) -> None:
        """Agrega un detalle a la factura."""
        detalle.validar()
        detalle.subtotal = detalle.calcular_subtotal()
        self.detalles.append(detalle)
    
    def calcular_total(self) -> float:
        """Calcula el total de la factura."""
        return sum(detalle.subtotal for detalle in self.detalles)
    
    def finalizar(self) -> None:
        """Finaliza la factura y calcula el total."""
        self.total = self.calcular_total()
        self.estado = "completada"
    
    def validar(self) -> bool:
        """Valida reglas de negocio básicas."""
        if not self.numero or len(self.numero.strip()) == 0:
            raise ValueError("El número de factura no puede estar vacío")
        if not self.cliente_id:
            raise ValueError("El cliente es obligatorio")
        if len(self.detalles) == 0:
            raise ValueError("La factura debe tener al menos un detalle")
        
        for detalle in self.detalles:
            detalle.validar()
        
        return True
