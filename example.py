"""
Example usage of the BrandBook generator
This demonstrates how to use the URL finder and brochure generator
"""

from url_finder import find_company_url
from generator import initialize_model, stream_brochure
import generator


def run_example():
    """Run an example brochure generation"""

    # Initialize the AI model
    print("Initializing AI model...")
    initialize_model()

    # Example companies to test
    test_companies = ["OpenAI", "Anthropic", "Google"]

    print("\n" + "="*60)
    print("Example: Automatic URL Discovery and Brochure Generation")
    print("="*60)

    # Let user choose or enter a company
    print("\nSelect a company to generate a brochure for:")
    for i, company in enumerate(test_companies, 1):
        print(f"{i}. {company}")
    print(f"{len(test_companies) + 1}. Enter custom company name")

    choice = input("\nEnter your choice: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(test_companies):
        company_name = test_companies[int(choice) - 1]
    else:
        company_name = input("Enter company name: ").strip()

    if not company_name:
        print("No company name provided. Exiting.")
        return

    # Find the URL automatically
    print(f"\n{'='*60}")
    print("🔍 Step 1: Finding Company Website URL")
    print('='*60)

    website_url = find_company_url(
        company_name, generator.MODEL_PROVIDER, generator.MODEL_NAME, generator.client)

    if not website_url:
        print("\n⚠️  Could not find URL automatically.")
        website_url = input("Please enter the URL manually: ").strip()
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url

    # Generate the brochure
    print(f"\n{'='*60}")
    print("📝 Step 2: Generating Brochure")
    print('='*60)
    print(f"Company: {company_name}")
    print(f"Website: {website_url}\n")

    try:
        stream_brochure(company_name, website_url)
        print(f"\n\n{'='*60}")
        print("✅ Success! Brochure generated.")
        print('='*60)
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    run_example()
