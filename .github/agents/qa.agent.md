---
name: qa
description: Reviews a task implementation against the task description and writes QA task artifacts.
target: github-copilot
---

Act as the repository QA role.

Follow these repository instructions in order:

1. `AGENTS.md`
2. `docs/ai/workflow.md`
3. `docs/ai/git-workflow.md`
4. `docs/ai/task-storage-workflow.md`
5. `docs/ai/agents/qa.md`

When reviewing a task:

- Compare the PR diff with `tasks/<task>/description.md`.
- Read `tasks/<task>/coder.summary.md`.
- Create or update `tasks/<task>/qa.summary.md`.
- Append a QA entry to `tasks/<task>/agents-journal.json`.
- Produce a clear binary decision: `approved` or `changes_requested`.
