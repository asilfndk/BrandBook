# BrandBook Web UI - Quick Start Guide

## Starting the Application

1. **Activate virtual environment** (if not already active):
```bash
source .venv/bin/activate
```

2. **Start the web server**:
```bash
.venv/bin/uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Or simply:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

3. **Open your browser** and navigate to:
```
http://localhost:8000
```

## Using the Web Interface

### Step 1: Enter Company Name
- Type the name of any company (e.g., "HuggingFace", "OpenAI", "Google")
- Click **"🔍 Find Website"** button
- The AI will automatically search and find the company's official website URL

### Step 2: Verify Website URL
- The URL will be automatically filled in
- You can edit it manually if needed
- Make sure it starts with `https://` or `http://`

### Step 3: Generate Brochure
- Click **"✨ Generate Brochure"** button
- Wait while the AI analyzes the website and creates your brochure
- The brochure will appear in real-time with streaming text

## Features

### 🤖 AI-Powered URL Discovery
- Uses LangChain and DuckDuckGo search
- Automatically finds official company websites
- Smart filtering to avoid social media and irrelevant links

### ⚡ Real-Time Streaming
- See the brochure being generated live
- Powered by Server-Sent Events (SSE)
- Smooth, typewriter-style animation

### 🎨 Beautiful Modern UI
- Gradient design
- Responsive layout
- Smooth animations
- Mobile-friendly

### 📄 Professional Brochures
- Analyzes company landing page
- Extracts relevant information from About, Careers, and other pages
- Creates comprehensive markdown-formatted brochures
- Includes company culture, customers, and career information

## API Endpoints

The FastAPI backend provides these RESTful endpoints:

### `GET /`
- Returns the main web interface

### `POST /api/find-url`
- **Body**: `company_name` (form data)
- **Returns**: `{"success": true, "url": "https://..."}`
- Finds the official website URL for a company

### `POST /api/generate-brochure`
- **Body**: `company_name`, `website_url` (form data)
- **Returns**: Server-Sent Events stream
- Generates and streams the brochure content

### `POST /api/set-model`
- **Body**: `provider` (openai/gemini/ollama), `model_name` (optional)
- **Returns**: `{"success": true, "provider": "...", "model": "..."}`
- Changes the AI model provider

### `GET /api/model-status`
- **Returns**: Current model configuration
- Shows which AI provider and model is active

## Environment Variables

Create a `.env` file with:

```env
# Required for OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Optional for Google Gemini
GOOGLE_API_KEY=your_google_api_key_here
```

## Troubleshooting

### Server won't start
- Make sure port 8000 is not in use
- Check that all dependencies are installed: `uv sync`
- Verify your `.env` file has valid API keys

### URL discovery fails
- Check your internet connection
- The search API might be rate-limited
- Try entering the URL manually

### Brochure generation fails
- Verify your OpenAI API key is valid
- Check you have sufficient API credits
- Make sure the website URL is accessible

## Advanced Usage

### Using Different AI Models

You can programmatically switch between AI providers:

```python
# In Python console or script
import requests

# Switch to Gemini
requests.post('http://localhost:8000/api/set-model', 
              data={'provider': 'gemini', 'model_name': 'gemini-2.5-pro'})

# Switch to Ollama (local)
requests.post('http://localhost:8000/api/set-model', 
              data={'provider': 'ollama', 'model_name': 'deepseek-r1'})
```

### API Integration

You can integrate the brochure generator into your own applications:

```python
import requests

# Find URL
response = requests.post('http://localhost:8000/api/find-url',
                        data={'company_name': 'OpenAI'})
url = response.json()['url']

# Generate brochure
response = requests.post('http://localhost:8000/api/generate-brochure',
                        data={'company_name': 'OpenAI', 'website_url': url},
                        stream=True)

for line in response.iter_lines():
    if line:
        # Process streaming data
        print(line.decode())
```

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **AI**: LangChain, OpenAI GPT-4
- **Search**: DuckDuckGo API via ddgs package
- **Scraping**: BeautifulSoup4
- **Markdown**: Marked.js for rendering

## Performance Tips

1. **Use OpenAI GPT-4** for best quality results
2. **Ollama (local)** for privacy and unlimited usage
3. **Gemini** for cost-effective alternative
4. Keep brochures under 2000 characters for faster generation
5. Use caching for frequently requested companies (TODO)

## Next Steps

- Add brochure export (PDF, DOCX)
- Implement caching for URL discoveries
- Add user authentication
- Support multiple brochure templates
- Add batch processing
- Implement rate limiting

---

**Happy Brochure Generating! 🎨📄**
