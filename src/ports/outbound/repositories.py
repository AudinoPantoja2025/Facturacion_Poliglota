"""Repository Ports - Abstract repository interfaces."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.domain.entities import Persona, Producto, Factura, DetalleFactura


class PersonaRepositoryPort(ABC):
    """Puerto para persistencia de Personas en Cassandra."""
    
    @abstractmethod
    async def crear(self, persona: Persona) -> Persona:
        """Crea una nueva persona."""
        pass
    
    @abstractmethod
    async def obtener_por_id(self, persona_id: UUID) -> Optional[Persona]:
        """Obtiene una persona por ID."""
        pass
    
    @abstractmethod
    async def obtener_por_email(self, email: str) -> Optional[Persona]:
        """Obtiene una persona por email."""
        pass
    
    @abstractmethod
    async def listar_todos(self) -> List[Persona]:
        """Lista todas las personas."""
        pass
    
    @abstractmethod
    async def listar_por_barrio(self, barrio: str) -> List[Persona]:
        """Lista personas por barrio."""
        pass
    
    @abstractmethod
    async def actualizar(self, persona: Persona) -> Persona:
        """Actualiza una persona existente."""
        pass
    
    @abstractmethod
    async def eliminar(self, persona_id: UUID) -> bool:
        """Elimina una persona."""
        pass


class ProductoRepositoryPort(ABC):
    """Puerto para persistencia de Productos en MongoDB."""
    
    @abstractmethod
    async def crear(self, producto: Producto) -> Producto:
        """Crea un nuevo producto."""
        pass
    
    @abstractmethod
    async def obtener_por_id(self, producto_id: UUID) -> Optional[Producto]:
        """Obtiene un producto por ID."""
        pass
    
    @abstractmethod
    async def obtener_por_codigo(self, codigo: str) -> Optional[Producto]:
        """Obtiene un producto por código."""
        pass
    
    @abstractmethod
    async def listar_todos(self) -> List[Producto]:
        """Lista todos los productos."""
        pass
    
    @abstractmethod
    async def listar_por_categoria(self, categoria: str) -> List[Producto]:
        """Lista productos por categoría."""
        pass
    
    @abstractmethod
    async def actualizar(self, producto: Producto) -> Producto:
        """Actualiza un producto existente."""
        pass
    
    @abstractmethod
    async def actualizar_stock(self, producto_id: UUID, cantidad: int) -> bool:
        """Actualiza el stock de un producto."""
        pass
    
    @abstractmethod
    async def eliminar(self, producto_id: UUID) -> bool:
        """Elimina un producto."""
        pass


class FacturaRepositoryPort(ABC):
    """Puerto para persistencia de Facturas en MySQL."""
    
    @abstractmethod
    async def crear(self, factura: Factura) -> Factura:
        """Crea una nueva factura."""
        pass
    
    @abstractmethod
    async def obtener_por_id(self, factura_id: UUID) -> Optional[Factura]:
        """Obtiene una factura por ID."""
        pass
    
    @abstractmethod
    async def obtener_por_numero(self, numero: str) -> Optional[Factura]:
        """Obtiene una factura por número."""
        pass
    
    @abstractmethod
    async def listar_por_cliente(self, cliente_id: UUID) -> List[Factura]:
        """Lista facturas por cliente."""
        pass
    
    @abstractmethod
    async def listar_todas(self) -> List[Factura]:
        """Lista todas las facturas."""
        pass
    
    @abstractmethod
    async def actualizar_estado(self, factura_id: UUID, estado: str) -> bool:
        """Actualiza el estado de una factura."""
        pass
    
    @abstractmethod
    async def agregar_detalle(self, factura_id: UUID, detalle: DetalleFactura) -> bool:
        """Agrega un detalle a una factura."""
        pass
    
    @abstractmethod
    async def eliminar(self, factura_id: UUID) -> bool:
        """Elimina una factura."""
        pass


class RecomendacionRepositoryPort(ABC):
    """Puerto para motor de recomendaciones en Neo4j."""
    
    @abstractmethod
    async def crear_cliente(self, cliente_id: UUID, nombre: str, barrio: str, genero: str, estrato: int) -> bool:
        """Crea un nodo Cliente en Neo4j."""
        pass
    
    @abstractmethod
    async def crear_producto(self, producto_id: UUID, nombre: str, categoria: str) -> bool:
        """Crea un nodo Producto en Neo4j."""
        pass
    
    @abstractmethod
    async def crear_compra(self, cliente_id: UUID, producto_id: UUID, *, cliente_nombre: str = "", producto_nombre: str = "", producto_categoria: str = "") -> bool:
        """Crea relación COMPRO entre Cliente y Producto (y crea nodos si no existen)."""
        pass
    
    @abstractmethod
    async def obtener_recomendaciones(self, cliente_id: UUID, limite: int = 5) -> List[dict]:
        """Obtiene recomendaciones para un cliente basadas en:
        - Compras de otros clientes del mismo género/estrato
        - Productos del mismo barrio/categoría
        - Preferencias similares
        """
        pass
    
    @abstractmethod
    async def obtener_clientes_similares(self, cliente_id: UUID) -> List[dict]:
        """Obtiene clientes similares al cliente dado."""
        pass
