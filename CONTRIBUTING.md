# Contributing to OMPA

Thanks for your interest in contributing. Here's everything you need to get started.

## Setup

```bash
git clone https://github.com/jmiaie/ompa
cd ompa
pip install -e ".[dev,all]"
```

## Running tests

```bash
pytest tests/ -v
```

All 77+ tests should pass. Tests are in `tests/test_ompa.py`.

## Linting and formatting

```bash
ruff check ompa/        # Lint
ruff format ompa/       # Format
```

CI enforces both. Run these before opening a PR.

## Project structure

```
ompa/
├── core.py              # Ompa main class — start here
├── vault.py             # Vault CRUD
├── palace.py            # Palace metadata
├── knowledge_graph.py   # Temporal KG (SQLite)
├── hooks.py             # Lifecycle hooks
├── classifier.py        # 15 message types
├── semantic.py          # Semantic search
├── mcp_server.py        # MCP server
├── config.py            # Dual-vault config
└── cli.py               # CLI commands
```

See [CLAUDE.md](CLAUDE.md) for architecture decisions and internal API docs.

## Adding a message type

1. Add enum value to `MessageType` in `classifier.py`
2. Add regex patterns to `PATTERNS[MessageType]`
3. Add routing hints to `ROUTING_HINTS[MessageType]`
4. Add folder to `FOLDER_MAP[MessageType]`
5. Add test cases to `TestClassifier` in `tests/test_ompa.py`

## Adding a lifecycle hook

```python
from ompa.hooks import Hook, HookContext, HookResult

class MyHook(Hook):
    def __init__(self):
        super().__init__("my_hook", token_budget=50)

    def execute(self, context: HookContext, **kwargs) -> HookResult:
        return HookResult(hook_name=self.name, success=True, output="...", tokens_hint=50)

ao = Ompa("./workspace")
ao.hooks.register_hook("my_hook", MyHook())
```

## Changelog

Update `CHANGELOG.md` under `[Unreleased]` with your change before opening a PR.

## Pull requests

- Open a PR against `main`
- Fill out the PR template
- CI must pass (tests + lint)

## Reporting bugs

Use the [bug report template](https://github.com/jmiaie/ompa/issues/new?template=bug_report.md).
Include a minimal reproduction and your environment details.
