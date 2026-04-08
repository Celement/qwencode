import httpx
from typing import Optional, Dict, Any
import base64

class AIService:
    """AI 图像生成服务 - 调用外部 AI 模型生成室内设计图"""
    
    def __init__(self, api_key: str = "", api_url: str = ""):
        self.api_key = api_key
        self.api_url = api_url or "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    
    async def generate_text_to_image(
        self,
        prompt: str,
        style: str = "modern",
        negative_prompt: str = "blurry, low quality, distorted",
        width: int = 1024,
        height: int = 1024,
        steps: int = 30,
        cfg_scale: float = 7.0
    ) -> Dict[str, Any]:
        """
        文生图：根据文本描述生成室内设计图
        
        Args:
            prompt: 文本描述
            style: 设计风格
            negative_prompt: 负面提示词
            width: 图片宽度
            height: 图片高度
            steps: 采样步数
            cfg_scale: 提示词相关性
            
        Returns:
            包含生成结果的字典
        """
        # 增强提示词 - 从知识库获取优秀提示词进行补充
        enhanced_prompt = self._enhance_prompt(prompt, style)
        
        payload = {
            "text_prompts": [
                {"text": enhanced_prompt, "weight": 1.0},
                {"text": negative_prompt, "weight": -0.5}
            ],
            "cfg_scale": cfg_scale,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": steps,
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        # 模拟生成（实际使用时取消注释并配置真实 API）
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(
        #         self.api_url,
        #         headers=headers,
        #         json=payload,
        #         timeout=60.0
        #     )
        #     result = response.json()
        #     return result
        
        # 返回模拟结果用于演示
        return {
            "success": True,
            "image_url": f"/generated/demo_{style}_{len(prompt)}.png",
            "prompt_used": enhanced_prompt,
            "generation_type": "text-to-image"
        }
    
    async def generate_image_to_image(
        self,
        image_data: str,
        prompt: str,
        style: str = "modern",
        strength: float = 0.7,
        negative_prompt: str = "blurry, low quality, distorted"
    ) -> Dict[str, Any]:
        """
        图生图：基于参考图生成新的设计
        
        Args:
            image_data: Base64 编码的图片数据
            prompt: 文本描述
            style: 设计风格
            strength: 重绘强度 (0-1)
            negative_prompt: 负面提示词
            
        Returns:
            包含生成结果的字典
        """
        enhanced_prompt = self._enhance_prompt(prompt, style)
        
        payload = {
            "text_prompts": [
                {"text": enhanced_prompt, "weight": 1.0},
                {"text": negative_prompt, "weight": -0.5}
            ],
            "init_image": image_data,
            "strength": strength,
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        # 模拟生成
        return {
            "success": True,
            "image_url": f"/generated/demo_img2img_{style}_{len(prompt)}.png",
            "prompt_used": enhanced_prompt,
            "generation_type": "image-to-image"
        }
    
    def _enhance_prompt(self, prompt: str, style: str) -> str:
        """
        从知识库获取优秀提示词，增强用户输入
        
        实际应用中会查询数据库中的知识库
        """
        style_prompts = {
            "modern": "modern minimalist interior design, clean lines, neutral colors, contemporary furniture",
            "minimalist": "minimalist interior, less is more, open space, simple geometric shapes",
            "industrial": "industrial style interior, exposed brick, metal fixtures, raw materials",
            "scandinavian": "scandinavian design, cozy hygge atmosphere, natural light, warm wood tones",
            "traditional": "traditional classic interior, elegant details, rich textures, timeless design",
            "bohemian": "bohemian eclectic interior, vibrant colors, layered textiles, artistic elements",
            "contemporary": "contemporary modern interior, sleek surfaces, innovative materials, sophisticated",
            "rustic": "rustic farmhouse interior, reclaimed wood, vintage accents, warm and inviting"
        }
        
        base_style = style_prompts.get(style.lower(), "")
        if base_style:
            return f"{prompt}, {base_style}, professional interior photography, high detail, 8k"
        return f"{prompt}, professional interior photography, high detail, 8k"
