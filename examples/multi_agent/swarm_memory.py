"""
OMPA Multi-Agent Swarm Memory Pattern.

Demonstrates a shared bulletin board pattern where multiple agents
write activities to a shared vault, read each other's context,
and consolidate knowledge over rounds.

Architecture:
    - Shared OMPA vault acts as the swarm's collective memory
    - Each agent has a named session (scoped KG triples, search results)
    - A bulletin board (brain notes) holds swarm-wide signals
    - After N rounds, each agent consolidates its KG into a summary note

Usage:
    python examples/multi_agent/swarm_memory.py
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from ompa import Ompa


@dataclass
class AgentActivity:
    agent_name: str
    action: str        # e.g. "CREATE_POST", "FOLLOW", "SEARCH"
    content: str = ""
    target: str = ""


@dataclass
class SwarmAgent:
    name: str
    ao: Ompa
    round: int = 0
    _injection_history: list[int] = field(default_factory=list)

    def inject_context(self) -> str:
        """Get memory context for this agent's next turn."""
        result = self.ao.session_start()
        token_estimate = len(result.output.split())
        self._injection_history.append(token_estimate)
        return result.output

    def record_activity(self, activity: AgentActivity) -> None:
        """Record an activity — classify it and persist to vault."""
        if activity.action in ("CREATE_POST", "CREATE_COMMENT") and len(activity.content) > 20:
            # Narrative actions go to vault as notes
            self.ao.write(
                content=f"{activity.agent_name} {activity.action}: {activity.content}",
                tags=[activity.action.lower(), activity.agent_name.lower()],
            )
        else:
            # Non-narrative actions (likes, follows) go to KG only
            self.ao.kg_add(
                subject=activity.agent_name,
                predicate=activity.action.lower(),
                object=activity.target or activity.content[:40],
            )

    def consolidate(self) -> None:
        """Merge KG triples into a single summary note (keeps vault lean)."""
        triples = self.ao.kg_query(self.name)
        if not triples:
            return

        summary_lines = [f"- {t.predicate}: {t.object}" for t in triples]
        summary = f"Agent {self.name} consolidated memory (round {self.round}):\n" + "\n".join(summary_lines)

        self.ao.update_brain(
            note_name=f"agent-{self.name.lower()}-summary",
            content=summary,
            append=False,  # Replace previous summary
        )

    def get_token_budget_warning(self) -> str | None:
        """Simple soft token monitoring."""
        if not self._injection_history:
            return None
        latest = self._injection_history[-1]
        if latest > 2000:
            return f"CRITICAL: {self.name} injecting {latest} tokens (>2000 limit)"
        if len(self._injection_history) >= 3:
            trend = self._injection_history[-3:]
            if all(b > trend[0] for b in trend[1:]):
                return f"TREND: {self.name} context growing over last 3 rounds"
        return None


class SwarmCoordinator:
    """Manages a swarm of agents sharing a common OMPA vault."""

    def __init__(self, vault_path: Path, agent_names: list[str]):
        self.vault_path = vault_path
        self.agents: dict[str, SwarmAgent] = {}
        self.round = 0

        for name in agent_names:
            ao = Ompa(vault_path=vault_path, agent_name=name, enable_semantic=False)
            self.agents[name] = SwarmAgent(name=name, ao=ao)

    def run_round(self, activities: list[AgentActivity]) -> dict:
        """Process one round of agent activities."""
        self.round += 1
        stats = {"round": self.round, "activities": len(activities), "warnings": []}

        for activity in activities:
            agent = self.agents.get(activity.agent_name)
            if not agent:
                continue
            agent.round = self.round
            agent.record_activity(activity)

            # Check token budget
            warning = agent.get_token_budget_warning()
            if warning:
                stats["warnings"].append(warning)

        # Every 5 rounds, consolidate all agents
        if self.round % 5 == 0:
            for agent in self.agents.values():
                agent.consolidate()
            stats["consolidated"] = True

        return stats

    def inject_all(self) -> dict[str, str]:
        """Get context injection for all agents (next round's system prompts)."""
        return {name: agent.inject_context() for name, agent in self.agents.items()}


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def run_demo():
    with tempfile.TemporaryDirectory() as tmp:
        vault_path = Path(tmp)

        print("=== OMPA Swarm Memory Demo ===\n")

        coordinator = SwarmCoordinator(
            vault_path=vault_path,
            agent_names=["Aria", "Bex", "Coda"],
        )

        # Simulate 3 rounds of agent activity
        rounds = [
            [
                AgentActivity("Aria", "CREATE_POST", "Introducing myself to the community! Excited to be here."),
                AgentActivity("Bex", "FOLLOW", target="Aria"),
                AgentActivity("Coda", "SEARCH", target="python tips"),
            ],
            [
                AgentActivity("Aria", "CREATE_COMMENT", "Great question! I think the key is to start small and iterate."),
                AgentActivity("Bex", "CREATE_POST", "Working on a new library for async task queues. Looking for feedback."),
                AgentActivity("Coda", "FOLLOW", target="Bex"),
            ],
            [
                AgentActivity("Aria", "LIKE", target="Bex post"),
                AgentActivity("Bex", "CREATE_COMMENT", "Thanks for the support! Release planned for next week."),
                AgentActivity("Coda", "CREATE_POST", "Just discovered that SQLite WAL mode is a game changer for concurrent reads."),
            ],
        ]

        for round_activities in rounds:
            stats = coordinator.run_round(round_activities)
            print(f"Round {stats['round']}: {stats['activities']} activities processed")
            if stats.get("warnings"):
                for w in stats["warnings"]:
                    print(f"  ⚠ {w}")
            if stats.get("consolidated"):
                print("  ✓ KG consolidated into summary notes")

        # Final injection (what each agent would see next round)
        print("\n=== Agent Context Sizes (next round) ===")
        contexts = coordinator.inject_all()
        for name, ctx in contexts.items():
            print(f"  {name}: ~{len(ctx.split())} tokens")

        # Check vault state
        from ompa import Vault
        vault = Vault(vault_path)
        stats = vault.get_stats()
        print(f"\nVault: {stats['total_notes']} notes, {stats['brain_notes']} brain notes")


if __name__ == "__main__":
    run_demo()
