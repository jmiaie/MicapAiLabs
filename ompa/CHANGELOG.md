# Changelog

All notable changes to OMPA are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

---

## [1.0.7] — 2026-05-08

### Fixed

- **Windows SQLite file locking**: `KnowledgeGraph.close()` + `__del__` now explicitly close
  the thread-local connection — prevents `PermissionError [WinError 32]` when temp directories
  are cleaned up while a connection is still held. `Ompa.close()` + `__del__` propagate to KG.
- **`test_properties.py` collection crash**: replaced try/except `HYPOTHESIS_AVAILABLE` pattern
  with `pytest.importorskip("hypothesis")` — the old pattern left `st.*` strategy definitions
  at module level where they crashed at collection time when hypothesis wasn't installed.
- **`TestSemanticIndex` duplicate class**: renamed second definition to `TestSemanticIndexBehavior`
  to resolve `F811` ruff violation.
- **Test ruff violations**: fixed `E712` (`== True` → truth check), `F841` (unused `count`
  assignments), `I001` (import sort), `SIM105` (contextlib.suppress), `F811` (duplicate class)
- **`tests/conftest.py`**: added Windows-safe `TemporaryDirectory` patch
  (`ignore_cleanup_errors=True`) as belt-and-suspenders for any test that doesn't explicitly
  call `close()` before temp directory teardown.

### Changed

- `__version__` → `1.0.7`

---

## [1.0.6] — 2026-05-08

### Added

- **`ao upgrade` command**: checks PyPI for the latest ompa version and upgrades in-place via
  `pip install --upgrade ompa==<latest>` using the current Python interpreter; prompts for
  confirmation unless `--yes` / `-y` is passed
- **Version check in `ao status`**: prints a one-line banner showing installed version and whether
  it is current; shows `→ <latest> available — run ao upgrade` when out of date
- **Version row in `ao doctor`**: the health-check table now includes an `ompa version` row
  (OK when current, WARN with upgrade hint when a newer version is available on PyPI)

### Changed

- `__version__` → `1.0.6`
- README CLI reference updated with `ao upgrade`, `ao doctor`, and `ao migrate-vault` entries

---

## [1.0.5] — 2026-05-08

### Fixed

- `ruff format`: applied auto-formatter to all 20 source files that had whitespace/line-length
  differences from ruff's canonical style — this was causing the CI `Lint & Format` job to fail

### Changed

- README: Three-Layer Architecture diagram replaced with a Mermaid flowchart (renders as a
  graphic on GitHub); added a summary table mapping each layer to what it stores and who reads it
- README: corrected stale `git clone` URL in Installation section (now points to MicapAiLabs monorepo)
- `__version__` → `1.0.5`

---

## [1.0.4] — 2026-05-08

### Fixed

- ruff lint: 99 violations fixed across the package (I001 import sort, UP* modernizations,
  F401 unused imports, B904 raise-from-None, B905 zip strict=, E741 ambiguous names,
  F841 unused variable, SIM102/SIM114 simplifications)
- `pyproject.toml`: added `B008` to ruff ignore list (typer requires `Option()` in defaults)

### Changed

- `__version__` → `1.0.4`

---

## [1.0.3] — 2026-05-08

### Fixed

- `ompa-publish.yml`: set `packages-dir: ompa/dist` so the PyPI publish action finds
  the built wheel — `defaults: run: working-directory` only applies to `run:` steps,
  not `uses:` actions, so the action was looking in the wrong directory

### Changed

- `__version__` → `1.0.3`

---

## [1.0.2] — 2026-05-08

### Fixed

- Import sort order in `ompa/__init__.py` (ruff I001 — alphabetical order required)
- Tag-triggered publish now uses a separate `ompa-publish.yml` workflow with no
  `paths` filter — the `paths` filter on `ompa-ci.yml` was silently blocking
  tag-triggered runs from reaching the publish job

### Changed

- `__version__` → `1.0.2`

---

## [1.0.1] — 2026-05-08

### Removed

- Orphaned `ompa/.github/` directory (old per-project `ci.yml`, `docs.yml`, issue templates,
  PR template) — these files are ignored by GitHub in the MicapAiLabs monorepo; CI is now
  handled exclusively by root-level `.github/workflows/ompa-ci.yml`

### Changed

- `__version__` → `1.0.1`

---

## [1.0.0] — 2026-05-07

First stable release. Semver commitment begins here — no breaking public API changes without a major version bump.

### Added

- **`ao doctor` command**: rich health check table — vault structure, KG, palace, semantic index, orphans
- **MkDocs Material documentation site** (`docs/`) deployed to GitHub Pages; guides for hooks, MCP, dual-vault, message types; full API reference
- **LongMemEval benchmark** (`benchmarks/longmemeval.py`) — reproducible R@5 measurement with 20-item built-in dataset
- **Framework adapters** (`ompa/adapters/`):
  - `OmpaMemory` + `OmpaRetriever` — LangChain `BaseChatMemory`-compatible components (`ompa[langchain]`)
  - `OmpaReader` + `OmpaVaultRetriever` — LlamaIndex reader + retriever (`ompa[llamaindex]`)
  - `OmpaAgentHooks` — OpenAI Agents SDK `AgentHooks` integration
  - `NIMEmbeddingBackend` — NVIDIA NIM API embeddings, drop-in for sentence-transformers (`ompa[nim]`)
  - `FAISSSemanticIndex` — sub-millisecond ANN search via FAISS flat/IVF index (`ompa[faiss]`)
- **`AsyncOmpa`** (`ompa/async_api.py`): full async-native API backed by `ThreadPoolExecutor`; `async with AsyncOmpa(...) as ao:` context manager; safe for concurrent multi-agent workloads
- **Token counting** (`ompa/token_counter.py`): tiktoken-precise counting with word-count heuristic fallback; `tokens_hint` in `HookResult` is now accurate (`ompa[tiktoken]`)
- **Pluggable embedding backend**: `SemanticIndex` and `Ompa` accept `embedding_backend=` — swap sentence-transformers for NIM or any `encode(text) -> list[float]` implementation
- **Multi-node vault sync** (`ompa/sync/`):
  - `SyncBackend` ABC + `SyncResult` dataclass
  - `GitSyncBackend` — add → commit → push / pull --rebase
  - `S3SyncBackend` — S3/R2/MinIO sync via boto3 (`ompa[s3]`)
  - `RsyncBackend` — rsync over SSH, Tailscale-ready (excludes semantic index)
  - `ao sync --backend git|s3|rsync --remote <target>` CLI option
- **Vault migration tooling** (`ompa/migration.py`): `VaultMigrator.check()` + `.run()` with dry-run; schema versioned via `.palace/schema_version`; three migrations: init palace, composite KG indexes, WAL mode
- **`ao migrate-vault` CLI command** with `--dry-run` and `--force` flags
- **Property-based tests** (`tests/test_properties.py`): 15 hypothesis-driven invariant tests across KG, classifier, token counter, vault, and sync
- **`STABILITY.md`**: documents the stable public API contract and deprecation policy
- Optional dep groups: `ompa[langchain]`, `ompa[llamaindex]`, `ompa[nim]`, `ompa[tiktoken]`, `ompa[s3]`, `ompa[faiss]`, `ompa[docs]`
- `ompa[all]` now includes `ompa[semantic]` + `ompa[tiktoken]`
- GitHub scaffolding: issue templates, PR template, `CONTRIBUTING.md`
- `.markdownlint.json`: project-wide markdown lint config
- CI: `Security Audit` job (bandit + pip-audit) on every push; `Deploy Docs` workflow for GitHub Pages

### Changed

- `__version__` → `1.0.0`; `Development Status` classifier → `Production/Stable`
- `KnowledgeGraph`: WAL mode + `PRAGMA synchronous=NORMAL`; thread-local connection cache; three new composite indexes (`subject_date`, `object_pred`, `validity`)
- `SemanticIndex` cosine similarity moved to pure numpy — removes `sentence_transformers.util` from hot path
- `ao sync` CLI: added `--backend`, `--remote`, `--message`, `--push` options
- `hooks.py`: `tokens_hint` computed via `count_tokens()` (tiktoken when available, heuristic otherwise)
- `pyproject.toml`: `Documentation` URL → `https://jmiaie.github.io/ompa`; `mypy`, `hypothesis`, `bandit`, `pip-audit` added to dev deps

### Security

- All 26 source files pass mypy with 0 errors
- bandit SAST: clean (exit 0, no medium/high findings)
- pip-audit added to CI for ongoing dependency vulnerability scanning
- See `SECURITY_AUDIT.md` for full report

---

## [0.4.2] — 2026-05-07

### Added

- Python 3.14 classifier and CI matrix support
- `pytest-cov` dev dependency for coverage reporting
- Codecov integration in CI workflow
- `mypy` dev dependency for type checking
- `[tool.ruff]`, `[tool.pytest.ini_options]`, `[tool.mypy]` config sections in `pyproject.toml`

### Changed

- CI workflow: added `fail-fast: false`, pip caching, explicit job names, and `--tb=short`
- CI lint job: replaced `black --check` with `ruff format --check`
- README: complete restructure — hero section, 8 badges, comparison table above the fold, CLI reference table, dual-vault section

### Removed

- Internal build/prompt files removed from public repo root (`CLAUDE_CODE_PROMPT.md`, `AGNOSTIC_OBSIDIAN_CLAUDE_CODE_PROMPT.md`, `PUSH.md`, `RELEASE.md`)

---

## [0.4.1] — 2026-04-11

### Fixed

- **Path traversal hardening**: all vault file operations now resolve and boundary-check paths against the vault root before proceeding
- **Semantic lazy-init**: `SemanticIndex._model` deferred until first access — import no longer triggers model download
- Brain note names with path separators now rejected at the API boundary

### Security

- Full security audit completed: 8/10 rating, 2 low-severity bandit findings (acceptable subprocess usage for git)
- 59/59 unit tests passing at audit time

---

## [0.4.0] — 2026-04-10

### Added

- **Dual-vault architecture**: `DualVaultConfig` + `IsolationMode` for shared/personal vault separation
- `IsolationMode.AUTO` — content auto-classified to shared or personal vault based on message type
- `IsolationMode.MANUAL` — explicit `VaultTarget` routing per operation
- Export/import between vaults with sanitization (strips personal identifiers before sharing)
- `ao_dual_vault_*` MCP tools for shared vault operations
- `DualVaultConfig`, `IsolationMode`, `VaultTarget` exported from public API

### Changed

- `Ompa` constructor accepts either `vault_path: str` or `config: DualVaultConfig`

---

## [0.3.1] — 2026-04-09

### Fixed

- Orphan detection: notes with broken wikilinks now correctly flagged
- Brain note counting: `ao status` count was off-by-one in nested structures
- Wikilink resolution: `[[Note Name]]` now resolves case-insensitively across the vault

---

## [0.3.0] — 2026-04-08

### Added

- **Auto-populate KG from vault**: `KnowledgeGraph.populate_from_vault()` scans existing notes, extracts entities from frontmatter tags, folder paths, and `[[wikilinks]]`
- **Incremental semantic index**: `SemanticIndex` tracks file modification times and only re-embeds changed notes
- **Brain note sync**: `ao session-start` now syncs the brain note list against actual vault contents

### Changed

- `ao rebuild-index` now skips unchanged files (was full rebuild previously)

---

## [0.2.2] — 2026-04-07

### Security

- Resolved all `bandit` scan issues: B110 (bare except), B404 (subprocess import), B603 (subprocess call)
- Added `usedforsecurity=False` to MD5 hash usage

### Changed

- PyPI publishing switched to **trusted publishing** (OIDC) — no more long-lived tokens

---

## [0.2.1] — 2026-04-06

### Added

- Expanded test suite: 59 test cases across 10 test classes
- `TestDualVault` with 18 test cases covering shared/personal isolation
- `TestKGPopulation` with 5 test cases for vault-to-KG auto-population
- `TestOrphanAndBrainFixes` with 6 regression test cases

### Fixed

- Reliability fixes for vault note CRUD under concurrent access
- `ao orphans` false-positive rate reduced by improved wikilink normalization
- UTF-8 encoding explicitly enforced for all vault file writes

### Security

- Path traversal protection added to all `vault.py` file operations

---

## [0.2.0] — 2026-04-05

### Changed

- **Complete rename**: `AgnosticObsidian` → `Ompa`, `agnostic_obsidian` → `ompa` throughout
- Backward compatibility alias: `AgnosticObsidian = Ompa` preserved in `__init__.py`
- Package published to PyPI as `ompa`

### Added

- Asciinema demo recording (`demo.cast`)
- PyPI version, Python version, and License shields in README
- `SECURITY_AUDIT.md`

### Fixed

- All ruff lint errors resolved
- All black formatting issues resolved

---

## [0.1.2] — 2026-04-04

### Fixed

- Import resolution: all internal imports updated from `agnostic_obsidian` to `ompa`
- CI: workflow now triggers correctly on `v*` version tags
- Build: setuptools package discovery config added

---

## [0.1.1] — 2026-04-03

### Changed

- Rebrand: **AgnosticObsidian → OMPA** (Obsidian-MemPalace-Agnostic)
- Credits section added to README acknowledging MemPalace, obsidian-mind, Claude Code, OpenClaw

---

## [0.1.0] — 2026-04-02

### Added

- Initial release as **AgnosticObsidian**
- **Three-layer memory architecture**: Vault (markdown) + Palace (metadata) + Knowledge Graph (SQLite)
- **5 lifecycle hooks**: `session_start`, `user_message`, `post_tool`, `pre_compact`, `stop`
- **15 message types** with auto-routing: DECISION, INCIDENT, WIN, LOSS, BLOCKER, QUESTION, SUGGESTION, REVIEW, BUG, FEATURE, LEARN, RETROSPECTIVE, ALERT, STATUS, CHORE
- **MCP server** with 14 tools via Model Context Protocol
- **CLI** with 14 commands (`ao init`, `ao session-start`, `ao classify`, etc.)
- **Local semantic search** using `sentence-transformers` (all-MiniLM-L6-v2), zero API cost
- **Temporal knowledge graph**: SQLite triples with validity windows, `query_entity`, `timeline`
- **Palace navigation**: wings, rooms, drawers, halls, tunnels
- GitHub Actions CI/CD with matrix testing (Python 3.10–3.13)

[Unreleased]: https://github.com/jmiaie/MicapAiLabs/compare/v1.0.7...HEAD
[1.0.7]: https://github.com/jmiaie/MicapAiLabs/compare/v1.0.6...v1.0.7
[1.0.6]: https://github.com/jmiaie/MicapAiLabs/compare/v1.0.5...v1.0.6
[1.0.5]: https://github.com/jmiaie/MicapAiLabs/compare/v1.0.4...v1.0.5
[1.0.4]: https://github.com/jmiaie/MicapAiLabs/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/jmiaie/MicapAiLabs/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/jmiaie/MicapAiLabs/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/jmiaie/MicapAiLabs/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/jmiaie/MicapAiLabs/compare/v0.4.2...v1.0.0
[0.4.2]: https://github.com/jmiaie/MicapAiLabs/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/jmiaie/MicapAiLabs/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/jmiaie/MicapAiLabs/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/jmiaie/MicapAiLabs/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/jmiaie/MicapAiLabs/compare/v0.2.2...v0.3.0
[0.2.2]: https://github.com/jmiaie/MicapAiLabs/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/jmiaie/MicapAiLabs/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/jmiaie/MicapAiLabs/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/jmiaie/MicapAiLabs/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/jmiaie/MicapAiLabs/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/jmiaie/MicapAiLabs/releases/tag/v0.1.0
