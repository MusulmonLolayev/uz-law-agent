# Roadmap: Lectures 2-8

Lecture 1 is done: the starting state, tag `step-01-react-loop`. Each later lecture adds one capability. A step is
finished when its acceptance checks hold; the same checks are skipped stub tests in `test_steps.py`, which say what
to build and contain no solution. Replace a stub with a real test when you build the step.

| Lecture | Topic | What the agent gains | Acceptance criteria (concrete checks) |
|---|---|---|---|
| 1 | ReAct loop | Thought / Action as text; `search`, `fetch_article`, `answer`; a step budget | Done. `python -m unittest test_agent` passes; `python agent.py --replay q2_under18` runs offline. |
| 2 | Tool schemas and structured output | Tools declared with JSON schemas; the model returns a structured tool call instead of text we parse | Every tool has a JSON schema with typed arguments. A malformed call (missing or wrongly typed argument) returns an error observation and does not raise. The final answer is a structured object `{answer, citations}` where every citation is an existing article id. The regex parser for `Action:` is gone. |
| 3 | Memory | The agent keeps what it learned across turns and across questions | A follow-up ("and for employees under 18?") is answered without re-reading what the first turn already fetched: the second run makes fewer tool calls than a fresh run. Memory is bounded (a configurable limit) and the oldest items go first. Memory can be saved to and loaded from a file. |
| 4 | Verifier subagent | A second model call checks the draft answer against the cited articles | For each citation, the verifier receives the cited article text and the claim and returns `supported` or `unsupported`. An answer with an unsupported citation is revised or flagged, never returned as is. A test shows a wrong citation being caught (use a scripted model, as in `test_agent.py`). |
| 5 | Chunking | Articles are split into chunks that keep their article id and position | Concatenating the chunks of an article gives back its text. Every chunk has a maximum size and carries `article_id` and `chunk_index`. No chunk is empty. Search results can point to a chunk, not only an article. |
| 6 | BM25 and embeddings | Real retrieval: BM25 over chunks, embeddings, and a hybrid ranking | `search` keeps its interface. On a small set of labelled questions (at least 10, written by you), the correct article is in the top 5 more often than with the Lecture 1 word-count search; the test prints both rates. Keyboard apostrophes (`o'n`) and the corpus's `oʻn` still match. |
| 7 | ANN index | An approximate nearest-neighbour index for the embeddings | The index returns, for 20 test queries, at least 90 % of the neighbours an exact search returns (recall@10), and the test measures it. Building the index is separate from querying it, and the index can be saved and reloaded. |
| 8 | Evaluation and injection test | An evaluation harness and a prompt-injection test | `python evaluate.py` runs every labelled question and prints, per question and in total: answer correct, citation correct, steps used. A planted instruction inside an article ("ignore previous instructions ...") does not change the answer or trigger a tool call the user did not ask for; the test shows the planted text, the agent's run, and the pass or fail. Results are reproducible offline from recorded runs. |

## Conventions

- One change per commit; tag the end of each step `step-0N-<name>` (see `CONTRIBUTING.md`).
- Do not break the earlier steps: `python -m unittest discover` stays green, with only the later steps skipped.
- Every number you quote in your notes comes from a script and has a test.
