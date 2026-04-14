# AGENTS

This repository currently uses a GitHub-based hybrid delivery workflow:

- `GitHub Actions Orchestrator` replaces the runtime `Manager` role.
- `Coder` is the implementation AI role.
- `QA` is the review AI role.

High-level process:

1. The user adds tasks to the repository under `tasks/`.
2. A GitHub Actions workflow selects one task and records the orchestration handoff in `agents-journal.json`.
3. The workflow assigns the task to the GitHub Copilot cloud agent configured as `Coder`.
4. `Coder` creates a `feature/*` branch from `dev`, implements the task, updates the task journal, creates `coder.summary.md`, and opens a PR to `dev`.
5. A PR-triggered workflow runs the `QA` role prompt against the PR diff and task description, writes `qa.summary.md`, and appends a QA journal entry.
6. If QA approves, the workflow squash-merges the PR into `dev`. If QA does not approve, the PR remains open for follow-up.

Repository instructions for AI agents:

- The root `AGENTS.md` file defines the repository-level workflow and guardrails.
- Role-specific instructions live in [docs/ai/agents/coder.md](/c:/projects/lessons-dashboard/docs/ai/agents/coder.md) and [docs/ai/agents/qa.md](/c:/projects/lessons-dashboard/docs/ai/agents/qa.md).
- The historical `Manager` role definition remains documented in [docs/ai/agents/manager.md](/c:/projects/lessons-dashboard/docs/ai/agents/manager.md), but the current runtime uses GitHub Actions orchestration instead of a separate AI manager session.

Detailed references:

- Business plan: [docs/business/plan.v1.md](/c:/projects/lessons-dashboard/docs/business/plan.v1.md)
- Runtime workflow: [docs/ai/workflow.md](/c:/projects/lessons-dashboard/docs/ai/workflow.md)
- Task storage workflow: [docs/ai/task-storage-workflow.md](/c:/projects/lessons-dashboard/docs/ai/task-storage-workflow.md)
- Git workflow: [docs/ai/git-workflow.md](/c:/projects/lessons-dashboard/docs/ai/git-workflow.md)
