# Palace

The `Palace` is the agent-accessible metadata layer — a navigational index over the vault.

## Structure

```
Wings  → high-level domains (projects, people, topics)
  Rooms → sub-topics within a wing
    Drawers → vault file references
Halls  → typed fact stores (facts, events, discoveries, preferences)
Tunnels → cross-wing connections
```

## Import

```python
from ompa import Palace
```

## Constructor

```python
palace = Palace(palace_path="./.palace")
```

## Wings

```python
palace.create_wing("Orion", type="project", keywords=["auth", "api"])
wings: list[dict] = palace.list_wings()
stats: dict = palace.stats()
# {"wing_count": 5, "room_count": 12, "drawer_count": 48, ...}
```

## Rooms and drawers

```python
palace.create_room("Orion", "auth-migration")
palace.link_drawer("Orion", "auth-migration", "work/active/auth-plan.md")

rooms: list[str] = palace.list_rooms("Orion")
drawers: list[str] = palace.get_drawers("Orion", "auth-migration")
```

## Tunnels (cross-wing connections)

```python
palace.create_tunnel("Kai", "Orion", "auth-migration")
tunnels: list[dict] = palace.find_tunnels("Kai", "Orion")
traversal = palace.traverse("Kai", "auth-migration")
```

## Auto-build from vault

```python
count: int = palace.auto_build_from_vault("./workspace")
# Scans vault structure and creates wings/rooms from folder hierarchy
```

::: ompa.palace.Palace
