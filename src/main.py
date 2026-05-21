"""Application Factory - Creación y configuración de la app Flask."""

import logging
import os
from flask import Flask, send_from_directory

from src.config import Config
from dbs.init_all import init_all
from src.adapters.outbound.persistence.cassandra import CassandraPersonaAdapter
from src.adapters.outbound.persistence.mongodb import MongoProductoAdapter
from src.adapters.outbound.persistence.mysql import MySQLFacturaAdapter
from src.adapters.outbound.persistence.neo4j import Neo4jRecomendacionAdapter
from src.usecases.factura import CrearFacturaUseCase, ObtenerRecomendacionesUseCase
from src.adapters.inbound.http import FacturaController, crear_rutas_factura, crear_rutas_datos


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """
    Application Factory - Crea y configura la aplicación Flask.
    
    Sigue el patrón de inyección de dependencias para desacoplar
    la lógica de negocio de la infraestructura.
    """
    app = Flask(__name__)
    
    # Cargar configuración
    config = Config()
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['FLASK_ENV'] = config.FLASK_ENV
    
    logger.info(f"Inicializando aplicación en modo {config.FLASK_ENV}")
    
    # INICIALIZAR BASES DE DATOS DESDE SCRIPTS
    # =========================================
    try:
        init_all(config)
    except Exception as e:
        logger.error(f"Error inicializando bases de datos: {e}")
    
    # INICIALIZAR ADAPTADORES (Infraestructura)
    # ===========================================
    
    try:
        # Cassandra - Personas
        persona_adapter = CassandraPersonaAdapter(
            hosts=config.db_config.cassandra_hosts,
            keyspace=config.db_config.cassandra_keyspace,
            username=config.db_config.cassandra_username,
            password=config.db_config.cassandra_password
        )
        logger.info("✓ Adaptador Cassandra inicializado")
    except Exception as e:
        logger.error(f"✗ Error inicializando Cassandra: {e}")
        persona_adapter = None
    
    try:
        # MongoDB - Productos
        producto_adapter = MongoProductoAdapter(
            uri=config.db_config.mongodb_url,
            database=config.db_config.mongodb_database
        )
        logger.info("✓ Adaptador MongoDB inicializado")
    except Exception as e:
        logger.error(f"✗ Error inicializando MongoDB: {e}")
        producto_adapter = None
    
    try:
        # MySQL - Facturas
        factura_adapter = MySQLFacturaAdapter(
            host=config.db_config.mysql_host,
            user=config.db_config.mysql_user,
            password=config.db_config.mysql_password,
            database=config.db_config.mysql_database,
            port=config.db_config.mysql_port
        )
        logger.info("✓ Adaptador MySQL inicializado")
    except Exception as e:
        logger.error(f"✗ Error inicializando MySQL: {e}")
        factura_adapter = None
    
    try:
        # Neo4j - Recomendaciones
        recomendacion_adapter = Neo4jRecomendacionAdapter(
            uri=config.db_config.neo4j_uri,
            user=config.db_config.neo4j_user,
            password=config.db_config.neo4j_password,
            database=config.db_config.neo4j_database
        )
        logger.info("✓ Adaptador Neo4j inicializado")
    except Exception as e:
        logger.error(f"✗ Error inicializando Neo4j: {e}")
        recomendacion_adapter = None
    
    # INICIALIZAR USE CASES (Orquestación de Negocio)
    # ===============================================
    
    crear_factura_usecase = CrearFacturaUseCase(
        persona_repo=persona_adapter,
        producto_repo=producto_adapter,
        factura_repo=factura_adapter,
        recomendacion_repo=recomendacion_adapter
    )
    
    obtener_recomendaciones_usecase = ObtenerRecomendacionesUseCase(
        recomendacion_repo=recomendacion_adapter
    )
    
    logger.info("✓ Use Cases inicializados")
    
    # INICIALIZAR CONTROLADORES (Adaptadores In)
    # ==========================================
    
    factura_controller = FacturaController(
        crear_factura_usecase=crear_factura_usecase,
        obtener_recomendaciones_usecase=obtener_recomendaciones_usecase,
        persona_adapter=persona_adapter,
        producto_adapter=producto_adapter,
        factura_adapter=factura_adapter,
        recomendacion_adapter=recomendacion_adapter
    )
    
    # REGISTRAR BLUEPRINTS
    # ====================
    
    factura_bp = crear_rutas_factura(factura_controller)
    app.register_blueprint(factura_bp)
    
    datos_bp = crear_rutas_datos(factura_controller)
    app.register_blueprint(datos_bp)
    
    logger.info("✓ Blueprints registrados")
    
    # RUTAS DE SALUD
    # ==============
    
    # RUTA FRONTEND
    # =============
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')

    @app.route('/', methods=['GET'])
    def index():
        return send_from_directory(frontend_path, 'index.html')
    
    health_status = {"cassandra": False, "mongodb": False, "mysql": False, "neo4j": False}
    if persona_adapter and persona_adapter.session:
        health_status["cassandra"] = True
    if producto_adapter and producto_adapter.client:
        health_status["mongodb"] = True
    if factura_adapter and factura_adapter.connection and factura_adapter.connection.is_connected():
        health_status["mysql"] = True
    if recomendacion_adapter and recomendacion_adapter.driver:
        health_status["neo4j"] = True

    @app.route('/api/v1/health', methods=['GET'])
    def health():
        return {
            "status": "healthy" if all(health_status.values()) else "degraded",
            "version": "1.0.0",
            "databases": health_status
        }, 200 if all(health_status.values()) else 200
    
    logger.info("✓ Aplicación Flask configurada correctamente")
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
