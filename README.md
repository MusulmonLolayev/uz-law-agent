# uz-law-agent

An open-source Uzbek law agent. It answers a question by searching Uzbek law and reading articles, and cites the
articles it used. It is developed following Module 7 (AI Agents, Tool Use & Retrieval) of the Advanced AI course. The
course used the Labor Code of Uzbekistan (581 articles, Uzbek, CC0) only as its example, and it is the one law in the
repository for now: the agent loop, the recorded runs and the tests use it.

The agent is a ReAct loop (Thought / Action as text) with three actions, `search`, `fetch_article` and `answer`, and
a step budget.

## Quick start

```bash
uv sync
uv run python agent.py --replay q2_under18     # a recorded run: no key, no network
```

Live run (needs a DeepSeek key; replay does not):

```bash
cp .env.example .env                           # then put your key in .env; it is git-ignored
uv run python agent.py "What is the maximum normal working week?"
uv run python agent.py --record NAME "question"    # run live and save it to traces/NAME.json
```

## Tests

```bash
uv run python -m unittest discover -v          # offline, no key
```

## Layout

| Path | What |
|---|---|
| `agent.py` | the ReAct loop and command line |
| `corpus.py` | the articles and the two tools (`search`, `fetch_article`) |
| `llm.py` | the model behind one function: live, record, replay |
| `data/` | the Labor Code, the example law (`mehnat_kodeksi.jsonl`, `SOURCE.md`) |
| `traces/` | recorded runs, replayed offline |
| `test_agent.py`, `test_no_secrets.py` | tests |
| `docs/` | [ADDING_A_LAW.md](docs/ADDING_A_LAW.md): how to add another code of Uzbekistan as a corpus |

## Corpora

- **Included: the Labor Code of Uzbekistan, the course example** (CC0, in the repository, `data/mehnat_kodeksi.jsonl`). The agent loop,
  the recorded runs and the tests use it.
- **More laws:** [docs/ADDING_A_LAW.md](docs/ADDING_A_LAW.md) describes the record format, the two tools, the source
  note and the licence check. No other law is included yet, and the loop is wired to the Labor Code, so using a second
  law in the agent is open work.

## Contributing

Pull requests are welcome, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

Code: MIT, see [LICENSE](LICENSE). Data: the Labor Code of Uzbekistan is CC0, see [data/SOURCE.md](data/SOURCE.md).
