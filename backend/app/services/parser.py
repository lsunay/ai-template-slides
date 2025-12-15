import json
from typing import Dict, Any, Optional

import httpx
from pydantic import BaseModel, Field

from ..core.config import settings


class SlideOutline(BaseModel):
    """Model for slide outline structure."""
    titles: list[str] = Field(..., description="List of slide titles")
    bullets: list[list[str]] = Field(..., description="Bullet points for each slide")


class OutlineParser:
    """Parser for generating slide outlines from text using AI models."""
    
    async def parse(self, text: str, template_config: Dict[str, Any], model: str = "openai") -> SlideOutline:
        """
        Parse text into slide outline using specified AI model.
        
        Args:
            text: Input text to parse
            template_config: Template configuration with prompt templates
            model: AI model to use (openai, ollama)
        
        Returns:
            SlideOutline object with titles and bullets
        """
        if model == "openai":
            return await self._parse_with_openai(text, template_config)
        elif model == "ollama":
            return await self._parse_with_ollama(text, template_config)
        else:
            raise ValueError(f"Unsupported model: {model}")
    
    async def _parse_with_openai(self, text: str, template_config: Dict[str, Any]) -> SlideOutline:
        """Parse text using OpenAI API."""
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key not configured")
        
        system_prompt = template_config.get("system_prompt", "")
        user_prompt_template = template_config.get("user_prompt_template", "{input_text}")
        user_prompt = user_prompt_template.format(input_text=text)
        
        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": settings.openai_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60.0
                )
                response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Extract JSON from response
            json_str = self._extract_json(content)
            outline_data = json.loads(json_str)
            
            return SlideOutline(**outline_data)
            
        except httpx.HTTPError as e:
            raise ValueError(f"OpenAI API error: {e}")
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Failed to parse OpenAI response: {e}")
    
    async def _parse_with_ollama(self, text: str, template_config: Dict[str, Any]) -> SlideOutline:
        """Parse text using local Ollama model."""
        system_prompt = template_config.get("system_prompt", "")
        user_prompt_template = template_config.get("user_prompt_template", "{input_text}")
        user_prompt = user_prompt_template.format(input_text=text)
        
        payload = {
            "model": settings.ollama_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            "format": "json"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.ollama_host}/api/chat",
                    json=payload,
                    timeout=120.0
                )
                response.raise_for_status()
            
            result = response.json()
            content = result["message"]["content"]
            
            # Extract JSON from response
            json_str = self._extract_json(content)
            outline_data = json.loads(json_str)
            
            return SlideOutline(**outline_data)
            
        except httpx.HTTPError as e:
            raise ValueError(f"Ollama API error: {e}")
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Failed to parse Ollama response: {e}")
    
    def _extract_json(self, content: str) -> str:
        """Extract JSON from text response."""
        content = content.strip()
        
        # Try to find JSON code blocks
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            return content[start:end].strip()
        elif "```" in content:
            start = content.find("```") + 3
            end = content.find("```", start)
            return content[start:end].strip()
        
        # Try to find JSON object
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            return content[start:end]
        
        return content