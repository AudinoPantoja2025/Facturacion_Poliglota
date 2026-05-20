# Facturación Políglota

Sistema de facturación con **4 bases de datos** (Cassandra, MongoDB, MySQL, Neo4j), **backend Flask** con arquitectura hexagonal y **frontend React** (Vite + Tailwind).

---

## Stack

| Capa | Tecnología |
|------|-----------|
| Backend | Flask (Python 3.12), hexagonal architecture |
| Frontend | React 18, Vite, Tailwind CSS, React Router, Axios |
| Cassandra | Personas (columnar NoSQL) |
| MongoDB | Productos (documental) |
| MySQL | Facturas (SQL ACID) |
| Neo4j | Recomendaciones (grafos) |

---

## Requisitos

- Python 3.12+
- Node.js 18+
- Cassandra 4+ (vía Docker)
- MongoDB 6+
- MySQL 8+
- Neo4j 5+

---

## Instalación

```bash
# Backend
python -m venv env
env\Scripts\activate      # Windows
pip install flask[async] cassandra-driver pymongo mysql-connector-python neo4j python-dotenv

# Frontend
cd frontend
npm install
```

## Configuración

Crear `.env` en la raíz:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key

CASSANDRA_HOSTS=127.0.0.1
CASSANDRA_PORT=9042
CASSANDRA_KEYSPACE=persona
CASSANDRA_USERNAME=
CASSANDRA_PASSWORD=

MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=productos

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=ventas

NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=pwneo4j
NEO4J_DATABASE=19mayo
```

## Inicializar Bases de Datos

```bash
# Cassandra
cqlsh localhost 9042 -f dbs/cassandra_init.cql

# MongoDB
mongosh localhost:27017 < dbs/mongodb_init.js

# MySQL
mysql -h localhost -u root -p < dbs/mysql_init.sql

# Neo4j (pegar dbs/neo4j_init.cypher en Neo4j Browser http://localhost:7474)
```

## Ejecutar

```bash
# Terminal 1 - Backend
python src/main.py            # http://localhost:5000

# Terminal 2 - Frontend
cd frontend
npm run dev                   # http://localhost:5173
```

---

## API Endpoints

### Personas (Cassandra)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/datos/personas` | Listar todas |
| POST | `/api/v1/datos/personas` | Crear |
| PUT | `/api/v1/datos/personas/<id>` | Actualizar |
| DELETE | `/api/v1/datos/personas/<id>` | Eliminar |

### Productos (MongoDB)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/datos/productos` | Listar todos |
| POST | `/api/v1/datos/productos` | Crear |
| PUT | `/api/v1/datos/productos/<id>` | Actualizar |
| DELETE | `/api/v1/datos/productos/<id>` | Eliminar |

### Facturas (MySQL)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/datos/facturas` | Listar todas (con conteo de items) |
| GET | `/api/v1/datos/facturas/<id>` | Obtener con detalles |
| POST | `/api/v1/facturas` | Crear (flujo multi-BD) |

### Recomendaciones (Neo4j)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/facturas/recomendaciones/<cliente_id>?limite=5` | Recomendaciones personalizadas |

### Salud

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/health` | Estado de conexión a cada BD |

---

## Frontend (5 tabs)

| Tab | Ruta | Descripción |
|-----|------|-------------|
| Dashboard | `/` | Stats + últimas facturas |
| Personas | `/personas` | CRUD completo con edición inline |
| Productos | `/productos` | CRUD completo con búsqueda y edición inline |
| Facturación | `/facturacion` | POS con carrito, historial y modal de detalle |
| Recomendaciones | `/recomendaciones` | Motor basado en Neo4j |

---

## Arquitectura

```
src/
├── domain/entities/     # Persona, Producto, Factura, DetalleFactura
├── ports/outbound/      # Interfaces abstractas (RepositoryPorts)
├── adapters/
│   ├── inbound/http/    # Controladores Flask
│   └── outbound/persistence/
│       ├── cassandra/   # Personas
│       ├── mongodb/     # Productos
│       ├── mysql/       # Facturas
│       └── neo4j/       # Recomendaciones
├── usecases/            # CrearFacturaUseCase, ObtenerRecomendacionesUseCase
├── config/              # Config desde .env
└── main.py              # Application Factory
```

### Flujo: Crear Factura

1. **Cassandra** — Valida que el cliente existe y es `rol=cliente`
2. **MongoDB** — Obtiene cada producto y descuenta stock
3. **MySQL** — Inserta factura + detalles en transacción ACID
4. **Neo4j** — Crea relación `(:Cliente)-[:COMPRO]->(:Producto)` (auto-crea nodos si no existen)

### Algoritmo de Recomendaciones

Busca productos que compraron clientes del **mismo género, estrato o barrio**, excluye los que el cliente ya compró, y ordena por relevancia = `compras_similares * 2 + score_categoria`.

---

## Ejemplo: Crear Factura

```bash
curl -X POST http://localhost:5000/api/v1/facturas \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "550e8400-e29b-41d4-a716-446655440001",
    "numero_factura": "FAC-2026-001",
    "items": [
      {"producto_id": "1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a", "cantidad": 1},
      {"producto_id": "2b2b2b2b-2b2b-2b2b-2b2b-2b2b2b2b2b2b", "cantidad": 2}
    ]
  }'
```

Respuesta:
```json
{
  "id": "uuid", "numero": "FAC-2026-001",
  "cliente_id": "550e8400-...", "total": 999.97,
  "estado": "completada", "items": 2
}
```

---

## Notas

- **Cassandra auth**: dejar `CASSANDRA_USERNAME`/`CASSANDRA_PASSWORD` vacío si no tiene autenticación
- **Neo4j Browser 2.1.4**: el script ya asigna `caption = nombre` automáticamente
- **Python 3.12+**: el driver de Cassandra requiere un patch (`_patch.py`) que reemplaza `asyncore` por `asyncio`
- **IDs**: Cassandra y Neo4j comparten mismos UUIDs de personas; MongoDB y Neo4j comparten mismos UUIDs de productos
