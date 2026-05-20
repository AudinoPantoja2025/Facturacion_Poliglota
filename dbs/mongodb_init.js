// MONGODB - Script de inicialización para Productos
// Base de datos: productos
// Colección: productos

db = db.getSiblingDB("productos");
db.createCollection("productos");

// Crear índices
db.productos.createIndex({ "codigo": 1 }, { unique: true });
db.productos.createIndex({ "categoria": 1 });
db.productos.createIndex({ "activo": 1 });


// DATOS DE PRUEBA - 15 productos con estructura flexible

db.productos.insertMany([
    {
        _id: "1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a",
        codigo: "PROD-001",
        nombre: "Laptop Dell Inspiron 15",
        precio: 799.99,
        stock: 10,
        categoria: "Electrónica",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            marca: "Dell",
            procesador: "Intel i7",
            ram_gb: 16,
            almacenamiento_gb: 512,
            pantalla_pulgadas: 15.6,
            peso_kg: 1.85
        }
    },
    {
        _id: "2b2b2b2b-2b2b-2b2b-2b2b-2b2b2b2b2b2b",
        codigo: "PROD-002",
        nombre: "Mouse Logitech MX Master 3",
        precio: 99.99,
        stock: 50,
        categoria: "Accesorios",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            marca: "Logitech",
            tipo: "Inalámbrico",
            bateria_dias: 70,
            dpi: 4000
        }
    },
    {
        _id: "3c3c3c3c-3c3c-3c3c-3c3c-3c3c3c3c3c3c",
        codigo: "PROD-003",
        nombre: "Teclado Mecánico Corsair K95",
        precio: 199.99,
        stock: 25,
        categoria: "Accesorios",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            marca: "Corsair",
            tipo: "Mecánico",
            switches: "Cherry MX",
            iluminacion: "RGB",
            programable: true
        }
    },
    {
        _id: "4d4d4d4d-4d4d-4d4d-4d4d-4d4d4d4d4d4d",
        codigo: "PROD-004",
        nombre: "Monitor LG 27 4K",
        precio: 399.99,
        stock: 15,
        categoria: "Monitores",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            marca: "LG",
            resolucion: "4K UHD",
            tamaño_pulgadas: 27,
            frecuencia_hz: 60,
            tiempo_respuesta_ms: 5
        }
    },
    {
        _id: "5e5e5e5e-5e5e-5e5e-5e5e-5e5e5e5e5e5e",
        codigo: "PROD-005",
        nombre: "Auriculares Sony WH-1000XM5",
        precio: 349.99,
        stock: 30,
        categoria: "Audio",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            marca: "Sony",
            tipo: "Inalámbricos",
            cancelacion_ruido: true,
            bateria_horas: 30,
            color: "Negro"
        }
    },
    {
        _id: "6f6f6f6f-6f6f-6f6f-6f6f-6f6f6f6f6f6f",
        codigo: "PROD-006",
        nombre: "Webcam Logitech C920",
        precio: 79.99,
        stock: 40,
        categoria: "Accesorios",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            marca: "Logitech",
            resolucion: "1080p Full HD",
            fps: 30,
            campo_vision: 78,
            micro_integrado: true
        }
    },
    {
        _id: "7a7a7a7a-7a7a-7a7a-7a7a-7a7a7a7a7a7a",
        codigo: "PROD-007",
        nombre: "SSD Samsung 970 EVO Plus 1TB",
        precio: 129.99,
        stock: 50,
        categoria: "Almacenamiento",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            marca: "Samsung",
            capacidad_gb: 1000,
            tipo: "NVMe M.2",
            velocidad_lectura_mbps: 7100,
            velocidad_escritura_mbps: 6000
        }
    },
    {
        _id: "8b8b8b8b-8b8b-8b8b-8b8b-8b8b8b8b8b8b",
        codigo: "PROD-008",
        nombre: "Memoria RAM Kingston DDR4 16GB",
        precio: 89.99,
        stock: 60,
        categoria: "Memoria",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            marca: "Kingston",
            capacidad_gb: 16,
            tipo: "DDR4",
            frecuencia_mhz: 3200,
            latencia: "CAS 16"
        }
    },
    {
        _id: "9c9c9c9c-9c9c-9c9c-9c9c-9c9c9c9c9c9c",
        codigo: "PROD-009",
        nombre: "Fuente de Poder Corsair 750W",
        precio: 119.99,
        stock: 20,
        categoria: "Componentes",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            marca: "Corsair",
            potencia_w: 750,
            eficiencia: "80+ Gold",
            modular: true,
            certificacion: "80 Plus Gold"
        }
    },
    {
        _id: "1d1d1d1d-1d1d-1d1d-1d1d-1d1d1d1d1d1d",
        codigo: "PROD-010",
        nombre: "Carcasa NZXT H510 Flow",
        precio: 99.99,
        stock: 35,
        categoria: "Componentes",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            marca: "NZXT",
            tipo: "ATX",
            capacidad_ventiladores: 6,
            panel_vidrio_templado: true,
            iluminacion_rgb: true
        }
    },
    {
        _id: "2e2e2e2e-2e2e-2e2e-2e2e-2e2e2e2e2e2e",
        codigo: "PROD-011",
        nombre: "Tarjeta Gráfica NVIDIA RTX 4070",
        precio: 699.99,
        stock: 8,
        categoria: "Componentes",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            marca: "NVIDIA",
            modelo: "RTX 4070",
            memoria_gb: 12,
            memoria_tipo: "GDDR6X",
            tdp_w: 200,
            arquitectura: "Ada"
        }
    },
    {
        _id: "3f3f3f3f-3f3f-3f3f-3f3f-3f3f3f3f3f3f",
        codigo: "PROD-012",
        nombre: "Cable USB-C 2.0 3 Metros",
        precio: 19.99,
        stock: 100,
        categoria: "Cables",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            tipo: "USB-C",
            longitud_m: 3,
            velocidad_transferencia_mbps: 480,
            corriente_maxima_a: 3
        }
    },
    {
        _id: "4a4a4a4a-4a4a-4a4a-4a4a-4a4a4a4a4a4a",
        codigo: "PROD-013",
        nombre: "Hub USB 3.0 7 Puertos",
        precio: 49.99,
        stock: 45,
        categoria: "Accesorios",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            marca: "Anker",
            puertos: 7,
            velocidad: "USB 3.0",
            alimentacion_externa: true,
            velocidad_transferencia_mbps: 5000
        }
    },
    {
        _id: "5b5b5b5b-5b5b-5b5b-5b5b-5b5b5b5b5b5b",
        codigo: "PROD-014",
        nombre: "Laptop Pad Refrigerador",
        precio: 39.99,
        stock: 60,
        categoria: "Accesorios",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            marca: "Cooler Master",
            tamaño_laptop_pulgadas: "hasta 17",
            ventiladores: 4,
            ruido_db: 28,
            alimentacion: "USB"
        }
    },
    {
        _id: "6c6c6c6c-6c6c-6c6c-6c6c-6c6c6c6c6c6c",
        codigo: "PROD-015",
        nombre: "Adaptador HDMI 2.1 4K@120Hz",
        precio: 29.99,
        stock: 80,
        categoria: "Cables",
        fecha_creacion: new Date(),
        activo: true,
        metadata: {
            tipo: "HDMI 2.1",
            resolucion_maxima: "4K@120Hz",
            longitud_m: 2,
            velocidad_gbps: 48,
            material_conector: "Oro"
        }
    }
]);

// Verificar datos
// db.productos.countDocuments()
// db.productos.find().pretty()
