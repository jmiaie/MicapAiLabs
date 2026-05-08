# Quickstart

This guide walks you from zero to a running OMPA vault in under 5 minutes.

## Install

```bash
pip install ompa          # Core only (vault + palace + KG + CLI + MCP)
pip install ompa[all]     # Adds local semantic search (sentence-transformers)
```

Requires Python 3.10+.

## Initialize a vault

Navigate to your project directory and run:

```bash
ao init
```

This creates the vault structure:

```
./
├── brain/        # Persistent agent memory: North Star, active work, people
├── work/         # Project work: decisions, incidents, wins, features
├── org/          # Organization: people, teams, processes
├── perf/         # Performance: retros, reviews, blockers
└── .palace/      # Agent metadata: wings, rooms, KG database, semantic index
```

Verify with:

```bash
ao status
ao doctor      # Full health check
```

## Use in a session

### CLI workflow

```bash
# At session start — inject ~2K tokens of context
ao session-start

# Route a message to the right vault folder
ao classify "We decided to go with Postgres over MySQL"
# → MessageType.DECISION → work/decisions/...

# Semantic search (zero API cost)
ao search "database decisions"

# Query the knowledge graph
ao kg-query "Postgres"

# End of session
ao wrap-up
```

### Python API

```python
from ompa import Ompa

ao = Ompa(vault_path="./workspace")

# Session start — returns ~2K token context string
context = ao.session_start()
print(context.output)  # inject this into your agent's system prompt

# Handle a user message
ao.handle_message("We're switching to Postgres for the main DB")

# After a tool call
ao.post_tool("write", {"file_path": "work/decisions/postgres.md"})

# Semantic search
results = ao.search("authentication decisions")
for r in results:
    print(f"{r.score:.2f}  {r.path}")

# Knowledge graph
ao.kg.add_triple("Kai", "works_on", "auth-service", valid_from="2026-01-01")
facts = ao.kg.query_entity("Kai")

# End session
ao.stop()
```

## MCP server (Claude Desktop / Cursor)

Add OMPA as an MCP server so Claude can access your vault directly:

```bash
claude mcp add ompa -- python -m ompa.mcp_server
```

Then restart Claude Desktop. You'll see 15 new tools: `ao_session_start`, `ao_search`, `ao_classify`, etc.

See the [MCP Server guide](guides/mcp.md) for full setup instructions.

## Semantic search

Semantic search is optional and uses `sentence-transformers` locally — no OpenAI/Anthropic API calls.

```bash
pip install ompa[all]       # Install with semantic support
ao rebuild-index            # Build the index from your vault
ao search "your query"      # Now uses semantic similarity
```

## Next steps

- [Lifecycle Hooks](guides/hooks.md) — wire OMPA into your agent's session loop
- [Dual-Vault](guides/dual-vault.md) — separate shared and personal notes
- [Message Types](guides/message-types.md) — all 15 types and their routing rules
- [API Reference](api/ompa.md) — full `Ompa` class documentation
