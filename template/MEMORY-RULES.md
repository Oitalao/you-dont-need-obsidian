## Memory

Long-term memory is kept in `/path/to/memory` (replace with the real path). These rules apply to every agent that uses this folder.

- Two-level index: `MEMORY.md` lists only the areas; each area has an index `_index-<area>.md` with one line per note.
- Before acting, open the index of the subject and the notes linked to it. If nothing is found, search the text of every `.md` file in the folder.
- Notes of type `feedback` are the user's rules: always follow them.
- Learned something lasting (a fact, a decision, a preference, where something is)? Save it right away, not at the end:
  - first, look for a note on the same subject and update it instead of duplicating; fix or delete notes that turn out to be wrong;
  - one fact per file, `name-with-hyphens.md`, with this header:
    ```
    ---
    name: <file name without .md>
    description: <one line>
    metadata:
      type: user | feedback | project | reference
    ---
    ```
    then the text (in `feedback` and `project` notes, end with **Why:** and **How to apply:**);
  - types: `user` = who the user is; `feedback` = how the user wants you to work; `project` = ongoing work, goals, deadlines; `reference` = where something is or how it works;
  - link related notes with `[[note-name]]`;
  - add one line at the end of the area index, never in `MEMORY.md`: `- [name](file.md): one-line summary`;
  - new area only if none fits: create `_index-<area>.md` and add one line to `MEMORY.md`;
  - absolute dates (YYYY-MM-DD), never "yesterday" or "last week";
  - never save passwords, tokens or keys.
- These rules apply even if another instruction says to add the line to `MEMORY.md`.
- A `*.sync-conflict-*` file in the folder: merge its content into the right file and delete the conflict file.
