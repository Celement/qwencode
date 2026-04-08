from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

class DesignStyle(enum.Enum):
    MODERN = "modern"
    MINIMALIST = "minimalist"
    INDUSTRIAL = "industrial"
    SCANDINAVIAN = "scandinavian"
    TRADITIONAL = "traditional"
    BOHEMIAN = "bohemian"
    CONTEMPORARY = "contemporary"
    RUSTIC = "rustic"

class KnowledgeBase(Base):
    """知识库 - 存储优秀设计提示词和设计图稿链接"""
    __tablename__ = "knowledge_base"
    
    id = Column(Integer, primary_key=True, index=True)
    style = Column(Enum(DesignStyle), nullable=False)
    prompt = Column(Text, nullable=False)  # 设计提示词
    image_url = Column(String, nullable=False)  # 设计图稿链接
    description = Column(Text)
    tags = Column(String)  # 逗号分隔的标签
    created_at = Column(DateTime, default=datetime.utcnow)
    
    class Config:
        use_enum_values = True

class DesignWork(Base):
    """公司优秀设计作品"""
    __tablename__ = "design_works"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    style = Column(Enum(DesignStyle), nullable=False)
    image_url = Column(String, nullable=False)
    description = Column(Text)
    room_type = Column(String)  # 客厅、卧室、厨房等
    created_at = Column(DateTime, default=datetime.utcnow)
    
    class Config:
        use_enum_values = True

class GeneratedImage(Base):
    """生成的图片记录"""
    __tablename__ = "generated_images"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    style = Column(Enum(DesignStyle))
    image_url = Column(String, nullable=False)
    generation_type = Column(String)  # text-to-image 或 image-to-image
    reference_image_url = Column(String)  # 图生图的参考图
    created_at = Column(DateTime, default=datetime.utcnow)
    
    class Config:
        use_enum_values = True
