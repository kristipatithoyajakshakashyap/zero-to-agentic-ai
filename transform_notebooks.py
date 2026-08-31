#!/usr/bin/env python3
"""
Transform all notebooks:
1. Convert title-comments in code cells to markdown cells
2. Normalize heading hierarchy: title=#, rest=###
3. Replace all long dashes with standard hyphens
4. Add missing h1 titles
"""

import json
import re
import os
from pathlib import Path
from typing import List, Tuple, Dict, Any

ROOT = Path(r"D:\projects\python\MLCourse")

# Unicode dashes to replace
DASH_PATTERN = re.compile(r"[\u2014\u2013\u2015\u2212]")  # em, en, horizontal bar, minus

# Patterns for detecting title comments in code cells
SEPARATOR_PATTERN = re.compile(r"^#\s*-{3,}\s*(.+?)\s*-{3,}$")  # # --- Title ---
NESTED_HASH_PATTERN = re.compile(r"^#\s+(#{1,6})\s+(.+)$")      # # ## Title
FLAT_HASH_PATTERN = re.compile(r"^#\s+([A-Z][^#].+)$")           # # Title (but not # --- etc)
CODE_BLOCK_PATTERN = re.compile(r"^```")  # code fences (should not be split)

# Patterns to EXCLUDE from conversion (explanatory comments)
EXCLUDE_PATTERNS = [
    r"^#\s*(your code here|Example \d+|Takeaway|Check yourself|Note:|In |We |Here |Notice |As |This |The |A |An |Alternative|Optional|Also|However|But |If |When |Then |Note |TODO|FIXME|XXX|HACK)",
    r"^#\s*\d+\.",
    r"^#\s*-+$",  # just dashes
]


def is_title_comment(line: str) -> Tuple[bool, str, int]:
    """
    Check if a line is a title comment that should become a markdown heading.
    Returns: (is_title, title_text, level)
    level: 1 for main title, 3 for sections
    """
    stripped = line.strip()
    
    # Check exclude patterns first
    for pat in EXCLUDE_PATTERNS:
        if re.match(pat, stripped, re.IGNORECASE):
            return (False, "", 0)
    
    # Pattern 1: # --- Title ---
    m = SEPARATOR_PATTERN.match(stripped)
    if m:
        title = m.group(1).strip()
        if title:
            return (True, title, 3)
    
    # Pattern 2: # ## Title or # ### Title (nested)
    m = NESTED_HASH_PATTERN.match(stripped)
    if m:
        inner_hashes = m.group(1)
        title = m.group(2).strip()
        if title:
            return (True, title, 3)
    
    # Pattern 3: # Title (flat, capitalized, not starting with excluded words)
    m = FLAT_HASH_PATTERN.match(stripped)
    if m:
        title = m.group(1).strip()
        # Additional checks to avoid false positives
        if len(title) < 80 and not title.startswith(("---", "===", "your", "Example", "Takeaway", "Check", "Note")):
            return (True, title, 3)
    
    return (False, "", 0)


def has_real_code(source_lines: List[str], start_idx: int) -> bool:
    """Check if there's real (non-comment) code after the given index."""
    for line in source_lines[start_idx:]:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return True
    return False


def replace_dashes(text: str) -> str:
    """Replace all long dashes with standard hyphen."""
    return DASH_PATTERN.sub("-", text)


def process_notebook(nb_path: Path) -> Dict[str, Any]:
    """Process a single notebook, return stats."""
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    
    stats = {
        "cells_converted": 0,
        "cells_split": 0,
        "headings_normalized": 0,
        "dashes_replaced": 0,
        "h1_added": 0,
        "errors": []
    }
    
    cells = nb.get("cells", [])
    if not cells:
        return stats
    
    # First pass: replace dashes everywhere
    for cell in cells:
        src = cell.get("source", [])
        new_src = [replace_dashes(line) for line in src]
        if new_src != src:
            stats["dashes_replaced"] += 1
            cell["source"] = new_src
    
    # Second pass: detect and convert title-comments in code cells
    new_cells = []
    i = 0
    while i < len(cells):
        cell = cells[i]
        if cell.get("cell_type") == "code":
            src = cell.get("source", [])
            if not src:
                new_cells.append(cell)
                i += 1
                continue
            
            src_text = "".join(src)
            lines = src_text.splitlines()
            
            # Check if first non-empty line is a title comment
            first_nonempty_idx = None
            for j, line in enumerate(lines):
                if line.strip():
                    first_nonempty_idx = j
                    break
            
            if first_nonempty_idx is not None:
                first_line = lines[first_nonempty_idx]
                is_title, title, level = is_title_comment(first_line)
                
                if is_title:
                    # Check if there's code after the title
                    has_code = has_real_code(lines, first_nonempty_idx + 1)
                    
                    # Extract the title line's leading whitespace (should be none)
                    # Create markdown cell
                    md_cell = {
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": [f"### {title}\n"]
                    }
                    new_cells.append(md_cell)
                    stats["cells_converted"] += 1
                    
                    if has_code:
                        # Keep the rest as a code cell
                        # Remove the title line and the following blank line if present
                        rest_lines = lines[first_nonempty_idx + 1:]
                        # Remove leading blank lines
                        while rest_lines and not rest_lines[0].strip():
                            rest_lines.pop(0)
                        if rest_lines:
                            code_cell = {
                                "cell_type": "code",
                                "metadata": cell.get("metadata", {}),
                                "outputs": [],
                                "execution_count": None,
                                "source": [line + "\n" for line in rest_lines]
                            }
                            new_cells.append(code_cell)
                            stats["cells_split"] += 1
                        # If no rest lines, just drop the cell (was title-only)
                    # If no code, the markdown cell replaces the whole code cell
                    i += 1
                    continue
        
        new_cells.append(cell)
        i += 1
    
    nb["cells"] = new_cells
    
    # Third pass: normalize heading levels in markdown cells
    first_h1_found = False
    has_h1 = False
    
    # First check if there's an h1 already
    for cell in nb["cells"]:
        if cell.get("cell_type") == "markdown":
            src = "".join(cell.get("source", []))
            lines = src.splitlines()
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("#"):
                    hash_count = len(stripped) - len(stripped.lstrip("#"))
                    if hash_count == 1:
                        has_h1 = True
                        break
    
    for cell in nb["cells"]:
        if cell.get("cell_type") != "markdown":
            continue
        src = cell.get("source", [])
        new_src = []
        for line in src:
            stripped = line.strip()
            if stripped.startswith("#"):
                hash_count = len(stripped) - len(stripped.lstrip("#"))
                if hash_count >= 1:
                    title_text = stripped.lstrip("#").strip()
                    if not first_h1_found:
                        # This is the main title
                        new_line = f"# {title_text}\n"
                        first_h1_found = True
                    else:
                        # All other headings become ###
                        new_line = f"### {title_text}\n"
                    new_src.append(new_line)
                    stats["headings_normalized"] += 1
                else:
                    new_src.append(line)
            else:
                new_src.append(line)
        if new_src != src:
            cell["source"] = new_src
    
    # If no h1 found, prepend one based on filename
    if not has_h1:
        # Derive title from filename
        stem = nb_path.stem
        # Clean up filename: remove leading numbers, underscores
        title = re.sub(r"^\d+[_-]", "", stem)
        title = title.replace("_", " ").replace("-", " ")
        # Capitalize words
        title = " ".join(w.capitalize() for w in title.split())
        
        h1_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [f"# {title}\n"]
        }
        nb["cells"].insert(0, h1_cell)
        stats["h1_added"] += 1
    
    # Write back
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    
    return stats


def main():
    all_stats = {
        "total_notebooks": 0,
        "total_cells_converted": 0,
        "total_cells_split": 0,
        "total_headings_normalized": 0,
        "total_dashes_replaced": 0,
        "total_h1_added": 0,
        "errors": []
    }
    
    # Find all notebooks
    notebooks = list(ROOT.rglob("*.ipynb"))
    # Filter out .ipynb_checkpoints
    notebooks = [n for n in notebooks if ".ipynb_checkpoints" not in str(n)]
    
    print(f"Found {len(notebooks)} notebooks to process")
    
    for nb_path in notebooks:
        try:
            rel_path = nb_path.relative_to(ROOT)
            stats = process_notebook(nb_path)
            
            all_stats["total_notebooks"] += 1
            all_stats["total_cells_converted"] += stats["cells_converted"]
            all_stats["total_cells_split"] += stats["cells_split"]
            all_stats["total_headings_normalized"] += stats["headings_normalized"]
            all_stats["total_dashes_replaced"] += stats["dashes_replaced"]
            all_stats["total_h1_added"] += stats["h1_added"]
            
            if stats["cells_converted"] > 0 or stats["cells_split"] > 0 or stats["headings_normalized"] > 0:
                print(f"  {rel_path}: converted={stats['cells_converted']}, split={stats['cells_split']}, headings={stats['headings_normalized']}, dashes={stats['dashes_replaced']}, h1_added={stats['h1_added']}")
                
        except Exception as e:
            print(f"ERROR processing {nb_path}: {e}")
            all_stats["errors"].append(str(nb_path))
    
    print("\n=== SUMMARY ===")
    print(f"Total notebooks processed: {all_stats['total_notebooks']}")
    print(f"Title-comment cells converted to markdown: {all_stats['total_cells_converted']}")
    print(f"Code cells split (title + code): {all_stats['total_cells_split']}")
    print(f"Headings normalized: {all_stats['total_headings_normalized']}")
    print(f"Dashes replaced: {all_stats['total_dashes_replaced']}")
    print(f"H1 titles added: {all_stats['total_h1_added']}")
    if all_stats["errors"]:
        print(f"Errors: {all_stats['errors']}")


if __name__ == "__main__":
    main()