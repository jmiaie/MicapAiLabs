# Lifecycle Hooks

OMPA provides 5 lifecycle hooks that wrap your agent's natural event loop. Each hook has a token budget — the maximum context it injects into your agent.

## Hook overview

| Hook | Token Budget | Fires When |
|------|-------------|------------|
| `session_start` | ~2,000 | Session begins |
| `user_message` | ~100 | Each user message arrives |
| `post_tool` | ~200 | After each tool call |
| `pre_compact` | ~100 | Before context compaction |
| `stop` | ~500 | Session ends |

## Wiring hooks into your agent

### Python API

```python
from ompa import Ompa

ao = Ompa(vault_path="./workspace")

# 1. At session start — inject memory context
result = ao.session_start()
system_prompt = result.output   # ~2K tokens — add to your system prompt

# 2. On each user message
for message in user_messages:
    hint = ao.handle_message(message)
    # hint.output contains routing guidance (~100 tokens)

# 3. After each tool call
ao.post_tool("write", {"file_path": "work/active/auth.md"})

# 4. Before context compaction (if your agent supports it)
ao.pre_compact(current_transcript)

# 5. At session end
ao.stop()
```

### Claude Code hooks (CLAUDE.md)

```markdown
## Hooks

- session_start: Run `python -c "from ompa import Ompa; ao=Ompa('./workspace'); print(ao.session_start().output)"`
- stop: Run `python -c "from ompa import Ompa; ao=Ompa('./workspace'); ao.stop()"`
```

### OpenClaw integration

```python
from ompa import Ompa

class OmpaMemoryPlugin:
    def __init__(self, vault_path: str):
        self.ao = Ompa(vault_path)

    def on_session_start(self) -> str:
        return self.ao.session_start().output

    def on_message(self, message: str) -> str:
        return self.ao.handle_message(message).output

    def on_tool_use(self, tool_name: str, tool_input: dict) -> None:
        self.ao.post_tool(tool_name, tool_input)

    def on_stop(self) -> str:
        return self.ao.stop().output
```

## Custom hooks

You can register your own hooks alongside the built-in ones:

```python
from ompa.hooks import Hook, HookContext, HookResult
from ompa import Ompa

class SlackNotifyHook(Hook):
    def __init__(self):
        super().__init__("slack_notify", token_budget=0)

    def execute(self, context: HookContext, **kwargs) -> HookResult:
        # Post to Slack on session end
        send_slack_message(f"Session ended: {context.vault_path}")
        return HookResult(hook_name=self.name, success=True, output="", tokens_hint=0)

ao = Ompa("./workspace")
ao.hooks.register_hook("stop", SlackNotifyHook())
```

## What `session_start` injects

The `session_start` hook assembles context from all three layers:

1. **Vault listing** — top-level note names and recent modifications
2. **North Star** — contents of `brain/north-star.md` (your persistent goals)
3. **Active work** — notes in `work/active/`
4. **Palace wings** — list of all wings and their rooms
5. **KG stats** — entity count, recent triples

Total output is capped at approximately 2,000 tokens.

## What `post_tool` does automatically

When a tool call writes or edits a markdown file, `post_tool` automatically:

1. Adds the file to the palace metadata layer
2. Extracts entities and wikilinks into the knowledge graph
3. Updates the semantic search index (if built)

This keeps all three layers in sync without manual intervention.
