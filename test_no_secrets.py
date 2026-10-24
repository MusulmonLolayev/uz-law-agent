"""No API key or token may be committed. Scans every tracked file (or, without git, every file in the tree)."""
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).parent
PATTERNS = {
    "OpenAI-style key": re.compile(r"sk-[A-Za-z0-9]{16,}"),
    "DEEPSEEK_API_KEY with a value": re.compile(r"DEEPSEEK_API_KEY\s*=\s*['\"]?\S"),
    "GitHub token": re.compile(r"ghp_[A-Za-z0-9]{8,}"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{12,}"),
}
SKIP_DIRS = {".git", ".venv", "__pycache__"}


def tracked_files():
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
        return [ROOT / p for p in out.decode().split("\0") if p]
    except (OSError, subprocess.CalledProcessError):
        return [p for p in ROOT.rglob("*") if p.is_file() and not SKIP_DIRS & set(p.relative_to(ROOT).parts)]


def findings(name, text):
    return [f"{name}: {label}" for label, rx in PATTERNS.items() if rx.search(text)]


class NoSecrets(unittest.TestCase):
    def test_no_tracked_file_contains_a_key(self):
        found = []
        for path in tracked_files():
            if path.name == Path(__file__).name or not path.is_file():
                continue                       # this file spells the patterns out
            found += findings(path.relative_to(ROOT), path.read_text(encoding="utf-8", errors="ignore"))
        self.assertEqual(found, [])

    def test_the_scanner_catches_keys_and_accepts_the_example(self):
        self.assertTrue(findings("x", "DEEPSEEK_API_KEY=abc123"))
        self.assertTrue(findings("x", "key = 'sk-" + "a" * 20 + "'"))
        self.assertTrue(findings("x", "ghp_" + "a" * 36))
        self.assertTrue(findings("x", "AKIA" + "A" * 16))
        self.assertEqual(findings(".env.example", (ROOT / ".env.example").read_text()), [])
        self.assertEqual(findings("x", "DEEPSEEK_API_KEY=\n"), [])

    def test_env_files_are_ignored_except_the_example(self):
        ignore = (ROOT / ".gitignore").read_text().split()
        self.assertIn(".env", ignore)
        self.assertIn(".env.*", ignore)
        self.assertIn("!.env.example", ignore)
        self.assertFalse([p for p in tracked_files() if p.name.startswith(".env") and p.name != ".env.example"])


if __name__ == "__main__":
    unittest.main()
