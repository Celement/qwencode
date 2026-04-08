# AI Interior Design Studio v2.0

AI 室内设计系统 - 支持文生图、图生图，对接阿里云百炼和火山方舟，使用 RAG 知识库

## 主要更新

### 🎯 核心改进

1. **支持国内 AI 模型服务商**
   - ✅ 阿里云百炼（通义万相）- 文生图、图生图
   - ✅ 火山方舟（豆包视觉）- 文生图、图生图
   - ✅ 可切换不同的服务商

2. **RAG 知识库**
   - ❌ 移除数据库存储方式
   - ✅ 对接阿里云百炼知识库进行 RAG 检索
   - ✅ 语义搜索相关知识增强提示词
   - ✅ 支持文档上传、删除、列表管理

3. **提示词增强**
   - 自动从 RAG 知识库获取相关知识
   - 智能拼接风格描述
   - 生成更专业的室内设计提示词

## 环境配置

### 环境变量

在运行前需要配置以下环境变量：

```bash
# 阿里云百炼配置（必需）
export ALIYUN_BAILIAN_API_KEY="your-aliyun-api-key"
export ALIYUN_KNOWLEDGE_BASE_ID="your-knowledge-base-id"

# 火山方舟配置（可选）
export VOLCANO_ARK_API_KEY="your-volcano-api-key"
```

### 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 启动服务

```bash
python main.py
```

或使用 uvicorn：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API 接口说明

### 知识库接口 (RAG)

#### 上传文档到知识库
```http
POST /api/knowledge/upload
Content-Type: multipart/form-data

file: <文件>
description: <可选描述>
```

#### 列出知识库文档
```http
GET /api/knowledge/list?limit=20
```

#### 删除知识库文档
```http
DELETE /api/knowledge/{document_id}
```

#### 搜索知识库（语义搜索）
```http
GET /api/knowledge/search?keywords=现代客厅&style=modern&top_k=10
```

#### 获取相似风格提示词
```http
GET /api/knowledge/similar/modern?limit=5
```

### AI 生成接口

#### 文生图
```http
POST /api/generate/text-to-image
Content-Type: application/x-www-form-urlencoded

prompt=一个温馨的客厅设计
style=modern
provider=aliyun  # 或 volcano
negative_prompt=模糊，低质量，失真，变形
width=1024
height=1024
```

响应示例：
```json
{
  "success": true,
  "image_url": "https://...",
  "original_prompt": "一个温馨的客厅设计",
  "enhanced_prompt": "一个温馨的客厅设计，[RAG 知识], 现代简约风格...",
  "rag_used": true,
  "generation_type": "text-to-image",
  "provider": "aliyun-bailian"
}
```

#### 图生图
```http
POST /api/generate/image-to-image
Content-Type: multipart/form-data

prompt=把这个客厅改成北欧风格
style=scandinavian
image: <上传图片>
strength=0.7
provider=aliyun  # 或 volcano
```

### 基础数据接口

#### 获取支持的风格
```http
GET /api/styles
```

返回：
```json
["modern", "minimalist", "industrial", "scandinavian", "traditional", "bohemian", "contemporary", "rustic"]
```

#### 获取房间类型
```http
GET /api/room-types
```

## 阿里云百炼知识库配置指南

### 1. 创建知识库

1. 登录 [阿里云百炼控制台](https://bailian.console.aliyun.com/)
2. 进入「知识库」页面
3. 点击「创建知识库」
4. 选择 appropriate 的知识库类型（推荐选择「通用型」）
5. 填写知识库名称和描述

### 2. 上传知识文档

支持以下格式：
- PDF 文档
- Word 文档 (.docx)
- TXT 文本文件
- Markdown 文件

建议上传：
- 室内设计风格指南
- 优秀设计案例描述
- 配色方案文档
- 材质搭配指南
- 灯光设计原则

### 3. 获取 API Key

1. 访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)
2. 创建或选择一个 API Key
3. 复制 API Key 并设置为环境变量

### 4. 获取知识库 ID

在百炼控制台的「知识库」列表中，找到创建的知识库，复制其 ID。

## 火山方舟配置指南

### 1. 创建应用

1. 登录 [火山方舟控制台](https://www.volcengine.com/product/ark)
2. 创建新应用
3. 选择视觉理解相关模型

### 2. 获取 API Key

在控制台的「密钥管理」页面创建并复制 API Key。

## 代码结构

```
backend/
├── main.py                          # FastAPI 主应用
├── services/
│   ├── ai_service.py                # AI 服务（阿里云百炼、火山方舟）
│   └── knowledge_base_service.py    # RAG 知识库服务
├── requirements.txt                 # Python 依赖
├── generated/                       # 生成的图片目录
└── uploads/                         # 上传文件目录
```

## 核心类说明

### AliyunBailianService

阿里云百炼服务类，提供：
- `generate_text_to_image()`: 文生图
- `generate_image_to_image()`: 图生图
- `query_rag_knowledge()`: 查询 RAG 知识库
- `enhance_prompt_with_rag()`: 使用 RAG 增强提示词

### VolcanoArkService

火山方舟服务类，提供：
- `generate_text_to_image()`: 文生图
- `generate_image_to_image()`: 图生图

### KnowledgeBaseService

知识库服务类，提供：
- `query_knowledge()`: 查询相关知识
- `search_prompts()`: 语义搜索
- `enhance_prompt_with_rag()`: 提示词增强
- `upload_document()`: 上传文档
- `delete_knowledge()`: 删除文档
- `list_documents()`: 列出文档

## 使用示例

### Python 客户端示例

```python
import httpx

# 文生图
async def generate_image():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/generate/text-to-image",
            data={
                "prompt": "一个现代简约风格的客厅，有大窗户和绿植",
                "style": "modern",
                "provider": "aliyun"
            }
        )
        result = response.json()
        print(f"生成的图片 URL: {result['image_url']}")
        print(f"增强后的提示词：{result['enhanced_prompt']}")

# 图生图
async def image_to_image(image_path: str):
    async with httpx.AsyncClient() as client:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {
                'prompt': '改成北欧风格',
                'style': 'scandinavian',
                'strength': 0.7,
                'provider': 'aliyun'
            }
            response = await client.post(
                "http://localhost:8000/api/generate/image-to-image",
                files=files,
                data=data
            )
            result = response.json()
            print(f"生成的图片 URL: {result['image_url']}")
```

### cURL 示例

```bash
# 文生图
curl -X POST "http://localhost:8000/api/generate/text-to-image" \
  -d "prompt=一个温馨的卧室设计" \
  -d "style=modern" \
  -d "provider=aliyun"

# 图生图
curl -X POST "http://localhost:8000/api/generate/image-to-image" \
  -F "prompt=改成工业风格" \
  -F "style=industrial" \
  -F "strength=0.7" \
  -F "provider=aliyun" \
  -F "image=@/path/to/image.jpg"

# 搜索知识库
curl "http://localhost:8000/api/knowledge/search?keywords=客厅配色&style=modern"
```

## 注意事项

1. **API Key 安全**: 不要将 API Key 提交到版本控制系统
2. **知识库质量**: RAG 效果取决于知识库文档的质量，建议上传专业、结构化的设计文档
3. **超时设置**: 图片生成可能需要较长时间，已设置 120 秒超时
4. **错误处理**: 当 API 调用失败时，系统会返回模拟结果用于演示
5. **历史记录**: 由于移除了数据库，生成历史记录功能需要配置外部存储服务

## 后续优化建议

1. 集成阿里云日志服务（SLS）存储生成历史
2. 添加更多国内 AI 模型服务商支持（如百度文心一格）
3. 实现批量生成和图片编辑功能
4. 添加用户认证和配额管理
5. 集成前端界面

## 许可证

MIT License
