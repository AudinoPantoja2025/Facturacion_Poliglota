"""Crear Factura Use Case - Flujo completo de facturación."""

import logging
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

from src.domain.entities import Factura, DetalleFactura
from src.ports.outbound.repositories import (
    PersonaRepositoryPort,
    ProductoRepositoryPort,
    FacturaRepositoryPort,
    RecomendacionRepositoryPort
)

logger = logging.getLogger(__name__)


class CrearFacturaUseCase:
    """
    Caso de uso para crear una factura completa.
    
    Flujo:
    1. Valida que el cliente exista en Cassandra
    2. Obtiene productos de MongoDB
    3. Descuenta stock en MongoDB
    4. Crea la transacción ACID en MySQL
    5. Registra la compra en Neo4j para recomendaciones
    """
    
    def __init__(
        self,
        persona_repo: PersonaRepositoryPort,
        producto_repo: ProductoRepositoryPort,
        factura_repo: FacturaRepositoryPort,
        recomendacion_repo: RecomendacionRepositoryPort
    ):
        """
        Inicializa el caso de uso con sus dependencias.
        
        Inyección de dependencias: Se reciben como parámetros los puertos (interfaces),
        permitiendo usar cualquier adaptador concreto.
        """
        self.persona_repo = persona_repo
        self.producto_repo = producto_repo
        self.factura_repo = factura_repo
        self.recomendacion_repo = recomendacion_repo
    
    async def ejecutar(
        self,
        cliente_id: UUID,
        numero_factura: str,
        items: list[dict]
    ) -> Optional[Factura]:
        logger.info(f"Iniciando creación de factura #{numero_factura}")
        
        if not all([self.persona_repo, self.producto_repo, self.factura_repo, self.recomendacion_repo]):
            logger.error("Una o más bases de datos no están disponibles")
            return None
        
        try:
            # PASO 1: Validar cliente en Cassandra
            cliente = await self.persona_repo.obtener_por_id(cliente_id)
            if not cliente:
                logger.error(f"Cliente no encontrado: {cliente_id}")
                return None
            
            if not cliente.es_cliente():
                logger.error(f"La persona {cliente_id} no es un cliente")
                return None
            
            logger.info(f"✓ Cliente validado: {cliente.nombre}")
            
            # PASO 2: Crear factura y obtener productos de MongoDB
            factura = Factura(
                id=uuid4(),
                numero=numero_factura,
                fecha=datetime.now(),
                cliente_id=cliente_id
            )
            
            total_factura = 0.0
            
            for item in items:
                # Obtener producto de MongoDB
                producto = await self.producto_repo.obtener_por_id(item["producto_id"])
                
                if not producto:
                    logger.error(f"Producto no encontrado: {item['producto_id']}")
                    return None
                
                cantidad = item["cantidad"]
                
                # Validar stock
                if not producto.tiene_stock_disponible(cantidad):
                    logger.error(f"Stock insuficiente para {producto.nombre}")
                    return None
                
                # PASO 3: Descontar stock en MongoDB
                actualizado = await self.producto_repo.actualizar_stock(
                    producto.id, 
                    cantidad
                )
                
                if not actualizado:
                    logger.error(f"Error descargando stock para {producto.nombre}")
                    return None
                
                logger.info(f"✓ Stock descontado: {producto.nombre} ({cantidad} unidades)")
                
                # Crear detalle de factura
                detalle = DetalleFactura(
                    id=uuid4(),
                    factura_id=factura.id,
                    producto_id=producto.id,
                    cantidad=cantidad,
                    precio_unitario=producto.obtener_precio_unitario(),
                    subtotal=cantidad * producto.obtener_precio_unitario()
                )
                
                factura.agregar_detalle(detalle)
                total_factura += detalle.subtotal
            
            # PASO 4: Finalizar factura y guardar en MySQL (transacción ACID)
            factura.finalizar()
            factura_creada = await self.factura_repo.crear(factura)
            
            if not factura_creada:
                logger.error("Error guardando factura en MySQL")
                return None
            
            logger.info(f"✓ Factura creada en MySQL: {factura.numero}")
            
            # PASO 5: Registrar compras en Neo4j para motor de recomendaciones
            for detalle in factura.detalles:
                producto = await self.producto_repo.obtener_por_id(detalle.producto_id)
                
                # Crear relación COMPRO en Neo4j (auto-crea nodos Cliente/Producto si no existen)
                await self.recomendacion_repo.crear_compra(
                    cliente_id,
                    detalle.producto_id,
                    cliente_nombre=cliente.nombre,
                    producto_nombre=producto.nombre,
                    producto_categoria=producto.categoria
                )
            
            logger.info(f"✓ Compras registradas en Neo4j para recomendaciones")
            
            logger.info(
                f"✓ FACTURA COMPLETADA: #{numero_factura} | "
                f"Cliente: {cliente.nombre} | Total: ${factura.total:.2f}"
            )
            
            return factura_creada
            
        except Exception as e:
            logger.error(f"Error en caso de uso CrearFactura: {e}", exc_info=True)
            return None


class ObtenerRecomendacionesUseCase:
    """Caso de uso para obtener recomendaciones personalizadas."""
    
    def __init__(self, recomendacion_repo: RecomendacionRepositoryPort):
        self.recomendacion_repo = recomendacion_repo
    
    async def ejecutar(self, cliente_id: UUID, limite: int = 5) -> list[dict]:
        logger.info(f"Obteniendo recomendaciones para cliente {cliente_id}")
        
        if not self.recomendacion_repo:
            logger.warning("Neo4j no disponible, sin recomendaciones")
            return []
        
        try:
            recomendaciones = await self.recomendacion_repo.obtener_recomendaciones(
                cliente_id,
                limite
            )
            
            logger.info(f"✓ {len(recomendaciones)} recomendaciones obtenidas")
            return recomendaciones
            
        except Exception as e:
            logger.error(f"Error obteniendo recomendaciones: {e}")
            return []
