"""
URL Finder Module
Uses LangChain and web search to automatically find company website URLs
"""

import os
import re
from dotenv import load_dotenv
from ddgs import DDGS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv(override=True)


def extract_domain_from_results(results):
    """
    Extract the most likely company domain from search results

    Args:
        results: List of search results

    Returns:
        str: Best matching domain URL or None
    """
    # Common patterns for official websites
    potential_urls = []

    # Skip these domains
    skip_domains = ['wikipedia.org', 'twitter.com', 'x.com', 'facebook.com',
                    'linkedin.com', 'youtube.com', 'stackoverflow.com',
                    'github.com', 'reddit.com', 'instagram.com', 'tiktok.com',
                    'sotwe.com', '1319lm.top', 'medium.com', 'quora.com']

    for result in results:
        href = result.get('href', '')
        title = result.get('title', '').lower()

        # Skip unwanted domains
        if any(skip in href for skip in skip_domains):
            continue

        # Check if URL looks like a main domain
        if href and href.startswith('http'):
            # Extract base domain
            match = re.search(r'https?://(?:www\.)?([^/]+)', href)
            if match:
                domain = match.group(1)
                # Count path segments - prefer URLs with fewer segments (likely homepage)
                path_count = href.rstrip('/').count('/')

                # Calculate a score for this URL
                score = 0

                # Prefer root domain URLs
                if path_count == 2:  # https://domain.com (has 2 slashes)
                    score += 10
                elif path_count == 3:  # https://domain.com/something
                    score += 5

                # Prefer .com and .co domains (higher priority)
                if '.com' in href:
                    score += 5
                elif '.co/' in href or href.endswith('.co'):
                    score += 4
                elif '.io' in href:
                    score += 2
                elif '.ai' in href:
                    score += 2

                # Penalize deep paths
                score -= path_count

                # Clean URL
                clean_url = href.split('?')[0].rstrip('/')
                if not clean_url.endswith(('.html', '.htm', '.php')):
                    potential_urls.append((score, clean_url, href))

    # Sort by score (descending)
    potential_urls.sort(reverse=True, key=lambda x: x[0])

    # Return the highest scored URL
    if potential_urls:
        best_url = potential_urls[0][1]
        # Make sure we return the base domain if possible
        match = re.search(r'(https?://(?:www\.)?[^/]+)', best_url)
        if match:
            base = match.group(1)
            # Check if this is just a root domain
            if best_url == base or best_url == base + '/':
                return base
            # If it has one path segment, keep it
            if best_url.count('/') <= 3:
                return best_url
            return base
        return best_url

    return None


def find_company_url(company_name, model_provider="openai", model_name="gpt-5", client=None):
    """
    Use LangChain to find the official website URL for a given company name

    Args:
        company_name: Name of the company or website
        model_provider: AI provider (openai, gemini, ollama)
        model_name: Model name to use
        client: Pre-configured AI client

    Returns:
        str: The official website URL
    """
    print(f"\n🔍 Searching for {company_name}'s website...")

    try:
        # Initialize DuckDuckGo search with the correct API
        ddgs = DDGS()

        # Search for the company - try multiple search strategies
        all_results = []

        # Strategy 1: Try with common domain extensions FIRST
        company_clean = company_name.lower().replace(' ', '').replace('-', '')
        # Try .co and .com first as they're most common
        for tld in ['.com', '.co', '.ai', '.io']:
            try:
                # Try site: operator for more accurate results
                domain_guess = f"{company_clean}{tld}"
                results = ddgs.text(f"site:{domain_guess}", max_results=2)
                all_results.extend(results)
                print(f"  📍 Searched: site:{domain_guess}")
            except:
                pass

            try:
                # Also try without site: operator
                results = ddgs.text(domain_guess, max_results=2)
                all_results.extend(results)
            except:
                pass

        # Strategy 2: Direct company name search
        try:
            results = ddgs.text(company_name, max_results=5)
            all_results.extend(results)
            print(f"  📍 Searched: {company_name}")
        except:
            pass

        # Strategy 3: Try with "official website"
        try:
            results = ddgs.text(
                f"{company_name} official website", max_results=3)
            all_results.extend(results)
            print(f"  📍 Searched: {company_name} official website")
        except:
            pass

        if not all_results:
            raise ValueError("No search results found")

        # First, try to extract a good URL directly from results
        direct_url = extract_domain_from_results(all_results)
        if direct_url:
            print(f"✅ Found website: {direct_url}")
            return direct_url

        # If direct extraction fails, use LLM
        # Format search results for LLM
        search_results = ""
        for idx, result in enumerate(all_results[:8], 1):
            search_results += f"{idx}. {result.get('title', 'No title')}\n"
            search_results += f"   URL: {result.get('href', 'No URL')}\n"
            search_results += f"   Description: {result.get('body', 'No description')[:150]}\n\n"

        # Use LLM to extract the most likely URL from search results
        print(f"📊 Analyzing {len(all_results)} search results with AI...")
        if model_provider == "openai":
            llm = ChatOpenAI(model=model_name, temperature=0)
        elif model_provider == "ollama":
            from langchain_community.llms import Ollama
            llm = Ollama(model=model_name, base_url="http://localhost:11434")
        elif model_provider == "gemini":
            # For Gemini, use direct approach without LangChain LLM
            # Just return the first result's URL
            if all_results and len(all_results) > 0:
                url = all_results[0].get('href', '')
                if url:
                    print(f"✅ Found website: {url}")
                    return url
            raise ValueError("No valid URL found in search results")
        else:
            # Fallback to OpenAI
            llm = ChatOpenAI(model="gpt-5", temperature=0)

        # Create prompt template
        template = """Based on the following search results, extract the official website URL for {company_name}.
        
Search Results:
{search_results}

Instructions:
- Return ONLY the URL (e.g., https://example.com)
- Choose the most official-looking domain
- Do not include any explanation, just the URL
- If multiple URLs found, choose the main one
- The URL should start with http:// or https://

Official Website URL:"""

        prompt = PromptTemplate(
            input_variables=["company_name", "search_results"],
            template=template
        )

        chain = prompt | llm

        # Get the URL from LLM
        response = chain.invoke({
            "company_name": company_name,
            "search_results": search_results
        })

        # Extract URL from response
        if hasattr(response, 'content'):
            url = response.content.strip()
        else:
            url = str(response).strip()

        # Clean up the URL
        url = url.replace('"', '').replace("'", "").strip()

        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            if '.' in url:
                url = 'https://' + url
            else:
                raise ValueError("Invalid URL format")

        print(f"✅ Found website: {url}")
        return url

    except Exception as e:
        print(f"⚠️ Error finding URL: {e}")
        print("💡 Falling back to manual input...")
        return None


def find_url_with_duckduckgo(company_name):
    """
    Simple fallback method using DuckDuckGo search directly

    Args:
        company_name: Name of the company

    Returns:
        str: Best guess URL or None
    """
    try:
        ddgs = DDGS()
        results = ddgs.text(f"{company_name} official website", max_results=3)

        if results and len(results) > 0:
            # Return the first result's link
            return results[0].get('href', None)
        return None
    except Exception as e:
        print(f"⚠️ Search error: {e}")
        return None


if __name__ == "__main__":
    # Test the URL finder
    test_companies = ["HuggingFace", "OpenAI", "Google"]

    for company in test_companies:
        url = find_company_url(company)
        print(f"{company}: {url}\n")
