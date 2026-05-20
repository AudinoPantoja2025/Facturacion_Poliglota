import { useEffect, useState } from 'react'
import {
  getPersonas, getProductos, getFacturas, healthApi,
} from '../api'
import Spinner from '../components/Spinner'
import { Database, Users, Package, Receipt, ArrowRight } from 'lucide-react'

const flow = [
  { step: 1, icon: '👤', title: 'Validar Cliente', db: 'Cassandra' },
  { step: 2, icon: '📦', title: 'Obtener Productos', db: 'MongoDB' },
  { step: 3, icon: '📉', title: 'Descontar Stock', db: 'MongoDB' },
  { step: 4, icon: '📄', title: 'Crear Factura', db: 'MySQL ACID' },
  { step: 5, icon: '🔗', title: 'Registrar en Grafo', db: 'Neo4j' },
]

export default function Dashboard() {
  const [stats, setStats] = useState({ personas: 0, productos: 0, facturas: 0, health: {} })
  const [facturas, setFacturas] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      getPersonas().then((r) => r.data).catch(() => []),
      getProductos().then((r) => r.data).catch(() => []),
      getFacturas().then((r) => r.data).catch(() => []),
      healthApi().then((r) => r.data.databases || {}).catch(() => ({})),
    ]).then(([personas, productos, facturas, health]) => {
      setStats({ personas: personas.length, productos: productos.length, facturas: facturas.length, health })
      setFacturas(facturas.slice(0, 5))
    }).finally(() => setLoading(false))
  }, [])

  const archCards = [
    { label: 'Personas', count: stats.personas, icon: '🐘', color: 'cassandra', db: 'Cassandra' },
    { label: 'Productos', count: stats.productos, icon: '🍃', color: 'mongodb', db: 'MongoDB' },
    { label: 'Facturas', count: stats.facturas, icon: '🐬', color: 'mysql', db: 'MySQL' },
    { label: 'BD Conectadas', count: Object.values(stats.health).filter(Boolean).length + '/4', icon: '🔷', color: 'neo4j', db: 'Neo4j' },
  ]

  if (loading) return <div className="flex justify-center py-20"><Spinner size={28} /></div>

  return (
    <div>
      <h1 className="text-xl font-semibold mb-5">📊 Panel de Control</h1>

      {/* Architecture Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        {archCards.map((c) => (
          <div key={c.label} className="rounded-xl p-4 text-center border" style={{
            borderColor: `var(--${c.color})`,
            background: `rgba(255,255,255,.02)`,
          }}>
            <div className="text-3xl mb-2">{c.icon}</div>
            <div className="font-semibold text-sm">{c.label}</div>
            <div className="text-xs text-slate-500 mt-0.5">{c.db}</div>
            <div className="text-2xl font-bold mt-1">{c.count}</div>
          </div>
        ))}
      </div>

      {/* Flow Diagram */}
      <div className="bg-[#131c31] border border-[#1e2a45] rounded-xl p-5 mb-6">
        <h2 className="text-sm font-semibold mb-4 flex items-center gap-2">
          <ArrowRight size={16} className="text-blue-400" /> Flujo de Creación de Factura
        </h2>
        <div className="flex items-center gap-0 overflow-x-auto pb-2">
          {flow.map((f, i) => (
            <div key={f.step} className="flex items-center min-w-0">
              <div className="bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2.5 text-center min-w-[120px]">
                <div className="text-[10px] text-slate-500 uppercase">Paso {f.step}</div>
                <div className="text-xl my-0.5">{f.icon}</div>
                <div className="text-xs font-semibold">{f.title}</div>
                <div className="text-[10px] text-slate-500 mt-0.5">{f.db}</div>
              </div>
              {i < flow.length - 1 && (
                <div className="text-slate-600 px-1 text-lg">→</div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        {[
          { label: 'Personas', count: stats.personas, color: '#c084fc', icon: Users },
          { label: 'Productos', count: stats.productos, color: '#4ade80', icon: Package },
          { label: 'Facturas', count: stats.facturas, color: '#f97316', icon: Receipt },
          { label: 'BD Online', count: Object.values(stats.health).filter(Boolean).length + '/4', color: '#06b6d4', icon: Database },
        ].map((s) => (
          <div key={s.label} className="bg-[#131c31] border border-[#1e2a45] rounded-xl p-4 text-center">
            <div className="text-2xl font-bold" style={{ color: s.color }}>{s.count}</div>
            <div className="text-xs text-slate-400 mt-1 flex items-center justify-center gap-1.5">
              <s.icon size={13} /> {s.label}
            </div>
          </div>
        ))}
      </div>

      {/* Last Invoices */}
      <div className="bg-[#131c31] border border-[#1e2a45] rounded-xl overflow-hidden">
        <div className="px-5 py-3 border-b border-[#1e2a45] flex items-center gap-2 text-sm font-semibold">
          <Receipt size={16} className="text-orange-400" /> Últimas Facturas
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-[11px] text-slate-500 uppercase tracking-wider border-b border-[#1e2a45]">
                <th className="py-3 px-4 font-medium">#</th>
                <th className="py-3 px-4 font-medium">Total</th>
                <th className="py-3 px-4 font-medium">Items</th>
                <th className="py-3 px-4 font-medium">Estado</th>
              </tr>
            </thead>
            <tbody>
              {facturas.map((f) => (
                <tr key={f.id} className="border-b border-[#1e2a45]/50 hover:bg-white/[.02]">
                  <td className="py-2.5 px-4 text-slate-300">{f.numero}</td>
                  <td className="py-2.5 px-4">${f.total?.toFixed(2)}</td>
                  <td className="py-2.5 px-4 text-slate-400">{f.items || 0}</td>
                  <td className="py-2.5 px-4">
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                      f.estado === 'completada' ? 'bg-green-900/40 text-green-400' : 'bg-yellow-900/40 text-yellow-400'
                    }`}>
                      {f.estado}
                    </span>
                  </td>
                </tr>
              ))}
              {!facturas.length && (
                <tr><td colSpan={4} className="py-8 text-center text-slate-500">Sin facturas registradas</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
