// ============================================================================
// NEO4J - MOTOR DE RECOMENDACIONES REALISTA
// Base de datos: 19mayo
//
// OBJETIVO:
// - Mostrar nombres reales en los nodos
// - Simular comportamiento de compras
// - Generar relaciones útiles para recomendaciones
// - Mejor visualización en Neo4j Browser

// PARA VER EL GRAFO COMPLETO AL FINAL:

//   MATCH (c:Cliente)-[r:COMPRO]->(p:Producto)
//   RETURN c, r, p

// ============================================================================
// LIMPIAR BASE DE DATOS (OPCIONAL)
// ============================================================================

// MATCH (n) DETACH DELETE n;

// CONSTRAINTS E ÍNDICES

CREATE CONSTRAINT cliente_id IF NOT EXISTS
FOR (c:Cliente)
REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT producto_id IF NOT EXISTS
FOR (p:Producto)
REQUIRE p.id IS UNIQUE;

CREATE INDEX idx_cliente_barrio IF NOT EXISTS
FOR (c:Cliente)
ON (c.barrio);

CREATE INDEX idx_producto_categoria IF NOT EXISTS
FOR (p:Producto)
ON (p.categoria);

CREATE INDEX idx_cliente_estrato IF NOT EXISTS
FOR (c:Cliente)
ON (c.estrato);


// ============================================================================
// CLIENTES
// ============================================================================

MERGE (c1:Cliente {id: "550e8400-e29b-41d4-a716-446655440001"})
SET c1.nombre = "Juan Pérez García",
    c1.genero = "M",
    c1.estrato = 3,
    c1.barrio = "Centro";

MERGE (c2:Cliente {id: "550e8400-e29b-41d4-a716-446655440002"})
SET c2.nombre = "María González López",
    c2.genero = "F",
    c2.estrato = 2,
    c2.barrio = "Centro";

MERGE (c3:Cliente {id: "550e8400-e29b-41d4-a716-446655440003"})
SET c3.nombre = "Carlos Rodríguez Martínez",
    c3.genero = "M",
    c3.estrato = 4,
    c3.barrio = "La Tola";

MERGE (c4:Cliente {id: "550e8400-e29b-41d4-a716-446655440004"})
SET c4.nombre = "Ana Martínez Sánchez",
    c4.genero = "F",
    c4.estrato = 3,
    c4.barrio = "La Tola";

MERGE (c5:Cliente {id: "550e8400-e29b-41d4-a716-446655440005"})
SET c5.nombre = "David López Fernández",
    c5.genero = "M",
    c5.estrato = 2,
    c5.barrio = "Olaya Herrera";

MERGE (c6:Cliente {id: "550e8400-e29b-41d4-a716-446655440008"})
SET c6.nombre = "Claudia Torres Ramírez",
    c6.genero = "F",
    c6.estrato = 2,
    c6.barrio = "Olaya Herrera";

MERGE (c7:Cliente {id: "550e8400-e29b-41d4-a716-446655440009"})
SET c7.nombre = "Fernando Ramírez Castro",
    c7.genero = "M",
    c7.estrato = 3,
    c7.barrio = "La Tola";

MERGE (c8:Cliente {id: "550e8400-e29b-41d4-a716-446655440010"})
SET c8.nombre = "Laura Castro Díaz",
    c8.genero = "F",
    c8.estrato = 4,
    c8.barrio = "Centro";


// ============================================================================
// PRODUCTOS
// ============================================================================

MERGE (p1:Producto {id: "1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a"})
SET p1.nombre = "Laptop Dell Inspiron 15",
    p1.categoria = "Electrónica",
    p1.precio = 3200;

MERGE (p2:Producto {id: "2b2b2b2b-2b2b-2b2b-2b2b-2b2b2b2b2b2b"})
SET p2.nombre = "Mouse Logitech MX Master 3",
    p2.categoria = "Accesorios",
    p2.precio = 450;

MERGE (p3:Producto {id: "3c3c3c3c-3c3c-3c3c-3c3c-3c3c3c3c3c3c"})
SET p3.nombre = "Teclado Mecánico Corsair K95",
    p3.categoria = "Accesorios",
    p3.precio = 650;

MERGE (p4:Producto {id: "4d4d4d4d-4d4d-4d4d-4d4d-4d4d4d4d4d4d"})
SET p4.nombre = "Monitor LG 27 4K",
    p4.categoria = "Monitores",
    p4.precio = 1800;

MERGE (p5:Producto {id: "5e5e5e5e-5e5e-5e5e-5e5e-5e5e5e5e5e5e"})
SET p5.nombre = "Auriculares Sony WH-1000XM5",
    p5.categoria = "Audio",
    p5.precio = 1400;

MERGE (p6:Producto {id: "6f6f6f6f-6f6f-6f6f-6f6f-6f6f6f6f6f6f"})
SET p6.nombre = "Webcam Logitech C920",
    p6.categoria = "Accesorios",
    p6.precio = 380;

MERGE (p7:Producto {id: "7a7a7a7a-7a7a-7a7a-7a7a-7a7a7a7a7a7a"})
SET p7.nombre = "SSD Samsung 970 EVO Plus 1TB",
    p7.categoria = "Almacenamiento",
    p7.precio = 520;

MERGE (p8:Producto {id: "8b8b8b8b-8b8b-8b8b-8b8b-8b8b8b8b8b8b"})
SET p8.nombre = "Memoria RAM Kingston DDR4 16GB",
    p8.categoria = "Memoria",
    p8.precio = 300;


// ============================================================================
// RELACIONES DE COMPRA
// ============================================================================

MATCH (c:Cliente {id: "550e8400-e29b-41d4-a716-446655440001"}),
      (p:Producto {id: "1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a"})
MERGE (c)-[:COMPRO {fecha: datetime("2026-05-01T10:30:00"), cantidad: 1}]->(p);

MATCH (c:Cliente {id: "550e8400-e29b-41d4-a716-446655440001"}),
      (p:Producto {id: "2b2b2b2b-2b2b-2b2b-2b2b-2b2b2b2b2b2b"})
MERGE (c)-[:COMPRO {fecha: datetime("2026-05-01T10:30:00"), cantidad: 1}]->(p);

MATCH (c:Cliente {id: "550e8400-e29b-41d4-a716-446655440002"}),
      (p:Producto {id: "2b2b2b2b-2b2b-2b2b-2b2b-2b2b2b2b2b2b"})
MERGE (c)-[:COMPRO {fecha: datetime("2026-05-03T12:00:00"), cantidad: 1}]->(p);

MATCH (c:Cliente {id: "550e8400-e29b-41d4-a716-446655440002"}),
      (p:Producto {id: "3c3c3c3c-3c3c-3c3c-3c3c-3c3c3c3c3c3c"})
MERGE (c)-[:COMPRO {fecha: datetime("2026-05-05T14:15:00"), cantidad: 1}]->(p);

MATCH (c:Cliente {id: "550e8400-e29b-41d4-a716-446655440003"}),
      (p:Producto {id: "4d4d4d4d-4d4d-4d4d-4d4d-4d4d4d4d4d4d"})
MERGE (c)-[:COMPRO {fecha: datetime("2026-05-10T09:45:00"), cantidad: 1}]->(p);

MATCH (c:Cliente {id: "550e8400-e29b-41d4-a716-446655440003"}),
      (p:Producto {id: "7a7a7a7a-7a7a-7a7a-7a7a-7a7a7a7a7a7a"})
MERGE (c)-[:COMPRO {fecha: datetime("2026-05-10T09:45:00"), cantidad: 1}]->(p);

MATCH (c:Cliente {id: "550e8400-e29b-41d4-a716-446655440004"}),
      (p:Producto {id: "5e5e5e5e-5e5e-5e5e-5e5e-5e5e5e5e5e5e"})
MERGE (c)-[:COMPRO {fecha: datetime("2026-05-12T16:20:00"), cantidad: 1}]->(p);

MATCH (c:Cliente {id: "550e8400-e29b-41d4-a716-446655440005"}),
      (p:Producto {id: "8b8b8b8b-8b8b-8b8b-8b8b-8b8b8b8b8b8b"})
MERGE (c)-[:COMPRO {fecha: datetime("2026-05-15T11:00:00"), cantidad: 1}]->(p);

MATCH (c:Cliente {id: "550e8400-e29b-41d4-a716-446655440006"}),
      (p:Producto {id: "2b2b2b2b-2b2b-2b2b-2b2b-2b2b2b2b2b2b"})
MERGE (c)-[:COMPRO {fecha: datetime("2026-05-18T09:00:00"), cantidad: 2}]->(p);

MATCH (c:Cliente {id: "550e8400-e29b-41d4-a716-446655440007"}),
      (p:Producto {id: "4d4d4d4d-4d4d-4d4d-4d4d-4d4d4d4d4d4d"})
MERGE (c)-[:COMPRO {fecha: datetime("2026-05-20T11:30:00"), cantidad: 1}]->(p);

MATCH (c:Cliente {id: "550e8400-e29b-41d4-a716-446655440008"}),
      (p:Producto {id: "3c3c3c3c-3c3c-3c3c-3c3c-3c3c3c3c3c3c"})
MERGE (c)-[:COMPRO {fecha: datetime("2026-05-22T15:00:00"), cantidad: 1}]->(p);

// ============================================================================
// RELACIONES CLIENTES SIMILARES (basado en mismo barrio + mismo estrato)
// ============================================================================

MATCH (c1:Cliente {nombre: "Juan Pérez García"}),
      (c2:Cliente {nombre: "María González López"})
MERGE (c1)-[:CLIENTE_SIMILAR {score: 0.89}]->(c2);

MATCH (c1:Cliente {nombre: "Carlos Rodríguez Martínez"}),
      (c2:Cliente {nombre: "Fernando Ramírez Castro"})
MERGE (c1)-[:CLIENTE_SIMILAR {score: 0.76}]->(c2);

MATCH (c1:Cliente {nombre: "David López Fernández"}),
      (c2:Cliente {nombre: "Claudia Torres Ramírez"})
MERGE (c1)-[:CLIENTE_SIMILAR {score: 0.82}]->(c2);

MATCH (c1:Cliente {nombre: "Ana Martínez Sánchez"}),
      (c2:Cliente {nombre: "Laura Castro Díaz"})
MERGE (c1)-[:CLIENTE_SIMILAR {score: 0.71}]->(c2);

// ============================================================================
// CONSULTAS DE RECOMENDACIÓN
// ============================================================================

// Productos comprados por cada cliente
MATCH (c:Cliente)-[:COMPRO]->(p:Producto)
RETURN c.nombre AS cliente, p.nombre AS producto, p.categoria AS categoria
ORDER BY cliente;

// Productos más populares
MATCH (:Cliente)-[r:COMPRO]->(p:Producto)
RETURN p.nombre AS producto, COUNT(r) AS total_compras
ORDER BY total_compras DESC;

// Recomendación: productos que compraron clientes similares
MATCH (c1:Cliente)-[:CLIENTE_SIMILAR]->(c2:Cliente),
      (c2)-[:COMPRO]->(p:Producto)
WHERE NOT EXISTS {MATCH (c1)-[:COMPRO]->(p)}
RETURN c1.nombre AS cliente, p.nombre AS producto_recomendado, p.categoria AS categoria;

// Recomendación: productos de la misma categoría ya comprada
MATCH (c:Cliente)-[:COMPRO]->(p1:Producto)
MATCH (p2:Producto)
WHERE p2.categoria = p1.categoria AND p2.id <> p1.id
  AND NOT EXISTS {MATCH (c)-[:COMPRO]->(p2)}
RETURN c.nombre AS cliente, p1.nombre AS compro, p2.nombre AS recomendado
ORDER BY cliente;

// Grafo visual completo
MATCH (c:Cliente)-[r:COMPRO]->(p:Producto)
RETURN c, r, p;

MATCH (n) WHERE n.nombre IS NOT NULL SET n.caption = n.nombre;
