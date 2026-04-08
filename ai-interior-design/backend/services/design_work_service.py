from sqlalchemy.orm import Session
from models import DesignWork, DesignStyle
from typing import List, Optional

class DesignWorkService:
    """设计作品服务 - 管理公司优秀设计作品"""
    
    @staticmethod
    def add_work(
        db: Session,
        title: str,
        style: str,
        image_url: str,
        description: Optional[str] = None,
        room_type: Optional[str] = None
    ) -> DesignWork:
        """添加新的设计作品"""
        work = DesignWork(
            title=title,
            style=style,
            image_url=image_url,
            description=description,
            room_type=room_type
        )
        db.add(work)
        db.commit()
        db.refresh(work)
        return work
    
    @staticmethod
    def get_by_style(db: Session, style: str) -> List[DesignWork]:
        """根据风格获取设计作品"""
        return db.query(DesignWork).filter(DesignWork.style == style).all()
    
    @staticmethod
    def get_by_room_type(db: Session, room_type: str) -> List[DesignWork]:
        """根据房间类型获取设计作品"""
        return db.query(DesignWork).filter(DesignWork.room_type == room_type).all()
    
    @staticmethod
    def search_works(db: Session, keywords: str, style: Optional[str] = None) -> List[DesignWork]:
        """搜索设计作品"""
        query = db.query(DesignWork).filter(
            (DesignWork.title.ilike(f"%{keywords}%")) |
            (DesignWork.description.ilike(f"%{keywords}%"))
        )
        if style:
            query = query.filter(DesignWork.style == style)
        return query.all()
    
    @staticmethod
    def get_all(db: Session, style: Optional[str] = None) -> List[DesignWork]:
        """获取所有设计作品，可按风格筛选"""
        query = db.query(DesignWork)
        if style:
            query = query.filter(DesignWork.style == style)
        return query.order_by(DesignWork.created_at.desc()).all()
