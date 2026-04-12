# AGENTS

This repository is planned around a three-agent delivery workflow:

- `Manager` validates tasks, resolves ambiguity, and coordinates work with the user.
- `Coder` implements approved tasks in code.
- `QA` reviews the result, checks business logic, and validates task completion.

High-level process:

1. The user adds tasks to the repository.
2. `Manager` reviews them and forwards development-ready work.
3. `Coder` creates a `feature/*` branch from `dev`, implements the task, and opens a PR to `dev`.
4. `QA` reviews the PR and either requests fixes or approves it.
5. After approval, the change is squash-merged into `dev`.
6. `Manager` tracks completion and assigns the next task.

Detailed references:

- Business plan: [docs/business/plan.v1.md](/c:/projects/lessons-dashboard/docs/business/plan.v1.md)
- Agent roles: [docs/ai/agents/manager.md](/c:/projects/lessons-dashboard/docs/ai/agents/manager.md), [docs/ai/agents/coder.md](/c:/projects/lessons-dashboard/docs/ai/agents/coder.md), [docs/ai/agents/qa.md](/c:/projects/lessons-dashboard/docs/ai/agents/qa.md)
- Runtime workflow: [docs/ai/workflow.md](/c:/projects/lessons-dashboard/docs/ai/workflow.md)
- Git workflow: [docs/ai/git-workflow.md](/c:/projects/lessons-dashboard/docs/ai/git-workflow.md)
