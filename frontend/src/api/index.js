import axios from 'axios'

const api = axios.create({ baseURL: '/api/v1' })

export const healthApi = () => api.get('/health')

// Personas
export const getPersonas = () => api.get('/datos/personas')
export const createPersona = (data) => api.post('/datos/personas', data)
export const updatePersona = (id, data) => api.put(`/datos/personas/${id}`, data)
export const deletePersona = (id) => api.delete(`/datos/personas/${id}`)

// Productos
export const getProductos = () => api.get('/datos/productos')
export const createProducto = (data) => api.post('/datos/productos', data)
export const updateProducto = (id, data) => api.put(`/datos/productos/${id}`, data)
export const deleteProducto = (id) => api.delete(`/datos/productos/${id}`)

// Facturas
export const getFacturas = () => api.get('/datos/facturas')
export const getFacturaById = (id) => api.get(`/datos/facturas/${id}`)
export const createFactura = (data) => api.post('/facturas', data)

// Recomendaciones
export const getRecomendaciones = (clienteId, limite = 5) =>
  api.get(`/facturas/recomendaciones/${clienteId}`, { params: { limite } })

export default api
