# Template

A ready-to-copy memory folder. The notes are fictional examples: delete them and keep the structure.

| File | Role | Read by the agent |
|---|---|---|
| `MEMORY-RULES.md` | layer 0: the rules; paste into `CLAUDE.md`, `AGENTS.md` or `GEMINI.md` | always |
| `MEMORY.md` | layer 1: the map, one line per area | always |
| `_index-<area>.md` | layer 2: one line per note of that area | when the subject belongs to the area |
| `<note-name>.md` | layer 3: one fact per note | when relevant |

The example notes show the four note types: `user` ([user-profile](user-profile.md)), `feedback` ([short-answers](short-answers.md)), `project` ([client-contract-acme](client-contract-acme.md), [car-service](car-service.md)) and `reference` ([photo-backup](photo-backup.md)).

Files whose name is all uppercase (`README.md`, `MEMORY-RULES.md`) are not notes; the checker ignores them.
