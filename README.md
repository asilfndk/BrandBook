# BrandBook - AI-Powered Company Brochure Generator

An intelligent brochure generator that automatically discovers company websites and creates professional marketing materials using AI.

## ✨ Features

- 🌐 **Web UI Interface**: Modern, responsive web application with real-time streaming
- 🤖 **AI-Powered URL Discovery**: Automatically finds company websites using LangChain and DuckDuckGo
- 🎨 **Multiple AI Providers**: Support for OpenAI (GPT-4/5), Google Gemini (2.5-pro), and Local Ollama (deepseek-r1)
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
```

### Running the Application

**Option 1: Web Interface (Recommended)**

```bash
# Start the FastAPI server
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Or simply
python app.py
```

Then open your browser at: **http://localhost:8000**

**Option 2: Command Line Interface**

```bash
python main.py
```

## 📖 How It Works

### Web Interface
1. **Enter Company Name**: Type any company name (e.g., "HuggingFace", "OpenAI", "Anthropic")
2. **Auto URL Discovery**: Click "Find Website" - AI searches and finds the official URL
3. **Generate Brochure**: Click "Generate Brochure" - Watch as the AI creates your brochure in real-time
4. **View Results**: Professional markdown-formatted brochure with company details

### Command Line
1. **Select AI Model**: Choose between OpenAI, Gemini, or Ollama
2. **Enter Company Name**: Provide the company name
3. **Automatic Processing**: System finds URL and generates brochure automatically
4. **View Output**: Brochure displayed with formatted markdown

## 🎯 Example Usage

### Web Interface
```
1. Open http://localhost:8000
2. Enter "HuggingFace" in the company name field
3. Click "🔍 Find Website" 
   → Finds: https://huggingface.co
4. Click "✨ Generate Brochure"
   → Streams brochure content in real-time
```

### Command Line
```bash
$ python main.py

=== AI Model Selection ===
1. OpenAI (GPT-5)
2. Google Gemini (2.5-pro)
3. Local Ollama (deepseek-r1)

Enter your choice (1-3): 1

Enter company name: HuggingFace

🔍 Searching for HuggingFace's website...
✅ Found website: https://huggingface.co

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
├── static/
│   └── style.css          # Additional styles
├── example.py             # Usage examples
├── test_url_finder.py     # URL finder tests
├── .env                   # Environment variables (API keys)
├── pyproject.toml         # Project dependencies
└── README.md              # This file
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
- **OpenAI API**: GPT-4/5 for content generation
- **Google Gemini**: Alternative AI model provider
- **Ollama**: Local LLM support
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
MODEL_NAME = "gpt-5"  # or "gpt-4"
```

**Google Gemini**
```python
MODEL_PROVIDER = "gemini"
MODEL_NAME = "gemini-2.5-pro"
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

# Server Configuration (Optional)
HOST=0.0.0.0
PORT=8000
```

## 🎨 Web UI Features

### Modern Interface
- ✨ Gradient design with smooth animations
- 🎯 Three-step workflow (Company → URL → Brochure)
- 📊 Real-time status updates
- 🔄 Loading indicators
- ✅ Success/error notifications

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

### Test URL Finder
```bash
python test_url_finder.py
```

This will test URL discovery for multiple companies:
- HuggingFace
- OpenAI
- Anthropic
- Google
- Microsoft

### Run Examples
```bash
python example.py
```

Interactive example with company selection and brochure generation.

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

1. **Use OpenAI GPT-5** for best quality results
2. **Ollama (local)** for privacy and unlimited usage
3. **Gemini** for cost-effective alternative
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

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models
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