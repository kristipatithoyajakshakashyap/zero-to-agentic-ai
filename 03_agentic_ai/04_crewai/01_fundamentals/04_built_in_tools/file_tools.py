"""
04_built_in_tools - Part 1: FileReadTool & FileWriterTool
===========================================================

`FileReadTool` reads file contents; `FileWriterTool` writes content to files.
Both are confined to `base_dir` (a sandbox directory) by modern crewai_tools.
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from crewai_tools import FileReadTool, FileWriterTool

DEMO_DIR = Path.cwd() / "_crewai_tools_demo"


def setup_demo_dir() -> Path:
    """Recreate a clean demo folder under the script's cwd (inside the sandbox)."""
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


def demonstrate_file_read(sample_file: Path):
    """Read a file with FileReadTool, standalone and restricted.

    Built-in tools like this are just Python classes with a `.run(...)`
    method - you can call that method directly (like below) to test a tool
    on its own, or hand the tool object to an Agent so the LLM can decide
    when to call it during a task.
    """
    print("=" * 60)
    print("FileReadTool")
    print("=" * 60)

    file_reader = FileReadTool()
    content = file_reader.run(file_path=str(sample_file))
    print("=== File Content ===")
    print(content)

    # FileReadTool can also be pinned to one fixed path at construction time.
    # That's useful when an agent should only ever be able to read ONE
    # specific file, instead of any path it decides to pass in.
    fixed_reader = FileReadTool(file_path=str(sample_file))
    print("\nFixed to file:", fixed_reader.file_path)


def demonstrate_file_writer():
    """Write a file with FileWriterTool and read it back.

    This is the tool an agent would use to save its own output (a report,
    a summary, generated code) to disk instead of just printing it.
    """
    print("\n" + "=" * 60)
    print("FileWriterTool")
    print("=" * 60)

    file_writer = FileWriterTool()
    output_file = DEMO_DIR / "output_report.txt"
    write_result = file_writer.run(
        filename="output_report.txt",
        directory=str(DEMO_DIR),
        content=(
            "AI Agent Report\n"
            "================\n"
            "Status: All systems operational.\n"
        ),
        overwrite=True,
    )
    print("Write result:", write_result)
    print("File contents:", output_file.read_text())


if __name__ == "__main__":
    sample = setup_demo_dir()
    demonstrate_file_read(sample)
    demonstrate_file_writer()
    shutil.rmtree(DEMO_DIR, ignore_errors=True)
    print("\nCleanup: removed", DEMO_DIR)
