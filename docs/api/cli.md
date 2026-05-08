# CLI Reference

All CLI commands are available via `ao <command>`.

```bash
ao --help       # List all commands
ao <cmd> --help # Help for a specific command
```

## Vault management

### `ao init`
Initialize a new vault at the current directory (or a specified path).

```bash
ao init
ao init --vault-path ./my-vault
ao init --shared-vault ./team --personal-vault ~/.private  # Dual-vault
```

### `ao status`
Show vault, palace, and KG overview.

```bash
ao status
ao status --vault-path ./my-vault
```

### `ao doctor`
Full health check — vault structure, KG, palace, semantic index, orphans.

```bash
ao doctor
ao doctor --vault-path ./my-vault
```

Output: rich table with OK / WARN / ERROR / INFO rows for each check.

### `ao validate`
Validate all notes in the vault for frontmatter and wikilink issues.

```bash
ao validate
```

### `ao orphans`
Detect orphaned notes (no incoming or outgoing wikilinks).

```bash
ao orphans
```

## Session hooks

### `ao session-start`
Run the session start hook. Outputs ~2K tokens of context.

```bash
ao session-start
```

### `ao wrap-up`
Run the stop/wrap-up hook. Saves session summary.

```bash
ao wrap-up
```

## Memory operations

### `ao classify`
Classify a message and show routing hints.

```bash
ao classify "We decided to use Postgres"
ao classify "The API went down for 20 minutes"
```

### `ao search`
Semantic search across the vault.

```bash
ao search "authentication decisions"
ao search "postgres" --limit 10
ao search "decisions" --vault shared          # Dual-vault
ao search "drafts" --vault personal
```

### `ao write-note`
Write content to the vault with auto-classification.

```bash
ao write-note "We won the Acme contract" --tags win,enterprise
ao write-note "Private notes" --vault personal  # Dual-vault
```

## Knowledge graph

### `ao kg-query`
Query the knowledge graph for an entity.

```bash
ao kg-query Kai
ao kg-query Kai --as-of 2025-12-31
```

### `ao kg-timeline`
Get the full timeline of events for an entity.

```bash
ao kg-timeline auth-service
```

### `ao kg-stats`
Show knowledge graph statistics.

```bash
ao kg-stats
```

### `ao kg-populate`
Populate the KG from all vault notes (wikilinks, tags, folders).

```bash
ao kg-populate
```

## Palace

### `ao wings`
List all palace wings.

```bash
ao wings
```

### `ao rooms`
List rooms in a wing.

```bash
ao rooms Orion
```

### `ao tunnel`
Find tunnels between two wings.

```bash
ao tunnel Kai Orion
```

## Index and sync

### `ao rebuild-index`
Rebuild the semantic search index.

```bash
ao rebuild-index
```

### `ao sync`
Full sync: rebuild KG, palace, and semantic index from vault.

```bash
ao sync
ao sync --shared-vault ./team --personal-vault ~/.private
```

## Dual-vault operations

### `ao export`
Export a note from personal vault to shared vault.

```bash
# Preview first
ao export work/decisions/postgres.md --shared-vault ./team --personal-vault ~/.private

# Confirm export
ao export work/decisions/postgres.md --shared-vault ./team --personal-vault ~/.private --confirm
```

### `ao import-note`
Import a note from shared vault to personal vault.

```bash
ao import-note team/decisions/postgres.md --shared-vault ./team --personal-vault ~/.private
```

### `ao migrate`
Migrate a single vault to dual-vault architecture.

```bash
ao migrate --shared-path ./team-vault --personal-path ~/.ompa-personal
ao migrate --shared-path ./team --personal-path ~/.private --rules all-shared
```
