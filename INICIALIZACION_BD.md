# Inicialización de Bases de Datos

## Inicio Automático (Recomendado)

Las 4 bases de datos se inicializan **automáticamente** al ejecutar el backend:

```bash
python run.py
```

Esto ejecuta `dbs/init_all.py` que lee los scripts en `dbs/` y los ejecuta
usando los drivers Python del proyecto. No requiere `cqlsh`, `mongosh`, `mysql`, ni pegar
nada en Neo4j Browser.

## Verificación

### Cassandra (Personas) — 10 registros

```bash
cqlsh localhost 9042 -e "SELECT COUNT(*) FROM persona.personas;"
```

### MongoDB (Productos) — 15 registros

```bash
mongosh localhost:27017 --eval "db.productos.countDocuments()" productos
```

### MySQL (Facturas) — 5 facturas con detalles

```bash
mysql -h localhost -u root -p -e "SELECT * FROM ventas.factura;"
mysql -h localhost -u root -p -e "SELECT * FROM ventas.detalle_factura;"
```

### Neo4j (Recomendaciones) — 8 clientes, 8 productos, ~12 compras

```cypher
MATCH (c:Cliente) RETURN COUNT(c);
MATCH (p:Producto) RETURN COUNT(p);
MATCH ()-[r:COMPRO]->() RETURN COUNT(r);
```

## Inicio Manual (Alternativa)

Si prefieres ejecutar los scripts manualmente:

```bash
# Cassandra
cqlsh localhost 9042 -f dbs/cassandra_init.cql

# MongoDB
mongosh localhost:27017 < dbs/mongodb_init.js

# MySQL
mysql -h localhost -u root -p < dbs/mysql_init.sql

# Neo4j — pegar dbs/neo4j_init.cypher en http://localhost:7474
```

**Nota**: El script de Neo4j asigna `caption = nombre` automáticamente para que Neo4j Browser muestre los nombres.

## Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

El proxy de Vite redirige `/api/*` al backend en `localhost:5000`.

## Troubleshooting

### Cassandra
- `Connection refused`: verificar que el contenedor Docker está corriendo (`docker ps`)
- Si usa Docker: `docker run -d --name cassandra -p 9042:9042 cassandra:5.0`

### MongoDB
- `Connection refused`: `sudo service mongod start` o iniciar MongoDB Compass

### MySQL
- `Access denied`: verificar credenciales en `.env`
- `Unknown database ventas`: ejecutar `CREATE DATABASE ventas;` antes del script

### Neo4j
- `Neo4j Browser 2.1.4`: no usa `:config setNodeCaption`, usa `:style` o la propiedad `caption`
- Cambiar contraseña por defecto: `ALTER USER neo4j SET PASSWORD 'nueva';`

### Python
- `RuntimeError: Install Flask with the 'async' extra`: `pip install flask[async]`
- `ModuleNotFoundError: No module named 'src'`: ejecutar desde la raíz del proyecto
