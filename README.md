# AI Template Slides 🤖📊

Generate professional PowerPoint presentations using AI. Transform your text content into beautifully structured slides with multiple AI model support.

## 🚀 Features

### CLI Tool (`kimi-cli`)
- **Multiple AI Models**: OpenAI GPT, Ollama (local), LM Studio (local)
- **Smart Templates**: Academic, Pitch Deck, Sales presentations
- **Flexible Input**: Read from files or stdin
- **Multiple Output Formats**: PPTX files or base64 stdout
- **Rich CLI Interface**: Progress indicators and colored output

### Backend API
- **FastAPI** powered REST API
- **Docker** support for easy deployment
- **Frontend** React application (in development)

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- Docker & Docker Compose (optional)

### CLI Installation

```bash
# Clone the repository
git clone https://github.com/lsunay/ai-template-slides.git
cd ai-template-slides

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install CLI package
pip install -e .
```

### Backend Installation

```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Or using Docker
docker-compose up -d
```

### Frontend Installation

```bash
cd frontend
npm install
npm run dev
```

## 🎯 Usage

### CLI Usage

#### Basic Commands
```bash
# Show help
kimi-cli --help

# List available models
kimi-cli models

# List available templates
kimi-cli templates
```

#### Generate Presentations

```bash
# From file with OpenAI
kimi-cli generate \
  --input content.txt \
  --template academic \
  --model openai \
  --api-key YOUR_API_KEY \
  --output presentation.pptx

# From stdin with Ollama (local)
echo "My presentation content" | kimi-cli generate \
  --template pitch_deck \
  --model ollama \
  --output startup_pitch.pptx

# Output to stdout as base64
kimi-cli generate \
  --input content.txt \
  --template sales \
  --model lmstudio \
  --output -
```

#### CLI Options
- `--input, -i`: Input file path (use `-` for stdin)
- `--template, -t`: Template name (academic, pitch_deck, sales)
- `--model, -m`: AI model (openai, ollama, lmstudio)
- `--api-key`: API key for OpenAI
- `--base-url`: Custom base URL for local models
- `--output, -o`: Output file path (use `-` for base64 stdout)
- `--verbose, -v`: Enable verbose output

### Backend API Usage

```bash
# Start the backend
cd backend
uvicorn app.main:app --reload

# API will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Docker Usage

```bash
# Full stack with Docker Compose
docker-compose up -d

# Development mode
docker-compose -f docker-compose.dev.yml up -d
```

## 🏗️ Architecture

```
ai-template-slides/
├── kimi_cli/                 # CLI Package
│   ├── __init__.py
│   ├── main.py              # Typer CLI application
│   ├── parser.py            # AI model clients
│   └── renderer.py          # PowerPoint generation
├── content_templates/       # Presentation templates
│   ├── academic.json
│   ├── pitch_deck.json
│   └── sales.json
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── services/
│   │   └── templates/
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/
│   │   └── pages/
│   ├── package.json
│   └── vite.config.ts
├── pyproject.toml          # CLI package configuration
└── docker-compose.yml
```

## 🔧 Configuration

### Environment Variables

```bash
# For OpenAI
export OPENAI_API_KEY="your-api-key"

# For custom endpoints
export OLLAMA_BASE_URL="http://localhost:11434"
export LMSTUDIO_BASE_URL="http://localhost:1234/v1"
```

### Custom Templates

Create JSON files in `content_templates/` directory:

```json
{
  "name": "My Template",
  "description": "Custom template description",
  "system_prompt": "You are a presentation creator...",
  "user_prompt_template": "Create a presentation about: {input_text}"
}
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
black kimi_cli/
isort kimi_cli/

# Type checking
mypy kimi_cli/
```

### Project Structure

- **CLI Package**: `kimi_cli/` - Standalone CLI tool
- **Backend**: `backend/` - FastAPI REST API
- **Frontend**: `frontend/` - React web interface
- **Templates**: `content_templates/` - JSON template files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Typer](https://typer.tiangolo.com/) - For the amazing CLI framework
- [python-pptx](https://python-pptx.readthedocs.io/) - For PowerPoint generation
- [FastAPI](https://fastapi.tiangolo.com/) - For the backend API
- [Pydantic](https://pydantic-docs.helpmanual.io/) - For data validation

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Happy Presenting!** 🎉