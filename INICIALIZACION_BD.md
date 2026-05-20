# Inicialización de Bases de Datos

## Cassandra (Personas)

```bash
cqlsh localhost 9042 -f dbs/cassandra_init.cql
```

Verificar:
```bash
cqlsh localhost 9042 -e "SELECT COUNT(*) FROM persona.personas;"
# → 10
```

## MongoDB (Productos)

```bash
mongosh localhost:27017 < dbs/mongodb_init.js
```

Verificar:
```bash
mongosh localhost:27017 --eval "db.productos.countDocuments()" productos
# → 15
```

## MySQL (Facturas)

```bash
mysql -h localhost -u root -p < dbs/mysql_init.sql
```

Verificar:
```bash
mysql -h localhost -u root -p -e "SELECT COUNT(*) FROM ventas.factura;"
# → 5
```

## Neo4j (Recomendaciones)

Abrir http://localhost:7484, conectar con `neo4j`/tu_password, pegar todo el contenido de `dbs/neo4j_init.cypher` y ejecutar.

Verificar:
```cypher
MATCH (c:Cliente) RETURN COUNT(c);
MATCH (p:Producto) RETURN COUNT(p);
MATCH ()-[r:COMPRO]->() RETURN COUNT(r);
```

**Nota**: El script asigna `caption = nombre` automáticamente para que Neo4j Browser muestre los nombres.

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
