"""
FastAPI Web Application for BrandBook Generator
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import asyncio
import json
from typing import Optional

# Import our existing modules
from url_finder import find_company_url
from generator import get_brochure_user_prompt, brochure_system_prompt
import generator

# Global state for model configuration
model_initialized = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    global model_initialized
    if not model_initialized:
        try:
            generator.MODEL_PROVIDER = "openai"
            generator.MODEL_NAME = "gpt-5.1"
            from openai import OpenAI
            generator.client = OpenAI()
            model_initialized = True
            print("✓ Model initialized with OpenAI GPT-5.1")
        except Exception as e:
            print(f"⚠️ Model initialization failed: {e}")

    yield

    # Shutdown (if needed)
    print("Shutting down...")


app = FastAPI(
    title="BrandBook Generator",
    description="AI-Powered Company Brochure Generator",
    lifespan=lifespan
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/find-url")
async def find_url(company_name: str = Form(...)):
    """API endpoint to find company URL"""
    try:
        if not model_initialized:
            return {"success": False, "error": "Model not initialized"}

        url = find_company_url(
            company_name,
            generator.MODEL_PROVIDER,
            generator.MODEL_NAME,
            generator.client
        )

        if url:
            return {"success": True, "url": url}
        else:
            return {"success": False, "error": "Could not find URL"}

    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/generate-brochure")
async def generate_brochure(
    company_name: str = Form(...),
    website_url: str = Form(...)
):
    """API endpoint to generate brochure (streaming)"""

    async def generate():
        try:
            # Get the prompt
            user_prompt = get_brochure_user_prompt(company_name, website_url)

            # Create messages
            messages = [
                {"role": "system", "content": brochure_system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            # Stream the response
            if generator.MODEL_PROVIDER == "openai" or generator.MODEL_PROVIDER == "ollama":
                stream = generator.client.chat.completions.create(
                    model=generator.MODEL_NAME,
                    messages=messages,
                    stream=True
                )

                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        yield f"data: {json.dumps({'content': content})}\n\n"
                        await asyncio.sleep(0.01)

            elif generator.MODEL_PROVIDER == "claude":
                # Claude streaming
                stream = generator.call_ai_model(messages, stream=True)

                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        yield f"data: {json.dumps({'content': content})}\n\n"
                        await asyncio.sleep(0.01)

            elif generator.MODEL_PROVIDER == "gemini":
                # Gemini doesn't support streaming in the same way
                model = generator.client.GenerativeModel(generator.MODEL_NAME)
                prompt = f"{brochure_system_prompt}\n\n{user_prompt}"
                response = model.generate_content(prompt)

                # Simulate streaming by sending chunks
                text = response.text
                chunk_size = 50
                for i in range(0, len(text), chunk_size):
                    chunk = text[i:i+chunk_size]
                    yield f"data: {json.dumps({'content': chunk})}\n\n"
                    await asyncio.sleep(0.05)

            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/api/set-model")
async def set_model(
    provider: str = Form(...),
    model_name: Optional[str] = Form(None)
):
    """API endpoint to change AI model"""
    global model_initialized

    try:
        generator.MODEL_PROVIDER = provider

        if provider == "openai":
            generator.MODEL_NAME = model_name or "gpt-5.1"
            from openai import OpenAI
            generator.client = OpenAI()

        elif provider == "gemini":
            generator.MODEL_NAME = model_name or "gemini-2.0-flash"
            import google.generativeai as genai
            import os
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            generator.client = genai

        elif provider == "ollama":
            generator.MODEL_NAME = model_name or "deepseek-r1"
            from openai import OpenAI as OllamaClient
            generator.client = OllamaClient(
                base_url="http://localhost:11434/v1",
                api_key="ollama"
            )

        elif provider == "claude":
            generator.MODEL_NAME = model_name or "claude-sonnet-4.5"
            from anthropic import Anthropic
            import os
            generator.client = Anthropic(
                api_key=os.getenv('ANTHROPIC_API_KEY'))

        model_initialized = True
        return {
            "success": True,
            "provider": generator.MODEL_PROVIDER,
            "model": generator.MODEL_NAME
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/model-status")
async def model_status():
    """Get current model status"""
    if model_initialized:
        return {
            "initialized": True,
            "provider": generator.MODEL_PROVIDER,
            "model": generator.MODEL_NAME
        }
    else:
        return {"initialized": False}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
