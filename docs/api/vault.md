# Vault

The `Vault` class manages the markdown note storage layer.

## Import

```python
from ompa import Vault, Note, VaultConfig
```

## Vault structure

```
vault_root/
├── brain/       # Persistent memory: north-star, active-agents, team, archive
├── work/        # Project work: decisions, incidents, wins, bugs, features, ...
├── org/         # Organization: people, teams, processes
└── perf/        # Performance: retros, blockers, reviews
```

## Constructor

```python
vault = Vault(vault_path="./workspace")
```

Initializes the folder structure if it doesn't exist.

## Note CRUD

```python
# List all notes
notes: list[Note] = vault.list_notes()

# Get brain note
note: Note | None = vault.get_brain_note("north-star")

# Update brain note
vault.update_brain_note("north-star", "My persistent goal", append=False)

# Search by name
notes = vault.search_by_name("postgres")

# Find orphans
orphans: list[Note] = vault.find_orphans()
```

## Stats

```python
stats: dict = vault.get_stats()
# {
#   "total_notes": 42,
#   "brain_notes": 5,
#   "orphans": 2,
# }
```

## Validation

```python
result: dict = vault.validate_write("work/decisions/postgres.md")
# {"warnings": [...], "errors": [...]}
```

## Note

```python
note = Note(
    path=Path("work/decisions/postgres.md"),
    frontmatter={"date": "2026-05-07", "tags": ["decision"]},
    content="We decided to use Postgres for the main DB.",
)
note.save()

# Load from file
note = Note.from_file(Path("work/decisions/postgres.md"))
```

::: ompa.vault.Vault

::: ompa.vault.Note
