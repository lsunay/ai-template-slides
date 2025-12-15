import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

import httpx
from pydantic import BaseModel, Field


class SlideContent(BaseModel):
    """Model for individual slide content."""
    title: str = Field(..., description="Title of the slide")
    content: str = Field(..., description="Main content/bullet points of the slide")
    notes: Optional[str] = Field(None, description="Speaker notes for the slide")


class PresentationStructure(BaseModel):
    """Model for complete presentation structure."""
    title: str = Field(..., description="Presentation title")
    subtitle: Optional[str] = Field(None, description="Presentation subtitle")
    slides: list[SlideContent] = Field(..., description="List of slides")


class AIClient(ABC):
    """Abstract base class for AI model clients."""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
    
    @abstractmethod
    def generate_presentation(self, input_text: str, template_config: Dict[str, Any]) -> PresentationStructure:
        """Generate presentation structure from input text using the template."""
        pass


class OpenAIClient(AIClient):
    """Client for OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(base_url=base_url or "https://api.openai.com/v1", api_key=api_key)
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or use --api-key")
    
    def generate_presentation(self, input_text: str, template_config: Dict[str, Any]) -> PresentationStructure:
        """Generate presentation using OpenAI GPT model."""
        system_prompt = template_config.get("system_prompt", "You are a helpful assistant that creates PowerPoint presentations.")
        user_prompt_template = template_config.get("user_prompt_template", "Create a presentation about: {input_text}")
        
        user_prompt = user_prompt_template.format(input_text=input_text)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = httpx.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse the response as JSON
            try:
                # Try to extract JSON from the response
                if "```json" in content:
                    json_start = content.find("```json") + 7
                    json_end = content.find("```", json_start)
                    json_str = content[json_start:json_end].strip()
                elif "```" in content:
                    json_start = content.find("```") + 3
                    json_end = content.find("```", json_start)
                    json_str = content[json_start:json_end].strip()
                else:
                    json_str = content.strip()
                
                presentation_data = json.loads(json_str)
                return PresentationStructure(**presentation_data)
            except (json.JSONDecodeError, KeyError) as e:
                raise ValueError(f"Failed to parse AI response as presentation structure: {e}")
                
        except httpx.HTTPError as e:
            raise ValueError(f"OpenAI API error: {e}")


class OllamaClient(AIClient):
    """Client for local Ollama models."""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__(base_url=base_url or "http://localhost:11434", api_key=api_key)
    
    def generate_presentation(self, input_text: str, template_config: Dict[str, Any]) -> PresentationStructure:
        """Generate presentation using Ollama local model."""
        system_prompt = template_config.get("system_prompt", "You are a helpful assistant that creates PowerPoint presentations.")
        user_prompt_template = template_config.get("user_prompt_template", "Create a presentation about: {input_text}")
        
        user_prompt = user_prompt_template.format(input_text=input_text)
        
        payload = {
            "model": "llama2",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            "format": "json"
        }
        
        try:
            response = httpx.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=120.0
            )
            response.raise_for_status()
            
            result = response.json()
            content = result["message"]["content"]
            
            # Parse the JSON response
            presentation_data = json.loads(content)
            return PresentationStructure(**presentation_data)
            
        except httpx.HTTPError as e:
            raise ValueError(f"Ollama API error: {e}")
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Failed to parse Ollama response as presentation structure: {e}")


class LMStudioClient(AIClient):
    """Client for LM Studio local models."""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__(base_url=base_url or "http://localhost:1234/v1", api_key=api_key)
    
    def generate_presentation(self, input_text: str, template_config: Dict[str, Any]) -> PresentationStructure:
        """Generate presentation using LM Studio local model."""
        system_prompt = template_config.get("system_prompt", "You are a helpful assistant that creates PowerPoint presentations.")
        user_prompt_template = template_config.get("user_prompt_template", "Create a presentation about: {input_text}")
        
        user_prompt = user_prompt_template.format(input_text=input_text)
        
        payload = {
            "model": "local-model",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = httpx.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=120.0
            )
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse the response as JSON
            try:
                # Try to extract JSON from the response
                if "```json" in content:
                    json_start = content.find("```json") + 7
                    json_end = content.find("```", json_start)
                    json_str = content[json_start:json_end].strip()
                elif "```" in content:
                    json_start = content.find("```") + 3
                    json_end = content.find("```", json_start)
                    json_str = content[json_start:json_end].strip()
                else:
                    json_str = content.strip()
                
                presentation_data = json.loads(json_str)
                return PresentationStructure(**presentation_data)
            except (json.JSONDecodeError, KeyError) as e:
                raise ValueError(f"Failed to parse LM Studio response as presentation structure: {e}")
                
        except httpx.HTTPError as e:
            raise ValueError(f"LM Studio API error: {e}")


def create_client(model_type: str, api_key: Optional[str] = None, base_url: Optional[str] = None) -> AIClient:
    """Factory function to create appropriate AI client."""
    if model_type == "openai":
        return OpenAIClient(api_key=api_key, base_url=base_url)
    elif model_type == "ollama":
        return OllamaClient(base_url=base_url)
    elif model_type == "lmstudio":
        return LMStudioClient(base_url=base_url)
    else:
        raise ValueError(f"Unsupported model type: {model_type}. Supported: openai, ollama, lmstudio")