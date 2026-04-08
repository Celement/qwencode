# AI Interior Design Studio

一个基于 Python + Vue3 + Element Plus 的 AI 室内设计系统，支持文生图、图生图功能，对接国内主流 AI 大模型服务商（阿里云百炼、火山方舟），并使用 RAG 知识库进行提示词增强。

## 🌟 核心特性

1. **文生图**：通过文本描述生成室内设计效果图
   - 支持 8 种设计风格选择（现代、极简、工业、北欧等）
   - 支持多种房间类型（客厅、卧室、厨房等）
   - 自动从 RAG 知识库获取优秀提示词进行增强
   - 实时预览生成结果

2. **图生图**：上传参考图生成新的设计方案
   - 拖拽上传图片
   - 可调节重绘强度
   - 结合文本描述进行创意变化
   - 保留原图结构的同时实现风格转换

3. **RAG 知识库**：使用阿里云百炼知识库进行语义检索
   - 上传设计文档到知识库
   - 语义搜索相关知识
   - 智能提示词增强
   - 管理知识条目

4. **多模型支持**：对接国内主流 AI 服务商
   - ✅ 阿里云百炼（通义万相）- 文生图、图生图
   - ✅ 火山方舟（豆包视觉）- 文生图、图生图
   - ✅ 可切换不同的服务商

## 📁 项目结构

```
ai-interior-design/
├── backend/                    # Python FastAPI 后端
│   ├── main.py                 # 主应用入口
│   ├── config.example.py       # 配置文件模板
│   ├── config.py               # 实际配置文件（需复制创建）
│   ├── models.py               # 数据模型
│   ├── database.py             # 数据库配置
│   ├── services/               # 业务逻辑
│   │   ├── ai_service.py       # AI 图像生成服务
│   │   └── knowledge_base_service.py  # RAG 知识库服务
│   ├── requirements.txt        # Python 依赖
│   ├── generated/              # 生成的图片目录
│   └── uploads/                # 上传文件目录
├── frontend/                   # Vue3 + Element Plus 前端
│   ├── src/
│   │   ├── views/              # 页面组件
│   │   │   ├── Home.vue        # 首页
│   │   │   ├── TextToImage.vue # 文生图页面
│   │   │   ├── ImageToImage.vue# 图生图页面
│   │   │   ├── Gallery.vue     # 作品展示页面
│   │   │   └── Knowledge.vue   # 知识库页面
│   │   ├── api/                # API 接口封装
│   │   ├── config.js           # 前端配置文件
│   │   ├── router/             # 路由配置
│   │   ├── App.vue             # 根组件
│   │   └── main.js             # 入口文件
│   ├── package.json
│   └── vite.config.js
└── README.md                   # 本文件
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 后端部署

#### 1. 安装依赖

```bash
cd ai-interior-design/backend
pip install -r requirements.txt
```

#### 2. 配置应用

```bash
# 复制配置文件模板
cp config.example.py config.py

# 编辑 config.py 填入实际配置，或设置环境变量
```

#### 3. 配置环境变量（必需）

**方式一：环境变量（推荐）**

```bash
# 阿里云百炼配置（必需）
export ALIYUN_BAILIAN_API_KEY="your-aliyun-api-key"
export ALIYUN_KNOWLEDGE_BASE_ID="your-knowledge-base-id"

# 火山方舟配置（可选）
export VOLCANO_ARK_API_KEY="your-volcano-api-key"
```

**方式二：修改 config.py**

编辑 `backend/config.py` 文件，填入实际的 API Key 和配置。

#### 4. 启动服务

```bash
# 方式一：直接运行
python main.py

# 方式二：使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

访问 http://localhost:8000/docs 查看 API 文档

### 前端部署

#### 1. 安装依赖

```bash
cd ai-interior-design/frontend
npm install
```

#### 2. 配置应用

编辑 `frontend/src/config.js` 文件，根据需要修改配置：

```javascript
const config = {
  apiBaseURL: '/api',  // 开发环境使用代理
  backendHost: 'http://localhost:8000',  // 生产环境后端地址
  // ... 其他配置
}
```

#### 3. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173 查看应用

#### 4. 生产构建

```bash
npm run build
```

## 🔧 配置说明

### 后端配置 (config.py)

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `ALIYUN_BAILIAN_API_KEY` | 阿里云百炼 API Key | 空 |
| `ALIYUN_KNOWLEDGE_BASE_ID` | 阿里云百炼知识库 ID | 空 |
| `VOLCANO_ARK_API_KEY` | 火山方舟 API Key | 空 |
| `DEFAULT_PROVIDER` | 默认 AI 服务商 | aliyun |
| `DEFAULT_IMAGE_WIDTH` | 默认图片宽度 | 1024 |
| `DEFAULT_IMAGE_HEIGHT` | 默认图片高度 | 1024 |
| `UPLOAD_FOLDER` | 上传文件目录 | uploads |
| `GENERATED_FOLDER` | 生成图片目录 | generated |

### 前端配置 (config.js)

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `apiBaseURL` | API 基础 URL | /api |
| `apiTimeout` | API 超时时间 (ms) | 60000 |
| `backendHost` | 后端服务地址 | http://localhost:8000 |
| `maxUploadSize` | 最大上传文件大小 | 10MB |
| `defaultProvider` | 默认 AI 服务商 | aliyun |

## 📡 API 接口

### 知识库接口 (RAG)

- `POST /api/knowledge/upload` - 上传文档到知识库
- `GET /api/knowledge/list` - 列出知识库文档
- `DELETE /api/knowledge/{document_id}` - 删除知识库文档
- `GET /api/knowledge/search` - 搜索知识库（语义搜索）
- `GET /api/knowledge/similar/{style}` - 获取相似风格提示词

### AI 生成接口

- `POST /api/generate/text-to-image` - 文生图
- `POST /api/generate/image-to-image` - 图生图
- `GET /api/generate/history` - 获取生成历史

### 基础数据接口

- `GET /api/styles` - 获取所有风格
- `GET /api/room-types` - 获取房间类型

## 🇨🇳 国内大模型对接

本项目已对接以下国内主流 AI 大模型服务商：

### 阿里云百炼

- **服务**：通义万相（文生图、图生图）
- **官网**：https://bailian.console.aliyun.com/
- **API 文档**：https://dashscope.console.aliyun.com/
- **获取 API Key**：登录 DashScope 控制台创建

### 火山方舟

- **服务**：豆包视觉（文生图、图生图）
- **官网**：https://www.volcengine.com/product/ark
- **获取 API Key**：登录火山方舟控制台创建

## 🔐 安全建议

1. **API Key 安全**：不要将 API Key 提交到版本控制系统
2. **环境变量**：使用环境变量管理敏感配置
3. **CORS 配置**：生产环境限制允许的源
4. **文件上传**：验证上传文件类型和大小

## 🛠️ 技术栈

- **后端**: 
  - Python 3.x
  - FastAPI (Web 框架)
  - Uvicorn (ASGI 服务器)
  - HTTPX (异步 HTTP 客户端)

- **前端**: 
  - Vue 3 (Composition API)
  - Element Plus (UI 组件库)
  - Vue Router (路由管理)
  - Axios (HTTP 客户端)
  - Vite (构建工具)

- **AI 集成**: 
  - 阿里云百炼（通义万相）
  - 火山方舟（豆包视觉）
  - RAG 知识库增强

## 📝 常见问题

### Q: 如何获取阿里云百炼 API Key？

A: 访问 https://dashscope.console.aliyun.com/，登录后在密钥管理页面创建 API Key。

### Q: 如何创建阿里云百炼知识库？

A: 
1. 登录 https://bailian.console.aliyun.com/
2. 进入「知识库」页面
3. 点击「创建知识库」
4. 上传设计相关文档（PDF、Word、TXT 等）
5. 复制知识库 ID 到配置文件

### Q: 为什么生成的是模拟结果？

A: 当未配置有效的 API Key 时，系统会自动启用模拟模式返回示例结果。请确保正确配置了至少一个 AI 服务商的 API Key。

### Q: 如何切换到火山方舟？

A: 在调用生成接口时，传入 `provider=volcano` 参数即可切换到火山方舟服务。

## 📄 License

MIT License
