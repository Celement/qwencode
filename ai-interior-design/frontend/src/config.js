// 前端配置文件 - 所有配置项集中管理

const config = {
  // ==================== 应用基础配置 ====================
  appName: 'AI Interior Design Studio',
  appVersion: '2.0.0',
  
  // ==================== API 配置 ====================
  // API 基础 URL，开发环境使用代理，生产环境需要修改为实际后端地址
  apiBaseURL: '/api',
  apiTimeout: 60000, // 60 秒
  
  // ==================== 后端服务地址 (生产环境使用) ====================
  // 部署时根据实际情况修改
  backendHost: process.env.VUE_APP_BACKEND_HOST || 'http://localhost:8000',
  
  // ==================== 图片配置 ====================
  maxUploadSize: 10 * 1024 * 1024, // 10MB
  allowedImageTypes: ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'],
  
  // 默认图片尺寸
  defaultImageWidth: 1024,
  defaultImageHeight: 1024,
  
  // ==================== 设计风格配置 ====================
  supportedStyles: [
    'modern',       // 现代风格
    'minimalist',   // 极简风格
    'industrial',   // 工业风格
    'scandinavian', // 北欧风格
    'traditional',  // 传统风格
    'bohemian',     // 波西米亚风格
    'contemporary', // 当代风格
    'rustic'        // 乡村风格
  ],
  
  styleLabels: {
    'modern': '现代风格',
    'minimalist': '极简风格',
    'industrial': '工业风格',
    'scandinavian': '北欧风格',
    'traditional': '传统风格',
    'bohemian': '波西米亚风格',
    'contemporary': '当代风格',
    'rustic': '乡村风格'
  },
  
  // ==================== 房间类型配置 ====================
  roomTypes: [
    '客厅', '卧室', '厨房', '卫生间',
    '书房', '餐厅', '阳台', '玄关'
  ],
  
  // ==================== AI 服务商配置 ====================
  // 可选值：aliyun, volcano
  defaultProvider: 'aliyun',
  
  providerLabels: {
    'aliyun': '阿里云百炼',
    'volcano': '火山方舟'
  },
  
  // ==================== 图生图配置 ====================
  defaultStrength: 0.7, // 默认重绘强度
  minStrength: 0.1,
  maxStrength: 1.0,
  
  // ==================== 分页配置 ====================
  defaultPageSize: 12,
  defaultTopK: 5, // RAG 查询默认返回数量
  
  // ==================== 日志配置 ====================
  enableDebugLog: process.env.NODE_ENV === 'development'
}

export default config
