import { NavLink, Outlet } from 'react-router-dom'
import {
  LayoutDashboard, Users, Package, Receipt, Lightbulb,
  Database, FlaskConical,
} from 'lucide-react'
import { useEffect, useState } from 'react'
import { healthApi } from '../api'
import { Toaster } from 'react-hot-toast'

const nav = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/personas', label: 'Personas', icon: Users },
  { to: '/productos', label: 'Productos', icon: Package },
  { to: '/facturacion', label: 'Facturación', icon: Receipt },
  { to: '/recomendaciones', label: 'Recomendaciones', icon: Lightbulb },
]

const dbs = [
  { key: 'cassandra', label: 'Cassandra', color: '#c084fc' },
  { key: 'mongodb', label: 'MongoDB', color: '#4ade80' },
  { key: 'mysql', label: 'MySQL', color: '#f97316' },
  { key: 'neo4j', label: 'Neo4j', color: '#06b6d4' },
]

export default function Layout() {
  const [health, setHealth] = useState({})
  const [sidebar, setSidebar] = useState(true)

  useEffect(() => {
    const check = async () => {
      try {
        const { data } = await healthApi()
        setHealth(data.databases || {})
      } catch {
        setHealth({})
      }
    }
    check()
    const id = setInterval(check, 10000)
    return () => clearInterval(id)
  }, [])

  return (
    <div className="flex min-h-screen">
      <Toaster position="bottom-right" toastOptions={{
        style: { background: '#131c31', color: '#e2e8f0', border: '1px solid #1e2a45' },
      }} />
      {/* Sidebar */}
      <aside className={`${sidebar ? 'w-60' : 'w-0'} transition-all duration-200 bg-[#131c31] border-r border-[#1e2a45] flex flex-col flex-shrink-0 overflow-hidden`}>
        <div className="p-4 border-b border-[#1e2a45] flex items-center gap-2.5">
          <FlaskConical className="text-blue-400" size={22} />
          <span className="font-semibold text-sm">Facturación Políglota</span>
        </div>
        <nav className="flex-1 p-2 space-y-0.5">
          {nav.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-blue-600/15 text-blue-400'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                }`
              }
            >
              <Icon size={17} />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="p-3 border-t border-[#1e2a45] space-y-1.5">
          <div className="text-[11px] text-slate-500 uppercase tracking-wider font-semibold mb-1">Estado BDs</div>
          {dbs.map(({ key, label, color }) => (
            <div key={key} className="flex items-center gap-2 text-xs text-slate-400">
              <span
                className="w-2 h-2 rounded-full inline-block transition-all duration-500"
                style={{
                  background: health[key] ? color : '#475569',
                  boxShadow: health[key] ? `0 0 6px ${color}` : 'none',
                }}
              />
              {label}
            </div>
          ))}
        </div>
      </aside>
      {/* Toggle */}
      <button
        onClick={() => setSidebar((s) => !s)}
        className="fixed top-3 left-3 z-50 bg-[#131c31] border border-[#1e2a45] rounded-lg p-1.5 text-slate-400 hover:text-slate-200"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M9 18l6-6-6-6" />
        </svg>
      </button>
      {/* Main */}
      <main className="flex-1 p-5 overflow-auto">
        <Outlet />
      </main>
    </div>
  )
}
