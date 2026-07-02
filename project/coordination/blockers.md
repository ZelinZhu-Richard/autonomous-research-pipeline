# Blockers

Use this file for unresolved blockers that require user input, lead-agent decision, or an external state change.

## Blocker Format

```text
Blocker ID:
Date:
Owner:
Component:
Blocked item:
Needed decision or action:
Impact:
```

## Current Blockers

- Upstream pinned commits still need to be collected into `external/LOCKFILE.md` and `external/LOCKFILE.json`.
- Concrete model alias values still need to be set in local environment variables.
- `PAPERREVIEW_EMAIL` still needs to be set in `.env.local` before manual PaperReview.ai submission metadata can be generated.
- Docker or equivalent sandbox availability still needs to be verified before any generated-code execution.
- Existing AI Scientist v1/v2 artifacts need to be selected for v0 import fixtures.
- Network egress policy for retrieval and package setup stages still needs to be defined.
