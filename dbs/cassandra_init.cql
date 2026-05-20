-- CASSANDRA - Inicialización para Personas (Clientes/Empleados)
-- Keyspace: persona

CREATE KEYSPACE IF NOT EXISTS persona
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE persona;

CREATE TABLE IF NOT EXISTS personas (
    id UUID PRIMARY KEY,
    nombre TEXT,
    email TEXT,
    rol TEXT,
    ciudad TEXT,
    barrio TEXT,
    genero TEXT,
    estrato INT,
    fecha_creacion TIMESTAMP,
    activo BOOLEAN
);

CREATE INDEX IF NOT EXISTS idx_personas_email ON personas (email);
CREATE INDEX IF NOT EXISTS idx_personas_rol ON personas (rol);
CREATE INDEX IF NOT EXISTS idx_personas_barrio ON personas (barrio);
CREATE INDEX IF NOT EXISTS idx_personas_activo ON personas (activo);

INSERT INTO personas (id, nombre, email, rol, ciudad, barrio, genero, estrato, fecha_creacion, activo)
VALUES (550e8400-e29b-41d4-a716-446655440001, 'Juan Pérez García', 'juan.perez@example.com', 'cliente', 'Putumayo', 'Centro', 'M', 3, toTimestamp(now()), true);

INSERT INTO personas (id, nombre, email, rol, ciudad, barrio, genero, estrato, fecha_creacion, activo)
VALUES (550e8400-e29b-41d4-a716-446655440002, 'María González López', 'maria.gonzalez@example.com', 'cliente', 'Putumayo', 'Centro', 'F', 2, toTimestamp(now()), true);

INSERT INTO personas (id, nombre, email, rol, ciudad, barrio, genero, estrato, fecha_creacion, activo)
VALUES (550e8400-e29b-41d4-a716-446655440003, 'Carlos Rodríguez Martínez', 'carlos.rodriguez@example.com', 'cliente', 'Putumayo', 'La Tola', 'M', 4, toTimestamp(now()), true);

INSERT INTO personas (id, nombre, email, rol, ciudad, barrio, genero, estrato, fecha_creacion, activo)
VALUES (550e8400-e29b-41d4-a716-446655440004, 'Ana Martínez Sánchez', 'ana.martinez@example.com', 'cliente', 'Putumayo', 'La Tola', 'F', 3, toTimestamp(now()), true);

INSERT INTO personas (id, nombre, email, rol, ciudad, barrio, genero, estrato, fecha_creacion, activo)
VALUES (550e8400-e29b-41d4-a716-446655440005, 'David López Fernández', 'david.lopez@example.com', 'cliente', 'Putumayo', 'Olaya Herrera', 'M', 2, toTimestamp(now()), true);

INSERT INTO personas (id, nombre, email, rol, ciudad, barrio, genero, estrato, fecha_creacion, activo)
VALUES (550e8400-e29b-41d4-a716-446655440006, 'Patricia Sánchez García', 'patricia.sanchez@example.com', 'empleado', 'Putumayo', 'Centro', 'F', 3, toTimestamp(now()), true);

INSERT INTO personas (id, nombre, email, rol, ciudad, barrio, genero, estrato, fecha_creacion, activo)
VALUES (550e8400-e29b-41d4-a716-446655440007, 'Roberto Fernández López', 'roberto.fernandez@example.com', 'empleado', 'Putumayo', 'Centro', 'M', 4, toTimestamp(now()), true);

INSERT INTO personas (id, nombre, email, rol, ciudad, barrio, genero, estrato, fecha_creacion, activo)
VALUES (550e8400-e29b-41d4-a716-446655440008, 'Claudia Torres Ramírez', 'claudia.torres@example.com', 'cliente', 'Putumayo', 'Olaya Herrera', 'F', 2, toTimestamp(now()), true);

INSERT INTO personas (id, nombre, email, rol, ciudad, barrio, genero, estrato, fecha_creacion, activo)
VALUES (550e8400-e29b-41d4-a716-446655440009, 'Fernando Ramírez Castro', 'fernando.ramirez@example.com', 'cliente', 'Putumayo', 'La Tola', 'M', 3, toTimestamp(now()), true);

INSERT INTO personas (id, nombre, email, rol, ciudad, barrio, genero, estrato, fecha_creacion, activo)
VALUES (550e8400-e29b-41d4-a716-446655440010, 'Laura Castro Díaz', 'laura.castro@example.com', 'cliente', 'Putumayo', 'Centro', 'F', 4, toTimestamp(now()), true);
