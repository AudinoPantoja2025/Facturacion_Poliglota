"""Configuration - Gestión de configuración de la aplicación."""

import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    """Configuración de bases de datos."""
    
    # Cassandra
    cassandra_hosts: list[str]
    cassandra_keyspace: str
    cassandra_username: str
    cassandra_password: str
    
    # MongoDB
    mongodb_url: str
    mongodb_database: str
    
    # MySQL
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_database: str
    
    # Neo4j
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    neo4j_database: str


class Config:
    """Configuración de la aplicación."""
    
    def __init__(self):
        load_dotenv(Path(__file__).parent.parent.parent / '.env')
        
        self.FLASK_ENV = os.getenv("FLASK_ENV", "development")
        self.FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
        
        self.db_config = DatabaseConfig(
            # Cassandra
            cassandra_hosts=os.getenv("CASSANDRA_HOSTS", "127.0.0.1").split(","),
            cassandra_keyspace=os.getenv("CASSANDRA_KEYSPACE", "persona"),
            cassandra_username=os.getenv("CASSANDRA_USERNAME", ""),
            cassandra_password=os.getenv("CASSANDRA_PASSWORD", ""),
            
            # MongoDB
            mongodb_url=os.getenv("MONGODB_URL", "mongodb://localhost:27017"),
            mongodb_database=os.getenv("MONGODB_DATABASE", "productos"),
            
            # MySQL
            mysql_host=os.getenv("MYSQL_HOST", "localhost"),
            mysql_port=int(os.getenv("MYSQL_PORT", "3306")),
            mysql_user=os.getenv("MYSQL_USER", "root"),
            mysql_password=os.getenv("MYSQL_PASSWORD", "root"),
            mysql_database=os.getenv("MYSQL_DATABASE", "ventas"),
            
            # Neo4j
            neo4j_uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            neo4j_user=os.getenv("NEO4J_USER", "neo4j"),
            neo4j_password=os.getenv("NEO4J_PASSWORD", "password123"),
            neo4j_database=os.getenv("NEO4J_DATABASE", "19mayo")
        )
