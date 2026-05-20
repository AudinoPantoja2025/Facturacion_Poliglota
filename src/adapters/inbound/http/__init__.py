"""HTTP Controllers - Flask blueprints."""

from flask import Blueprint, request, jsonify
from uuid import UUID, uuid4
from datetime import datetime
import logging

from src.domain.entities import Persona, Rol, Producto
from src.usecases.factura import CrearFacturaUseCase, ObtenerRecomendacionesUseCase

logger = logging.getLogger(__name__)

# Blueprints
factura_bp = Blueprint('facturacion', __name__, url_prefix='/api/v1/facturas')
data_bp = Blueprint('datos', __name__, url_prefix='/api/v1/datos')


class FacturaController:
    """Controlador para operaciones de facturación."""

    def __init__(
        self,
        crear_factura_usecase: CrearFacturaUseCase,
        obtener_recomendaciones_usecase: ObtenerRecomendacionesUseCase,
        persona_adapter=None,
        producto_adapter=None,
        factura_adapter=None,
        recomendacion_adapter=None
    ):
        self.crear_factura_usecase = crear_factura_usecase
        self.obtener_recomendaciones_usecase = obtener_recomendaciones_usecase
        self.persona_adapter = persona_adapter
        self.producto_adapter = producto_adapter
        self.factura_adapter = factura_adapter
        self.recomendacion_adapter = recomendacion_adapter

    async def crear_factura(self):
        """POST /api/v1/facturas"""
        try:
            datos = request.get_json()
            cliente_id = UUID(datos["cliente_id"])
            numero_factura = datos["numero_factura"]
            items = datos["items"]
            factura = await self.crear_factura_usecase.ejecutar(cliente_id, numero_factura, items)
            if not factura:
                return jsonify({"error": "Error creando factura"}), 400
            return jsonify({
                "id": str(factura.id), "numero": factura.numero,
                "cliente_id": str(factura.cliente_id), "total": factura.total,
                "estado": factura.estado, "items": len(factura.detalles)
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error en controlador: {e}")
            return jsonify({"error": "Error interno del servidor"}), 500

    async def obtener_recomendaciones(self, cliente_id: str):
        if not self.obtener_recomendaciones_usecase:
            return jsonify({"warning": "Neo4j no disponible", "recomendaciones": []}), 200
        try:
            cliente_uuid = UUID(cliente_id)
            limite = request.args.get("limite", 5, type=int)
            recs = await self.obtener_recomendaciones_usecase.ejecutar(cliente_uuid, limite)
            return jsonify({"cliente_id": cliente_id, "recomendaciones": recs}), 200
        except ValueError:
            return jsonify({"error": "ID de cliente inválido"}), 400
        except Exception as e:
            return jsonify({"error": "Error interno del servidor"}), 500

    # ─── PERSONAS ────────────────────────────────────────────────

    async def listar_personas(self):
        if not self.persona_adapter:
            return jsonify([]), 200
        try:
            data = await self.persona_adapter.listar_todos()
            return jsonify([{
                "id": str(p.id), "nombre": p.nombre, "email": p.email,
                "rol": p.rol.value, "ciudad": p.ciudad, "barrio": p.barrio,
                "genero": p.genero, "estrato": p.estrato
            } for p in data]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    async def crear_persona(self):
        if not self.persona_adapter:
            return jsonify({"error": "Cassandra no disponible"}), 503
        try:
            d = request.get_json()
            persona = Persona(
                id=uuid4(), nombre=d["nombre"], email=d["email"],
                rol=Rol(d.get("rol", "cliente")), ciudad=d.get("ciudad", "Putumayo"),
                barrio=d.get("barrio", "Centro"), genero=d.get("genero", "M"),
                estrato=int(d.get("estrato", 3)), fecha_creacion=datetime.now(), activo=True
            )
            creada = await self.persona_adapter.crear(persona)
            if self.recomendacion_adapter and persona.es_cliente():
                await self.recomendacion_adapter.crear_cliente(
                    creada.id, creada.nombre, creada.barrio, creada.genero, creada.estrato
                )
            return jsonify({"id": str(creada.id), "nombre": creada.nombre}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    async def actualizar_persona(self, persona_id: str):
        if not self.persona_adapter:
            return jsonify({"error": "Cassandra no disponible"}), 503
        try:
            d = request.get_json()
            persona = Persona(
                id=UUID(persona_id), nombre=d["nombre"], email=d["email"],
                rol=Rol(d.get("rol", "cliente")), ciudad=d.get("ciudad", "Putumayo"),
                barrio=d.get("barrio", "Centro"), genero=d.get("genero", "M"),
                estrato=int(d.get("estrato", 3)), fecha_creacion=datetime.now(), activo=True
            )
            actualizada = await self.persona_adapter.actualizar(persona)
            return jsonify({"id": str(actualizada.id), "nombre": actualizada.nombre}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    async def eliminar_persona(self, persona_id: str):
        if not self.persona_adapter:
            return jsonify({"error": "Cassandra no disponible"}), 503
        try:
            ok = await self.persona_adapter.eliminar(UUID(persona_id))
            return jsonify({"ok": ok}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # ─── PRODUCTOS ──────────────────────────────────────────────

    async def listar_productos(self):
        if not self.producto_adapter:
            return jsonify([]), 200
        try:
            data = await self.producto_adapter.listar_todos()
            return jsonify([{
                "id": str(p.id), "codigo": p.codigo, "nombre": p.nombre,
                "precio": p.precio, "stock": p.stock, "categoria": p.categoria
            } for p in data]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    async def crear_producto(self):
        if not self.producto_adapter:
            return jsonify({"error": "MongoDB no disponible"}), 503
        try:
            d = request.get_json()
            producto = Producto(
                id=uuid4(), codigo=d["codigo"], nombre=d["nombre"],
                precio=float(d["precio"]), stock=int(d.get("stock", 0)),
                categoria=d.get("categoria", "General"),
                fecha_creacion=datetime.now(), metadata=d.get("metadata", {}), activo=True
            )
            creado = await self.producto_adapter.crear(producto)
            if self.recomendacion_adapter:
                await self.recomendacion_adapter.crear_producto(
                    creado.id, creado.nombre, creado.categoria
                )
            return jsonify({"id": str(creado.id), "nombre": creado.nombre}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    async def actualizar_producto(self, producto_id: str):
        if not self.producto_adapter:
            return jsonify({"error": "MongoDB no disponible"}), 503
        try:
            d = request.get_json()
            producto = Producto(
                id=UUID(producto_id), codigo=d["codigo"], nombre=d["nombre"],
                precio=float(d["precio"]), stock=int(d.get("stock", 0)),
                categoria=d.get("categoria", "General"),
                fecha_creacion=datetime.now(), metadata=d.get("metadata", {}), activo=True
            )
            actualizado = await self.producto_adapter.actualizar(producto)
            return jsonify({"id": str(actualizado.id), "nombre": actualizado.nombre}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    async def eliminar_producto(self, producto_id: str):
        if not self.producto_adapter:
            return jsonify({"error": "MongoDB no disponible"}), 503
        try:
            ok = await self.producto_adapter.eliminar(UUID(producto_id))
            return jsonify({"ok": ok}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # ─── FACTURAS ───────────────────────────────────────────────

    async def listar_facturas(self):
        if not self.factura_adapter:
            return jsonify([]), 200
        try:
            data = await self.factura_adapter.listar_todas()
            return jsonify([{
                "id": str(f.id), "numero": f.numero, "fecha": str(f.fecha),
                "cliente_id": str(f.cliente_id), "total": f.total,
                "estado": f.estado, "items": getattr(f, 'items', len(f.detalles))
            } for f in data]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    async def obtener_factura_por_id(self, factura_id: str):
        if not self.factura_adapter:
            return jsonify({"error": "MySQL no disponible"}), 503
        try:
            f = await self.factura_adapter.obtener_por_id(UUID(factura_id))
            if not f:
                return jsonify({"error": "Factura no encontrada"}), 404
            cliente_nombre = str(f.cliente_id)
            if self.persona_adapter:
                p = await self.persona_adapter.obtener_por_id(f.cliente_id)
                if p:
                    cliente_nombre = p.nombre
            detalles = []
            for d in f.detalles:
                prod_nombre = d.producto_id
                if self.producto_adapter:
                    prod = await self.producto_adapter.obtener_por_id(d.producto_id)
                    if prod:
                        prod_nombre = prod.nombre
                detalles.append({
                    "id": str(d.id), "producto_id": str(d.producto_id),
                    "producto_nombre": prod_nombre,
                    "cantidad": d.cantidad, "precio_unitario": d.precio_unitario,
                    "subtotal": d.subtotal
                })
            return jsonify({
                "id": str(f.id), "numero": f.numero, "fecha": str(f.fecha),
                "cliente_id": str(f.cliente_id), "cliente_nombre": cliente_nombre,
                "total": f.total, "estado": f.estado,
                "detalles": detalles
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


def crear_rutas_factura(controller: FacturaController):
    """Crea las rutas Flask para facturación."""
    
    @factura_bp.route("", methods=["POST"])
    async def crear():
        return await controller.crear_factura()
    
    @factura_bp.route("/recomendaciones/<cliente_id>", methods=["GET"])
    async def recomendaciones(cliente_id):
        return await controller.obtener_recomendaciones(cliente_id)
    
    return factura_bp


def crear_rutas_datos(controller: FacturaController):
    """Crea las rutas Flask para datos de las BDs."""

    @data_bp.route("/personas", methods=["GET"])
    async def listar_personas():
        return await controller.listar_personas()

    @data_bp.route("/personas", methods=["POST"])
    async def crear_persona():
        return await controller.crear_persona()

    @data_bp.route("/personas/<persona_id>", methods=["DELETE"])
    async def eliminar_persona(persona_id):
        return await controller.eliminar_persona(persona_id)

    @data_bp.route("/personas/<persona_id>", methods=["PUT"])
    async def actualizar_persona(persona_id):
        return await controller.actualizar_persona(persona_id)

    @data_bp.route("/productos", methods=["GET"])
    async def listar_productos():
        return await controller.listar_productos()

    @data_bp.route("/productos", methods=["POST"])
    async def crear_producto():
        return await controller.crear_producto()

    @data_bp.route("/productos/<producto_id>", methods=["DELETE"])
    async def eliminar_producto(producto_id):
        return await controller.eliminar_producto(producto_id)

    @data_bp.route("/productos/<producto_id>", methods=["PUT"])
    async def actualizar_producto(producto_id):
        return await controller.actualizar_producto(producto_id)

    @data_bp.route("/facturas", methods=["GET"])
    async def listar_facturas():
        return await controller.listar_facturas()

    @data_bp.route("/facturas/<factura_id>", methods=["GET"])
    async def obtener_factura(factura_id):
        return await controller.obtener_factura_por_id(factura_id)

    return data_bp
