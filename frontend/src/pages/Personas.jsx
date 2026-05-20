import { useEffect, useState } from 'react'
import { getPersonas, createPersona, updatePersona, deletePersona } from '../api'
import { Plus, Trash2, Pencil, Users, X, Check } from 'lucide-react'
import toast from 'react-hot-toast'
import Spinner from '../components/Spinner'

export default function Personas() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    nombre: '', email: '', rol: 'cliente', barrio: 'Centro', genero: 'M', estrato: 3,
  })
  const [editando, setEditando] = useState(null)
  const [editForm, setEditForm] = useState({})
  const [page, setPage] = useState(0)
  const perPage = 8

  const load = async () => {
    try {
      const { data } = await getPersonas()
      setData(data)
    } catch {
      toast.error('Error cargando personas')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.nombre || !form.email) return toast.error('Nombre y email requeridos')
    try {
      await createPersona(form)
      toast.success('Persona creada')
      setShowForm(false)
      setForm({ nombre: '', email: '', rol: 'cliente', barrio: 'Centro', genero: 'M', estrato: 3 })
      await load()
    } catch (e) {
      toast.error(e.response?.data?.error || 'Error al crear')
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('¿Eliminar esta persona?')) return
    try {
      await deletePersona(id)
      toast.success('Persona eliminada')
      await load()
    } catch {
      toast.error('Error al eliminar')
    }
  }

  const iniciarEdicion = (p) => {
    setEditando(p.id)
    setEditForm({ nombre: p.nombre, email: p.email, rol: p.rol, barrio: p.barrio, genero: p.genero, estrato: p.estrato })
  }

  const handleUpdate = async (id) => {
    if (!editForm.nombre || !editForm.email) return toast.error('Nombre y email requeridos')
    try {
      await updatePersona(id, editForm)
      toast.success('Persona actualizada')
      setEditando(null)
      await load()
    } catch (e) {
      toast.error(e.response?.data?.error || 'Error al actualizar')
    }
  }

  const pages = Math.ceil(data.length / perPage)
  const pageData = data.slice(page * perPage, (page + 1) * perPage)

  if (loading) return <div className="flex justify-center py-20"><Spinner size={28} /></div>

  return (
    <div>
      <div className="flex items-center justify-between mb-5">
        <h1 className="text-xl font-semibold flex items-center gap-2.5">
          <Users size={22} className="text-[#c084fc]" />
          Personas <span className="text-sm font-normal text-slate-400">· Cassandra</span>
        </h1>
        <button onClick={() => setShowForm((s) => !s)} className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-3.5 py-2 rounded-lg transition-all">
          <Plus size={16} /> {showForm ? 'Cancelar' : 'Nueva Persona'}
        </button>
      </div>

      {/* Form */}
      {showForm && (
        <form onSubmit={handleSubmit} className="bg-[#131c31] border border-[#1e2a45] rounded-xl p-5 mb-5">
          <h3 className="text-sm font-semibold mb-4">➕ Nueva Persona</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            <div>
              <label className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Nombre *</label>
              <input value={form.nombre} onChange={(e) => setForm((f) => ({ ...f, nombre: e.target.value }))}
                className="w-full bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm mt-1" required />
            </div>
            <div>
              <label className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Email *</label>
              <input type="email" value={form.email} onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
                className="w-full bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm mt-1" required />
            </div>
            <div>
              <label className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Rol</label>
              <select value={form.rol} onChange={(e) => setForm((f) => ({ ...f, rol: e.target.value }))}
                className="w-full bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm mt-1">
                <option value="cliente">Cliente</option>
                <option value="empleado">Empleado</option>
              </select>
            </div>
            <div>
              <label className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Barrio</label>
              <input value={form.barrio} onChange={(e) => setForm((f) => ({ ...f, barrio: e.target.value }))}
                className="w-full bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm mt-1" />
            </div>
            <div>
              <label className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Género</label>
              <select value={form.genero} onChange={(e) => setForm((f) => ({ ...f, genero: e.target.value }))}
                className="w-full bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm mt-1">
                <option value="M">Masculino</option>
                <option value="F">Femenino</option>
              </select>
            </div>
            <div>
              <label className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Estrato</label>
              <input type="number" min="1" max="6" value={form.estrato}
                onChange={(e) => setForm((f) => ({ ...f, estrato: +e.target.value }))}
                className="w-full bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm mt-1" />
            </div>
          </div>
          <div className="flex gap-2 mt-4">
            <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded-lg">💾 Guardar</button>
            <button type="button" onClick={() => setShowForm(false)} className="text-sm text-slate-400 hover:text-slate-200 px-3 py-2">Cancelar</button>
          </div>
        </form>
      )}

      {/* Table */}
      <div className="bg-[#131c31] border border-[#1e2a45] rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-[11px] text-slate-500 uppercase tracking-wider border-b border-[#1e2a45]">
                <th className="py-3 px-4 font-medium">Nombre</th>
                <th className="py-3 px-4 font-medium">Email</th>
                <th className="py-3 px-4 font-medium">Rol</th>
                <th className="py-3 px-4 font-medium">Barrio</th>
                <th className="py-3 px-4 font-medium">Género</th>
                <th className="py-3 px-4 font-medium">Estrato</th>
                <th className="py-3 px-4 font-medium"></th>
              </tr>
            </thead>
            <tbody>
              {pageData.map((p) => (
                editando === p.id ? (
                  <tr key={p.id} className="border-b border-[#1e2a45]/50 bg-blue-900/10">
                    <td className="py-2 px-4">
                      <input value={editForm.nombre} onChange={(e) => setEditForm((f) => ({ ...f, nombre: e.target.value }))}
                        className="w-full bg-[#0b1121] border border-[#1e2a45] rounded px-2 py-1 text-sm" />
                    </td>
                    <td className="py-2 px-4">
                      <input value={editForm.email} onChange={(e) => setEditForm((f) => ({ ...f, email: e.target.value }))}
                        className="w-full bg-[#0b1121] border border-[#1e2a45] rounded px-2 py-1 text-sm" />
                    </td>
                    <td className="py-2 px-4">
                      <select value={editForm.rol} onChange={(e) => setEditForm((f) => ({ ...f, rol: e.target.value }))}
                        className="bg-[#0b1121] border border-[#1e2a45] rounded px-2 py-1 text-sm">
                        <option value="cliente">Cliente</option>
                        <option value="empleado">Empleado</option>
                      </select>
                    </td>
                    <td className="py-2 px-4">
                      <input value={editForm.barrio} onChange={(e) => setEditForm((f) => ({ ...f, barrio: e.target.value }))}
                        className="w-full bg-[#0b1121] border border-[#1e2a45] rounded px-2 py-1 text-sm" />
                    </td>
                    <td className="py-2 px-4">
                      <select value={editForm.genero} onChange={(e) => setEditForm((f) => ({ ...f, genero: e.target.value }))}
                        className="bg-[#0b1121] border border-[#1e2a45] rounded px-2 py-1 text-sm">
                        <option value="M">M</option>
                        <option value="F">F</option>
                      </select>
                    </td>
                    <td className="py-2 px-4">
                      <input type="number" min="1" max="6" value={editForm.estrato}
                        onChange={(e) => setEditForm((f) => ({ ...f, estrato: +e.target.value }))}
                        className="w-16 bg-[#0b1121] border border-[#1e2a45] rounded px-2 py-1 text-sm" />
                    </td>
                    <td className="py-2 px-4">
                      <div className="flex gap-1">
                        <button onClick={() => handleUpdate(p.id)}
                          className="text-green-400 hover:text-green-300 transition-colors p-1">
                          <Check size={14} />
                        </button>
                        <button onClick={() => setEditando(null)}
                          className="text-slate-400 hover:text-slate-300 transition-colors p-1">
                          <X size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ) : (
                  <tr key={p.id} className="border-b border-[#1e2a45]/50 hover:bg-white/[.02]">
                    <td className="py-2.5 px-4">{p.nombre}</td>
                    <td className="py-2.5 px-4 text-slate-400 text-xs">{p.email}</td>
                    <td className="py-2.5 px-4">
                      <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                        p.rol === 'cliente' ? 'bg-green-900/40 text-green-400' : 'bg-orange-900/40 text-orange-400'
                      }`}>{p.rol}</span>
                    </td>
                    <td className="py-2.5 px-4">{p.barrio}</td>
                    <td className="py-2.5 px-4">{p.genero}</td>
                    <td className="py-2.5 px-4">{p.estrato}</td>
                    <td className="py-2.5 px-4">
                      <div className="flex gap-1">
                        <button onClick={() => iniciarEdicion(p)} className="text-blue-400 hover:text-blue-300 transition-colors p-1">
                          <Pencil size={14} />
                        </button>
                        <button onClick={() => handleDelete(p.id)} className="text-red-400 hover:text-red-300 transition-colors p-1">
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                )
              ))}
              {!pageData.length && (
                <tr><td colSpan={7} className="py-10 text-center text-slate-500">No hay personas registradas</td></tr>
              )}
            </tbody>
          </table>
        </div>
        {/* Pagination */}
        {pages > 1 && (
          <div className="flex items-center justify-center gap-1 py-3 border-t border-[#1e2a45]">
            {Array.from({ length: pages }).map((_, i) => (
              <button key={i} onClick={() => setPage(i)}
                className={`w-7 h-7 rounded text-xs font-medium transition-all ${
                  page === i ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-white/5'
                }`}>{i + 1}</button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
