# Adding another Uzbek law as a corpus

This project is an open-source research agent over Uzbek law. Its starter corpus is the Labor Code of Uzbekistan
(`data/mehnat_kodeksi.jsonl`), the corpus used in the course videos; the loop, the recorded runs and the tests in this
repository use it. This page says how to add another law, using only what the code does today, with `corpus.py` as
the pattern.

**What is and is not wired.** Today the agent loop is wired to the Labor Code corpus: `agent.py`'s command line sets
`law = corpus`, and `llm.py` replays traces recorded against it. `agent.run(question, model, law=...)` and
`agent.act(..., law=...)` already take a corpus module as an argument, but nothing builds one for a second law and no
command-line switch chooses it. Wiring a second law into `agent.py` is open work for contributors; this page does not
do it, and does not change `agent.py`.

## 1. The data file: one JSON object per line

Put the file in `data/` as UTF-8 JSON Lines, one provision (article, regulation, section) per line. Fields `corpus.py`
reads:

| Field | Used by | Meaning |
|---|---|---|
| `article_id` | `ARTICLES`, `search`, `fetch_article` | unique id, a string; the key of the `ARTICLES` dict and what the agent cites. Labor Code: `"182"`. |
| `title` | `search`, `fetch_article` | the provision's heading; indexed for `search`, a title word counting twice, and shown in search results. |
| `text` | `search`, `fetch_article` | the full text of the provision; indexed and returned by `fetch_article`. |
| `article_display` | `fetch_article` | how the provision is named when printed, e.g. `"1-modda"`. |

The Labor Code records also carry `seq`, `code`, `article_raw`, `kind`, `section`, `chapter`, `lex_uz_doc` and
`snapshot_date`. They are provenance and navigation and the search ignores them, but keep what your source gives you
(a document id or URI, the date of the text) so a quote can be traced back. If your loader needs a field, say which in
the loader's docstring.

Rules `corpus.py` relies on: ids are unique (a repeated id silently overwrites the earlier record in `ARTICLES`),
`text` is not empty, and the file is one line per record, so `len(ARTICLES)` equals the number of lines. Keep the text
as published; do not edit the law. If you leave out repealed provisions with no text, say so in the source note.

## 2. The two tools a corpus provides

A corpus module exposes the same two functions as `corpus.py`:

- `search(query, k=5)` returns the `k` best provisions as a list of `(article_id, title, score)`, best first. The
  current version counts the query's word stems that a provision contains (stems are the first five letters, so
  Uzbek suffixes meet). A better retriever may replace the inside; the interface stays. Normalise the language's
  quirks on both sides: `corpus.py` maps keyboard apostrophes to the corpus's `ʻ`, so `o'n` finds `oʻn`.
- `fetch_article(ref)` returns the full text of one provision as a string, or `None` if there is no such provision.
  It must accept what a model writes: `corpus.py` strips whitespace and a trailing `-modda`.

The loop also reads these module-level names from the corpus passed as `law` (see `act` and `run` in `agent.py`):
`FETCH` (the action's name, `"fetch_article"`), `CITE` (a format such as `"Art. {}"`), `NOT_FOUND`, `MISSING` (a
format with one `{}`), `SYSTEM` (the system prompt that tells the model what the actions are and how to cite) and,
for the no-tools baseline, `NO_TOOLS` and `QUESTIONS`. `corpus.py` defines them. A corpus for the agent defines all of
them.

## 3. The source note: `data/SOURCE_<name>.md`

Every data file has a note next to it, named like `SOURCE.md` (Labor Code). Write:

- what the file is: the law's title, number and adoption date, and the count of records;
- where the text came from: the URL (or repository and commit), the date you retrieved it, and the date the text is
  valid for if the law is amended over time;
- how you made the file: unchanged from a source, or converted by a script you commit (listing the source files and
  their sha256);
- the licence or legal basis, quoted with its link (see section 5);
- the sha256 of the data file, which the tests check.

## 4. Pin the file with a hash

```bash
sha256sum data/<name>.jsonl
```

Paste the 64-character digest into `SOURCE_<name>.md`. The tests recompute the digest from the file and require it to
occur in the note (`test_the_file_is_the_pinned_one` in `test_agent.py`), so an accidental edit, a changed line ending
or a re-download of an amended text fails loudly. If you rebuild the file on purpose, update the note in the same
commit. If you convert from downloaded sources, also record the sha256 of each source file.

## 5. Licence caution

Check that the text may be reused before you commit it, and say so in the note; do not assume. For the Labor Code, the
file comes from a corpus released under CC0, and the note adds the legal basis that legislative text is not
copyrightable under Art. 8 of the Law on Copyright and Related Rights. For a new law:

- state who published the text you used (an official portal, a third-party corpus, a gazette) and under what terms;
- an official legal text is not automatically free to redistribute in a dataset, and a third-party corpus may add its
  own terms to the texts it hosts; state the status you found, with the link, and do not guess;
- if you cannot establish that the text may be reused, do not commit it. Keep the file local, or ask in the pull
  request.

Nothing in this repository is legal advice, and the agent's answers are not legal advice.

## 6. Checklist

- [ ] `data/<name>.jsonl`: UTF-8, one record per line, unique non-empty `article_id`, a `title`, a non-empty `text`
- [ ] `article_display` (and any other field your `fetch_article` prints) present in every record
- [ ] `data/SOURCE_<name>.md`: law, URL, date retrieved, how made, licence with link, sha256
- [ ] the sha256 in the note matches `sha256sum` of the file
- [ ] a loader module with `search(query, k)` and `fetch_article(ref)`, `fetch_article` returning `None` for a missing id
- [ ] the language's spelling quirks (apostrophes, case, diacritics) are normalised in `search` and `fetch_article`
- [ ] for use in the agent: `FETCH`, `CITE`, `NOT_FOUND`, `MISSING`, `SYSTEM`, `NO_TOOLS`, `QUESTIONS` defined, and
      the command line chooses the corpus (open work; do not change the Labor Code prompts, the recorded runs are
      keyed to them)
- [ ] every number or quoted fact in your notes has a test that recomputes it from the file
- [ ] `uv run python -m unittest discover` is green, and the Labor Code tests still pass unchanged

## 7. A minimal loader test

Modelled on the `Corpus` tests in `test_agent.py`. Replace `corpus_xx` with your module, and the counts and the known
article with values you read from the file.

```python
import hashlib
import unittest

import corpus_xx


class NewCorpus(unittest.TestCase):
    def test_it_loads_the_pinned_file(self):
        note = (corpus_xx.DATA.parent / "SOURCE_XX.md").read_text()
        self.assertIn(hashlib.sha256(corpus_xx.DATA.read_bytes()).hexdigest(), note)
        lines = corpus_xx.DATA.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(corpus_xx.ARTICLES), len(lines))     # no id used twice
        self.assertEqual(len(lines), 123)                         # the count the note states

    def test_the_tools(self):
        hit = corpus_xx.search("a word from a known article")[0][0]
        self.assertEqual(hit, "7")                                # the article you know it is
        self.assertIn("a phrase from its text", corpus_xx.fetch_article("7"))
        self.assertIsNone(corpus_xx.fetch_article("no such id"))
```
