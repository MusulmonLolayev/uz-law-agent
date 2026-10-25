# uz-law-agent

An open-source Uzbek law agent: it answers a question by searching Uzbek law and reading articles, and cites the
articles it used. It is developed following Module 7 (AI Agents, Tool Use & Retrieval) of the Advanced AI course.

The repository is an empty skeleton. The work starts here.

| Folder | For |
|---|---|
| `data/` | the laws (one file per law) and a source note next to each: where the text comes from, the date, the licence |
| `agent/` | the agent code |
| `tests/` | tests |
| `traces/` | recorded runs |
| `docs/` | documentation |

Keys go in `.env` (git-ignored); `.env.example` is the template. Never commit a key.

## Licence

Code: MIT, see [LICENSE](LICENSE). Each law's text carries the licence stated in its source note.
