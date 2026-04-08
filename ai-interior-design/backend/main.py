from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
import os

from config import settings
from services.knowledge_base_service import KnowledgeBaseService
from services.ai_service import AliyunBailianService, VolcanoArkService

# 创建必要的目录
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(settings.GENERATED_FOLDER, exist_ok=True)

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# 静态文件目录
app.mount(f"/{settings.GENERATED_FOLDER}", StaticFiles(directory=settings.GENERATED_FOLDER), name="generated")
app.mount(f"/{settings.UPLOAD_FOLDER}", StaticFiles(directory=settings.UPLOAD_FOLDER), name="uploads")

# AI 服务实例 - 支持阿里云百炼和火山方舟
aliyun_service = AliyunBailianService()
volcano_service = VolcanoArkService()

# 知识库服务实例 - 使用阿里云百炼 RAG 知识库
knowledge_service = KnowledgeBaseService()


# ==================== 知识库接口 (RAG) ====================

@app.post("/api/knowledge/upload", tags=["知识库"])
async def upload_knowledge_document(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    """上传文档到阿里云百炼 RAG 知识库"""
    # 保存临时文件
    temp_path = f"uploads/temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        result = await knowledge_service.upload_document(temp_path, description)
        return result
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.get("/api/knowledge/list", tags=["知识库"])
async def list_knowledge_documents(limit: int = 20):
    """列出知识库中的文档"""
    return await knowledge_service.list_documents(limit)


@app.delete("/api/knowledge/{document_id}", tags=["知识库"])
async def delete_knowledge_document(document_id: str):
    """删除知识库文档"""
    return await knowledge_service.delete_knowledge(document_id)


@app.get("/api/knowledge/search", tags=["知识库"])
async def search_knowledge(keywords: str, style: Optional[str] = None, top_k: int = 10):
    """搜索知识库中的相关内容（RAG 语义搜索）"""
    results = await knowledge_service.search_prompts(keywords, style, top_k)
    return {"results": results, "count": len(results)}


@app.get("/api/knowledge/similar/{style}", tags=["知识库"])
async def get_similar_knowledge(style: str, limit: int = 5):
    """获取相似风格的提示词"""
    results = await knowledge_service.get_similar_prompts(style, limit)
    return {"results": results, "count": len(results)}


# ==================== AI 生成接口 ====================

@app.post("/api/generate/text-to-image", tags=["AI 生成"])
async def text_to_image(
    prompt: str = Form(...),
    style: str = Form("modern"),
    negative_prompt: Optional[str] = Form("模糊，低质量，失真，变形"),
    provider: str = Form("aliyun"),  # aliyun 或 volcano
    width: int = Form(1024),
    height: int = Form(1024)
):
    """
    文生图：根据文本描述生成室内设计图
    
    会自动从 RAG 知识库中获取相关知识进行提示词增强
    """
    # 使用 RAG 增强提示词
    enhanced_prompt = await knowledge_service.enhance_prompt_with_rag(prompt, style)
    
    # 选择服务商
    if provider == "volcano":
        result = await volcano_service.generate_text_to_image(
            prompt=enhanced_prompt,
            style=style,
            negative_prompt=negative_prompt or "模糊，低质量，失真",
            width=width,
            height=height
        )
    else:
        result = await aliyun_service.generate_text_to_image(
            prompt=enhanced_prompt,
            style=style,
            negative_prompt=negative_prompt or "模糊，低质量，失真，变形",
            width=width,
            height=height
        )
    
    return {
        **result,
        "original_prompt": prompt,
        "enhanced_prompt": enhanced_prompt,
        "rag_used": True
    }


@app.post("/api/generate/image-to-image", tags=["AI 生成"])
async def image_to_image(
    prompt: str = Form(...),
    style: str = Form("modern"),
    image: UploadFile = File(...),
    strength: float = Form(0.7),
    provider: str = Form("aliyun")  # aliyun 或 volcano
):
    """
    图生图：上传参考图生成新的设计方案
    
    结合参考图和文本描述，从 RAG 知识库获取知识增强生成效果
    """
    # 读取上传的图片
    contents = await image.read()
    import base64
    image_base64 = base64.b64encode(contents).decode('utf-8')
    
    # 保存参考图
    upload_path = f"uploads/{image.filename}"
    with open(upload_path, "wb") as f:
        f.write(contents)
    
    # 使用 RAG 增强提示词
    enhanced_prompt = await knowledge_service.enhance_prompt_with_rag(prompt, style)
    
    # 选择服务商
    if provider == "volcano":
        result = await volcano_service.generate_image_to_image(
            image_data=image_base64,
            prompt=enhanced_prompt,
            style=style,
            strength=strength
        )
    else:
        result = await aliyun_service.generate_image_to_image(
            image_data=image_base64,
            prompt=enhanced_prompt,
            style=style,
            strength=strength
        )
    
    return {
        **result,
        "original_prompt": prompt,
        "enhanced_prompt": enhanced_prompt,
        "reference_image": upload_path,
        "rag_used": True
    }


@app.get("/api/generate/history", tags=["AI 生成"])
def get_generation_history():
    """获取生成历史记录
    
    注意：由于不再使用数据库存储，此接口返回空列表
    实际应用中可以集成阿里云日志服务或其他存储方案
    """
    return {"message": "历史记录功能需要配置外部存储服务", "history": []}


# ==================== 样式枚举接口 ====================

@app.get("/api/styles", tags=["基础数据"])
def get_styles():
    """获取所有支持的设计风格"""
    return settings.SUPPORTED_STYLES


@app.get("/api/room-types", tags=["基础数据"])
def get_room_types():
    """获取房间类型列表"""
    return settings.ROOM_TYPES


# ==================== 首页 ====================

@app.get("/")
def read_root():
    return {
        "message": f"欢迎使用 {settings.APP_NAME} v{settings.APP_VERSION}",
        "docs": "/docs",
        "features": [
            "文生图 - 通过文本描述生成室内设计效果图（支持阿里云百炼、火山方舟）",
            "图生图 - 上传参考图生成新的设计方案（支持阿里云百炼、火山方舟）",
            "RAG 知识库 - 使用阿里云百炼知识库进行语义检索和提示词增强",
            "多模型支持 - 可切换不同的国内 AI 模型服务商"
        ],
        "configuration": {
            "aliyun_bailian": "配置 ALIYUN_BAILIAN_API_KEY 和 ALIYUN_KNOWLEDGE_BASE_ID 环境变量",
            "volcano_ark": "配置 VOLCANO_ARK_API_KEY 环境变量",
            "config_file": "复制 config.example.py 为 config.py 并修改配置"
        },
        "supported_styles": settings.SUPPORTED_STYLES,
        "room_types": settings.ROOM_TYPES
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
