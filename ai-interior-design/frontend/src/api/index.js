import axios from 'axios'
import config from '@/config'

// 创建 axios 实例
const api = axios.create({
  baseURL: config.apiBaseURL,
  timeout: config.apiTimeout
})

// 知识库相关接口
export const knowledgeApi = {
  upload: (formData) => api.post('/knowledge/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
  getList: (limit = 20) => api.get('/knowledge/list', { params: { limit } }),
  delete: (documentId) => api.delete(`/knowledge/${documentId}`),
  search: (keywords, style, top_k = 10) => api.get('/knowledge/search', { params: { keywords, style, top_k } }),
  getSimilar: (style, limit = 5) => api.get(`/knowledge/similar/${style}`, { params: { limit } })
}

// AI 生成相关接口
export const generateApi = {
  textToImage: (data) => api.post('/generate/text-to-image', data, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }),
  imageToImage: (formData) => api.post('/generate/image-to-image', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
  getHistory: () => api.get('/generate/history')
}

// 基础数据接口
export const baseApi = {
  getStyles: () => api.get('/styles'),
  getRoomTypes: () => api.get('/room-types')
}

export default api
