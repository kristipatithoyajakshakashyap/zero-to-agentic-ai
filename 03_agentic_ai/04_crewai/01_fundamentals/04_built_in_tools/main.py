"""
04_built_in_tools - Main Entry Point
======================================

Runs all parts of the module in sequence.
"""

import sys
import time
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

import llm_setup  # noqa: F401 - imported for its side effect (live LLM check)
import file_tools
import directory_tools
import web_scrape_tool
import serper_search_tool
import multi_tool_agent


def main():
    print("=" * 70)
    print("MODULE 04: BUILT-IN TOOLS")
    print("=" * 70)

    pause = 10

    print("\n>>> Part 1: File Tools")
    sample = file_tools.setup_demo_dir()
    file_tools.demonstrate_file_read(sample)
    file_tools.demonstrate_file_writer()
    file_tools.shutil.rmtree(file_tools.DEMO_DIR, ignore_errors=True)

    print("\n>>> Part 2: Directory Tools")
    directory_tools.setup_demo_dir()
    directory_tools.demonstrate_directory_read()
    directory_tools.demonstrate_directory_search()
    directory_tools.shutil.rmtree(directory_tools.DEMO_DIR, ignore_errors=True)

    print("\n>>> Part 3: Web Scrape Tool")
    web_scrape_tool.demonstrate_web_scrape()

    print("\n>>> Part 4: Serper Search Tool")
    serper_search_tool.demonstrate_serper_search()

    print("\n>>> Part 5: Multi-Tool Agent")
    time.sleep(pause)
    sample = multi_tool_agent.setup_demo_dir()
    multi_tool_agent.demonstrate_agent_with_tools(sample)
    time.sleep(pause)
    multi_tool_agent.demonstrate_standalone_tool_usage(sample)
    multi_tool_agent.demonstrate_error_handling(sample)
    time.sleep(pause)
    multi_tool_agent.demonstrate_full_pattern(sample)
    multi_tool_agent.shutil.rmtree(multi_tool_agent.DEMO_DIR, ignore_errors=True)

    print("\n" + "=" * 70)
    print("MODULE 04 COMPLETE")
    print("=" * 70)
    print("\nNext: Continue to 05_research_assistant_crew for the fundamentals capstone.")


if __name__ == "__main__":
    main()
