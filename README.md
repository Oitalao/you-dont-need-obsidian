# You don't need Obsidian

**English** | [Português (Brasil)](README.pt-BR.md)

Long-term memory for AI agents (Claude Code, Codex, Gemini CLI and any other agent that can read files) using nothing but a folder of Markdown files. Nothing to install, no database, no subscription. It grows without limit and works the same way in every agent.

## The problem

At the start of every conversation, each agent reads one instruction or memory file (`CLAUDE.md`, `MEMORY.md`, `AGENTS.md`, `GEMINI.md`). That file has a size limit:

| Agent | What is loaded | Limit (Oct 2026) |
|---|---|---|
| Claude Code | `MEMORY.md` of the auto memory | first 200 lines or 25 KB, whichever comes first |
| Codex CLI | `AGENTS.md` | 32 KB in total (`project_doc_max_bytes`) |
| Gemini CLI | `GEMINI.md` and its imports | depends on the version |

Limits change; check each agent's documentation.

If you keep everything in one file, sooner or later you hit the limit and the agent starts to "forget" without telling you: the end of the file is simply not read.

The usual answer is to install Obsidian, a memory plugin or a vector database. None of these solves the real problem: the agent does not use Obsidian's interface, only the `.md` files, which any text editor can open.

## The idea: layered memory

The agent always reads a small map and opens the details only when the subject comes up. It works like a book: you do not read the whole book to find one page. You look at the table of contents, go to the chapter, then to the page.

```
memory/
├── MEMORY.md                  layer 1: map of the areas (about 10 lines, does not grow)
├── _index-work.md             layer 2: one line per note in that area
├── _index-home.md
├── _index-computer.md
├── client-contract-acme.md    layer 3: notes, one fact per note
├── photo-backup.md
└── ...
```

| Layer | What it holds | When the agent reads it | Size |
|---|---|---|---|
| 0. Rules | how you want the agent to work | always (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) | small, fixed |
| 1. Map | the areas and the keywords of each one | always | about 10 lines, does not grow |
| 2. Area index | title and one-line summary of each note | when the subject belongs to that area | no practical limit |
| 3. Note | the details | when it is relevant | no limit |

Safety net: if the index fails, the agent searches the text of every file in the folder (`grep`). That is enough for thousands of notes.

## Getting started (5 minutes)

1. Copy the [`template/`](template) folder to wherever you want to keep the memory, and delete the example notes.
2. Replace the areas in `MEMORY.md` with your own (work, home, projects...). Start with a few.
3. Connect the folder to your agent (see below) and paste the content of [`template/MEMORY-RULES.md`](template/MEMORY-RULES.md) into its instructions, changing the folder path.
4. Already have a large `MEMORY.md`? Ask your agent to migrate it with [`MIGRATE-PROMPT.md`](MIGRATE-PROMPT.md).
5. From time to time, run the checker:

```
python tools/check.py path/to/memory
```

It reports notes missing from the indexes, broken links, notes without a description, sync conflicts and a map that has grown too big. It needs only Python 3.8 or newer.

The notes can be written in any language. The file names and the structure are what matter.

### Claude Code

In `~/.claude/settings.json`, point the auto memory to the folder:

```json
{ "autoMemoryDirectory": "/path/to/memory" }
```

Claude Code already loads the `MEMORY.md` of that folder by itself. Paste the rules into `~/.claude/CLAUDE.md`, or import the file with `@/path/to/memory/MEMORY-RULES.md`.

Note: by default, Claude Code is told to add one line to `MEMORY.md` for each new memory. The rules in `CLAUDE.md` take priority and send that line to the area index instead. If one slips through, the checker reports it.

### Codex

Codex reads `~/.codex/AGENTS.md` (or the one in `CODEX_HOME`) and cannot import other files. Paste the rules and the content of `MEMORY.md` into it. Since the map almost never changes, you rarely need to redo this.

### Gemini CLI

In `~/.gemini/GEMINI.md`, import both files:

```
@/path/to/memory/MEMORY-RULES.md
@/path/to/memory/MEMORY.md
```

### Other agents

Any agent that can read files works: point its instructions to the rules and to the map.

## The rules that make it work

1. **One fact per note**, with a one-line `description:` in the header. The agent uses the description to decide whether to open the note.
2. **Update instead of duplicating:** before creating a note, look for one on the same subject.
3. **Save it right away**, as soon as it is learned, not at the end of the conversation, which may end first.
4. **Absolute dates** (`2026-10-28`, never "yesterday").
5. **A new note goes in its area index, never in the map.** The map gets a new line only when a new area appears.
6. **Clean up from time to time:** merge repeated notes and fix or delete wrong ones. Ask the agent to do it.
7. **No passwords, tokens or keys** in the memory. The folder usually ends up in the cloud and in backups.

## Several agents, several computers

- **One source:** the rules live in one file, and `CLAUDE.md`, `AGENTS.md` and `GEMINI.md` only point to it (or are copied from it). Change a rule in one place.
- **Same folder for all:** every agent reads and writes the same memory. What one learns, the others already know.
- **Sync:** Syncthing, Git, Dropbox or Nextcloud take the folder to your other computers. If a conflict file shows up (`*.sync-conflict-*`), ask the agent to merge it and delete it.

## FAQ

**So is Obsidian useless?**
It is great for you to read and browse, and it can open this same folder (the `[[name]]` links work in it). For the agent, it adds nothing. If you find it heavy, Notepad, VS Code or any editor will do.

**What about a vector database / RAG?**
It pays off only with tens of thousands of notes or with long documents. For personal memory, text search is simpler, more predictable and needs nothing installed.

**Why not let the agent decide on its own what to keep?**
It does decide, but without structure the file grows until it is cut off. The layers just give each thing its proper place (and letting the AI do absolutely everything costs money).

**How far does this scale?**
The map stays the same size forever. If an area index gets too big (hundreds of lines), split the area in two.

## License

MIT. See [LICENSE](LICENSE).
