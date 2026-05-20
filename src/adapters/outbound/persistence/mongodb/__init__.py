"""MongoDB Adapter - Persistencia de Productos."""

import logging
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from src.domain.entities import Producto
from src.ports.outbound.repositories import ProductoRepositoryPort

logger = logging.getLogger(__name__)


class MongoProductoAdapter(ProductoRepositoryPort):
    """Adaptador concreto para persistencia de Productos en MongoDB."""
    
    def __init__(self, uri: str, database: str):
        """
        Inicializa la conexión a MongoDB.
        
        Args:
            uri: URI de conexión a MongoDB
            database: Nombre de la base de datos (productos)
        """
        self.client = MongoClient(uri)
        self.db: Database = self.client[database]
        self.collection: Collection = self.db["productos"]
        
        self._crear_indices()
        logger.info(f"Conectado a MongoDB - Database: {database}")
    
    def _crear_indices(self) -> None:
        """Crea índices para optimizar consultas."""
        try:
            self.collection.create_index("codigo", unique=True)
            self.collection.create_index("categoria")
            self.collection.create_index("activo")
            logger.info("Índices creados en colección productos")
        except Exception as e:
            logger.warning(f"Error creando índices: {e}")
    
    async def crear(self, producto: Producto) -> Producto:
        """Crea un nuevo producto en MongoDB."""
        producto.validar()
        
        doc = {
            "_id": str(producto.id),
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "stock": producto.stock,
            "categoria": producto.categoria,
            "fecha_creacion": producto.fecha_creacion,
            "metadata": producto.metadata,
            "activo": producto.activo
        }
        
        try:
            result = self.collection.insert_one(doc)
            logger.info(f"Producto creado: {producto.id}")
            return producto
        except Exception as e:
            logger.error(f"Error creando producto: {e}")
            raise
    
    async def obtener_por_id(self, producto_id: UUID) -> Optional[Producto]:
        """Obtiene un producto por ID."""
        try:
            doc = self.collection.find_one({"_id": str(producto_id)})
            if not doc:
                return None
            
            return self._mapear_doc_a_producto(doc)
        except Exception as e:
            logger.error(f"Error obteniendo producto {producto_id}: {e}")
            return None
    
    async def obtener_por_codigo(self, codigo: str) -> Optional[Producto]:
        """Obtiene un producto por código."""
        try:
            doc = self.collection.find_one({"codigo": codigo})
            if not doc:
                return None
            
            return self._mapear_doc_a_producto(doc)
        except Exception as e:
            logger.error(f"Error obteniendo producto por código {codigo}: {e}")
            return None
    
    async def listar_todos(self) -> List[Producto]:
        """Lista todos los productos activos."""
        try:
            docs = self.collection.find({"activo": True})
            return [self._mapear_doc_a_producto(doc) for doc in docs]
        except Exception as e:
            logger.error(f"Error listando productos: {e}")
            return []
    
    async def listar_por_categoria(self, categoria: str) -> List[Producto]:
        """Lista productos por categoría."""
        try:
            docs = self.collection.find({
                "categoria": categoria,
                "activo": True
            })
            return [self._mapear_doc_a_producto(doc) for doc in docs]
        except Exception as e:
            logger.error(f"Error listando productos por categoría {categoria}: {e}")
            return []
    
    async def actualizar(self, producto: Producto) -> Producto:
        """Actualiza un producto existente."""
        producto.validar()
        
        update_doc = {
            "$set": {
                "nombre": producto.nombre,
                "precio": producto.precio,
                "stock": producto.stock,
                "categoria": producto.categoria,
                "metadata": producto.metadata,
                "activo": producto.activo
            }
        }
        
        try:
            self.collection.update_one(
                {"_id": str(producto.id)},
                update_doc
            )
            logger.info(f"Producto actualizado: {producto.id}")
            return producto
        except Exception as e:
            logger.error(f"Error actualizando producto: {e}")
            raise
    
    async def actualizar_stock(self, producto_id: UUID, cantidad: int) -> bool:
        """Actualiza el stock de un producto."""
        try:
            result = self.collection.update_one(
                {"_id": str(producto_id)},
                {"$inc": {"stock": -cantidad}}
            )
            if result.modified_count == 0:
                logger.warning(f"Producto no encontrado: {producto_id}")
                return False
            
            logger.info(f"Stock actualizado para producto {producto_id}")
            return True
        except Exception as e:
            logger.error(f"Error actualizando stock: {e}")
            return False
    
    async def eliminar(self, producto_id: UUID) -> bool:
        """Elimina (soft delete) un producto."""
        try:
            result = self.collection.update_one(
                {"_id": str(producto_id)},
                {"$set": {"activo": False}}
            )
            if result.modified_count == 0:
                logger.warning(f"Producto no encontrado: {producto_id}")
                return False
            
            logger.info(f"Producto eliminado: {producto_id}")
            return True
        except Exception as e:
            logger.error(f"Error eliminando producto: {e}")
            return False
    
    def _mapear_doc_a_producto(self, doc: dict) -> Producto:
        """Mapea un documento de MongoDB a la entidad Producto."""
        return Producto(
            id=UUID(doc["_id"]),
            codigo=doc["codigo"],
            nombre=doc["nombre"],
            precio=doc["precio"],
            stock=doc["stock"],
            categoria=doc["categoria"],
            fecha_creacion=doc["fecha_creacion"],
            metadata=doc.get("metadata", {}),
            activo=doc.get("activo", True)
        )
    
    def close(self) -> None:
        """Cierra la conexión a MongoDB."""
        if self.client:
            self.client.close()
