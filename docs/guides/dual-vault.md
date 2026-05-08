# Dual-Vault

Dual-vault mode separates **shared** (team/org) content from **personal** (private/sensitive) content into two isolated vaults. Each vault has its own palace, knowledge graph, and semantic index.

## When to use dual-vault

- You're working with a team and some notes should stay private
- You want to share vault snapshots without leaking personal information
- You need different sync strategies for shared vs. personal content (e.g., shared syncs to git, personal stays local)

## Setup

```python
from ompa import Ompa, DualVaultConfig, IsolationMode

# Auto mode — content is classified automatically
ao = Ompa(
    shared_vault_path="./team-vault",
    personal_vault_path="~/.ompa-personal",
    isolation_mode="auto",
)

# Strict mode — explicit routing required
ao = Ompa(
    shared_vault_path="./team-vault",
    personal_vault_path="~/.ompa-personal",
    isolation_mode="strict",
)
```

Or via `DualVaultConfig`:

```python
from ompa import Ompa, DualVaultConfig, IsolationMode

config = DualVaultConfig(
    shared_path="./team-vault",
    personal_path="~/.ompa-personal",
    isolation_mode=IsolationMode.AUTO,
)
ao = Ompa(config=config)
```

## Isolation modes

| Mode | Behavior |
|------|----------|
| `AUTO` | Content auto-classified based on message type and tags |
| `STRICT` | Explicit `vault` parameter required on every write |
| `MANUAL` | Defaults to personal vault; shared writes are opt-in |

## Writing to a specific vault

```python
# Auto-classify (uses message type to decide)
ao.write("We decided to use Postgres", tags=["decision"])

# Force to shared vault
ao.write("Team standup notes", vault="shared")

# Force to personal vault
ao.write("My draft thoughts on the auth redesign", vault="personal")
```

## Searching across vaults

```python
# Search shared vault only (default)
results = ao.search("authentication decisions")

# Search personal vault
results = ao.search("my notes", vaults=["personal"])

# Search both
results = ao.search("postgres", vaults=["shared", "personal"])
```

## Exporting a note to shared

```python
# Preview first (strict mode default)
preview = ao.export_to_shared("work/decisions/postgres.md")
print(preview["preview"])

# Confirm the export
result = ao.export_to_shared("work/decisions/postgres.md", confirm=False, sanitize=True)
```

Sanitization removes `@private` markers, `#personal` tags, and redacts credentials (`sk-...`, `AKIA...`, `token=...`).

## Importing a shared note to personal

```python
result = ao.import_to_personal(
    "work/decisions/postgres.md",
    link_back=True,  # Adds a wikilink reference to the original
)
```

## CLI commands

```bash
# Init dual-vault
ao init --shared-vault ./team-vault --personal-vault ~/.ompa-personal

# Search
ao search "postgres" --vault shared
ao search "drafts" --vault personal

# Sync both vaults
ao sync --shared-vault ./team-vault --personal-vault ~/.ompa-personal

# Export to shared (preview first)
ao export work/decisions/postgres.md \
  --shared-vault ./team-vault \
  --personal-vault ~/.ompa-personal

# Export with confirmation
ao export work/decisions/postgres.md \
  --shared-vault ./team-vault \
  --personal-vault ~/.ompa-personal \
  --confirm

# Import from shared
ao import-note work/decisions/postgres.md \
  --shared-vault ./team-vault \
  --personal-vault ~/.ompa-personal
```

## Migrating from single vault

```python
ao = Ompa("./my-existing-vault")
result = ao.migrate_to_dual_vault(
    shared_path="./team-vault",
    personal_path="~/.ompa-personal",
    classification_rules="auto",   # or "all-shared"
)
print(f"Shared: {result['shared_notes']} | Personal: {result['personal_notes']}")
```

```bash
ao migrate \
  --shared-path ./team-vault \
  --personal-path ~/.ompa-personal \
  --rules auto
```
