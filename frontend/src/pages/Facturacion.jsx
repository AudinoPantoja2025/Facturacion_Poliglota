import { useEffect, useState, useMemo } from 'react'
import { getPersonas, getProductos, createFactura, getFacturas, getFacturaById } from '../api'
import { Search, Plus, Trash2, Receipt, Minus, ShoppingCart, Eye, X } from 'lucide-react'
import toast from 'react-hot-toast'
import Spinner from '../components/Spinner'

export default function Facturacion() {
  const [personas, setPersonas] = useState([])
  const [productos, setProductos] = useState([])
  const [facturas, setFacturas] = useState([])
  const [loading, setLoading] = useState(true)
  const [clienteId, setClienteId] = useState('')
  const [numFactura, setNumFactura] = useState('')
  const [carrito, setCarrito] = useState([])
  const [searchProd, setSearchProd] = useState('')
  const [buscando, setBuscando] = useState(false)
  const [detalleModal, setDetalleModal] = useState(null)
  const [cargandoDetalle, setCargandoDetalle] = useState(false)

  const load = async () => {
    try {
      const [per, pro, fac] = await Promise.all([
        getPersonas().then((r) => r.data),
        getProductos().then((r) => r.data),
        getFacturas().then((r) => r.data),
      ])
      setPersonas(per)
      setProductos(pro)
      setFacturas(fac)
    } catch {
      toast.error('Error cargando datos')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const prodFiltrados = useMemo(
    () => productos.filter((p) => {
      const q = searchProd.toLowerCase()
      return !q || p.nombre.toLowerCase().includes(q) || p.codigo.toLowerCase().includes(q)
    }),
    [productos, searchProd],
  )

  const agregar = (p) => {
    setCarrito((prev) => {
      const idx = prev.findIndex((i) => i.id === p.id)
      if (idx >= 0) {
        const next = [...prev]
        next[idx] = { ...next[idx], cantidad: next[idx].cantidad + 1 }
        return next
      }
      return [...prev, { id: p.id, nombre: p.nombre, precio: p.precio, cantidad: 1, stock: p.stock }]
    })
  }

  const cambiarCant = (id, delta) => {
    setCarrito((prev) => {
      const next = prev.map((i) => i.id === id ? { ...i, cantidad: Math.max(1, i.cantidad + delta) } : i)
      return next.filter((i) => i.cantidad > 0)
    })
  }

  const quitar = (id) => setCarrito((prev) => prev.filter((i) => i.id !== id))

  const subtotal = carrito.reduce((s, i) => s + i.precio * i.cantidad, 0)
  const iva = subtotal * 0.19
  const total = subtotal + iva
  const nFactura = useMemo(() => {
    if (numFactura) return numFactura
    const count = facturas.length + 1
    const now = new Date()
    return `FAC-${now.getFullYear()}-${String(count).padStart(3, '0')}`
  }, [numFactura, facturas.length])

  const procesar = async () => {
    if (!clienteId) return toast.error('Selecciona un cliente')
    if (!carrito.length) return toast.error('Agrega productos al carrito')
    setBuscando(true)
    try {
      const res = await createFactura({
        cliente_id: clienteId,
        numero_factura: nFactura,
        items: carrito.map((i) => ({ producto_id: i.id, cantidad: i.cantidad })),
      })
      toast.success(`Factura ${res.data.numero} creada — Total: $${res.data.total.toFixed(2)}`)
      setCarrito([])
      setClienteId('')
      setNumFactura('')
      const { data } = await getFacturas()
      setFacturas(data)
    } catch (e) {
      toast.error(e.response?.data?.error || 'Error al crear factura')
    } finally {
      setBuscando(false)
    }
  }

  const verDetalle = async (id) => {
    setCargandoDetalle(true)
    setDetalleModal(null)
    try {
      const { data } = await getFacturaById(id)
      setDetalleModal(data)
    } catch {
      toast.error('Error cargando detalle de factura')
    } finally {
      setCargandoDetalle(false)
    }
  }

  if (loading) return <div className="flex justify-center py-20"><Spinner size={28} /></div>

  return (
    <div>
      <h1 className="text-xl font-semibold mb-5 flex items-center gap-2.5">
        <Receipt size={22} className="text-orange-400" />
        Facturación <span className="text-sm font-normal text-slate-400">· MySQL · Punto de Venta</span>
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* LEFT: Productos */}
        <div className="lg:col-span-2 space-y-4">
          {/* Select Cliente */}
          <div className="bg-[#131c31] border border-[#1e2a45] rounded-xl p-4">
            <label className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Cliente</label>
            <div className="flex gap-2 mt-1">
              <select value={clienteId} onChange={(e) => setClienteId(e.target.value)}
                className="flex-1 bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm">
                <option value="">Seleccionar cliente...</option>
                {personas.filter((p) => p.rol === 'cliente').map((p) => (
                  <option key={p.id} value={p.id}>{p.nombre} — {p.barrio}</option>
                ))}
              </select>
              <input placeholder="N° Factura" value={numFactura} onChange={(e) => setNumFactura(e.target.value)}
                className="w-44 bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm" />
            </div>
          </div>

          {/* Buscador */}
          <div className="relative">
            <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <input placeholder="Buscar productos por nombre o código..." value={searchProd}
              onChange={(e) => setSearchProd(e.target.value)}
              className="w-full bg-[#0b1121] border border-[#1e2a45] rounded-xl pl-10 pr-4 py-3 text-sm" />
          </div>

          {/* Grid productos */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 max-h-[420px] overflow-y-auto pr-1">
            {prodFiltrados.map((p) => {
              const enCarrito = carrito.find((i) => i.id === p.id)
              return (
                <button key={p.id} onClick={() => agregar(p)}
                  className="bg-[#131c31] border border-[#1e2a45] rounded-xl p-3 text-left hover:border-blue-500/40 transition-all text-sm group">
                  <div className="font-semibold text-sm truncate">{p.nombre}</div>
                  <div className="text-[#4ade80] font-bold mt-1">${p.precio.toFixed(2)}</div>
                  <div className="flex items-center justify-between mt-1.5">
                    <span className={`text-[11px] ${p.stock <= 5 ? 'text-yellow-400' : 'text-slate-500'}`}>
                      Stock: {p.stock}
                    </span>
                    {enCarrito && (
                      <span className="text-[11px] bg-blue-600/20 text-blue-400 px-1.5 py-0.5 rounded">
                        {enCarrito.cantidad} en carrito
                      </span>
                    )}
                  </div>
                </button>
              )
            })}
            {!prodFiltrados.length && (
              <div className="col-span-full py-8 text-center text-slate-500 text-sm">
                {searchProd ? 'Sin resultados' : 'No hay productos'}
              </div>
            )}
          </div>
        </div>

        {/* RIGHT: Carrito */}
        <div className="bg-[#131c31] border border-[#1e2a45] rounded-xl flex flex-col">
          <div className="px-4 py-3 border-b border-[#1e2a45] flex items-center gap-2 text-sm font-semibold">
            <ShoppingCart size={16} /> Carrito {carrito.length > 0 && `(${carrito.length})`}
          </div>
          <div className="flex-1 overflow-y-auto max-h-[340px] p-2 space-y-1.5">
            {carrito.map((item) => (
              <div key={item.id} className="bg-[#0b1121] rounded-lg p-2.5 text-sm">
                <div className="flex items-center justify-between">
                  <span className="font-medium truncate flex-1">{item.nombre}</span>
                  <button onClick={() => quitar(item.id)} className="text-red-400/60 hover:text-red-400 ml-2">
                    <Trash2 size={13} />
                  </button>
                </div>
                <div className="flex items-center justify-between mt-1.5">
                  <div className="flex items-center gap-1.5">
                    <button onClick={() => cambiarCant(item.id, -1)}
                      className="w-6 h-6 rounded bg-[#1e2a45] hover:bg-[#2a3a5a] flex items-center justify-center transition-colors">
                      <Minus size={12} />
                    </button>
                    <span className="w-6 text-center font-medium text-sm">{item.cantidad}</span>
                    <button onClick={() => cambiarCant(item.id, 1)}
                      className="w-6 h-6 rounded bg-[#1e2a45] hover:bg-[#2a3a5a] flex items-center justify-center transition-colors">
                      <Plus size={12} />
                    </button>
                  </div>
                  <span className="font-semibold">${(item.precio * item.cantidad).toFixed(2)}</span>
                </div>
              </div>
            ))}
            {!carrito.length && (
              <div className="py-8 text-center text-slate-500 text-sm">Carrito vacío</div>
            )}
          </div>
          {/* Totals */}
          <div className="border-t border-[#1e2a45] p-4 space-y-1.5 text-sm">
            <div className="flex justify-between text-slate-400">
              <span>Subtotal</span>
              <span>${subtotal.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>IVA (19%)</span>
              <span>${iva.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-base font-bold pt-1.5 border-t border-[#1e2a45]">
              <span>Total</span>
              <span className="text-[#4ade80]">${total.toFixed(2)}</span>
            </div>
            <button onClick={procesar} disabled={buscando || !carrito.length}
              className="w-full mt-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold py-2.5 rounded-lg text-sm transition-all flex items-center justify-center gap-2">
              {buscando ? <Spinner size={16} /> : '🚀 Procesar Factura'}
            </button>
          </div>
        </div>
      </div>

      {/* Invoice History */}
      <div className="bg-[#131c31] border border-[#1e2a45] rounded-xl overflow-hidden mt-5">
        <div className="px-5 py-3 border-b border-[#1e2a45] flex items-center gap-2 text-sm font-semibold">
          <Receipt size={16} className="text-orange-400" /> Historial de Facturas
        </div>
        <div className="overflow-x-auto max-h-[260px] overflow-y-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-[11px] text-slate-500 uppercase tracking-wider border-b border-[#1e2a45]">
                <th className="py-2.5 px-4 font-medium">#</th>
                <th className="py-2.5 px-4 font-medium">Fecha</th>
                <th className="py-2.5 px-4 font-medium">Total</th>
                <th className="py-2.5 px-4 font-medium">Items</th>
                <th className="py-2.5 px-4 font-medium">Estado</th>
                <th className="py-2.5 px-4 font-medium"></th>
              </tr>
            </thead>
            <tbody>
              {facturas.slice().reverse().map((f) => (
                <tr key={f.id} className="border-b border-[#1e2a45]/50 hover:bg-white/[.02]">
                  <td className="py-2 px-4">{f.numero}</td>
                  <td className="py-2 px-4 text-xs text-slate-400">{f.fecha?.substring(0, 19).replace('T', ' ')}</td>
                  <td className="py-2 px-4">${f.total?.toFixed(2)}</td>
                  <td className="py-2 px-4 text-slate-400">{f.items}</td>
                  <td className="py-2 px-4">
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                      f.estado === 'completada' ? 'bg-green-900/40 text-green-400' : 'bg-yellow-900/40 text-yellow-400'
                    }`}>{f.estado}</span>
                  </td>
                  <td className="py-2 px-4">
                    <button onClick={() => verDetalle(f.id)}
                      className="text-blue-400 hover:text-blue-300 transition-colors p-1" title="Ver detalle">
                      <Eye size={14} />
                    </button>
                  </td>
                </tr>
              ))}
              {!facturas.length && (
                <tr><td colSpan={6} className="py-8 text-center text-slate-500">Sin facturas</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal Detalle Factura */}
      {detalleModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
          <div className="bg-[#131c31] border border-[#1e2a45] rounded-xl w-full max-w-lg mx-4 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between px-5 py-3 border-b border-[#1e2a45]">
              <h3 className="text-sm font-semibold flex items-center gap-2">
                <Receipt size={16} className="text-orange-400" />
                Factura {detalleModal.numero}
              </h3>
              <button onClick={() => setDetalleModal(null)} className="text-slate-400 hover:text-slate-200 p-1">
                <X size={16} />
              </button>
            </div>
            <div className="p-5 space-y-3">
              <div className="flex justify-between text-sm text-slate-400">
                <span>Fecha: {detalleModal.fecha?.substring(0, 19).replace('T', ' ')}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                  detalleModal.estado === 'completada' ? 'bg-green-900/40 text-green-400' : 'bg-yellow-900/40 text-yellow-400'
                }`}>{detalleModal.estado}</span>
              </div>
              <div className="text-sm text-slate-400">
                Cliente: <span className="text-white font-medium">{detalleModal.cliente_nombre}</span>
              </div>
              <div className="border-t border-[#1e2a45] pt-3">
                <h4 className="text-[11px] text-slate-500 uppercase tracking-wider font-semibold mb-2">Detalles</h4>
                {detalleModal.detalles?.length > 0 ? (
                  <div className="space-y-2">
                    {detalleModal.detalles.map((d, i) => (
                      <div key={d.id} className="flex items-center justify-between bg-[#0b1121] rounded-lg px-3 py-2 text-sm">
                        <div className="flex-1 min-w-0">
                          <span className="text-slate-400 text-xs mr-2">#{i + 1}</span>
                          <span className="text-sm truncate">{d.producto_nombre || d.producto_id?.substring(0, 8)}</span>
                        </div>
                        <div className="flex items-center gap-4 flex-shrink-0">
                          <span className="text-slate-400">{d.cantidad} x ${d.precio_unitario?.toFixed(2)}</span>
                          <span className="font-semibold text-[#4ade80]">${d.subtotal?.toFixed(2)}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-slate-500">Cargando detalles...</p>
                )}
              </div>
              <div className="border-t border-[#1e2a45] pt-3 flex justify-between text-sm font-bold">
                <span>Total</span>
                <span className="text-[#4ade80]">${detalleModal.total?.toFixed(2)}</span>
              </div>
            </div>
            <div className="px-5 py-3 border-t border-[#1e2a45] flex justify-end">
              <button onClick={() => setDetalleModal(null)}
                className="bg-slate-700 hover:bg-slate-600 text-white text-sm font-medium px-4 py-2 rounded-lg">
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
