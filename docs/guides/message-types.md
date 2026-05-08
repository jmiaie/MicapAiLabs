# Message Types

OMPA classifies messages into 15 types, each with auto-routing rules that file content in the right vault folder.

## Classification

```python
from ompa import Ompa

ao = Ompa("./workspace")
c = ao.classify("We decided to use Postgres over MySQL for the main database")
print(c.message_type)     # MessageType.DECISION
print(c.confidence)       # 0.92
print(c.suggested_action) # "File in work/decisions/"
print(c.routing_hints)    # ["Contains explicit decision language", ...]
```

Or via CLI:

```bash
ao classify "We decided to use Postgres"
# Type:       DECISION
# Confidence: 92%
# Action:     File in work/decisions/
```

## All 15 types

### DECISION
Explicit decisions or chosen directions.

- Triggers: "decided", "we'll go with", "chosen", "approved"
- Routes to: `work/decisions/`
- Example: "We decided to use Postgres over MySQL"

### INCIDENT
Outages, failures, or unexpected problems that occurred.

- Triggers: "incident", "outage", "went down", "broke", "failed"
- Routes to: `work/incidents/`
- Example: "The API was down for 20 minutes due to a memory leak"

### WIN
Successes, achievements, milestones.

- Triggers: "shipped", "landed", "closed", "won", "launched", "completed"
- Routes to: `work/wins/`
- Example: "We closed the enterprise deal with Acme Corp"

### LOSS
Setbacks, failures, missed targets.

- Triggers: "lost", "missed", "failed to", "couldn't", "rejected"
- Routes to: `work/losses/`
- Example: "We lost the bid to a competitor on price"

### BLOCKER
Something actively preventing progress.

- Triggers: "blocked", "blocking", "can't proceed", "waiting on", "stuck"
- Routes to: `work/blockers/`
- Example: "Blocked on legal approval before we can launch"

### QUESTION
Open questions requiring answers.

- Triggers: "?", "wondering", "unsure", "need to know", "what is"
- Routes to: `work/questions/`
- Example: "What's the right approach for handling auth token refresh?"

### SUGGESTION
Proposals or ideas not yet decided.

- Triggers: "suggest", "propose", "idea", "what if", "consider"
- Routes to: `work/suggestions/`
- Example: "What if we used Redis for the session cache?"

### REVIEW
Code, design, or document reviews.

- Triggers: "reviewed", "review", "feedback on", "LGTM", "approved"
- Routes to: `work/reviews/`
- Example: "Reviewed the auth PR — looks good with one comment"

### BUG
Code defects or unexpected behavior.

- Triggers: "bug", "defect", "broken", "regression", "error in"
- Routes to: `work/bugs/`
- Example: "Found a regression in the login flow after the last deploy"

### FEATURE
Feature requests or new capabilities.

- Triggers: "feature", "capability", "want to add", "build", "implement"
- Routes to: `work/features/`
- Example: "We need a bulk export feature for the dashboard"

### LEARN
Learnings, insights, or knowledge gained.

- Triggers: "learned", "realized", "turns out", "discovered", "insight"
- Routes to: `brain/learnings/`
- Example: "Learned that SQLite WAL mode significantly improves read concurrency"

### RETROSPECTIVE
Retrospectives or team reflection sessions.

- Triggers: "retro", "retrospective", "what went well", "what didn't"
- Routes to: `perf/retros/`
- Example: "Q1 retro: shipped on time but QA was rushed"

### ALERT
Warnings, risks, or items needing attention.

- Triggers: "alert", "warning", "at risk", "heads up", "watch out"
- Routes to: `work/alerts/`
- Example: "Alert: our API rate limit with Stripe is at 80% utilization"

### STATUS
Status updates or progress reports.

- Triggers: "status", "update", "progress", "as of", "currently"
- Routes to: `work/status/`
- Example: "Auth migration is 60% complete, on track for Friday"

### CHORE
Admin, maintenance, or housekeeping tasks.

- Triggers: "chore", "cleanup", "maintenance", "updated", "bumped"
- Routes to: `work/chores/`
- Example: "Updated all dependencies, bumped Python to 3.14"

## Confidence scores

When confidence is below 0.5, OMPA defaults to `STATUS` and flags it as low confidence. You can always override routing manually:

```python
c = ao.classify(message)
if c.confidence < 0.5:
    # Manually route
    ao.write(message, file_path="work/status/uncertain.md")
```
