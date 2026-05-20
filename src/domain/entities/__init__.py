"""Domain Entities - Pure business objects."""
from .persona import Persona, Rol
from .producto import Producto
from .factura import Factura, DetalleFactura

__all__ = ["Persona", "Rol", "Producto", "Factura", "DetalleFactura"]
