# Contributing

Pull requests are welcome.

## Commits

Make small commits, one change each. The message says what changed and why ("Chunk articles at 500 characters so a
search hit points to a passage"), not only the file names. Do not mix a refactor with a new feature.

## Tests

```bash
uv sync
uv run python -m unittest discover
```

Run this before you open a pull request. The tests are offline and need no key. Every number the documentation quotes
should come from a script and have a test that recomputes it from the raw data.

## Keys

Never commit a key. `.env` is git-ignored; `.env.example` is the template to copy. `test_no_secrets.py` fails if a key
is found in a tracked file.

## Recorded runs

`traces/` holds recorded runs of the agent (the model's replies, saved in order). They are replayed offline, without a
key, and the tests check them:

```bash
uv run python agent.py --replay q2_under18                # replay a recorded run
uv run python agent.py --record NAME "your question"      # run live (needs a key in .env) and save traces/NAME.json
```

A replay checks that each prompt is the one that was recorded, so a change to the prompts or the tools means the
affected traces must be recorded again.
