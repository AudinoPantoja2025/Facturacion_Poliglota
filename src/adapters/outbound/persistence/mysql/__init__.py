"""MySQL Adapter - Persistencia de Facturas."""

import logging
from typing import List, Optional
from uuid import UUID
from datetime import datetime

import mysql.connector
from mysql.connector import MySQLConnection

from src.domain.entities import Factura, DetalleFactura
from src.ports.outbound.repositories import FacturaRepositoryPort

logger = logging.getLogger(__name__)


class MySQLFacturaAdapter(FacturaRepositoryPort):
    """Adaptador concreto para persistencia de Facturas en MySQL."""
    
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        """
        Inicializa la conexión a MySQL.
        
        Args:
            host: Host del servidor MySQL
            user: Usuario MySQL
            password: Contraseña MySQL
            database: Nombre de la base de datos (ventas)
            port: Puerto MySQL (default: 3306)
        """
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
            "port": port,
            "autocommit": False
        }
        
        self.connection: Optional[MySQLConnection] = None
        self._connect()
    
    def _connect(self) -> None:
        """Establece la conexión a MySQL."""
        try:
            self.connection = mysql.connector.connect(**self.config)
            logger.info(f"Conectado a MySQL - Database: {self.config['database']}")
        except Exception as e:
            logger.error(f"Error conectando a MySQL: {e}")
            raise
    
    async def crear(self, factura: Factura) -> Factura:
        """Crea una nueva factura en MySQL."""
        factura.validar()
        
        cursor = self.connection.cursor()
        
        try:
            # Insertar factura
            query_factura = """
                INSERT INTO factura (id, numero, fecha, cliente_id, total, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query_factura, [
                str(factura.id), factura.numero, factura.fecha or datetime.now(),
                str(factura.cliente_id), factura.calcular_total(), factura.estado
            ])
            
            # Insertar detalles
            query_detalle = """
                INSERT INTO detalle_factura (id, factura_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            for detalle in factura.detalles:
                if not detalle.id:
                    detalle.id = UUID('12345678-1234-5678-1234-567812345678')  # Generar ID
                
                cursor.execute(query_detalle, [
                    str(detalle.id), str(factura.id), str(detalle.producto_id),
                    detalle.cantidad, detalle.precio_unitario, detalle.subtotal
                ])
            
            self.connection.commit()
            logger.info(f"Factura creada: {factura.id}")
            return factura
            
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error creando factura: {e}")
            raise
        finally:
            cursor.close()
    
    async def obtener_por_id(self, factura_id: UUID) -> Optional[Factura]:
        """Obtiene una factura por ID."""
        cursor = self.connection.cursor(dictionary=True)
        
        try:
            # Obtener factura
            query = "SELECT * FROM factura WHERE id = %s"
            cursor.execute(query, [str(factura_id)])
            row = cursor.fetchone()
            
            if not row:
                return None
            
            factura = self._mapear_fila_a_factura(row)
            
            # Obtener detalles
            query_detalles = "SELECT * FROM detalle_factura WHERE factura_id = %s"
            cursor.execute(query_detalles, [str(factura_id)])
            rows_detalles = cursor.fetchall()
            
            for row_detalle in rows_detalles:
                detalle = self._mapear_fila_a_detalle(row_detalle)
                factura.detalles.append(detalle)
            
            return factura
            
        except Exception as e:
            logger.error(f"Error obteniendo factura {factura_id}: {e}")
            return None
        finally:
            cursor.close()
    
    async def obtener_por_numero(self, numero: str) -> Optional[Factura]:
        """Obtiene una factura por número."""
        cursor = self.connection.cursor(dictionary=True)
        
        try:
            query = "SELECT * FROM factura WHERE numero = %s"
            cursor.execute(query, [numero])
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return self._mapear_fila_a_factura(row)
            
        except Exception as e:
            logger.error(f"Error obteniendo factura por número {numero}: {e}")
            return None
        finally:
            cursor.close()
    
    async def listar_por_cliente(self, cliente_id: UUID) -> List[Factura]:
        """Lista facturas por cliente."""
        cursor = self.connection.cursor(dictionary=True)
        
        try:
            query = "SELECT * FROM factura WHERE cliente_id = %s ORDER BY fecha DESC"
            cursor.execute(query, [str(cliente_id)])
            rows = cursor.fetchall()
            
            return [self._mapear_fila_a_factura(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Error listando facturas por cliente {cliente_id}: {e}")
            return []
        finally:
            cursor.close()
    
    async def listar_todas(self) -> List[Factura]:
        """Lista todas las facturas con conteo de items."""
        cursor = self.connection.cursor(dictionary=True)
        
        try:
            query = """
                SELECT f.*, COUNT(df.id) AS items
                FROM factura f
                LEFT JOIN detalle_factura df ON df.factura_id = f.id
                GROUP BY f.id
                ORDER BY f.fecha DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            
            facturas = []
            for row in rows:
                f = self._mapear_fila_a_factura(row)
                f.items = row["items"]
                facturas.append(f)
            return facturas
            
        except Exception as e:
            logger.error(f"Error listando facturas: {e}")
            return []
        finally:
            cursor.close()
    
    async def actualizar_estado(self, factura_id: UUID, estado: str) -> bool:
        """Actualiza el estado de una factura."""
        cursor = self.connection.cursor()
        
        try:
            query = "UPDATE factura SET estado = %s WHERE id = %s"
            cursor.execute(query, [estado, str(factura_id)])
            self.connection.commit()
            
            if cursor.rowcount == 0:
                logger.warning(f"Factura no encontrada: {factura_id}")
                return False
            
            logger.info(f"Estado actualizado para factura {factura_id}")
            return True
            
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error actualizando estado: {e}")
            return False
        finally:
            cursor.close()
    
    async def agregar_detalle(self, factura_id: UUID, detalle: DetalleFactura) -> bool:
        """Agrega un detalle a una factura."""
        cursor = self.connection.cursor()
        
        try:
            detalle.validar()
            
            if not detalle.id:
                detalle.id = UUID('12345678-1234-5678-1234-567812345678')  # Generar ID
            
            query = """
                INSERT INTO detalle_factura 
                (id, factura_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, [
                str(detalle.id), str(factura_id), str(detalle.producto_id),
                detalle.cantidad, detalle.precio_unitario, detalle.subtotal
            ])
            
            self.connection.commit()
            logger.info(f"Detalle agregado a factura {factura_id}")
            return True
            
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error agregando detalle: {e}")
            return False
        finally:
            cursor.close()
    
    async def eliminar(self, factura_id: UUID) -> bool:
        """Elimina una factura y sus detalles."""
        cursor = self.connection.cursor()
        
        try:
            # Eliminar detalles
            cursor.execute("DELETE FROM detalle_factura WHERE factura_id = %s", [str(factura_id)])
            
            # Eliminar factura
            cursor.execute("DELETE FROM factura WHERE id = %s", [str(factura_id)])
            
            self.connection.commit()
            
            if cursor.rowcount == 0:
                logger.warning(f"Factura no encontrada: {factura_id}")
                return False
            
            logger.info(f"Factura eliminada: {factura_id}")
            return True
            
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error eliminando factura: {e}")
            return False
        finally:
            cursor.close()
    
    def _mapear_fila_a_factura(self, row: dict) -> Factura:
        """Mapea una fila de MySQL a la entidad Factura."""
        return Factura(
            id=UUID(row["id"]),
            numero=row["numero"],
            fecha=row["fecha"],
            cliente_id=UUID(row["cliente_id"]),
            detalles=[],
            total=float(row["total"]),
            estado=row["estado"]
        )
    
    def _mapear_fila_a_detalle(self, row: dict) -> DetalleFactura:
        """Mapea una fila de MySQL a la entidad DetalleFactura."""
        return DetalleFactura(
            id=UUID(row["id"]),
            factura_id=UUID(row["factura_id"]),
            producto_id=UUID(row["producto_id"]),
            cantidad=row["cantidad"],
            precio_unitario=float(row["precio_unitario"]),
            subtotal=float(row["subtotal"])
        )
    
    def close(self) -> None:
        """Cierra la conexión a MySQL."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
