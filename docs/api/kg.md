# Knowledge Graph

The `KnowledgeGraph` stores temporal triples: `subject → predicate → object` with optional validity windows.

## Import

```python
from ompa import KnowledgeGraph
```

## Constructor

```python
kg = KnowledgeGraph(db_path="./.palace/knowledge_graph.sqlite3")
```

## Adding triples

```python
kg.add_triple(
    subject="Kai",
    predicate="works_on",
    object="auth-service",
    valid_from="2026-01-01",         # optional ISO date
    valid_to="2026-06-30",           # optional — open-ended if omitted
    source="work/decisions/auth.md", # optional provenance
)
```

## Querying

```python
# All current facts about an entity
triples: list = kg.query_entity("Kai")

# Facts as of a specific date
triples = kg.query_entity("Kai", as_of="2025-12-31")

# Entity timeline (all events, sorted by date)
timeline: list[dict] = kg.timeline("auth-service")
```

## Auto-population from vault

```python
# Populate from all notes in a vault
count: int = kg.populate_from_vault("./workspace")

# Populate from a single note
count = kg.populate_from_note(
    note_path=Path("work/decisions/postgres.md"),
    vault_root=Path("./workspace"),
)
```

Auto-population extracts:

- Frontmatter `tags` → `(tag, "tagged_in", note_stem)` triples
- Folder path → `(note_stem, "in_folder", folder_name)` triples
- `[[wikilinks]]` → `(source_note, "links_to", target_note)` triples

## Statistics

```python
stats: dict = kg.stats()
# {
#   "entity_count": 15,
#   "triple_count": 87,
#   "current_facts": 62,
# }
```

## Temporal validity

Triples support validity windows. A triple is "current" if today falls within `[valid_from, valid_to]` (open-ended if `valid_to` is null).

```python
# Fact valid for Q1 2026
kg.add_triple("Kai", "role", "tech-lead", valid_from="2026-01-01", valid_to="2026-03-31")

# Fact still valid (no end date)
kg.add_triple("Kai", "works_on", "Orion", valid_from="2026-01-01")

# Query as of a past date
old_facts = kg.query_entity("Kai", as_of="2025-06-01")
```

::: ompa.knowledge_graph.KnowledgeGraph
