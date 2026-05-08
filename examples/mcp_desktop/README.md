# MCP Desktop Setup

Step-by-step guide for connecting OMPA to Claude Desktop, Cursor, or Windsurf via MCP.

## Prerequisites

```bash
pip install ompa
ao init   # Initialize your vault
```

## Claude Desktop

### Option 1: CLI (easiest)

```bash
claude mcp add ompa -- python -m ompa.mcp_server
```

### Option 2: Manual config

Edit `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ompa": {
      "command": "python",
      "args": ["-m", "ompa.mcp_server"],
      "env": {
        "OMPA_VAULT_PATH": "/absolute/path/to/your/vault"
      }
    }
  }
}
```

Restart Claude Desktop. You'll see OMPA tools in the MCP panel.

## Cursor

Create `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "ompa": {
      "command": "python",
      "args": ["-m", "ompa.mcp_server"],
      "env": {
        "OMPA_VAULT_PATH": "${workspaceFolder}/.ompa-vault",
        "OMPA_ENABLE_SEMANTIC": "false"
      }
    }
  }
}
```

## Windsurf

Same as Cursor. Add to `.windsurf/mcp.json`:

```json
{
  "mcpServers": {
    "ompa": {
      "command": "python",
      "args": ["-m", "ompa.mcp_server"],
      "env": {
        "OMPA_VAULT_PATH": "/path/to/vault"
      }
    }
  }
}
```

## With semantic search

To enable local semantic search (adds ~500MB for the model download on first run):

```bash
pip install ompa[all]
```

Then set `OMPA_ENABLE_SEMANTIC=true` in your MCP config env block.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `OMPA_VAULT_PATH` | `.` | Absolute path to vault |
| `OMPA_ENABLE_SEMANTIC` | `false` | Enable local semantic search |
| `OMPA_AGENT_NAME` | `agent` | Agent name (scopes KG entries) |
| `OMPA_SHARED_VAULT` | — | Shared vault path (dual-vault mode) |
| `OMPA_PERSONAL_VAULT` | — | Personal vault path (dual-vault mode) |

## Dual-vault with MCP

```json
{
  "mcpServers": {
    "ompa": {
      "command": "python",
      "args": ["-m", "ompa.mcp_server"],
      "env": {
        "OMPA_SHARED_VAULT": "/path/to/shared-vault",
        "OMPA_PERSONAL_VAULT": "/path/to/personal-vault",
        "OMPA_ISOLATION_MODE": "auto"
      }
    }
  }
}
```

## Verifying the connection

Once connected, ask Claude:

> "Use the ao_status tool to check my OMPA vault health"

Claude should respond with your vault stats. If it can't find the tool, restart the desktop app and check the vault path is absolute and exists.

## Troubleshooting

**Tool not appearing:** Restart the desktop app after config changes.

**"Vault not found" error:** Make sure `OMPA_VAULT_PATH` is an absolute path and the vault has been initialized with `ao init`.

**Slow first run:** If `OMPA_ENABLE_SEMANTIC=true`, the first run downloads the `all-MiniLM-L6-v2` model (~90MB). Subsequent runs are instant.
