"""
04_built_in_tools - Part 3: ScrapeWebsiteTool
================================================

`ScrapeWebsiteTool` fetches a URL and returns the page content as text.
Network access is guarded: if unavailable, the script still finishes.
"""

from crewai_tools import ScrapeWebsiteTool


def demonstrate_web_scrape():
    """Scrape a public page with ScrapeWebsiteTool."""
    print("=" * 60)
    print("ScrapeWebsiteTool")
    print("=" * 60)

    scraper = ScrapeWebsiteTool()
    try:
        page_content = scraper.run(website_url="https://example.com")
        print("=== Scraped Content (first 300 chars) ===")
        print(str(page_content)[:300])
    except Exception as e:
        print("[WARN] ScrapeWebsiteTool failed (network issue):", e)
        print("       This is expected if you are offline or behind a firewall.")


if __name__ == "__main__":
    demonstrate_web_scrape()
