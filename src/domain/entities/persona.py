"""Entidad Persona - Clientes y Empleados."""

from dataclasses import dataclass
from enum import Enum
from uuid import UUID
from typing import Optional
from datetime import datetime


class Rol(str, Enum):
    """Roles de personas en el sistema."""
    CLIENTE = "cliente"
    EMPLEADO = "empleado"


@dataclass
class Persona:
    """
    Entidad de negocio Persona.
    Representa clientes y empleados en el sistema.
    """
    id: UUID
    nombre: str
    email: str
    rol: Rol
    ciudad: str
    barrio: str
    genero: str
    estrato: int
    fecha_creacion: datetime
    activo: bool = True
    
    def es_cliente(self) -> bool:
        """Verifica si la persona es cliente."""
        return self.rol == Rol.CLIENTE
    
    def es_empleado(self) -> bool:
        """Verifica si la persona es empleado."""
        return self.rol == Rol.EMPLEADO
    
    def validar(self) -> bool:
        """Valida reglas de negocio básicas."""
        if not self.nombre or len(self.nombre.strip()) == 0:
            raise ValueError("El nombre no puede estar vacío")
        if not self.email or "@" not in self.email:
            raise ValueError("Email inválido")
        if self.estrato < 1 or self.estrato > 6:
            raise ValueError("El estrato debe estar entre 1 y 6")
        return True
