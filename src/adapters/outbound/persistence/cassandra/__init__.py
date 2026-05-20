"""Cassandra Adapter - Persistencia de Personas."""

import logging
from typing import List, Optional
from uuid import UUID
from datetime import datetime

# Python 3.12+ compatibility: patch cassandra-driver default connection
from ._patch import patch_cassandra_cluster
patch_cassandra_cluster()

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from src.domain.entities import Persona, Rol
from src.ports.outbound.repositories import PersonaRepositoryPort

logger = logging.getLogger(__name__)


class CassandraPersonaAdapter(PersonaRepositoryPort):
    """Adaptador concreto para persistencia de Personas en Cassandra."""
    
    def __init__(self, hosts: List[str], keyspace: str, username: str = None, password: str = None):
        """
        Inicializa la conexión a Cassandra.
        
        Args:
            hosts: Lista de hosts de Cassandra
            keyspace: Nombre del keyspace (persona)
            username: Usuario opcional
            password: Contraseña opcional
        """
        self.hosts = hosts
        self.keyspace = keyspace
        
        if username and password:
            auth_provider = PlainTextAuthProvider(username=username, password=password)
            self.cluster = Cluster(hosts, auth_provider=auth_provider)
        else:
            self.cluster = Cluster(hosts)
        
        self.session = None
        self._connect()
    
    def _connect(self) -> None:
        """Establece la conexión al cluster de Cassandra."""
        try:
            self.session = self.cluster.connect(self.keyspace)
            logger.info(f"Conectado a Cassandra - Keyspace: {self.keyspace}")
        except Exception as e:
            logger.error(f"Error conectando a Cassandra: {e}")
            raise
    
    async def crear(self, persona: Persona) -> Persona:
        """Crea una nueva persona en Cassandra."""
        persona.validar()
        
        query = """
            INSERT INTO personas (
                id, nombre, email, rol, ciudad, barrio, genero, estrato, 
                fecha_creacion, activo
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        
        try:
            self.session.execute(query, [
                persona.id, persona.nombre, persona.email, persona.rol.value,
                persona.ciudad, persona.barrio, persona.genero, persona.estrato,
                persona.fecha_creacion, persona.activo
            ])
            logger.info(f"Persona creada: {persona.id}")
            return persona
        except Exception as e:
            logger.error(f"Error creando persona: {e}")
            raise
    
    async def obtener_por_id(self, persona_id: UUID) -> Optional[Persona]:
        """Obtiene una persona por ID."""
        query = "SELECT * FROM personas WHERE id = %s"
        
        try:
            row = self.session.execute(query, [persona_id]).one()
            if not row:
                return None
            
            return self._mapear_fila_a_persona(row)
        except Exception as e:
            logger.error(f"Error obteniendo persona {persona_id}: {e}")
            return None

    async def obtener_por_email(self, email: str) -> Optional[Persona]:
        """Obtiene una persona por email (requiere índice secundario)."""
        query = "SELECT * FROM personas WHERE email = %s ALLOW FILTERING"
        
        try:
            row = self.session.execute(query, [email]).one()
            if not row:
                return None
            
            return self._mapear_fila_a_persona(row)
        except Exception as e:
            logger.error(f"Error obteniendo persona por email {email}: {e}")
            return None
    
    async def listar_todos(self) -> List[Persona]:
        """Lista todas las personas."""
        query = "SELECT * FROM personas WHERE activo = true ALLOW FILTERING"
        
        try:
            rows = self.session.execute(query)
            return [self._mapear_fila_a_persona(row) for row in rows]
        except Exception as e:
            logger.error(f"Error listando personas: {e}")
            return []
    
    async def listar_por_barrio(self, barrio: str) -> List[Persona]:
        """Lista personas por barrio."""
        query = "SELECT * FROM personas WHERE barrio = %s AND activo = true ALLOW FILTERING"
        
        try:
            rows = self.session.execute(query, [barrio])
            return [self._mapear_fila_a_persona(row) for row in rows]
        except Exception as e:
            logger.error(f"Error listando personas por barrio {barrio}: {e}")
            return []
    
    async def actualizar(self, persona: Persona) -> Persona:
        """Actualiza una persona existente."""
        persona.validar()
        
        query = """
            UPDATE personas SET 
                nombre = %s, email = %s, ciudad = %s, barrio = %s,
                genero = %s, estrato = %s, activo = %s
            WHERE id = %s
        """
        
        try:
            self.session.execute(query, [
                persona.nombre, persona.email, persona.ciudad, persona.barrio,
                persona.genero, persona.estrato, persona.activo, persona.id
            ])
            logger.info(f"Persona actualizada: {persona.id}")
            return persona
        except Exception as e:
            logger.error(f"Error actualizando persona: {e}")
            raise
    
    async def eliminar(self, persona_id: UUID) -> bool:
        """Elimina (soft delete) una persona."""
        query = "UPDATE personas SET activo = false WHERE id = %s"
        
        try:
            self.session.execute(query, [persona_id])
            logger.info(f"Persona eliminada: {persona_id}")
            return True
        except Exception as e:
            logger.error(f"Error eliminando persona: {e}")
            return False
    
    def _mapear_fila_a_persona(self, row) -> Persona:
        """Mapea una fila de Cassandra a la entidad Persona."""
        return Persona(
            id=row.id,
            nombre=row.nombre,
            email=row.email,
            rol=Rol(row.rol),
            ciudad=row.ciudad,
            barrio=row.barrio,
            genero=row.genero,
            estrato=row.estrato,
            fecha_creacion=row.fecha_creacion,
            activo=row.activo
        )
    
    def close(self) -> None:
        """Cierra la conexión a Cassandra."""
        if self.session:
            self.session.shutdown()
        if self.cluster:
            self.cluster.shutdown()
