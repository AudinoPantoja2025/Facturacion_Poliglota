import { useEffect, useState } from 'react'
import { getPersonas, getRecomendaciones } from '../api'
import { Lightbulb, Star, Users, MapPin, Sparkles } from 'lucide-react'
import toast from 'react-hot-toast'
import Spinner from '../components/Spinner'

export default function Recomendaciones() {
  const [personas, setPersonas] = useState([])
  const [clienteId, setClienteId] = useState('')
  const [recs, setRecs] = useState([])
  const [loading, setLoading] = useState(false)
  const [consultado, setConsultado] = useState(false)
  const [clienteSel, setClienteSel] = useState(null)

  useEffect(() => {
    getPersonas().then((r) => setPersonas(r.data.filter((p) => p.rol === 'cliente'))).catch(() => {})
  }, [])

  const buscar = async () => {
    if (!clienteId) return toast.error('Selecciona un cliente')
    setLoading(true)
    setConsultado(false)
    const cliente = personas.find((p) => p.id === clienteId)
    setClienteSel(cliente)
    try {
      const { data } = await getRecomendaciones(clienteId, 6)
      setRecs(data.recomendaciones || [])
    } catch {
      toast.error('Error obteniendo recomendaciones')
      setRecs([])
    } finally {
      setLoading(false)
      setConsultado(true)
    }
  }

  return (
    <div>
      <h1 className="text-xl font-semibold mb-5 flex items-center gap-2.5">
        <Lightbulb size={22} className="text-[#06b6d4]" />
        Recomendaciones <span className="text-sm font-normal text-slate-400">· Neo4j · Motor de Grafos</span>
      </h1>

      {/* Selector */}
      <div className="bg-[#131c31] border border-[#1e2a45] rounded-xl p-5 mb-5">
        <p className="text-sm text-slate-400 mb-4 leading-relaxed">
          <Sparkles size={14} className="inline text-yellow-400 mr-1" />
          Algoritmo híbrido basado en clientes del mismo <strong className="text-slate-200">género</strong>,
          <strong className="text-slate-200"> estrato</strong> o <strong className="text-slate-200">barrio</strong>
          que compraron productos que aún no has adquirido.
        </p>
        <div className="flex gap-2 items-end">
          <div className="flex-1">
            <label className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Cliente</label>
            <select value={clienteId} onChange={(e) => setClienteId(e.target.value)}
              className="w-full bg-[#0b1121] border border-[#1e2a45] rounded-lg px-3 py-2 text-sm mt-1">
              <option value="">Seleccionar cliente...</option>
              {personas.map((p) => (
                <option key={p.id} value={p.id}>{p.nombre}</option>
              ))}
            </select>
          </div>
          <button onClick={buscar} disabled={loading || !clienteId}
            className="bg-[#06b6d4] hover:bg-[#0891b2] disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium px-5 py-2 rounded-lg text-sm transition-all flex items-center gap-2">
            {loading ? <Spinner size={15} /> : '🎯 Recomendar'}
          </button>
        </div>
      </div>

      {/* Results */}
      {clienteSel && consultado && !loading && (
        <div className="bg-[#131c31] border border-[#1e2a45] rounded-xl p-4 mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-blue-600/20 flex items-center justify-center text-lg">
              {clienteSel.genero === 'M' ? '👤' : '👩'}
            </div>
            <div>
              <div className="font-semibold text-sm">{clienteSel.nombre}</div>
              <div className="text-xs text-slate-400 flex items-center gap-3 mt-0.5">
                <span className="flex items-center gap-1"><MapPin size={11} /> {clienteSel.barrio}</span>
                <span className="flex items-center gap-1"><Users size={11} /> Estrato {clienteSel.estrato}</span>
                <span>Género: {clienteSel.genero === 'M' ? 'Masculino' : 'Femenino'}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Feed */}
      {loading && (
        <div className="flex justify-center py-16"><Spinner size={28} /></div>
      )}

      {consultado && !loading && (
        <div>
          {recs.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {recs.map((r, i) => (
                <div key={i}
                  className="bg-[#131c31] border border-[#1e2a45] rounded-xl p-4 hover:border-[#06b6d4]/40 transition-all group">
                  <div className="flex items-start justify-between mb-2">
                    <span className="text-2xl">🎯</span>
                    <span className="flex items-center gap-1 text-xs text-yellow-400 bg-yellow-900/20 px-2 py-0.5 rounded-full">
                      <Star size={11} /> {r.relevancia}
                    </span>
                  </div>
                  <h3 className="font-semibold text-sm mb-1">{r.nombre}</h3>
                  <div className="text-xs text-slate-500 mb-2">📂 {r.categoria}</div>
                  <div className="flex items-center gap-3 text-xs text-slate-400">
                    <span className="flex items-center gap-1">
                      <Users size={12} /> {r.compras_similares} compras
                    </span>
                  </div>
                  <div className="mt-2 h-1.5 bg-[#0b1121] rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-[#06b6d4] to-blue-500 rounded-full"
                      style={{ width: `${Math.min(100, r.relevancia * 6)}%` }} />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-[#131c31] border border-[#1e2a45] rounded-xl py-12 text-center">
              <div className="text-3xl mb-2">🔍</div>
              <p className="text-slate-400 text-sm">No hay recomendaciones disponibles para este cliente.</p>
              <p className="text-xs text-slate-500 mt-1">
                El cliente debe haber realizado compras previas y existir clientes similares en el grafo.
              </p>
            </div>
          )}
        </div>
      )}

      {!consultado && !loading && (
        <div className="bg-[#131c31] border border-[#1e2a45] rounded-xl py-16 text-center">
          <div className="text-4xl mb-3">🔮</div>
          <p className="text-slate-400 text-sm">
            Selecciona un cliente y haz clic en <strong className="text-slate-200">"Recomendar"</strong>
          </p>
          <p className="text-xs text-slate-500 mt-1">
            El motor consulta Neo4j en tiempo real usando el grafo de relaciones
          </p>
        </div>
      )}
    </div>
  )
}
