# Ompa

The `Ompa` class is the main entry point. It integrates all three layers (Vault, Palace, Knowledge Graph) with lifecycle hooks, message classification, and semantic search.

## Import

```python
from ompa import Ompa
```

## Constructor

```python
Ompa(
    vault_path: str | Path = None,
    agent_name: str = "agent",
    enable_semantic: bool = True,
    # Dual-vault
    shared_vault_path: str | Path = None,
    personal_vault_path: str | Path = None,
    isolation_mode: str = "strict",
)
```

**Single vault:**
```python
ao = Ompa(vault_path="./workspace")
ao = Ompa(vault_path="./workspace", agent_name="Kai", enable_semantic=False)
```

**Dual vault:**
```python
ao = Ompa(
    shared_vault_path="./team-vault",
    personal_vault_path="~/.ompa-personal",
    isolation_mode="auto",
)
```

## Lifecycle hooks

```python
result: HookResult = ao.session_start()
# result.output — ~2K token string, inject into agent system prompt
# result.success — bool
# result.tokens_hint — estimated token count

result = ao.handle_message("We decided to use Postgres")
result = ao.post_tool("write", {"file_path": "work/decisions/postgres.md"})
result = ao.pre_compact(transcript_so_far)
result = ao.stop()

# Aliases
ao.wrap_up()    # alias for stop()
ao.standup()    # alias for session_start()
```

## Classification

```python
c: Classification = ao.classify("We decided to use Postgres")
c.message_type      # MessageType.DECISION
c.confidence        # 0.92
c.suggested_action  # "File in work/decisions/"
c.routing_hints     # list[str]

hint: str = ao.get_routing_hint("We decided to use Postgres")
# → "DECISION → work/decisions/"
```

## Search

```python
results: list[SearchResult] = ao.search(
    query="authentication decisions",
    limit=5,
    hybrid=True,          # semantic + keyword
    wing="Orion",         # filter by palace wing
    room="auth",          # filter by room
    vaults=["shared"],    # "shared", "personal", or both
)

for r in results:
    print(r.path, r.score, r.content_excerpt)

# Rebuild semantic index
count: int = ao.rebuild_index()
```

## Knowledge graph

```python
ao.kg_add("Kai", "works_on", "auth-service", valid_from="2026-01-01")
ao.kg_add("Postgres", "chosen_over", "MySQL", source="work/decisions/db.md")

triples: list = ao.kg_query("Kai")
triples = ao.kg_query("Kai", as_of="2025-12-31")

timeline: list = ao.kg_timeline("auth-service")

count: int = ao.kg_populate()   # populate from all vault notes
```

## Vault management

```python
stats: dict = ao.get_stats()
# {"total_notes": 42, "brain_notes": 5, "orphans": 2}

orphans: list[Note] = ao.find_orphans()

ao.update_brain("north-star", "Build the best agent memory layer")
note = ao.get_brain_note("north-star")
```

## Palace

```python
count: int = ao.palace_build()  # auto-build from vault structure

ao.palace.create_wing("Orion", type="project")
ao.palace.create_room("Orion", "auth-migration")
ao.palace.create_tunnel("Kai", "Orion", "auth-migration")

wings = ao.palace.list_wings()
rooms = ao.palace.list_rooms("Orion")
```

## Dual-vault operations

```python
result = ao.write("content", vault="shared", tags=["decision"])
result = ao.export_to_shared("work/decisions/postgres.md", sanitize=True)
result = ao.import_to_personal("team/decisions/postgres.md", link_back=True)
result = ao.sync()  # full sync: KG + palace + semantic index
```

## Properties

```python
ao.is_dual_vault    # bool — True if dual-vault mode active
ao.vault            # Vault instance (shared/primary)
ao.palace           # Palace instance
ao.kg               # KnowledgeGraph instance
ao.hooks            # HookManager instance
ao.classifier       # MessageClassifier instance
ao.semantic         # SemanticIndex | None (lazy-loaded)
```

::: ompa.core.Ompa
