# A full business solution - Company Brochure Generator
# Creates a brochure for a company to be used for prospective clients, investors and potential recruits

# imports
import os
import json
from dotenv import load_dotenv
from IPython.display import Markdown, display, update_display
from scraper import fetch_website_links, fetch_website_contents
from openai import OpenAI

# Initialize and constants
load_dotenv(override=True)

# Global variables for model configuration
MODEL_PROVIDER = None
MODEL_NAME = None
client = None


def initialize_model():
    """Initialize the AI model based on user selection"""
    global MODEL_PROVIDER, MODEL_NAME, client

    print("\n=== AI Model Selection ===")
    print("Please choose your AI provider:")
    print("1. OpenAI (GPT-5.1)")
    print("2. Google Gemini (2.5-pro)")
    print("3. Local Ollama (deepseek-r1)")

    while True:
        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            MODEL_PROVIDER = "openai"
            MODEL_NAME = "gpt-5.1"
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key and api_key.startswith('sk-') and len(api_key) > 10:
                print("✓ OpenAI API key looks good")
                client = OpenAI()
                break
            else:
                print(
                    "⚠ Warning: OpenAI API key might be invalid. Please check your .env file")
                retry = input("Continue anyway? (y/n): ").strip().lower()
                if retry == 'y':
                    client = OpenAI()
                    break

        elif choice == "2":
            MODEL_PROVIDER = "gemini"
            MODEL_NAME = "gemini-2.5-pro"
            try:
                import google.generativeai as genai
                api_key = os.getenv('GOOGLE_API_KEY')
                if api_key:
                    genai.configure(api_key=api_key)
                    client = genai
                    print("✓ Google Gemini configured successfully")
                    break
                else:
                    print("⚠ Error: GOOGLE_API_KEY not found in .env file")
            except ImportError:
                print("⚠ Error: google-generativeai package not installed")
                print("Install it with: uv add google-generativeai")

        elif choice == "3":
            MODEL_PROVIDER = "ollama"
            MODEL_NAME = "deepseek-r1"
            try:
                from openai import OpenAI as OllamaClient
                client = OllamaClient(
                    base_url="http://localhost:11434/v1",
                    api_key="ollama"  # Ollama doesn't require API key
                )
                print("✓ Ollama configured successfully")
                print("⚠ Make sure Ollama is running and deepseek-r1 model is installed")
                break
            except Exception as e:
                print(f"⚠ Error configuring Ollama: {e}")

        else:
            print("Invalid choice. Please enter 1, 2, or 3")

    print(f"\n✓ Selected: {MODEL_PROVIDER.upper()} - {MODEL_NAME}")
    return MODEL_PROVIDER, MODEL_NAME, client


# Global variables will be initialized when initialize_model() is called
# Do not auto-initialize to avoid duplicate prompts when importing


# First step: Have AI figure out which links are relevant
link_system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You must respond in English only.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""


def get_links_user_prompt(url):
    user_prompt = f"""
Here is the list of links on the website {url} -
Please decide which of these are relevant web links for a brochure about the company, 
respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):

"""
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt


def call_ai_model(messages, json_mode=False, stream=False):
    """Universal function to call any AI model"""
    if MODEL_PROVIDER == "openai":
        params = {
            "model": MODEL_NAME,
            "messages": messages,
            "stream": stream
        }
        if json_mode:
            params["response_format"] = {"type": "json_object"}
        return client.chat.completions.create(**params)

    elif MODEL_PROVIDER == "gemini":
        # Convert messages to Gemini format
        model = client.GenerativeModel(MODEL_NAME)
        prompt = "\n\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in messages])
        if json_mode:
            prompt += "\n\nRespond in valid JSON format only."
        response = model.generate_content(prompt)
        # Create OpenAI-compatible response object

        class GeminiResponse:
            class Choice:
                class Message:
                    def __init__(self, content):
                        self.content = content

                def __init__(self, content):
                    self.message = self.Message(content)

            def __init__(self, content):
                self.choices = [self.Choice(content)]
        return GeminiResponse(response.text)

    elif MODEL_PROVIDER == "ollama":
        params = {
            "model": MODEL_NAME,
            "messages": messages,
            "stream": stream
        }
        if json_mode:
            params["response_format"] = {"type": "json_object"}
        return client.chat.completions.create(**params)


def select_relevant_links(url):
    print(
        f"Selecting relevant links for {url} by calling {MODEL_PROVIDER.upper()} {MODEL_NAME}")
    response = call_ai_model(
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(url)}
        ],
        json_mode=True
    )
    result = response.choices[0].message.content
    links = json.loads(result)
    print(f"Found {len(links['links'])} relevant links")
    return links


# Second step: make the brochure!
def fetch_page_and_all_relevant_links(url):
    contents = fetch_website_contents(url)
    relevant_links = select_relevant_links(url)
    result = f"## Landing Page:\n\n{contents}\n## Relevant Links:\n"
    for link in relevant_links['links']:
        result += f"\n\n### Link: {link['type']}\n"
        result += fetch_website_contents(link["url"])
    return result


brochure_system_prompt = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
You must respond in English only, regardless of the website's language.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
"""

# Or uncomment the lines below for a more humorous brochure:
# brochure_system_prompt = """
# You are an assistant that analyzes the contents of several relevant pages from a company website
# and creates a short, humorous, entertaining, witty brochure about the company for prospective customers, investors and recruits.
# Respond in markdown without code blocks.
# Include details of company culture, customers and careers/jobs if you have the information.
# """


def get_brochure_user_prompt(company_name, url):
    user_prompt = f"""
You are looking at a company called: {company_name}
Here are the contents of its landing page and other relevant pages;
use this information to build a short brochure of the company in markdown without code blocks.\n\n
"""
    user_prompt += fetch_page_and_all_relevant_links(url)
    user_prompt = user_prompt[:5_000]  # Truncate if more than 5,000 characters
    return user_prompt


def create_brochure(company_name, url):
    response = call_ai_model(
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(
                company_name, url)}
        ]
    )
    result = response.choices[0].message.content
    display(Markdown(result))


def stream_brochure(company_name, url):
    """Stream brochure with typewriter animation"""
    if MODEL_PROVIDER == "gemini":
        # Gemini doesn't support streaming in the same way, so we'll just display the full result
        print("Note: Streaming not available for Gemini, generating full response...")
        create_brochure(company_name, url)
        return

    stream = call_ai_model(
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(
                company_name, url)}
        ],
        stream=True
    )
    response = ""
    display_handle = display(Markdown(""), display_id=True)
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        update_display(Markdown(response),
                       display_id=display_handle.display_id)


# Example usage:
if __name__ == "__main__":
    from url_finder import find_company_url

    # Initialize model when running directly
    initialize_model()

    # Get user input
    company_name = input(
        "Enter company name or website (e.g., HuggingFace, OpenAI): ").strip()

    # Automatically find the website URL using LangChain
    print("\n🔍 Searching for website URL...")
    website_url = find_company_url(
        company_name, MODEL_PROVIDER, MODEL_NAME, client)

    # If automatic search fails, ask for manual input
    if not website_url:
        website_url = input(
            "Enter website URL manually (e.g., https://huggingface.co): ").strip()

        # Add https:// if not present
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url

    # Stream brochure with animation
    stream_brochure(company_name, website_url)
