from generator import initialize_model, stream_brochure
from url_finder import find_company_url
import generator


def main():
    print("=" * 60)
    print("🎨 Welcome - Company Brochure Generator 🎨")
    print("=" * 60)

    # Initialize AI model
    initialize_model()

    print("\n" + "=" * 60)
    print("📋 Brochure Information")
    print("=" * 60)

    # Get company name from user
    company_name = input(
        "\n🏢 Enter company name or website (e.g., HuggingFace, OpenAI): ").strip()

    while not company_name:
        print("⚠️  Company name cannot be empty!")
        company_name = input("🏢 Enter company name: ").strip()

    # Automatically find the website URL using LangChain
    print("\n" + "=" * 60)
    print("🤖 AI-Powered URL Discovery")
    print("=" * 60)

    website_url = find_company_url(
        company_name, generator.MODEL_PROVIDER, generator.MODEL_NAME, generator.client)

    # If automatic search fails, ask user for manual input
    if not website_url:
        print("\n⚠️  Automatic URL search failed.")
        website_url = input(
            "🌐 Please enter website URL manually (e.g., https://huggingface.co): ").strip()

        while not website_url:
            print("⚠️  Website URL cannot be empty!")
            website_url = input("🌐 Enter website URL: ").strip()

        # Add https:// if not present
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url

    print("\n" + "=" * 60)
    print(f"✨ Generating brochure for {company_name}...")
    print(f"🔗 Website: {website_url}")
    print("=" * 60 + "\n")

    # Generate the brochure
    try:
        stream_brochure(company_name, website_url)
        print("\n\n" + "=" * 60)
        print("✅ Brochure generated successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("Please make sure the website URL is correct.")


if __name__ == "__main__":
    main()
