from typing import List, Optional, Dict, Any
import os
import logging

from config import settings

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


class KnowledgeBaseService:
    """知识库服务 - 对接阿里云百炼 RAG 知识库
    
    不再使用数据库存储，而是使用阿里云百炼的知识库进行 RAG 检索
    支持上传文档、查询相关知识、管理知识条目
    """
    
    def __init__(self):
        self.api_key = settings.ALIYUN_BAILIAN_API_KEY
        self.knowledge_base_id = settings.ALIYUN_KNOWLEDGE_BASE_ID
        self.base_url = settings.ALIYUN_BASE_URL
    
    async def query_knowledge(
        self,
        query: str,
        style: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        查询 RAG 知识库获取相关知识
        
        Args:
            query: 查询文本
            style: 设计风格（用于过滤）
            top_k: 返回结果数量
            
        Returns:
            相关知识列表
        """
        if not self.api_key or not self.knowledge_base_id:
            logger.warning("未配置阿里云 API Key 或知识库 ID，返回空结果")
            return []
        
        # 构建查询
        if style:
            full_query = f"{style} 室内设计 {query}"
        else:
            full_query = query
        
        import httpx
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "knowledge_base_id": self.knowledge_base_id,
            "query": full_query,
            "top_k": top_k
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/retrieval",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                result = response.json()
                
                if result.get("code") == 200:
                    documents = result.get("data", {}).get("documents", [])
                    return [
                        {
                            "content": doc.get("content", ""),
                            "score": doc.get("score", 0),
                            "source": doc.get("source", ""),
                            "metadata": doc.get("metadata", {})
                        }
                        for doc in documents
                    ]
                
                logger.error(f"查询 RAG 知识库失败：{result}")
                return []
        except Exception as e:
            logger.error(f"查询 RAG 知识库异常：{e}")
            return []
    
    async def search_prompts(
        self,
        keywords: str,
        style: Optional[str] = None,
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        搜索提示词 - 使用 RAG 语义搜索
        
        Args:
            keywords: 关键词
            style: 风格
            top_k: 返回数量
            
        Returns:
            搜索结果列表
        """
        return await self.query_knowledge(keywords, style, top_k)
    
    async def get_similar_prompts(
        self,
        style: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        获取相似风格的提示词
        
        Args:
            style: 风格
            limit: 数量限制
            
        Returns:
            相似提示词列表
        """
        query = f"{style} 风格室内设计提示词 优秀案例"
        return await self.query_knowledge(query, style, limit)
    
    async def enhance_prompt_with_rag(
        self,
        prompt: str,
        style: str
    ) -> str:
        """
        使用 RAG 知识库增强提示词
        
        Args:
            prompt: 原始提示词
            style: 风格
            
        Returns:
            增强后的提示词
        """
        knowledge = await self.query_knowledge(prompt, style, top_k=3)
        
        if knowledge:
            # 拼接相关知识到提示词
            knowledge_text = " ".join([doc["content"] for doc in knowledge])
            style_desc = self._get_style_description(style)
            return f"{prompt}, {knowledge_text}, {style_desc}, 专业室内摄影，高细节，8k"
        
        # 如果没有 RAG 知识，返回原始提示词
        return prompt
    
    def _get_style_description(self, style: str) -> str:
        """获取风格的详细描述"""
        style_descriptions = {
            "modern": "现代简约风格，干净利落的线条，中性色调，时尚家具",
            "minimalist": "极简主义，少即是多，开放空间，简单几何形状",
            "industrial": "工业风格，裸露砖墙，金属装饰，原始材料",
            "scandinavian": "北欧设计，舒适 hygge 氛围，自然光线，温暖木质色调",
            "traditional": "传统经典，优雅细节，丰富纹理，永恒设计",
            "bohemian": "波西米亚混搭，鲜艳色彩，层次纺织品，艺术元素",
            "contemporary": "当代现代，光滑表面，创新材料，精致",
            "rustic": "乡村农舍，再生木材，复古点缀，温馨舒适"
        }
        return style_descriptions.get(style.lower(), "专业室内摄影，高细节，8k")
    
    async def upload_document(
        self,
        file_path: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        上传文档到知识库
        
        Args:
            file_path: 文件路径
            description: 文件描述
            
        Returns:
            上传结果
        """
        if not self.api_key or not self.knowledge_base_id:
            return {"success": False, "error": "未配置 API Key 或知识库 ID"}
        
        import httpx
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                with open(file_path, 'rb') as f:
                    files = {'file': f}
                    data = {
                        'knowledge_base_id': self.knowledge_base_id,
                        'description': description or ''
                    }
                    
                    response = await client.post(
                        f"{self.base_url}/knowledge/upload",
                        headers=headers,
                        files=files,
                        data=data,
                        timeout=300.0
                    )
                    result = response.json()
                    
                    if result.get("code") == 200:
                        return {"success": True, "data": result.get("data", {})}
                    
                    return {"success": False, "error": result.get("message", "上传失败")}
        except Exception as e:
            logger.error(f"上传文档异常：{e}")
            return {"success": False, "error": str(e)}
    
    async def delete_knowledge(self, document_id: str) -> Dict[str, Any]:
        """
        删除知识库文档
        
        Args:
            document_id: 文档 ID
            
        Returns:
            删除结果
        """
        if not self.api_key or not self.knowledge_base_id:
            return {"success": False, "error": "未配置 API Key 或知识库 ID"}
        
        import httpx
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "knowledge_base_id": self.knowledge_base_id,
            "document_id": document_id
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/knowledge/delete",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                result = response.json()
                
                if result.get("code") == 200:
                    return {"success": True}
                
                return {"success": False, "error": result.get("message", "删除失败")}
        except Exception as e:
            logger.error(f"删除文档异常：{e}")
            return {"success": False, "error": str(e)}
    
    async def list_documents(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        列出知识库中的文档
        
        Args:
            limit: 数量限制
            
        Returns:
            文档列表
        """
        if not self.api_key or not self.knowledge_base_id:
            return []
        
        import httpx
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "knowledge_base_id": self.knowledge_base_id,
            "limit": limit
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/knowledge/list",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                result = response.json()
                
                if result.get("code") == 200:
                    return result.get("data", {}).get("documents", [])
                
                return []
        except Exception as e:
            logger.error(f"列出文档异常：{e}")
            return []
