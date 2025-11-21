# BrandBook - AI-Powered Company Brochure Generator

An intelligent brochure generator that automatically discovers company websites and creates professional marketing materials using AI.

## ✨ Features

- 🌐 **Web UI Interface**: Modern, responsive web application with real-time streaming
- 🤖 **AI-Powered URL Discovery**: Automatically finds company websites using LangChain and DuckDuckGo
- 🎨 **Multiple AI Providers**: Support for OpenAI (GPT-5.1), Anthropic Claude (Sonnet 4.5), Google Gemini (2.0-Flash), and Local Ollama (deepseek-r1)
- 🔍 **Smart Web Scraping**: Intelligently extracts relevant information from company websites
- 📄 **Professional Brochures**: Generates comprehensive brochures in markdown format
- ⚡ **Streaming Output**: Real-time brochure generation with typewriter animation
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/asilfndk/BrandBook.git
cd BrandBook

# Install dependencies using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
# Required for OpenAI
OPENAI_API_KEY=your_openai_key_here

# Optional for Google Gemini
GOOGLE_API_KEY=your_google_key_here

# Optional for Anthropic Claude
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### Running the Application

**Option 1: Web Interface (Recommended)**

```bash
# Start the FastAPI server (use virtual environment Python)
.venv/bin/uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Or with activated virtual environment
source .venv/bin/activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Then open your browser at: **http://localhost:8000**

**Important:** Always use `.venv/bin/uvicorn` to ensure correct Python environment.

**Option 2: Command Line Interface**

```bash
# Use virtual environment Python
.venv/bin/python main.py

# Or with activated virtual environment
source .venv/bin/activate
python main.py
```

## 📖 How It Works

### Web Interface
1. **Select AI Model**: Choose between OpenAI (GPT-5.1), Claude (Sonnet 4.5), Gemini (2.0-Flash), or Ollama (deepseek-r1)
2. **Enter Company Name**: Type any company name (e.g., "HuggingFace", "OpenAI", "Anthropic")
3. **Auto URL Discovery**: Click "Find Website" - AI searches and finds the official URL
4. **Generate Brochure**: Click "Generate Brochure" - Watch as the AI creates your brochure in real-time
5. **View Results**: Professional markdown-formatted brochure with company details

### Command Line
1. **Select AI Model**: Choose between OpenAI, Claude, Gemini, or Ollama
2. **Enter Company Name**: Provide the company name
3. **Automatic Processing**: System finds URL and generates brochure automatically
4. **View Output**: Brochure displayed with formatted markdown

## 🎯 Example Usage

### Web Interface
```
1. Open http://localhost:8000
2. Enter "HuggingFace" in the company name field
3. Click "🔍 Find Website" 
   → Finds: https://huggingface.com
4. Click "✨ Generate Brochure"
   → Streams brochure content in real-time
```

### Command Line
```bash
$ python main.py

=== AI Model Selection ===
1. OpenAI (GPT-5.1)
2. Google Gemini (2.0-Flash)
3. Local Ollama (deepseek-r1)
4. Anthropic Claude (Sonnet 4.5)

Enter your choice (1-4): 1

Enter company name: HuggingFace

🔍 Searching for HuggingFace's website...
✅ Found website: https://huggingface.com

✨ Generating brochure for HuggingFace...
[Brochure content streams here...]
```

## 📁 Project Structure

```
BrandBook/
├── app.py                  # FastAPI web application (main entry point)
├── main.py                 # Command-line interface
├── generator.py            # Core brochure generation logic with AI models
├── scraper.py              # Web scraping utilities (BeautifulSoup)
├── url_finder.py           # Intelligent URL discovery (LangChain + DuckDuckGo)
├── templates/
│   └── index.html         # Web UI template
├── static/                 # Static assets (if needed)
├── .env                   # Environment variables (API keys)
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── README.md              # This file
└── WEB_UI_GUIDE.md        # Web UI documentation
```

## 🔧 API Endpoints (FastAPI)

The web application exposes these REST API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve the web interface |
| `/api/find-url` | POST | Find company website URL |
| `/api/generate-brochure` | POST | Generate brochure (streaming) |
| `/api/set-model` | POST | Change AI model provider |
| `/api/model-status` | GET | Get current model configuration |

### Example API Usage

```python
import requests

# Find company URL
response = requests.post('http://localhost:8000/api/find-url',
                        data={'company_name': 'OpenAI'})
url_data = response.json()  # {'success': True, 'url': 'https://openai.com'}

# Generate brochure with streaming
response = requests.post('http://localhost:8000/api/generate-brochure',
                        data={'company_name': 'OpenAI', 
                              'website_url': 'https://openai.com'},
                        stream=True)

for line in response.iter_lines():
    if line:
        print(line.decode())
```

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **LangChain**: Framework for building AI-powered applications
- **OpenAI API**: GPT-5.1 for content generation
- **Anthropic API**: Claude Sonnet 4.5 for high-quality reasoning
- **Google Gemini**: Gemini 2.0-Flash AI model provider
- **Ollama**: Local LLM support (deepseek-r1)
- **BeautifulSoup4**: HTML parsing and web scraping
- **DDGS**: DuckDuckGo search integration
- **Uvicorn**: ASGI server

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **HTML5/CSS3**: Modern, responsive design
- **Marked.js**: Markdown rendering
- **Server-Sent Events (SSE)**: Real-time streaming

### AI & Search
- **LangChain Core**: Prompt management and AI orchestration
- **LangChain Community**: Tool integrations
- **DuckDuckGo API**: Privacy-focused web search
- **OpenAI GPT Models**: Natural language processing

## ⚙️ Configuration Options

### AI Model Selection

**OpenAI (Default)**
```python
MODEL_PROVIDER = "openai"
MODEL_NAME = "gpt-5.1"
```

**Google Gemini**
```python
MODEL_PROVIDER = "gemini"
MODEL_NAME = "gemini-2.0-flash"
```

**Anthropic Claude**
```python
MODEL_PROVIDER = "claude"
MODEL_NAME = "claude-sonnet-4.5"
```

**Ollama (Local)**
```python
MODEL_PROVIDER = "ollama"
MODEL_NAME = "deepseek-r1"
# Requires Ollama running at http://localhost:11434
```

### Environment Variables

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-...

# Google Gemini Configuration (Optional)
GOOGLE_API_KEY=AIza...

# Anthropic Claude Configuration (Optional)
ANTHROPIC_API_KEY=sk-ant-...

# Server Configuration (Optional)
HOST=0.0.0.0
PORT=8000
```

## 🎨 Web UI Features

### Modern Interface
- ✨ Gradient design with smooth animations
- 🎯 Four-step workflow (Model Selection → Company Name → URL Discovery → Brochure)
- 📊 Real-time status updates
- 🔄 Loading indicators
- ✅ Success/error notifications
- 🤖 AI model selection (OpenAI/Claude/Gemini/Ollama)

### User Experience
- 🚀 One-click URL discovery
- ⚡ Streaming brochure generation
- 📱 Mobile-responsive layout
- ⌨️ Keyboard shortcuts (Enter to submit)
- 🎭 Typewriter animation effect

### Brochure Output
- 📝 Markdown-formatted content
- 🏢 Company overview
- 👥 Customer information
- 💼 Career opportunities
- 🌟 Company culture details

## 🧪 Testing

You can test the application using either the web interface or command line:

### Web Interface Testing
```bash
python -m uvicorn app:app --reload
# Open http://localhost:8000 and test with various companies
```

### Command Line Testing
```bash
python main.py
# Follow the prompts to test URL discovery and brochure generation
```

## 🐛 Troubleshooting

### Common Issues

**Server won't start**
```bash
# Check if port 8000 is already in use
lsof -i :8000

# Kill the process if needed
kill -9 <PID>

# Or use a different port
python -m uvicorn app:app --port 8001
```

**URL Discovery Fails**
- Check internet connection
- Verify DuckDuckGo search is accessible
- Try entering URL manually
- Check for rate limiting

**Brochure Generation Errors**
- Verify API key in `.env` file
- Check API credits/quota
- Ensure website URL is accessible
- Try with a different AI provider

**Module Import Errors**
```bash
# Reinstall dependencies
uv sync

# Or with pip
pip install -r requirements.txt
```

## 📚 Additional Documentation

- **Web UI Guide**: See `WEB_UI_GUIDE.md` for detailed web interface documentation
- **API Documentation**: Access interactive docs at `http://localhost:8000/docs` when running
- **LangChain Docs**: https://python.langchain.com/docs/
- **FastAPI Docs**: https://fastapi.tiangolo.com/

## 🔐 Security Notes

- Never commit `.env` files to version control
- Keep API keys secure and rotate regularly
- Use environment variables for sensitive data
- Consider rate limiting for production deployments
- Validate and sanitize user inputs

## 🚀 Performance Tips

1. **Use OpenAI GPT-5.1** for best overall quality
2. **Claude Sonnet 4.5** for advanced reasoning and analysis
3. **Ollama (local)** for privacy and unlimited usage
4. **Gemini** for cost-effective alternative
4. **Cache URL discoveries** to avoid repeated searches
5. **Implement request queuing** for high traffic
6. **Use CDN** for static assets in production

## 📈 Future Enhancements

- [ ] PDF/DOCX export functionality
- [ ] Brochure templates and themes
- [ ] Multi-language support
- [ ] Batch processing for multiple companies
- [ ] User authentication and saved brochures
- [ ] Caching layer for URL discoveries
- [ ] Analytics dashboard
- [ ] Custom AI prompt templates
- [ ] Integration with CRM systems
- [ ] API rate limiting and quotas

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude models
- LangChain for AI orchestration framework
- FastAPI for the excellent web framework
- DuckDuckGo for privacy-focused search API
- BeautifulSoup for HTML parsing

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting section

---

**Built with ❤️ using AI and Python**

*Generate professional company brochures in seconds, not hours!* 🎨📄
