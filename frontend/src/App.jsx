import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Personas from './pages/Personas'
import Productos from './pages/Productos'
import Facturacion from './pages/Facturacion'
import Recomendaciones from './pages/Recomendaciones'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/personas" element={<Personas />} />
        <Route path="/productos" element={<Productos />} />
        <Route path="/facturacion" element={<Facturacion />} />
        <Route path="/recomendaciones" element={<Recomendaciones />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}
