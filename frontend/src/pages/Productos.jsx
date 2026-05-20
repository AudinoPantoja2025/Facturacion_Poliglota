import { useEffect, useState } from 'react'
import { getProductos, createProducto, updateProducto, deleteProducto } from '../api'
import { Plus, Trash2, Pencil, Package, Search, X, Check } from 'lucide-react'
import toast from 'react-hot-toast'
import Spinner from '../components/Spinner'

export default function Productos() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editando, setEditando] = useState(null)
  const [editForm, setEditForm] = useState({})
  const [search, setSearch] = useState('')
  const [catFilter, setCatFilter] = useState('')
  const [form, setForm] = useState({
    nombre: '', codigo: '', precio: '', stock: 10, categoria: 'General',
  })

  const load = async () => {
    try {
      const { data } = await getProductos()
      setData(data)
    } catch {
      toast.error('Error cargando productos')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.nombre || !form.codigo || !form.precio) return toast.error('Nombre, código y precio requeridos')
    try {
      await createProducto({ ...form, precio: parseFloat(form.precio), stock: +form.stock })
      toast.success('Producto creado')
      setShowForm(false)
      setForm({ nombre: '', codigo: '', precio: '', stock: 10, categoria: 'General' })
      await load()
    } catch (e) {
      toast.error(e.response?.data?.error || 'Error al crear')
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('¿Eliminar este producto?')) return
    try {
      await deleteProducto(id)
      toast.success('Producto eliminado')
      await load()
    } catch {
      toast.error('Error al eliminar')
    }
  }

  const iniciarEdicion = (p) => {
    setEditando(p.id)
    setEditForm({ nombre: p.nombre, codigo: p.codigo, precio: p.precio, stock: p.stock, categoria: p.categoria })
  }

  const handleUpdate = async (id) => {
    if (!editForm.nombre || !editForm.codigo || !editForm.precio) return toast.error('Nombre, código y precio requeridos')
    try {
      await updateProducto(id, { ...editForm, precio: parseFloat(editForm.precio), stock: +editForm.stock })
      toast.success('Producto actualizado')
      setEditando(null)
      await load()
    } catch (e) {
      toast.error(e.response?.data?.error || 'Error al actualizar')
    }
  }

  const categorias = [...new Set(data.map((p) => p.categoria))]
  const filtered = data.filter((p) => {
    const q = search.toLowerCase()
    return (p.nombre.toLowerCase().includes(q) || p.codigo.toLowerCase().includes(q)) &&
      (!catFilter || p.categoria === catFilter)
  })

  if (loading) return <div className="flex justify-center py-20"><Spinner size={28} /></div>

  return (
    <div>
      <div className="flex items-center justify-between mb-5">
        <h1 className="text-xl font-semibold flex items-center gap-2.5">
          <Package size={22} className="text-[#4ade80]" />
          Productos <span className="text-sm font-normal text-slate-400">· MongoDB</span>
        </h1>
        <button onClick={() => setShowForm((s) => !s)} className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-3.5 py-2 rounded-lg transition-all">
          <Plus size={16} /> {showForm ? 'Cancelar' : 'Nuevo Producto'}
        </button>
      </div>

      {/* Form */}
      {showForm && (
        <form onSubmit={handleSubmit} className="bg-[#131c31] border border-[#1e2a45] rounded-xl p-5 mb-5">
          <h3 className="text-sm font-semibold mb-4">➕ Nuevo Producto</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            <div>
              <label className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Nombre *</label>
              <input value={form.nombre} onChange={(e) => setForm((f) => ({ ...f, nombre: e.target.value }))}
                className="w-full bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm mt-1" required />
            </div>
            <div>
              <label className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Código *</label>
              <input value={form.codigo} onChange={(e) => setForm((f) => ({ ...f, codigo: e.target.value }))}
                className="w-full bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm mt-1" required />
            </div>
            <div>
              <label className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Precio *</label>
              <input type="number" step="0.01" min="0" value={form.precio}
                onChange={(e) => setForm((f) => ({ ...f, precio: e.target.value }))}
                className="w-full bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm mt-1" required />
            </div>
            <div>
              <label className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Stock</label>
              <input type="number" min="0" value={form.stock}
                onChange={(e) => setForm((f) => ({ ...f, stock: +e.target.value }))}
                className="w-full bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm mt-1" />
            </div>
            <div>
              <label className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Categoría</label>
              <input value={form.categoria} onChange={(e) => setForm((f) => ({ ...f, categoria: e.target.value }))}
                className="w-full bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm mt-1" />
            </div>
          </div>
          <div className="flex gap-2 mt-4">
            <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded-lg">💾 Guardar</button>
            <button type="button" onClick={() => setShowForm(false)} className="text-sm text-slate-400 hover:text-slate-200 px-3 py-2">Cancelar</button>
          </div>
        </form>
      )}

      {/* Search & Filter */}
      <div className="flex items-center gap-3 mb-4 flex-wrap">
        <div className="relative flex-1 max-w-xs">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input placeholder="Buscar productos..." value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-[#0b1121] border border-[#1e2a45] rounded-lg pl-9 pr-3 py-2 text-sm" />
        </div>
        <select value={catFilter} onChange={(e) => setCatFilter(e.target.value)}
          className="bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm">
          <option value="">Todas las categorías</option>
          {categorias.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
        <span className="text-xs text-slate-500">{filtered.length} productos</span>
      </div>

      {/* Product Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
        {filtered.map((p) => {
          if (editando === p.id) {
            return (
              <div key={p.id} className="bg-[#131c31] border border-blue-500/50 rounded-xl p-4">
                <div className="space-y-2">
                  <input value={editForm.nombre} onChange={(e) => setEditForm((f) => ({ ...f, nombre: e.target.value }))}
                    placeholder="Nombre" className="w-full bg-[#0b1121] border border-[#1e2a45] rounded px-2 py-1 text-sm" />
                  <input value={editForm.codigo} onChange={(e) => setEditForm((f) => ({ ...f, codigo: e.target.value }))}
                    placeholder="Código" className="w-full bg-[#0b1121] border border-[#1e2a45] rounded px-2 py-1 text-sm" />
                  <div className="flex gap-2">
                    <input type="number" step="0.01" min="0" value={editForm.precio}
                      onChange={(e) => setEditForm((f) => ({ ...f, precio: e.target.value }))}
                      placeholder="Precio" className="flex-1 bg-[#0b1121] border border-[#1e2a45] rounded px-2 py-1 text-sm" />
                    <input type="number" min="0" value={editForm.stock}
                      onChange={(e) => setEditForm((f) => ({ ...f, stock: +e.target.value }))}
                      placeholder="Stock" className="w-20 bg-[#0b1121] border border-[#1e2a45] rounded px-2 py-1 text-sm" />
                  </div>
                  <input value={editForm.categoria} onChange={(e) => setEditForm((f) => ({ ...f, categoria: e.target.value }))}
                    placeholder="Categoría" className="w-full bg-[#0b1121] border border-[#1e2a45] rounded px-2 py-1 text-sm" />
                  <div className="flex gap-2 pt-1">
                    <button onClick={() => handleUpdate(p.id)}
                      className="flex-1 bg-green-600 hover:bg-green-700 text-white text-sm font-medium py-1.5 rounded-lg flex items-center justify-center gap-1">
                      <Check size={14} /> Guardar
                    </button>
                    <button onClick={() => setEditando(null)}
                      className="flex-1 bg-slate-700 hover:bg-slate-600 text-white text-sm py-1.5 rounded-lg flex items-center justify-center gap-1">
                      <X size={14} /> Cancelar
                    </button>
                  </div>
                </div>
              </div>
            )
          }
          const lowStock = p.stock <= 5
          const criticalStock = p.stock === 0
          return (
            <div key={p.id} className="bg-[#131c31] border border-[#1e2a45] rounded-xl p-4 hover:border-blue-500/30 transition-all group">
              <div className="flex items-start justify-between mb-2">
                <div className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                  criticalStock ? 'bg-red-900/40 text-red-400' : lowStock ? 'bg-yellow-900/40 text-yellow-400' : 'bg-green-900/40 text-green-400'
                }`}>
                  {criticalStock ? 'Sin stock' : lowStock ? 'Stock bajo' : 'Disponible'}
                </div>
                <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-all">
                  <button onClick={() => iniciarEdicion(p)} className="text-blue-400/50 hover:text-blue-400 p-1">
                    <Pencil size={13} />
                  </button>
                  <button onClick={() => handleDelete(p.id)} className="text-red-400/50 hover:text-red-400 p-1">
                    <Trash2 size={13} />
                  </button>
                </div>
              </div>
              <h3 className="font-semibold text-sm mb-1">{p.nombre}</h3>
              <p className="text-xs text-slate-500 mb-2">{p.codigo}</p>
              <div className="flex items-center justify-between">
                <span className="text-lg font-bold text-[#4ade80]">${p.precio?.toFixed(2)}</span>
                <span className={`text-xs ${criticalStock ? 'text-red-400' : lowStock ? 'text-yellow-400' : 'text-slate-400'}`}>
                  Stock: {p.stock}
                </span>
              </div>
              <div className="text-[11px] text-slate-500 mt-1.5">{p.categoria}</div>
            </div>
          )
        })}
        {!filtered.length && (
          <div className="col-span-full py-12 text-center text-slate-500">
            {search ? 'Sin resultados para tu búsqueda' : 'No hay productos registrados'}
          </div>
        )}
      </div>
    </div>
  )
}
