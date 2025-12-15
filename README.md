# AI Template Slides 🤖📊

Transform your text content into professional PowerPoint presentations using AI. Upload any text (article, report, blog, bullet list) and get beautifully structured slides in seconds.

## 🎯 New Target (Summary)

Users provide ready-made text content (article, report, blog, bullet list...). The system splits this text into predefined "content templates":
- **Academic** → Introduction, Method, Findings, Conclusion...
- **Pitch Deck** → Problem, Solution, Market, Business Model...
- **Sales Presentation** → Customer Pain, Product, ROI, References...

The splitting is done by high-capacity remote models (OpenAI / Claude / Gemini); local models are optional (not mandatory). The resulting `{titles:[], bullets:[[]]}` object is placed into ready .pptx template files using python-pptx. Output: downloadable .pptx + browser preview.

## 📁 Folder & Data Structure (GitHub Repository)

```
ai-template-slides/
├─ backend/
│  ├─ app/
│  │  ├─ api/               – FastAPI routes
│  │  ├─ core/              – config, logging
│  │  ├─ services/
│  │  │  ├─ parser.py       – parse text to template (remote model)
│  │  │  ├─ renderer.py     – create pptx with python-pptx
│  │  │  └─ ollama_stub.py  – local model option experiments
│  │  ├─ templates/          – each: .pptx + meta.yaml
│  │  │  ├─ academic/
│  │  │  ├─ pitch_deck/
│  │  │  ├─ sales/
│  │  │  └─ …
│  │  └─ main.py
│  ├─ requirements.txt
│  └─ Dockerfile
├─ frontend/
│  ├─ src/
│  │  ├─ components/UploadText.vue
│  │  ├─ components/Preview.vue
│  │  └─ api.ts
│  ├─ package.json
│  └─ vite.config.ts
├─ content_templates/        – JSON schemas (for external model prompts)
│  ├─ academic.json
│  ├─ pitch_deck.json
│  └─ sales.json
├─ docs/                     – example inputs, API documentation
└─ slidegen/                 – CLI package (optional)
```

## 📋 What is a "Content Template"?

Each folder's meta.yaml contains these fields:
```yaml
name: academic
slide_masters:
  - title_slide
  - section_header
  - bullet_slide
placeholders:
  - name: title
    shape_id: 0          # slide.shapes[0] in python-pptx
  - name: content
    shape_id: 1
styles:
  font: Calibri
  primary_color: "#003366"
```

`content_templates/academic.json` is the prompt template sent to the external model:
```json
{
  "role": "system",
  "content": "You are a slide outline extractor. The user will paste an academic paper excerpt. Return ONLY JSON:\n{\n  \"titles\": [\"Introduction\",\"Methodology\",\"Results\",\"Conclusion\"],\n  \"bullets\": [\n      [\"bullet-1\",\"bullet-2\"],\n      [\"bullet-1\",\"bullet-2\"],\n      …\n  ]\n}\nEach bullet max 15 words."
}
```

When user text arrives, the backend:
1. Reads content_templates/academic.json → creates prompt
2. If OPENAI_API_KEY env var exists, POST to OpenAI
3. If not, tries local model via ollama_stub.py
4. Validates returned JSON (Pydantic model)
5. Clones templates/academic/template.pptx file; inserts titles[i] and bullets[i] into each slide
6. Saves → provides download link to user

## 🚀 Example Usage Flow

**User in UI:**
- Pastes 500-2000 word report into text area
- Selects "Academic" from dropdown
- Clicks [Generate] button

**Frontend POST /api/generate**
```json
{
  "text": "...",
  "template": "academic",
  "model": "openai"
}
```

**Backend:**
- Compiles prompt, gets JSON from remote model
- renderer.py → clones template.pptx + inserts content
- Writes output.pptx as /<uuid>.pptx on server

**Frontend:**
- Gets /{uuid}.pptx link
- Download button becomes active
- Shows preview via https://view.officeapps.live.com/… iframe

## 🔧 Local Model Option (Optional)

Pull Ollama with mistral:instruct or llama3:8b.
In ollama_stub.py:
```python
import httpx
async def generate_outline(prompt: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{settings.OLLAMA_HOST}/api/generate",
            json={"model": "mistral:instruct",
                  "prompt": prompt,
                  "format": "json",
                  "stream": False}
        )
    return r.json()
```

Validate with same Pydantic model; if error rate is high, fall back to "remote model".

## ✅ Quick MVP Checklist

- [x] 3 ready .pptx templates (academic, pitch, sales)
- [x] 3 content_templates/*.json prompt templates
- [x] FastAPI /generate + /health endpoints
- [x] Single page React structure: UploadText → Preview → Download
- [x] .env.example (OpenAI key, Ollama host, LM Studio host)
- [x] Docker-compose: app, ollama (optional)
- [x] README with example curl, screenshot, local setup

## 🐳 Docker Support

```bash
# Full stack with Docker Compose
docker-compose up -d

# Development mode
docker-compose -f docker-compose.dev.yml up -d
```

The API will be available at `http://localhost:8000` and frontend at `http://localhost:5173`.

## 🛠️ Local Development

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### CLI Setup (Optional)
```bash
pip install -e .
slidegen --help
```

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- Docker & Docker Compose (optional)

### Quick Start
```bash
git clone https://github.com/lsunay/ai-template-slides.git
cd ai-template-slides

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys

# Run with Docker (recommended)
docker-compose up -d

# Or run locally
cd backend && uvicorn app.main:app --reload
cd frontend && npm run dev
```

## 🎯 API Endpoints

- `POST /api/generate` - Generate presentation from text
- `GET /api/download/{id}` - Download generated presentation
- `GET /api/health` - Health check
- `GET /api/templates` - List available templates
- `GET /api/models` - List available AI models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**%99 vibe coded with KimiK2** 🤖