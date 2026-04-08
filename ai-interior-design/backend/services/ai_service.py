import httpx
from typing import Optional, Dict, Any, List
import base64
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AliyunBailianService:
    """阿里云百炼服务 - 支持文生图、图生图和 RAG 知识库"""
    
    def __init__(self, api_key: str = "", region: str = "cn-shanghai"):
        self.api_key = api_key or os.getenv("ALIYUN_BAILIAN_API_KEY", "")
        self.region = region
        # 阿里云百炼 API 端点
        self.base_url = f"https://dashscope.aliyuncs.com/api/v1"
        # 文生图模型 - 通义万相
        self.text_to_image_model = "wanx-v1"
        # 图生图模型
        self.image_to_image_model = "wanx-v1"
        # RAG 知识库 ID
        self.knowledge_base_id = os.getenv("ALIYUN_KNOWLEDGE_BASE_ID", "")
    
    async def generate_text_to_image(
        self,
        prompt: str,
        style: str = "modern",
        negative_prompt: str = "模糊，低质量，失真，变形",
        width: int = 1024,
        height: int = 1024,
        n: int = 1
    ) -> Dict[str, Any]:
        """
        文生图：使用阿里云百炼通义万相生成图片
        
        Args:
            prompt: 文本描述
            style: 设计风格
            negative_prompt: 负面提示词
            width: 图片宽度
            height: 图片高度
            n: 生成数量
            
        Returns:
            包含生成结果的字典
        """
        if not self.api_key:
            logger.warning("未配置阿里云 API Key，返回模拟结果")
            return self._mock_generate(prompt, style, "text-to-image")
        
        # 增强提示词
        enhanced_prompt = self._enhance_prompt_with_style(prompt, style)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-WorkSpace": "stable-diffusion"
        }
        
        payload = {
            "model": self.text_to_image_model,
            "input": {
                "prompt": enhanced_prompt,
                "negative_prompt": negative_prompt
            },
            "parameters": {
                "size": f"{width}*{height}",
                "n": n,
                "style": self._map_style_to_bailian(style)
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/services/aigc/text2image/image-synthesis",
                    headers=headers,
                    json=payload,
                    timeout=120.0
                )
                result = response.json()
                
                if result.get("code") == 200 or result.get("status") == "SUCCEEDED":
                    images = result.get("output", {}).get("results", [])
                    if images:
                        return {
                            "success": True,
                            "image_url": images[0].get("url", ""),
                            "image_base64": images[0].get("b64", ""),
                            "prompt_used": enhanced_prompt,
                            "generation_type": "text-to-image",
                            "provider": "aliyun-bailian"
                        }
                
                logger.error(f"阿里云百炼文生图失败：{result}")
                return {
                    "success": False,
                    "error": result.get("message", "生成失败"),
                    "generation_type": "text-to-image"
                }
        except Exception as e:
            logger.error(f"调用阿里云百炼文生图异常：{e}")
            return self._mock_generate(prompt, style, "text-to-image")
    
    async def generate_image_to_image(
        self,
        image_data: str,
        prompt: str,
        style: str = "modern",
        strength: float = 0.7,
        negative_prompt: str = "模糊，低质量，失真，变形"
    ) -> Dict[str, Any]:
        """
        图生图：使用阿里云百炼通义万相基于参考图生成
        
        Args:
            image_data: Base64 编码的图片数据或图片 URL
            prompt: 文本描述
            style: 设计风格
            strength: 重绘强度 (0-1)
            negative_prompt: 负面提示词
            
        Returns:
            包含生成结果的字典
        """
        if not self.api_key:
            logger.warning("未配置阿里云 API Key，返回模拟结果")
            return self._mock_generate(prompt, style, "image-to-image")
        
        enhanced_prompt = self._enhance_prompt_with_style(prompt, style)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-WorkSpace": "stable-diffusion"
        }
        
        # 判断是 base64 还是 URL
        init_image = {}
        if image_data.startswith("http"):
            init_image["init_image_url"] = image_data
        else:
            init_image["init_image"] = image_data
        
        payload = {
            "model": self.image_to_image_model,
            "input": {
                "prompt": enhanced_prompt,
                "negative_prompt": negative_prompt,
                **init_image
            },
            "parameters": {
                "strength": strength,
                "style": self._map_style_to_bailian(style)
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/services/aigc/image2image/image-synthesis",
                    headers=headers,
                    json=payload,
                    timeout=120.0
                )
                result = response.json()
                
                if result.get("code") == 200 or result.get("status") == "SUCCEEDED":
                    images = result.get("output", {}).get("results", [])
                    if images:
                        return {
                            "success": True,
                            "image_url": images[0].get("url", ""),
                            "image_base64": images[0].get("b64", ""),
                            "prompt_used": enhanced_prompt,
                            "generation_type": "image-to-image",
                            "provider": "aliyun-bailian"
                        }
                
                logger.error(f"阿里云百炼图生图失败：{result}")
                return {
                    "success": False,
                    "error": result.get("message", "生成失败"),
                    "generation_type": "image-to-image"
                }
        except Exception as e:
            logger.error(f"调用阿里云百炼图生图异常：{e}")
            return self._mock_generate(prompt, style, "image-to-image")
    
    async def query_rag_knowledge(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        查询阿里云百炼 RAG 知识库
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            
        Returns:
            相关知识列表
        """
        if not self.api_key or not self.knowledge_base_id:
            logger.warning("未配置阿里云 API Key 或知识库 ID")
            return []
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "knowledge_base_id": self.knowledge_base_id,
            "query": query,
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
                    return result.get("data", {}).get("documents", [])
                
                logger.error(f"查询 RAG 知识库失败：{result}")
                return []
        except Exception as e:
            logger.error(f"查询 RAG 知识库异常：{e}")
            return []
    
    async def enhance_prompt_with_rag(self, prompt: str, style: str) -> str:
        """
        使用 RAG 知识库增强提示词
        
        Args:
            prompt: 原始提示词
            style: 风格
            
        Returns:
            增强后的提示词
        """
        # 从 RAG 知识库获取相关知识
        query = f"{style} 室内设计 提示词 {prompt}"
        knowledge = await self.query_rag_knowledge(query, top_k=3)
        
        if knowledge:
            # 拼接相关知识到提示词
            knowledge_text = " ".join([doc.get("content", "") for doc in knowledge])
            return f"{prompt}, {knowledge_text}, {self._get_style_description(style)}"
        
        # 如果没有 RAG 知识，使用内置的风格描述
        return self._enhance_prompt_with_style(prompt, style)
    
    def _map_style_to_bailian(self, style: str) -> str:
        """映射风格到阿里云百炼支持的风格"""
        style_mapping = {
            "modern": "现代",
            "minimalist": "极简",
            "industrial": "工业风",
            "scandinavian": "北欧",
            "traditional": "传统",
            "bohemian": "波西米亚",
            "contemporary": "当代",
            "rustic": "乡村"
        }
        return style_mapping.get(style.lower(), "现代")
    
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
    
    def _enhance_prompt_with_style(self, prompt: str, style: str) -> str:
        """使用内置风格描述增强提示词"""
        style_desc = self._get_style_description(style)
        return f"{prompt}, {style_desc}, 专业室内摄影，高细节，8k"
    
    def _mock_generate(self, prompt: str, style: str, gen_type: str) -> Dict[str, Any]:
        """返回模拟结果用于演示"""
        return {
            "success": True,
            "image_url": f"/generated/demo_{gen_type}_{style}_{len(prompt)}.png",
            "prompt_used": self._enhance_prompt_with_style(prompt, style),
            "generation_type": gen_type,
            "provider": "aliyun-bailian-mock"
        }


class VolcanoArkService:
    """火山方舟服务 - 支持文生图、图生图"""
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key or os.getenv("VOLCANO_ARK_API_KEY", "")
        # 火山方舟 API 端点
        self.base_url = "https://ark.cn-beijing.volces.com/api/v1"
        # 文生图模型 - 可灵或豆包视觉理解
        self.text_to_image_model = "doubao-vision-pro-32k"
        self.image_to_image_model = "doubao-vision-pro-32k"
    
    async def generate_text_to_image(
        self,
        prompt: str,
        style: str = "modern",
        negative_prompt: str = "模糊，低质量，失真",
        width: int = 1024,
        height: int = 1024
    ) -> Dict[str, Any]:
        """
        文生图：使用火山方舟模型生成图片
        """
        if not self.api_key:
            logger.warning("未配置火山方舟 API Key，返回模拟结果")
            return self._mock_generate(prompt, style, "text-to-image")
        
        enhanced_prompt = self._enhance_prompt(prompt, style)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.text_to_image_model,
            "prompt": enhanced_prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/images/generations",
                    headers=headers,
                    json=payload,
                    timeout=120.0
                )
                result = response.json()
                
                if "data" in result and len(result["data"]) > 0:
                    return {
                        "success": True,
                        "image_url": result["data"][0].get("url", ""),
                        "prompt_used": enhanced_prompt,
                        "generation_type": "text-to-image",
                        "provider": "volcano-ark"
                    }
                
                logger.error(f"火山方舟文生图失败：{result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "生成失败"),
                    "generation_type": "text-to-image"
                }
        except Exception as e:
            logger.error(f"调用火山方舟文生图异常：{e}")
            return self._mock_generate(prompt, style, "text-to-image")
    
    async def generate_image_to_image(
        self,
        image_data: str,
        prompt: str,
        style: str = "modern",
        strength: float = 0.7
    ) -> Dict[str, Any]:
        """
        图生图：使用火山方舟模型基于参考图生成
        """
        if not self.api_key:
            logger.warning("未配置火山方舟 API Key，返回模拟结果")
            return self._mock_generate(prompt, style, "image-to-image")
        
        enhanced_prompt = self._enhance_prompt(prompt, style)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.image_to_image_model,
            "prompt": enhanced_prompt,
            "image": image_data,
            "strength": strength
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/images/edits",
                    headers=headers,
                    json=payload,
                    timeout=120.0
                )
                result = response.json()
                
                if "data" in result and len(result["data"]) > 0:
                    return {
                        "success": True,
                        "image_url": result["data"][0].get("url", ""),
                        "prompt_used": enhanced_prompt,
                        "generation_type": "image-to-image",
                        "provider": "volcano-ark"
                    }
                
                logger.error(f"火山方舟图生图失败：{result}")
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "生成失败"),
                    "generation_type": "image-to-image"
                }
        except Exception as e:
            logger.error(f"调用火山方舟图生图异常：{e}")
            return self._mock_generate(prompt, style, "image-to-image")
    
    def _enhance_prompt(self, prompt: str, style: str) -> str:
        """增强提示词"""
        style_prompts = {
            "modern": "现代简约室内设计，干净线条，中性色，当代家具",
            "minimalist": "极简主义室内，少即是多，开放空间，简单几何",
            "industrial": "工业风格室内，裸露砖墙，金属装置，原始材料",
            "scandinavian": "北欧设计，舒适 hygge 氛围，自然光，温暖木色",
            "traditional": "传统经典室内，优雅细节，丰富纹理，永恒设计",
            "bohemian": "波西米亚折衷室内，鲜艳色彩，分层纺织品，艺术元素",
            "contemporary": "当代现代室内，光滑表面，创新材料，精致",
            "rustic": "乡村农舍室内，再生木材，复古点缀，温馨 inviting"
        }
        
        base_style = style_prompts.get(style.lower(), "")
        if base_style:
            return f"{prompt}, {base_style}, 专业室内摄影，高细节，8k"
        return f"{prompt}, 专业室内摄影，高细节，8k"
    
    def _mock_generate(self, prompt: str, style: str, gen_type: str) -> Dict[str, Any]:
        """返回模拟结果"""
        return {
            "success": True,
            "image_url": f"/generated/demo_{gen_type}_{style}_{len(prompt)}.png",
            "prompt_used": self._enhance_prompt(prompt, style),
            "generation_type": gen_type,
            "provider": "volcano-ark-mock"
        }
