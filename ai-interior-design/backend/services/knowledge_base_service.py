from sqlalchemy.orm import Session
from models import KnowledgeBase, DesignStyle
from typing import List, Optional

class KnowledgeBaseService:
    """知识库服务 - 管理设计提示词和图稿"""
    
    @staticmethod
    def add_knowledge(
        db: Session,
        style: str,
        prompt: str,
        image_url: str,
        description: Optional[str] = None,
        tags: Optional[str] = None
    ) -> KnowledgeBase:
        """添加新的知识条目"""
        knowledge = KnowledgeBase(
            style=style,
            prompt=prompt,
            image_url=image_url,
            description=description,
            tags=tags
        )
        db.add(knowledge)
        db.commit()
        db.refresh(knowledge)
        return knowledge
    
    @staticmethod
    def get_by_style(db: Session, style: str) -> List[KnowledgeBase]:
        """根据风格获取知识库条目"""
        return db.query(KnowledgeBase).filter(KnowledgeBase.style == style).all()
    
    @staticmethod
    def search_prompts(db: Session, keywords: str, style: Optional[str] = None) -> List[KnowledgeBase]:
        """搜索提示词"""
        query = db.query(KnowledgeBase).filter(
            KnowledgeBase.prompt.ilike(f"%{keywords}%")
        )
        if style:
            query = query.filter(KnowledgeBase.style == style)
        return query.all()
    
    @staticmethod
    def get_similar_prompts(db: Session, style: str, limit: int = 5) -> List[KnowledgeBase]:
        """获取相似风格的提示词用于辅助生成"""
        return db.query(KnowledgeBase).filter(
            KnowledgeBase.style == style
        ).limit(limit).all()
    
    @staticmethod
    def get_all(db: Session) -> List[KnowledgeBase]:
        """获取所有知识库条目"""
        return db.query(KnowledgeBase).all()
