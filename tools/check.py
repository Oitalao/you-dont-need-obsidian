#!/usr/bin/env python3
"""Check a layered memory folder.

Usage: python check.py [folder] [--prefix _index-]

Reports:
  - a map (MEMORY.md) that is too big, or that lists notes directly;
  - an area index missing from the map;
  - links to files that do not exist;
  - notes missing from every area index, or listed in more than one;
  - notes without a header or without a description;
  - [[links]] to notes that do not exist;
  - Syncthing conflict files.

Files whose name is all uppercase (README.md, MEMORY-RULES.md) are not notes.
Exits with code 1 if there are errors. Uses only the Python 3.8+ standard library.
"""
import argparse
import re
import sys
from pathlib import Path

MAX_LINES = 200          # Claude Code reads only the first 200 lines
MAX_BYTES = 25 * 1024    # or the first 25 KB
BIG_MAP = 30             # the map should have only a few lines
BIG_INDEX = 300          # above this, split the area in two

LINK = re.compile(r"\]\(([^)#\s]+\.md)\)")
WIKILINK = re.compile(r"\[\[([^\]|#]+)")


def read(p):
    """Read text, accepting a BOM and Windows line endings."""
    return p.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def without_code(text):
    """Remove code blocks and inline code, where [[ ]] is not a link."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def header(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    fields = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip().strip('"')
    return fields


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Check a layered memory folder.")
    ap.add_argument("folder", nargs="?", default=".")
    ap.add_argument("--prefix", default="_index-", help="file name prefix of the area indexes")
    args = ap.parse_args()
    folder = Path(args.folder).resolve()
    prefix = args.prefix
    errors, warnings = [], []

    def is_note(p):
        return (p.suffix == ".md" and p.name != "MEMORY.md"
                and not p.name.startswith(prefix)
                and p.stem.upper() != p.stem)

    map_file = folder / "MEMORY.md"
    if not map_file.exists():
        print(f"{map_file} not found.")
        return 1
    map_text = read(map_file)
    lines = map_text.rstrip("\n").count("\n") + 1
    size = len(map_file.read_bytes())
    if lines > MAX_LINES or size > MAX_BYTES:
        errors.append(f"MEMORY.md has {lines} lines and {size} bytes, more than the agent reads "
                      f"({MAX_LINES} lines / {MAX_BYTES} bytes). Move notes to the area indexes.")
    elif lines > BIG_MAP:
        warnings.append(f"MEMORY.md has {lines} lines; the map should list only the areas.")

    in_map = LINK.findall(map_text)
    indexes = sorted(folder.glob(prefix + "*.md"))
    for target in in_map:
        if not (folder / target).exists():
            errors.append(f"MEMORY.md links to {target}, which does not exist.")
        elif not Path(target).name.startswith(prefix):
            warnings.append(f"MEMORY.md lists the note {target} directly; it belongs in an area index.")
    for ix in indexes:
        if ix.name not in in_map:
            errors.append(f"{ix.name} is not in MEMORY.md, so the agent will never find it.")

    where = {}
    for ix in indexes:
        t = read(ix)
        if t.count("\n") + 1 > BIG_INDEX:
            warnings.append(f"{ix.name} has more than {BIG_INDEX} lines; consider splitting the area.")
        for target in LINK.findall(t):
            if not (folder / target).exists():
                errors.append(f"{ix.name} links to {target}, which does not exist.")
            where.setdefault(Path(target).name, []).append(ix.name)
    for target in in_map:
        where.setdefault(Path(target).name, []).append("MEMORY.md")

    notes = sorted(p for p in folder.glob("*.md") if is_note(p))
    names = {p.stem for p in notes}
    for p in notes:
        places = where.get(p.name, [])
        if not places:
            errors.append(f"{p.name} is not in any area index.")
        elif len([x for x in places if x != "MEMORY.md"]) > 1:
            warnings.append(f"{p.name} is listed in more than one index: {', '.join(places)}.")
        t = read(p)
        h = header(t)
        if h is None:
            errors.append(f"{p.name} has no header (--- name / description ---).")
        else:
            if not h.get("description"):
                errors.append(f"{p.name} has no description.")
            if h.get("name") and h["name"] != p.stem:
                warnings.append(f"{p.name}: header name is '{h['name']}', different from the file name.")
        for link in WIKILINK.findall(without_code(t)):
            if link.strip() not in names:
                warnings.append(f"{p.name} links to [[{link.strip()}]], which does not exist yet.")

    for p in folder.rglob("*.sync-conflict-*"):
        errors.append(f"Sync conflict: {p.relative_to(folder)}. Merge it into the right file and delete it.")

    print(f"Folder: {folder}")
    print(f"{len(notes)} notes, {len(indexes)} area indexes, map with {lines} lines.")
    for e in errors:
        print(f"ERROR    {e}")
    for w in warnings:
        print(f"warning  {w}")
    if not errors and not warnings:
        print("All good.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
