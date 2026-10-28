# Prompt to migrate an existing memory

Paste the text below into your agent, changing the folder path. It works in any language: write it in yours if you prefer.

---

Reorganize the memory in `/path/to/memory` into the layered memory format described in `MEMORY-RULES.md`:

1. Read the current `MEMORY.md` and the header (`description:`) of every `.md` note in the folder.
2. Propose 4 to 8 areas that cover everything (for example: work, home, projects, computer). Show me the proposal and wait for my approval.
3. For each area, create `_index-<area>.md` with one line per note: `- [name](name.md): one-line description`.
4. Every note must be in exactly one area index. A note without `description:` gets one.
5. Information that lived only inside `MEMORY.md` (with no note of its own) becomes a note of its own.
6. Rewrite `MEMORY.md` with only the instruction paragraph and one line per area (link to the area index plus keywords).
7. Do not delete any note. When done, run `python tools/check.py /path/to/memory` and fix whatever it reports.
