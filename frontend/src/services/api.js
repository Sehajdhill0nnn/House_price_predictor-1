import axios from 'axios'

const getBaseUrl = () => {
  const envUrl = import.meta.env.VITE_API_URL
  if (!envUrl) {
    return 'http://localhost:8000/api'
  }
  const trimmed = envUrl.trim().replace(/\/+$/, '')
  return trimmed.endsWith('/api') ? trimmed : `${trimmed}/api`
}

const api = axios.create({ baseURL: getBaseUrl() })
export const predictHouse = (payload) => api.post('/predict', payload)
export const fetchMetrics = () => api.get('/models/metrics')
export const fetchHistory = () => api.get('/history')
export const deleteHistory = (id) => api.delete(`/history/${id}`)
export const trainUploadedDataset = (file) => { const formData = new FormData(); formData.append('file', file); return api.post('/datasets/train', formData) }
export const fetchDatasetSchema = () => api.get('/datasets/schema')
export default api
