from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from database import engine, get_db, Base
from models import DesignStyle
from services.knowledge_base_service import KnowledgeBaseService
from services.design_work_service import DesignWorkService
from services.ai_service import AIService

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Interior Design Studio",
    description="AI 室内设计系统 - 支持文生图、图生图，展示优秀设计作品",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件目录
os.makedirs("generated", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
app.mount("/generated", StaticFiles(directory="generated"), name="generated")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# AI 服务实例
ai_service = AIService()


# ==================== 知识库接口 ====================

@app.post("/api/knowledge/", tags=["知识库"])
def add_knowledge(
    style: str = Form(...),
    prompt: str = Form(...),
    image_url: str = Form(...),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """添加知识条目到知识库"""
    return KnowledgeBaseService.add_knowledge(
        db=db,
        style=style,
        prompt=prompt,
        image_url=image_url,
        description=description,
        tags=tags
    )


@app.get("/api/knowledge/", tags=["知识库"])
def get_knowledge(style: Optional[str] = None, db: Session = Depends(get_db)):
    """获取知识库条目，可按风格筛选"""
    if style:
        return KnowledgeBaseService.get_by_style(db, style)
    return KnowledgeBaseService.get_all(db)


@app.get("/api/knowledge/search", tags=["知识库"])
def search_knowledge(keywords: str, style: Optional[str] = None, db: Session = Depends(get_db)):
    """搜索知识库中的提示词"""
    return KnowledgeBaseService.search_prompts(db, keywords, style)


# ==================== 设计作品接口 ====================

@app.post("/api/works/", tags=["设计作品"])
def add_work(
    title: str = Form(...),
    style: str = Form(...),
    image_url: str = Form(...),
    description: Optional[str] = Form(None),
    room_type: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """添加新的设计作品"""
    return DesignWorkService.add_work(
        db=db,
        title=title,
        style=style,
        image_url=image_url,
        description=description,
        room_type=room_type
    )


@app.get("/api/works/", tags=["设计作品"])
def get_works(style: Optional[str] = None, room_type: Optional[str] = None, db: Session = Depends(get_db)):
    """获取设计作品列表"""
    if style:
        return DesignWorkService.get_by_style(db, style)
    elif room_type:
        return DesignWorkService.get_by_room_type(db, room_type)
    return DesignWorkService.get_all(db)


@app.get("/api/works/search", tags=["设计作品"])
def search_works(keywords: str, style: Optional[str] = None, db: Session = Depends(get_db)):
    """搜索设计作品"""
    return DesignWorkService.search_works(db, keywords, style)


# ==================== AI 生成接口 ====================

@app.post("/api/generate/text-to-image", tags=["AI 生成"])
async def text_to_image(
    prompt: str = Form(...),
    style: str = Form("modern"),
    negative_prompt: Optional[str] = Form("blurry, low quality, distorted"),
    db: Session = Depends(get_db)
):
    """
    文生图：根据文本描述生成室内设计图
    
    会自动从知识库中获取相似风格的优秀提示词进行增强
    """
    result = await ai_service.generate_text_to_image(
        prompt=prompt,
        style=style,
        negative_prompt=negative_prompt or "blurry, low quality, distorted"
    )
    
    # 保存生成记录
    from models import GeneratedImage
    generated = GeneratedImage(
        prompt=prompt,
        style=style,
        image_url=result["image_url"],
        generation_type="text-to-image"
    )
    db.add(generated)
    db.commit()
    db.refresh(generated)
    
    return {
        **result,
        "id": generated.id,
        "knowledge_used": True  # 标识是否使用了知识库增强
    }


@app.post("/api/generate/image-to-image", tags=["AI 生成"])
async def image_to_image(
    prompt: str = Form(...),
    style: str = Form("modern"),
    image: UploadFile = File(...),
    strength: float = Form(0.7),
    db: Session = Depends(get_db)
):
    """
    图生图：上传参考图生成新的设计方案
    
    结合参考图和文本描述，从知识库获取提示词增强生成效果
    """
    # 读取上传的图片
    contents = await image.read()
    import base64
    image_base64 = base64.b64encode(contents).decode('utf-8')
    
    # 保存参考图
    import os
    upload_path = f"uploads/{image.filename}"
    with open(upload_path, "wb") as f:
        f.write(contents)
    
    result = await ai_service.generate_image_to_image(
        image_data=image_base64,
        prompt=prompt,
        style=style,
        strength=strength
    )
    
    # 保存生成记录
    from models import GeneratedImage
    generated = GeneratedImage(
        prompt=prompt,
        style=style,
        image_url=result["image_url"],
        generation_type="image-to-image",
        reference_image_url=upload_path
    )
    db.add(generated)
    db.commit()
    db.refresh(generated)
    
    return {
        **result,
        "id": generated.id,
        "reference_image": upload_path,
        "knowledge_used": True
    }


@app.get("/api/generate/history", tags=["AI 生成"])
def get_generation_history(db: Session = Depends(get_db)):
    """获取生成历史记录"""
    from models import GeneratedImage
    return db.query(GeneratedImage).order_by(GeneratedImage.created_at.desc()).limit(50).all()


# ==================== 样式枚举接口 ====================

@app.get("/api/styles", tags=["基础数据"])
def get_styles():
    """获取所有支持的设计风格"""
    return [style.value for style in DesignStyle]


@app.get("/api/room-types", tags=["基础数据"])
def get_room_types():
    """获取房间类型列表"""
    return ["客厅", "卧室", "厨房", "卫生间", "书房", "餐厅", "阳台", "玄关"]


# ==================== 首页 ====================

@app.get("/")
def read_root():
    return {
        "message": "欢迎使用 AI Interior Design Studio",
        "docs": "/docs",
        "features": [
            "文生图 - 通过文本描述生成室内设计效果图",
            "图生图 - 上传参考图生成新的设计方案",
            "作品展示 - 按风格分类展示公司优秀设计作品",
            "知识库 - 存储优秀设计提示词和设计图稿链接"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
