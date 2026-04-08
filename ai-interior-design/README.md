# AI Interior Design Studio

一个基于 Python + Vue3 + Element Plus 的 AI 室内设计系统，支持文生图、图生图功能，并展示公司优秀设计作品。

## 项目结构

```
ai-interior-design/
├── backend/          # Python FastAPI 后端
│   ├── main.py       # 主应用入口
│   ├── models.py     # 数据模型
│   ├── database.py   # 数据库配置
│   ├── services/     # 业务逻辑
│   │   ├── ai_service.py           # AI 图像生成服务
│   │   ├── knowledge_base_service.py # 知识库服务
│   │   └── design_work_service.py  # 设计作品服务
│   └── requirements.txt
└── frontend/         # Vue3 + Element Plus 前端
    ├── src/
    │   ├── views/      # 页面组件
    │   │   ├── Home.vue          # 首页
    │   │   ├── TextToImage.vue   # 文生图页面
    │   │   ├── ImageToImage.vue  # 图生图页面
    │   │   ├── Gallery.vue       # 作品展示页面
    │   │   └── Knowledge.vue     # 知识库页面
    │   ├── components/ # 可复用组件
    │   ├── api/        # API 接口封装
    │   └── router/     # 路由配置
    └── package.json
```

## 功能特性

1. **文生图**：通过文本描述生成室内设计效果图
   - 支持 8 种设计风格选择（现代、极简、工业、北欧等）
   - 支持多种房间类型（客厅、卧室、厨房等）
   - 自动从知识库获取优秀提示词进行增强
   - 实时预览生成结果

2. **图生图**：上传参考图生成新的设计方案
   - 拖拽上传图片
   - 可调节重绘强度
   - 结合文本描述进行创意变化
   - 保留原图结构的同时实现风格转换

3. **作品展示**：按风格分类展示公司优秀设计作品
   - 支持风格和房间类型筛选
   - 关键词搜索功能
   - 图片预览和详情展示
   - 响应式网格布局

4. **知识库**：存储优秀设计提示词和设计图稿链接
   - 添加和管理知识条目
   - 按风格分类浏览
   - 快速使用提示词到生成页面
   - 辅助 AI 生成更优质的设计

## 技术栈

- **后端**: 
  - Python 3.x
  - FastAPI (Web 框架)
  - SQLAlchemy (ORM)
  - SQLite (数据库)
  - Uvicorn (ASGI 服务器)

- **前端**: 
  - Vue 3 (Composition API)
  - Element Plus (UI 组件库)
  - Vue Router (路由管理)
  - Axios (HTTP 客户端)
  - Vite (构建工具)

- **AI 集成**: 
  - 支持调用 Stability AI API
  - 可扩展支持其他图像生成模型
  - 内置提示词增强机制

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 后端启动

```bash
cd ai-interior-design/backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档

### 前端启动

```bash
cd ai-interior-design/frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:5173 查看应用

## API 接口

### 知识库接口
- `GET /api/knowledge/` - 获取知识库列表
- `POST /api/knowledge/` - 添加知识条目
- `GET /api/knowledge/search` - 搜索提示词

### 设计作品接口
- `GET /api/works/` - 获取作品列表
- `POST /api/works/` - 添加作品
- `GET /api/works/search` - 搜索作品

### AI 生成接口
- `POST /api/generate/text-to-image` - 文生图
- `POST /api/generate/image-to-image` - 图生图
- `GET /api/generate/history` - 获取生成历史

### 基础数据接口
- `GET /api/styles` - 获取所有风格
- `GET /api/room-types` - 获取房间类型

## 配置 AI API

在 `backend/services/ai_service.py` 中配置您的 AI 服务：

```python
class AIService:
    def __init__(self, api_key: str = "your-api-key", api_url: str = "your-api-url"):
        self.api_key = api_key
        self.api_url = api_url
```

当前默认使用模拟模式返回示例结果，配置真实 API 后取消注释相应代码即可。

## 扩展建议

1. **接入真实 AI 模型**: 配置 Stability AI、Midjourney 或其他图像生成 API
2. **用户系统**: 添加用户认证和权限管理
3. **图片存储**: 集成云存储服务（如 AWS S3、阿里云 OSS）
4. **更多风格**: 扩展支持更多设计风格
5. **批量生成**: 支持一次生成多个方案供选择
6. **导出功能**: 支持导出高清图片和设计报告

## License

MIT License
