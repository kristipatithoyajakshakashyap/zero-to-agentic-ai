"""
04_built_in_tools - Part 2: DirectoryReadTool & DirectorySearchTool
========================================================================

`DirectoryReadTool` lists a directory's contents. `DirectorySearchTool`
performs semantic search over a directory's content.
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from crewai_tools import DirectoryReadTool, DirectorySearchTool

DEMO_DIR = Path.cwd() / "_crewai_tools_demo"


def setup_demo_dir() -> Path:
    shutil.rmtree(DEMO_DIR, ignore_errors=True)
    DEMO_DIR.mkdir(parents=True)
    sample_file = DEMO_DIR / "sample_data.txt"
    sample_file.write_text(
        "Name,Score,Grade\n"
        "Alice,95,A\n"
        "Bob,82,B\n"
        "Charlie,91,A\n"
        "Diana,76,C\n"
    )
    return sample_file


def demonstrate_directory_read():
    """List a directory's contents with DirectoryReadTool."""
    print("=" * 60)
    print("DirectoryReadTool")
    print("=" * 60)

    dir_reader = DirectoryReadTool()
    listing = dir_reader.run(directory=str(DEMO_DIR))
    print("=== Directory Listing ===")
    print(listing)


def demonstrate_directory_search():
    """Semantic search over a directory's content with DirectorySearchTool.

    DirectorySearchTool embeds file content to search it. It defaults to
    OpenAI embeddings, so this course points it at a local Ollama embedding
    model instead (no OpenAI key involved). If no local Ollama embedding
    model is available, this demo is skipped with a clear message rather
    than crashing.
    """
    print("\n" + "=" * 60)
    print("DirectorySearchTool")
    print("=" * 60)

    try:
        dir_searcher = DirectorySearchTool(
            config={
                "embedding_model": {
                    "provider": "ollama",
                    "config": {"model": "nomic-embed-text"},
                },
            },
        )
        results = dir_searcher.run(search_query="Alice", directory=str(DEMO_DIR))
        print("=== Search Results (query: 'Alice') ===")
        print(results)
    except Exception as e:
        print("[INFO] DirectorySearchTool needs a local Ollama embedding model.")
        print("       Run: ollama pull nomic-embed-text")
        print("       Detail:", e)


if __name__ == "__main__":
    setup_demo_dir()
    demonstrate_directory_read()
    demonstrate_directory_search()
    shutil.rmtree(DEMO_DIR, ignore_errors=True)
    print("\nCleanup: removed", DEMO_DIR)
