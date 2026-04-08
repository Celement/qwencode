import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000
})

// 知识库相关接口
export const knowledgeApi = {
  getList: (style) => api.get('/knowledge/', { params: { style } }),
  search: (keywords, style) => api.get('/knowledge/search', { params: { keywords, style } }),
  add: (data) => api.post('/knowledge/', data, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
}

// 设计作品相关接口
export const worksApi = {
  getList: (style, roomType) => api.get('/works/', { params: { style, room_type: roomType } }),
  search: (keywords, style) => api.get('/works/search', { params: { keywords, style } }),
  add: (data) => api.post('/works/', data, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
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
