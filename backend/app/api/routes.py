from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ..core.config import settings
from ..services.parser import OutlineParser, SlideOutline
from ..services.renderer import PresentationRenderer


router = APIRouter()
parser = OutlineParser()
renderer = PresentationRenderer()


class GenerateRequest(BaseModel):
    text: str
    template: str = "academic"
    model: str = "openai"


class GenerateResponse(BaseModel):
    success: bool
    message: str
    presentation_id: Optional[str] = None
    download_url: Optional[str] = None


@router.post("/generate", response_model=GenerateResponse)
async def generate_presentation(request: GenerateRequest):
    """
    Generate a PowerPoint presentation from text using AI.
    
    - **text**: Input text content
    - **template**: Template name (academic, pitch_deck, sales)
    - **model**: AI model to use (openai, ollama, lmstudio)
    """
    try:
        # Load template configuration
        template_config_path = Path("content_templates") / f"{request.template}.json"
        if not template_config_path.exists():
            raise HTTPException(
                status_code=400,
                detail=f"Template '{request.template}' not found"
            )
        
        import json
        template_config = json.loads(template_config_path.read_text(encoding="utf-8"))
        
        # Generate outline using AI
        outline = await parser.parse(
            text=request.text,
            template_config=template_config,
            model=request.model
        )
        
        # Get template file
        template_file = Path("backend/app/templates") / request.template / "template.pptx"
        if not template_file.exists():
            raise HTTPException(
                status_code=400,
                detail=f"Template file for '{request.template}' not found"
            )
        
        # Render presentation
        presentation_path = renderer.render(
            template_path=template_file,
            outline=outline.dict(),
            presentation_title=outline.titles[0] if outline.titles else "Presentation"
        )
        
        # Generate download URL
        presentation_id = presentation_path.stem
        download_url = f"/api/download/{presentation_id}"
        
        return GenerateResponse(
            success=True,
            message="Presentation generated successfully",
            presentation_id=presentation_id,
            download_url=download_url
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{presentation_id}")
async def download_presentation(presentation_id: str):
    """Download a generated presentation."""
    file_path = Path(settings.output_dir) / f"{presentation_id}.pptx"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Presentation not found")
    
    return FileResponse(
        path=file_path,
        filename=f"presentation_{presentation_id}.pptx",
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "ai-template-slides-api",
        "templates": ["academic", "pitch_deck", "sales"]
    }


@router.get("/templates")
async def list_templates():
    """List available templates."""
    templates_dir = Path("content_templates")
    if not templates_dir.exists():
        return {"templates": []}
    
    template_files = list(templates_dir.glob("*.json"))
    templates = []
    
    for template_file in template_files:
        import json
        config = json.loads(template_file.read_text(encoding="utf-8"))
        templates.append({
            "name": template_file.stem,
            "description": config.get("description", ""),
            "display_name": config.get("name", template_file.stem)
        })
    
    return {"templates": templates}


@router.get("/models")
async def list_models():
    """List available AI models."""
    models = [
        {
            "name": "openai",
            "description": "OpenAI GPT models (requires API key)",
            "available": bool(settings.openai_api_key)
        },
        {
            "name": "ollama",
            "description": "Local Ollama models",
            "available": True
        },
        {
            "name": "lmstudio",
            "description": "LM Studio local models",
            "available": True
        }
    ]
    
    return {"models": models}