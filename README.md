# uz-law-agent

An open-source research agent over the Labor Code of Uzbekistan (581 articles, Uzbek), built step by step by
students in Module 7 (AI Agents, Tool Use & Retrieval) of the Advanced AI course. The repository starts at
Lecture 1: a ReAct loop (Thought / Action as text) with three actions, `search`, `fetch_article` and `answer`, and a
step budget. Lectures 2-8 add schemas, memory, a verifier, retrieval and evaluation; see [STEPS.md](STEPS.md).

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
uv run python -m unittest discover -v          # offline; the tests for Lectures 2-8 are skipped stubs
```

## Layout

| Path | What |
|---|---|
| `agent.py` | the ReAct loop and command line |
| `corpus.py` | the articles and the two tools (`search`, `fetch_article`) |
| `llm.py` | the model behind one function: live, record, replay |
| `data/` | the Labor Code (`mehnat_kodeksi.jsonl`, `SOURCE.md`) and an optional UK example corpus |
| `traces/` | recorded runs, replayed offline |
| `test_agent.py`, `test_steps.py`, `test_no_secrets.py`, `test_pr_scope.py` | tests; `test_steps.py` holds the skipped acceptance stubs |
| `assignments/` | one folder per student; `_template/` to copy |
| `scripts/check_pr_scope.py` | the pull-request scope check |

## Submitting your work

Copy `assignments/_template` to `assignments/<your-github-username>/`, work only there, and submit by pull request.
A pull request that changes anything outside your folder fails the `pr-scope` check. See
[assignments/README.md](assignments/README.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

Code: MIT, see [LICENSE](LICENSE). Data: the Labor Code of Uzbekistan is CC0, see [data/SOURCE.md](data/SOURCE.md).
The optional UK example corpus is under the Open Government Licence v3.0, see [data/SOURCE_UK.md](data/SOURCE_UK.md).
