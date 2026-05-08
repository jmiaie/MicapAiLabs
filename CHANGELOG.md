# Changelog

All notable changes to OMPA are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added

- **`ao doctor` command**: rich health check table — vault structure, KG, palace, semantic index, orphan count
- **MkDocs Material documentation site** (`docs/`) with guides, API reference, and GitHub Pages workflow
- **Examples**: `examples/langchain_agent/`, `examples/multi_agent/`, `examples/mcp_desktop/`
- **LongMemEval benchmark** (`benchmarks/longmemeval.py`) — reproducible R@5 measurement
- **Framework adapters** (`ompa/adapters/`):
  - `OmpaMemory` + `OmpaRetriever` — LangChain `BaseChatMemory`-compatible components (`ompa[langchain]`)
  - `OmpaReader` + `OmpaVaultRetriever` — LlamaIndex reader + retriever (`ompa[llamaindex]`)
  - `OmpaAgentHooks` — OpenAI Agents SDK `AgentHooks` implementation
  - `NIMEmbeddingBackend` — NVIDIA NIM API embeddings backend, drop-in for sentence-transformers (`ompa[nim]`)
- **Token counting** (`ompa/token_counter.py`): tiktoken-precise counting with word-count heuristic fallback (`ompa[tiktoken]`); hooks now report accurate `tokens_hint`
- **Pluggable embedding backend**: `SemanticIndex` and `Ompa` accept `embedding_backend=` parameter — swap sentence-transformers for NIM or any custom encoder
- **Multi-node vault sync** (`ompa/sync/`):
  - `SyncBackend` abstract base class with `push` / `pull` / `status` interface
  - `GitSyncBackend` — add → commit → push / pull --rebase
  - `S3SyncBackend` — S3/R2/MinIO sync via boto3 (`ompa[s3]`)
  - `RsyncBackend` — rsync over SSH, ideal for Tailscale LAN deployments
  - `ao sync --backend git|s3|rsync --remote <target>` CLI option
- `ompa[docs]` optional dependency group (`mkdocs-material`, `mkdocstrings`)
- New optional dep groups: `ompa[langchain]`, `ompa[llamaindex]`, `ompa[nim]`, `ompa[tiktoken]`, `ompa[s3]`
- `ompa[all]` now includes `ompa[semantic]` + `ompa[tiktoken]`
- Documentation URL updated to `https://jmiaie.github.io/ompa`

### Changed

- `__version__` bumped to `0.6.0-dev`
- `SemanticIndex` cosine similarity now uses pure numpy (removes `sentence_transformers.util` dependency from the search path)
- `ao sync` CLI: added `--backend`, `--remote`, `--message`, `--push` options

---

*(Phase 4 — in development)*

### Added (Phase 4)

- **`AsyncOmpa`** (`ompa/async_api.py`): async-native wrapper — every lifecycle method is a coroutine backed by `ThreadPoolExecutor`; supports `async with AsyncOmpa(...) as ao:` context manager; safe for concurrent multi-agent use
- **FAISS semantic index** (`ompa/adapters/faiss.py`): `FAISSSemanticIndex` — drop-in for `SemanticIndex` with sub-millisecond ANN search; flat (exact) or IVF (approximate) modes; stores embeddings as `.npy` + FAISS binary index; `ompa[faiss]` optional dep
- **Vault migration tooling** (`ompa/migration.py`): `VaultMigrator` with `check()` + `run()` + dry-run support; schema versioned via `.palace/schema_version`; current migrations: init palace, add composite KG indexes, enable WAL mode
- **`ao migrate-vault` CLI command**: runs pending migrations with `--dry-run` and `--force` options

### Changed (Phase 4)

- `KnowledgeGraph`: WAL mode + `PRAGMA synchronous=NORMAL` enabled in `_init_db()`; thread-local connection cache via `threading.local()` (avoids open/close overhead per call); three new composite indexes: `idx_triples_subject_date`, `idx_triples_object_pred`, `idx_triples_validity`
- `ompa[faiss]` optional dep group added (`faiss-cpu>=1.7.0`)

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

[Unreleased]: https://github.com/jmiaie/ompa/compare/v0.4.2...HEAD
[0.4.2]: https://github.com/jmiaie/ompa/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/jmiaie/ompa/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/jmiaie/ompa/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/jmiaie/ompa/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/jmiaie/ompa/compare/v0.2.2...v0.3.0
[0.2.2]: https://github.com/jmiaie/ompa/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/jmiaie/ompa/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/jmiaie/ompa/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/jmiaie/ompa/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/jmiaie/ompa/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/jmiaie/ompa/releases/tag/v0.1.0
