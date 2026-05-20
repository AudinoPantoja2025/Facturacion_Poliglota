-- MYSQL - Script de inicialización para Facturas
-- Base de datos: ventas

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS ventas;
USE ventas;

-- Tabla de Facturas
CREATE TABLE IF NOT EXISTS factura (
    id CHAR(36) PRIMARY KEY COMMENT 'UUID de la factura',
    numero VARCHAR(50) NOT NULL UNIQUE COMMENT 'Número secuencial de factura',
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de emisión',
    cliente_id CHAR(36) NOT NULL COMMENT 'Referencia al cliente en Cassandra',
    total DECIMAL(10, 2) NOT NULL DEFAULT 0 COMMENT 'Total de la factura',
    estado VARCHAR(50) NOT NULL DEFAULT 'pendiente' COMMENT 'Estado: pendiente, completada, cancelada',
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_cliente_id (cliente_id),
    INDEX idx_numero (numero),
    INDEX idx_fecha (fecha),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tabla de facturas/transacciones de venta';

-- Tabla de Detalles de Factura
CREATE TABLE IF NOT EXISTS detalle_factura (
    id CHAR(36) PRIMARY KEY COMMENT 'UUID del detalle',
    factura_id CHAR(36) NOT NULL COMMENT 'Referencia a la factura',
    producto_id CHAR(36) NOT NULL COMMENT 'Referencia al producto en MongoDB',
    cantidad INT NOT NULL COMMENT 'Cantidad de producto',
    precio_unitario DECIMAL(10, 2) NOT NULL COMMENT 'Precio unitario al momento de la compra',
    subtotal DECIMAL(10, 2) NOT NULL COMMENT 'Cantidad * Precio Unitario',
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (factura_id) REFERENCES factura(id) ON DELETE CASCADE,
    INDEX idx_factura_id (factura_id),
    INDEX idx_producto_id (producto_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tabla de detalles/items de facturas';

-- DATOS DE PRUEBA - Facturas iniciales

-- Factura 1: Cliente Juan Pérez
INSERT INTO factura (id, numero, fecha, cliente_id, total, estado) VALUES
('f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1', 'FAC-2026-001', '2026-05-01 10:30:00', '550e8400-e29b-41d4-a716-446655440001', 1099.97, 'completada');

INSERT INTO detalle_factura (id, factura_id, producto_id, cantidad, precio_unitario, subtotal) VALUES
('d1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1', 'f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1', '1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a', 1, 799.99, 799.99),
('d2d2d2d2-d2d2-d2d2-d2d2-d2d2d2d2d2d2', 'f1f1f1f1-f1f1-f1f1-f1f1-f1f1f1f1f1f1', '2b2b2b2b-2b2b-2b2b-2b2b-2b2b2b2b2b2b', 3, 99.99, 299.97);

-- Factura 2: Cliente María González
INSERT INTO factura (id, numero, fecha, cliente_id, total, estado) VALUES
('f2f2f2f2-f2f2-f2f2-f2f2-f2f2f2f2f2f2', 'FAC-2026-002', '2026-05-05 14:15:00', '550e8400-e29b-41d4-a716-446655440002', 529.96, 'completada');

INSERT INTO detalle_factura (id, factura_id, producto_id, cantidad, precio_unitario, subtotal) VALUES
('d3d3d3d3-d3d3-d3d3-d3d3-d3d3d3d3d3d3', 'f2f2f2f2-f2f2-f2f2-f2f2-f2f2f2f2f2f2', '3c3c3c3c-3c3c-3c3c-3c3c-3c3c3c3c3c3c', 2, 199.99, 399.98),
('d4d4d4d4-d4d4-d4d4-d4d4-d4d4d4d4d4d4', 'f2f2f2f2-f2f2-f2f2-f2f2-f2f2f2f2f2f2', '6f6f6f6f-6f6f-6f6f-6f6f-6f6f6f6f6f6f', 5, 79.99, 129.98);

-- Factura 3: Cliente Carlos Rodríguez
INSERT INTO factura (id, numero, fecha, cliente_id, total, estado) VALUES
('f3f3f3f3-f3f3-f3f3-f3f3-f3f3f3f3f3f3', 'FAC-2026-003', '2026-05-10 09:45:00', '550e8400-e29b-41d4-a716-446655440003', 919.96, 'completada');

INSERT INTO detalle_factura (id, factura_id, producto_id, cantidad, precio_unitario, subtotal) VALUES
('d5d5d5d5-d5d5-d5d5-d5d5-d5d5d5d5d5d5', 'f3f3f3f3-f3f3-f3f3-f3f3-f3f3f3f3f3f3', '4d4d4d4d-4d4d-4d4d-4d4d-4d4d4d4d4d4d', 2, 399.99, 799.98),
('d6d6d6d6-d6d6-d6d6-d6d6-d6d6d6d6d6d6', 'f3f3f3f3-f3f3-f3f3-f3f3-f3f3f3f3f3f3', '7a7a7a7a-7a7a-7a7a-7a7a-7a7a7a7a7a7a', 1, 129.99, 129.99);

-- Factura 4: Cliente Ana Martínez
INSERT INTO factura (id, numero, fecha, cliente_id, total, estado) VALUES
('f4f4f4f4-f4f4-f4f4-f4f4-f4f4f4f4f4f4', 'FAC-2026-004', '2026-05-12 16:20:00', '550e8400-e29b-41d4-a716-446655440004', 349.99, 'completada');

INSERT INTO detalle_factura (id, factura_id, producto_id, cantidad, precio_unitario, subtotal) VALUES
('d7d7d7d7-d7d7-d7d7-d7d7-d7d7d7d7d7d7', 'f4f4f4f4-f4f4-f4f4-f4f4-f4f4f4f4f4f4', '5e5e5e5e-5e5e-5e5e-5e5e-5e5e5e5e5e5e', 1, 349.99, 349.99);

-- Factura 5: Cliente David López
INSERT INTO factura (id, numero, fecha, cliente_id, total, estado) VALUES
('f5f5f5f5-f5f5-f5f5-f5f5-f5f5f5f5f5f5', 'FAC-2026-005', '2026-05-15 11:00:00', '550e8400-e29b-41d4-a716-446655440005', 209.97, 'completada');

INSERT INTO detalle_factura (id, factura_id, producto_id, cantidad, precio_unitario, subtotal) VALUES
('d8d8d8d8-d8d8-d8d8-d8d8-d8d8d8d8d8d8', 'f5f5f5f5-f5f5-f5f5-f5f5-f5f5f5f5f5f5', '8b8b8b8b-8b8b-8b8b-8b8b-8b8b8b8b8b8b', 2, 89.99, 179.98),
('d9d9d9d9-d9d9-d9d9-d9d9-d9d9d9d9d9d9', 'f5f5f5f5-f5f5-f5f5-f5f5-f5f5f5f5f5f5', '1d1d1d1d-1d1d-1d1d-1d1d-1d1d1d1d1d1d', 1, 19.99, 19.99);

-- ============================================================================
-- VERIFICACIÓN
-- ============================================================================

-- SELECT COUNT(*) as total_facturas FROM factura;
-- SELECT * FROM factura;
-- SELECT * FROM detalle_factura;
