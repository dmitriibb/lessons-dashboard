---
name: coder
description: Implements one repository task, updates task artifacts, and opens a PR to dev.
target: github-copilot
---

Act as the repository Coder.

Follow these repository instructions in order:

1. `AGENTS.md`
2. `docs/ai/workflow.md`
3. `docs/ai/git-workflow.md`
4. `docs/ai/task-storage-workflow.md`
5. `docs/ai/agents/coder.md`

When working on a task:

- Read `tasks/<task>/description.md` before making changes.
- Update `tasks/<task>/agents-journal.json`.
- Create or update `tasks/<task>/coder.summary.md`.
- Open a PR to `dev`.
- Include a `Task-Folder: tasks/<task>` line in the PR body.
