# ==================== AI Interior Design Studio 配置 ====================
# 复制此文件为 .env 并填入实际配置值
# cp config.example.py config.py

import os
from typing import Optional

class Settings:
    """应用配置类 - 所有配置项集中管理"""
    
    # ==================== 应用基础配置 ====================
    APP_NAME: str = "AI Interior Design Studio"
    APP_VERSION: str = "2.0.0"
    APP_DESCRIPTION: str = "AI 室内设计系统 - 支持文生图、图生图，对接阿里云百炼和火山方舟，使用 RAG 知识库"
    
    # 服务配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # CORS 配置
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # ==================== 阿里云百炼配置 (必需) ====================
    # 获取 API Key: https://dashscope.console.aliyun.com/
    # 获取知识库 ID: https://bailian.console.aliyun.com/
    ALIYUN_BAILIAN_API_KEY: str = os.getenv("ALIYUN_BAILIAN_API_KEY", "")
    ALIYUN_KNOWLEDGE_BASE_ID: str = os.getenv("ALIYUN_KNOWLEDGE_BASE_ID", "")
    ALIYUN_REGION: str = "cn-shanghai"
    
    # 阿里云百炼模型配置
    ALIYUN_TEXT_TO_IMAGE_MODEL: str = "wanx-v1"  # 通义万相
    ALIYUN_IMAGE_TO_IMAGE_MODEL: str = "wanx-v1"
    ALIYUN_BASE_URL: str = "https://dashscope.aliyuncs.com/api/v1"
    
    # ==================== 火山方舟配置 (可选) ====================
    # 获取 API Key: https://www.volcengine.com/product/ark
    VOLCANO_ARK_API_KEY: str = os.getenv("VOLCANO_ARK_API_KEY", "")
    VOLCANO_BASE_URL: str = "https://ark.cn-beijing.volces.com/api/v1"
    
    # 火山方舟模型配置
    VOLCANO_TEXT_TO_IMAGE_MODEL: str = "doubao-vision-pro-32k"  # 豆包视觉
    VOLCANO_IMAGE_TO_IMAGE_MODEL: str = "doubao-vision-pro-32k"
    
    # ==================== 默认 AI 服务商配置 ====================
    # 可选值：aliyun, volcano
    DEFAULT_PROVIDER: str = "aliyun"
    
    # ==================== 图片生成配置 ====================
    DEFAULT_IMAGE_WIDTH: int = 1024
    DEFAULT_IMAGE_HEIGHT: int = 1024
    DEFAULT_NEGATIVE_PROMPT: str = "模糊，低质量，失真，变形，错误的比例"
    MAX_IMAGE_SIZE: int = 2048
    MIN_IMAGE_SIZE: int = 512
    
    # 图生图默认配置
    DEFAULT_STRENGTH: float = 0.7  # 重绘强度 (0-1)
    
    # ==================== RAG 知识库配置 ====================
    RAG_TOP_K: int = 5  # 默认返回相关知识数量
    RAG_TIMEOUT: int = 30  # RAG 查询超时时间 (秒)
    
    # ==================== 文件存储配置 ====================
    UPLOAD_FOLDER: str = "uploads"
    GENERATED_FOLDER: str = "generated"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 最大上传文件大小 10MB
    ALLOWED_EXTENSIONS: set = {"png", "jpg", "jpeg", "gif", "webp"}
    
    # ==================== 设计风格配置 ====================
    SUPPORTED_STYLES: list = [
        "modern",       # 现代风格
        "minimalist",   # 极简风格
        "industrial",   # 工业风格
        "scandinavian", # 北欧风格
        "traditional",  # 传统风格
        "bohemian",     # 波西米亚风格
        "contemporary", # 当代风格
        "rustic"        # 乡村风格
    ]
    
    STYLE_LABELS: dict = {
        "modern": "现代风格",
        "minimalist": "极简风格",
        "industrial": "工业风格",
        "scandinavian": "北欧风格",
        "traditional": "传统风格",
        "bohemian": "波西米亚风格",
        "contemporary": "当代风格",
        "rustic": "乡村风格"
    }
    
    STYLE_DESCRIPTIONS: dict = {
        "modern": "现代简约风格，干净利落的线条，中性色调，时尚家具",
        "minimalist": "极简主义，少即是多，开放空间，简单几何形状",
        "industrial": "工业风格，裸露砖墙，金属装饰，原始材料",
        "scandinavian": "北欧设计，舒适 hygge 氛围，自然光线，温暖木质色调",
        "traditional": "传统经典，优雅细节，丰富纹理，永恒设计",
        "bohemian": "波西米亚混搭，鲜艳色彩，层次纺织品，艺术元素",
        "contemporary": "当代现代，光滑表面，创新材料，精致",
        "rustic": "乡村农舍，再生木材，复古点缀，温馨舒适"
    }
    
    # ==================== 房间类型配置 ====================
    ROOM_TYPES: list = [
        "客厅", "卧室", "厨房", "卫生间", 
        "书房", "餐厅", "阳台", "玄关"
    ]
    
    # ==================== API 超时配置 ====================
    API_TIMEOUT: int = 120  # AI 生成接口超时时间 (秒)
    HTTP_TIMEOUT: int = 30  # 普通 HTTP 请求超时时间 (秒)
    
    # ==================== 日志配置 ====================
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # ==================== 其他配置 ====================
    # 是否启用模拟模式 (当未配置 API Key 时自动启用)
    MOCK_MODE: bool = not (ALIYUN_BAILIAN_API_KEY or VOLCANO_ARK_API_KEY)


# 创建全局配置实例
settings = Settings()


# ==================== 使用说明 ====================
"""
使用方法:
1. 复制此文件为 config.py: cp config.example.py config.py
2. 在 config.py 中修改配置值，或设置环境变量
3. 在代码中导入: from config import settings

环境变量优先级高于配置文件:
- ALIYUN_BAILIAN_API_KEY: 阿里云百炼 API Key
- ALIYUN_KNOWLEDGE_BASE_ID: 阿里云百炼知识库 ID
- VOLCANO_ARK_API_KEY: 火山方舟 API Key

示例:
export ALIYUN_BAILIAN_API_KEY="your-api-key"
export ALIYUN_KNOWLEDGE_BASE_ID="your-knowledge-base-id"
export VOLCANO_ARK_API_KEY="your-volcano-api-key"
"""
