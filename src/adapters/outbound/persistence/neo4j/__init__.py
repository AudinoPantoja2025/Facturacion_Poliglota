"""Neo4j Adapter - Motor de Recomendaciones Creativas."""

import logging
from typing import List, Optional
from uuid import UUID

from neo4j import GraphDatabase, Session, Result

from src.ports.outbound.repositories import RecomendacionRepositoryPort

logger = logging.getLogger(__name__)


class Neo4jRecomendacionAdapter(RecomendacionRepositoryPort):
    """Adaptador concreto para el motor de recomendaciones en Neo4j."""
    
    def __init__(self, uri: str, user: str, password: str, database: str = "19mayo"):
        """
        Inicializa la conexión a Neo4j.
        
        Args:
            uri: URI de conexión a Neo4j (bolt://localhost:7687)
            user: Usuario Neo4j
            password: Contraseña Neo4j
            database: Nombre de la base de datos (19mayo)
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database
        
        self._verificar_conexion()
        logger.info(f"Conectado a Neo4j - Database: {database}")
    
    def _verificar_conexion(self) -> None:
        """Verifica que la conexión sea válida."""
        try:
            with self.driver.session(database=self.database) as session:
                session.run("RETURN 1")
            logger.info("Conexión a Neo4j verificada")
        except Exception as e:
            logger.error(f"Error verificando conexión a Neo4j: {e}")
            raise
    
    async def crear_cliente(self, cliente_id: UUID, nombre: str, barrio: str, genero: str, estrato: int) -> bool:
        """Crea un nodo Cliente en Neo4j."""
        query = """
            MERGE (c:Cliente {id: $id})
            SET c.nombre = $nombre, c.barrio = $barrio, c.genero = $genero, c.estrato = $estrato
            RETURN c
        """
        
        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, {
                    "id": str(cliente_id),
                    "nombre": nombre,
                    "barrio": barrio,
                    "genero": genero,
                    "estrato": estrato
                })
                
                if result.single():
                    logger.info(f"Cliente creado en Neo4j: {cliente_id}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Error creando cliente en Neo4j: {e}")
            return False
    
    async def crear_producto(self, producto_id: UUID, nombre: str, categoria: str) -> bool:
        """Crea un nodo Producto en Neo4j."""
        query = """
            MERGE (p:Producto {id: $id})
            SET p.nombre = $nombre, p.categoria = $categoria
            RETURN p
        """
        
        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, {
                    "id": str(producto_id),
                    "nombre": nombre,
                    "categoria": categoria
                })
                
                if result.single():
                    logger.info(f"Producto creado en Neo4j: {producto_id}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Error creando producto en Neo4j: {e}")
            return False
    
    async def crear_compra(self, cliente_id: UUID, producto_id: UUID, *, cliente_nombre: str = "", producto_nombre: str = "", producto_categoria: str = "") -> bool:
        """Crea relación COMPRO entre Cliente y Producto.
        
        Si los nodos Cliente o Producto no existen en Neo4j, los crea automáticamente
        usando los datos adicionales proporcionados (self-healing).
        """
        query = """
            MERGE (c:Cliente {id: $cliente_id})
            SET c.nombre = CASE WHEN $cliente_nombre <> '' THEN $cliente_nombre ELSE c.nombre END
            MERGE (p:Producto {id: $producto_id})
            SET p.nombre = CASE WHEN $producto_nombre <> '' THEN $producto_nombre ELSE p.nombre END,
                p.categoria = CASE WHEN $producto_categoria <> '' THEN $producto_categoria ELSE p.categoria END
            MERGE (c)-[r:COMPRO]->(p)
            SET r.fecha = datetime()
            RETURN r
        """
        
        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, {
                    "cliente_id": str(cliente_id),
                    "producto_id": str(producto_id),
                    "cliente_nombre": cliente_nombre,
                    "producto_nombre": producto_nombre,
                    "producto_categoria": producto_categoria
                })
                
                if result.single():
                    logger.info(f"Compra registrada: Cliente {cliente_id} -> Producto {producto_id}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Error creando relación COMPRO: {e}")
            return False
    
    async def obtener_recomendaciones(self, cliente_id: UUID, limite: int = 5) -> List[dict]:
        """
        Obtiene recomendaciones para un cliente basadas en:
        - Compras de otros clientes del mismo género o estrato
        - Productos del mismo barrio/categoría
        - Preferencias similares
        
        Algoritmo híbrido de recomendación.
        """
        query = """
            MATCH (cliente:Cliente {id: $cliente_id})
            
            // Encontrar clientes similares: mismo género, estrato o barrio
            MATCH (cliente_similar:Cliente)
            WHERE (cliente_similar.genero = cliente.genero 
                   OR cliente_similar.estrato = cliente.estrato 
                   OR cliente_similar.barrio = cliente.barrio)
                   AND cliente_similar.id <> cliente.id
            
            // Obtener productos que compraron clientes similares
            MATCH (cliente_similar)-[:COMPRO]->(producto_recomendado:Producto)
            
            // Excluir productos que el cliente ya compró
            WHERE NOT (cliente)-[:COMPRO]->(producto_recomendado)
            
            // Agrupar y calcular score de relevancia
            WITH producto_recomendado, 
                 COUNT(DISTINCT cliente_similar) AS compras_similares,
                 COLLECT(DISTINCT cliente_similar.genero) AS generos_compradores,
                 COLLECT(DISTINCT cliente_similar.estrato) AS estratos_compradores
            
            // Calcular score basado en frecuencia y similitud
            WITH producto_recomendado, 
                 compras_similares,
                 CASE 
                     WHEN producto_recomendado.categoria IN ['recomendado'] THEN 10
                     ELSE 0
                 END AS score_categoria,
                 compras_similares * 2 AS score_frecuencia
            
            RETURN {
                producto_id: producto_recomendado.id,
                nombre: producto_recomendado.nombre,
                categoria: producto_recomendado.categoria,
                relevancia: score_frecuencia + score_categoria,
                compras_similares: compras_similares
            } AS recomendacion
            
            ORDER BY recomendacion.relevancia DESC
            LIMIT $limite
        """
        
        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, {
                    "cliente_id": str(cliente_id),
                    "limite": limite
                })
                
                recomendaciones = [record["recomendacion"] for record in result]
                logger.info(f"Recomendaciones obtenidas para cliente {cliente_id}: {len(recomendaciones)}")
                return recomendaciones
        except Exception as e:
            logger.error(f"Error obteniendo recomendaciones: {e}")
            return []
    
    async def obtener_clientes_similares(self, cliente_id: UUID) -> List[dict]:
        """Obtiene clientes similares al cliente dado."""
        query = """
            MATCH (cliente:Cliente {id: $cliente_id})
            
            // Encontrar clientes con mismo género, estrato o barrio
            MATCH (similar:Cliente)
            WHERE (similar.genero = cliente.genero 
                   OR similar.estrato = cliente.estrato 
                   OR similar.barrio = cliente.barrio)
                   AND similar.id <> cliente.id
            
            // Calcular similitud basada en atributos compartidos
            WITH cliente, similar,
                 (CASE WHEN similar.genero = cliente.genero THEN 1 ELSE 0 END +
                  CASE WHEN similar.estrato = cliente.estrato THEN 1 ELSE 0 END +
                  CASE WHEN similar.barrio = cliente.barrio THEN 1 ELSE 0 END) AS atributos_similares
            
            RETURN {
                cliente_id: similar.id,
                nombre: similar.nombre,
                genero: similar.genero,
                estrato: similar.estrato,
                barrio: similar.barrio,
                similitud: atributos_similares
            } AS cliente_similar
            
            ORDER BY cliente_similar.similitud DESC
            LIMIT 10
        """
        
        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, {"cliente_id": str(cliente_id)})
                
                clientes_similares = [record["cliente_similar"] for record in result]
                logger.info(f"Clientes similares encontrados: {len(clientes_similares)}")
                return clientes_similares
        except Exception as e:
            logger.error(f"Error obteniendo clientes similares: {e}")
            return []
    
    def close(self) -> None:
        """Cierra la conexión a Neo4j."""
        if self.driver:
            self.driver.close()
