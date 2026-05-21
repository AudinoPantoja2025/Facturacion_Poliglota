"""Inicializa las 4 bases de datos desde los scripts en dbs/ al arrancar.

Lee cada archivo (.cql, .js, .sql, .cypher) y ejecuta las sentencias
usando los mismos drivers Python del proyecto. No requiere herramientas CLI.
"""

import logging
import re
from pathlib import Path

# ── Aplicar parche de Cassandra para Python 3.12+ ─────────────────
# Esto debe ejecutarse ANTES de importar cassandra.cluster, porque
# reemplaza asyncore (eliminado en 3.12) por asyncio en el módulo de
# cluster. El parche se aplica automáticamente al importar _patch.
from src.adapters.outbound.persistence.cassandra import _patch  # noqa

logger = logging.getLogger(__name__)

DBS_DIR = Path(__file__).parent


def _load(name: str) -> str | None:
    p = DBS_DIR / name
    if not p.exists():
        logger.warning(f"Script no encontrado: {p}")
        return None
    return p.read_text(encoding="utf-8")


def _statements(text: str) -> list[str]:
    """Divide un script por punto y coma, limpia comentarios y líneas vacías."""
    out = []
    for raw in text.split(";"):
        cleaned = re.sub(r"(//|--).*", "", raw).strip()
        if cleaned:
            out.append(cleaned)
    return out


# ── Cassandra ────────────────────────────────────────────────────

def _init_cassandra(config):
    from cassandra.cluster import Cluster
    from cassandra.auth import PlainTextAuthProvider

    content = _load("cassandra_init.cql")
    if not content:
        return

    auth = None
    if config.db_config.cassandra_username:
        auth = PlainTextAuthProvider(
            config.db_config.cassandra_username,
            config.db_config.cassandra_password,
        )

    cluster = Cluster(config.db_config.cassandra_hosts, auth_provider=auth)
    session = cluster.connect()

    for stmt in _statements(content):
        try:
            session.execute(stmt)
        except Exception:
            pass

    session.shutdown()
    cluster.shutdown()
    logger.info("  ✓ Cassandra")


# ── MongoDB ──────────────────────────────────────────────────────

PRODUCTOS_SEED = [
    {"codigo": "PROD-001", "nombre": "Laptop Dell Inspiron 15",       "precio": 799.99,  "stock": 10, "categoria": "Electrónica"},
    {"codigo": "PROD-002", "nombre": "Mouse Logitech MX Master 3",     "precio": 99.99,   "stock": 50, "categoria": "Accesorios"},
    {"codigo": "PROD-003", "nombre": "Teclado Mecánico Corsair K95",   "precio": 199.99,  "stock": 25, "categoria": "Accesorios"},
    {"codigo": "PROD-004", "nombre": "Monitor LG 27 4K",               "precio": 399.99,  "stock": 15, "categoria": "Monitores"},
    {"codigo": "PROD-005", "nombre": "Auriculares Sony WH-1000XM5",    "precio": 349.99,  "stock": 30, "categoria": "Audio"},
    {"codigo": "PROD-006", "nombre": "Webcam Logitech C920",           "precio": 79.99,   "stock": 40, "categoria": "Accesorios"},
    {"codigo": "PROD-007", "nombre": "SSD Samsung 970 EVO Plus 1TB",   "precio": 129.99,  "stock": 50, "categoria": "Almacenamiento"},
    {"codigo": "PROD-008", "nombre": "Memoria RAM Kingston DDR4 16GB", "precio": 89.99,   "stock": 60, "categoria": "Memoria"},
    {"codigo": "PROD-009", "nombre": "Fuente de Poder Corsair 750W",   "precio": 119.99,  "stock": 20, "categoria": "Componentes"},
    {"codigo": "PROD-010", "nombre": "Carcasa NZXT H510 Flow",         "precio": 99.99,   "stock": 35, "categoria": "Componentes"},
    {"codigo": "PROD-011", "nombre": "Tarjeta Gráfica NVIDIA RTX 4070","precio": 699.99,  "stock": 8,  "categoria": "Componentes"},
    {"codigo": "PROD-012", "nombre": "Cable USB-C 2.0 3 Metros",       "precio": 19.99,   "stock": 100,"categoria": "Cables"},
    {"codigo": "PROD-013", "nombre": "Hub USB 3.0 7 Puertos",          "precio": 49.99,   "stock": 45, "categoria": "Accesorios"},
    {"codigo": "PROD-014", "nombre": "Laptop Pad Refrigerador",        "precio": 39.99,   "stock": 60, "categoria": "Accesorios"},
    {"codigo": "PROD-015", "nombre": "Adaptador HDMI 2.1 4K@120Hz",    "precio": 29.99,   "stock": 80, "categoria": "Cables"},
]


_UUID_PRODUCTOS = [
    "1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a",
    "2b2b2b2b-2b2b-2b2b-2b2b-2b2b2b2b2b2b",
    "3c3c3c3c-3c3c-3c3c-3c3c-3c3c3c3c3c3c",
    "4d4d4d4d-4d4d-4d4d-4d4d-4d4d4d4d4d4d",
    "5e5e5e5e-5e5e-5e5e-5e5e-5e5e5e5e5e5e",
    "6f6f6f6f-6f6f-6f6f-6f6f-6f6f6f6f6f6f",
    "7a7a7a7a-7a7a-7a7a-7a7a-7a7a7a7a7a7a",
    "8b8b8b8b-8b8b-8b8b-8b8b-8b8b8b8b8b8b",
    "9c9c9c9c-9c9c-9c9c-9c9c-9c9c9c9c9c9c",
    "1d1d1d1d-1d1d-1d1d-1d1d-1d1d1d1d1d1d",
    "2e2e2e2e-2e2e-2e2e-2e2e-2e2e2e2e2e2e",
    "3f3f3f3f-3f3f-3f3f-3f3f-3f3f3f3f3f3f",
    "4a4a4a4a-4a4a-4a4a-4a4a-4a4a4a4a4a4a",
    "5b5b5b5b-5b5b-5b5b-5b5b-5b5b5b5b5b5b",
    "6c6c6c6c-6c6c-6c6c-6c6c-6c6c6c6c6c6c",
]


def _init_mongodb(config):
    import pymongo

    client = pymongo.MongoClient(config.db_config.mongodb_url)
    db = client[config.db_config.mongodb_database]
    coll = db["productos"]

    if coll.count_documents({}) == 0:
        from datetime import datetime
        docs = []
        for i, p in enumerate(PRODUCTOS_SEED):
            doc = {
                "_id": _UUID_PRODUCTOS[i],
                "codigo": p["codigo"],
                "nombre": p["nombre"],
                "precio": p["precio"],
                "stock": p["stock"],
                "categoria": p["categoria"],
                "activo": True,
                "fecha_creacion": datetime.now(),
                "metadata": {},
            }
            docs.append(doc)
        coll.insert_many(docs)
        logger.info(f"  ✓ MongoDB ({len(docs)} docs)")

    for idx_name in ("codigo", "categoria", "activo"):
        try:
            coll.create_index(idx_name, unique=(idx_name == "codigo"))
        except Exception:
            pass

    client.close()
    logger.info("  ✓ MongoDB")


# ── MySQL ─────────────────────────────────────────────────────────

def _init_mysql(config):
    import mysql.connector

    content = _load("mysql_init.sql")
    if not content:
        return

    conn = mysql.connector.connect(
        host=config.db_config.mysql_host,
        user=config.db_config.mysql_user,
        password=config.db_config.mysql_password,
        port=config.db_config.mysql_port,
    )
    cursor = conn.cursor()

    for stmt in _statements(content):
        try:
            cursor.execute(stmt)
            conn.commit()
        except Exception:
            pass

    cursor.close()
    conn.close()
    logger.info("  ✓ MySQL")


# ── Neo4j ─────────────────────────────────────────────────────────

def _init_neo4j(config):
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(
        config.db_config.neo4j_uri,
        auth=(config.db_config.neo4j_user, config.db_config.neo4j_password),
    )

    db_name = config.db_config.neo4j_database

    # Crear la BD primero (conectando a system)
    try:
        with driver.session(database="system") as session:
            session.run(f"CREATE DATABASE `{db_name}` IF NOT EXISTS")
    except Exception:
        pass

    # Ejecutar script de inicialización
    content = _load("neo4j_init.cypher")
    if content:
        with driver.session(database=db_name) as session:
            for stmt in _statements(content):
                try:
                    session.run(stmt)
                except Exception:
                    pass

    driver.close()
    logger.info("  ✓ Neo4j")


# ── Entry point ───────────────────────────────────────────────────

def init_all(config):
    """Lee y ejecuta los 4 scripts de inicialización de bases de datos."""
    logger.info("━" * 45)
    logger.info("Inicializando bases de datos desde scripts...")
    logger.info("━" * 45)
    for name, fn in [("Cassandra", _init_cassandra),
                     ("MongoDB", _init_mongodb),
                     ("MySQL", _init_mysql),
                     ("Neo4j", _init_neo4j)]:
        try:
            fn(config)
        except Exception as e:
            logger.error(f"  ✗ {name}: {e}")
    logger.info("━" * 45)
    logger.info("Inicialización completada")
    logger.info("━" * 45)
