"""
01_installation_and_first_crew - Part 1: Install and Verify CrewAI
===================================================================

This module covers installing CrewAI and its tooling extras,
verifying the installation, and setting up the environment.
"""

from pathlib import Path

from dotenv import load_dotenv

# Walk up from the current directory until we hit the track root "03_agentic_ai"
TRACK = Path.cwd()
while TRACK.name != "03_agentic_ai" and TRACK != TRACK.parent:
    TRACK = TRACK.parent

load_dotenv(TRACK / ".env")

print("Setup complete. Track root resolved to:", TRACK)


def verify_crewai_installation() -> bool:
    """Verify that CrewAI and its tools are properly installed."""
    try:
        import crewai
        from crewai import Agent, Task, Crew, Process  # noqa: F401
        print("[OK] crewai imported successfully. Version:", crewai.__version__)
    except ImportError as e:
        print("[ERROR] crewai not installed. Run: pip install crewai \"crewai[tools]\"")
        print("        Detail:", e)
        return False

    try:
        from crewai_tools import FileReadTool  # noqa: F401
        print("[OK] crewai_tools imported. FileReadTool is available.")
    except ImportError as e:
        print("[WARN] crewai_tools not installed.")
        print("       Run: pip install \"crewai[tools]\"")
        print("       Detail:", e)
        return False

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Part 1: Install and Verify CrewAI")
    print("=" * 60)
    success = verify_crewai_installation()
    if success:
        print("\n[SUCCESS] CrewAI installation verified!")
    else:
        print("\n[FAILED] Please install CrewAI and try again.")
