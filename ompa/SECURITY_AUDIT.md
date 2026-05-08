# Security Audit — OMPA v1.0.0

**Date:** 2026-05-07
**Version:** 1.0.0
**Tool versions:** bandit 1.8.x, mypy 1.x, manual review

---

## Summary

**Overall rating: 9/10 (Good)**

OMPA v1.0.0 passes all automated security checks with no medium or high severity findings. The two low-severity bandit findings from prior audits (subprocess usage for git) remain classified as acceptable. mypy now reports 0 errors across 26 source files.

---

## Test results

| Check | Result |
|---|---|
| bandit SAST | ✓ Clean (exit 0, no medium/high findings) |
| mypy type checking | ✓ Clean (0 errors across 26 source files) |
| Tests | ✓ 77+ unit tests + property-based tests (hypothesis) |
| Path traversal | ✓ All vault ops boundary-checked via `_safe_resolve` |
| SQL injection | ✓ Parameterized queries throughout |
| Credential sanitization | ✓ `_sanitize_content()` redacts tokens, API keys, secrets |
| Dependency audit | ✓ pip-audit in CI (checks against PyPI advisory database) |

---

## Known low-severity findings

### B404 / B603 — subprocess usage for git

**Location:** `ompa/hooks.py`, `ompa/sync/git.py`

**Status:** Accepted

**Justification:** Subprocess is used exclusively to call `git` by absolute path (located via `shutil.which`). No user input is passed to the shell; all arguments are constructed from internal constants. The git binary path is resolved before passing to `subprocess.run` (B603 pattern). No viable pure-Python alternative for `git log` / `git push` exists.

---

## Architecture security notes

### Path traversal protection

All vault file operations resolve paths through `_safe_resolve(vault_root, user_path)` before access. Paths that escape the vault root raise `ValueError` and are rejected before any I/O.

### SQL injection prevention

All KnowledgeGraph operations use parameterized SQLite queries (`?` placeholders). No string interpolation is used in SQL statements. WAL mode and thread-local connections were added in v1.0.0 without changing the parameterization model.

### Credential sanitization in export

`Ompa._sanitize_content()` redacts the following patterns before exporting personal vault notes to shared:

- `sk-*` (OpenAI-style API keys)
- `AKIA*` (AWS access key IDs)
- `token:`, `password:`, `secret:`, `api_key:`, `api-key:` (any value)

### Local-only by default

OMPA stores all data locally. No data is transmitted to external services unless:

- `ompa[nim]` is used (sends text to NVIDIA NIM API for embeddings)
- `ompa[s3]` sync is configured (sends files to S3/R2/MinIO)
- Git remote push is configured

All external communication is opt-in and documented.

### Dependency surface

Core runtime: `typer`, `rich`, `python-frontmatter` — minimal, widely-audited.
Optional: `sentence-transformers`, `faiss-cpu`, `boto3`, `httpx` — loaded only when explicitly installed.

---

## Recommendations for users

1. **Pin versions** in production: `pip install ompa==1.0.0`
2. **Restrict vault permissions** to the agent user (e.g. `chmod 700 ./vault`)
3. **Never store credentials in vault notes** — use environment variables
4. **Use `--sanitize` (default: on)** when exporting personal notes to shared vault
5. **Run `pip-audit`** in your own CI to catch newly disclosed dependency vulnerabilities

---

## Previous audit

v0.4.1 audit: 59/59 tests, rating 8/10. Archived in `.internal/`.
