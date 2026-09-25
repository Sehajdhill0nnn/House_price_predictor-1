import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api' })
export const predictHouse = (payload) => api.post('/predict', payload)
export const fetchMetrics = () => api.get('/models/metrics')
export const fetchHistory = () => api.get('/history')
export const deleteHistory = (id) => api.delete(`/history/${id}`)
export const trainUploadedDataset = (file) => { const formData = new FormData(); formData.append('file', file); return api.post('/datasets/train', formData) }
export const fetchDatasetSchema = () => api.get('/datasets/schema')
export default api
