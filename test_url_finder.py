#!/usr/bin/env python3
"""
Quick test of URL finder without needing AI API
"""

from url_finder import extract_domain_from_results
from ddgs import DDGS


def test_url_finder(company_name):
    """Test URL finding for a company"""
    print(f"\n{'='*60}")
    print(f"Testing: {company_name}")
    print('='*60)

    try:
        ddgs = DDGS()

        # Get search results
        print(f"🔍 Searching...")
        results = ddgs.text(company_name, max_results=5)

        print(f"📊 Found {len(results)} results:")
        for i, r in enumerate(results[:3], 1):
            print(f"  {i}. {r.get('title', 'N/A')}")
            print(f"     {r.get('href', 'N/A')}")

        # Try to extract domain
        print(f"\n🎯 Extracting official domain...")
        url = extract_domain_from_results(results)

        if url:
            print(f"✅ Found: {url}")
        else:
            print(f"❌ Could not extract URL")

        return url

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    # Test with several companies
    test_companies = [
        "HuggingFace",
        "OpenAI",
        "Anthropic",
        "Google",
        "Microsoft"
    ]

    for company in test_companies:
        test_url_finder(company)
        print()
