"""
04_built_in_tools - Part 4: SerperDevTool
============================================

`SerperDevTool` performs web searches using the Serper API (serper.dev).
Requires a SERPER_API_KEY. If unset, this file states so plainly and exits
cleanly - it never crashes for a missing optional key.
"""

import os


def demonstrate_serper_search():
    """Run a web search with SerperDevTool if SERPER_API_KEY is configured."""
    print("=" * 60)
    print("SerperDevTool")
    print("=" * 60)

    serper_key = os.environ.get("SERPER_API_KEY", "")
    if not serper_key:
        print("[INFO] SERPER_API_KEY not set in .env - skipping this demo.")
        print("       Add SERPER_API_KEY=your_key to your .env to run web search.")
        print("       Get a free key at https://serper.dev")
        return

    from crewai_tools import SerperDevTool

    serper_searcher = SerperDevTool()
    try:
        search_results = serper_searcher.run("latest developments in CrewAI 2026")
        print("=== Serper Search Results (first 400 chars) ===")
        print(str(search_results)[:400])
    except Exception as e:
        print("[WARN] SerperDevTool failed:", e)


if __name__ == "__main__":
    demonstrate_serper_search()
