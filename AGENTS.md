# AGENTS

This repository uses a GitHub-based three-stage delivery flow:

- `Manager` is a GitHub Actions dispatch workflow. It picks the next task from `tasks/` and hands it to `Coder`. It does not use an LLM and it does not update task journals.
- `Coder` is a GitHub Copilot cloud agent. It works from the repository custom agent profile in `.github/agents/coder.agent.md`, which mirrors [docs/ai/agents/coder.md](docs/ai/agents/coder.md). It creates a feature branch from `dev`, implements the task, writes `code.summary.md` in the task folder, and opens a PR to `dev`.
- `QA` is a GitHub Copilot cloud agent. It works from `.github/agents/qa.agent.md`, which mirrors [docs/ai/agents/qa.md](docs/ai/agents/qa.md). It reviews the Coder PR, writes `qa.summary.md` in the task folder, requests fixes when needed, and merges to `dev` when the change is acceptable and the environment permits it.

High-level process:

1. The user adds a task folder under `tasks/` on `dev`.
2. The `Manager Dispatch` workflow picks the next task or a requested task and assigns it to Copilot with the `coder` custom agent.
3. `Coder` creates `feature/<task-name>` from `dev`, implements the task, writes `code.summary.md`, and opens a PR to `dev`.
4. `QA` reviews the Coder PR with the `qa` custom agent, writes `qa.summary.md`, and either requests fixes or merges the PR.
5. After merge, the `Complete Task On Merge` workflow moves the task folder from `tasks/` to `tasks_done/`.
6. `Manager` can then dispatch the next task.

Detailed references:

- Business plan: [docs/business/plan.v1.md](docs/business/plan.v1.md)
- AI workflow: [docs/ai/workflow.md](docs/ai/workflow.md)
- Git workflow: [docs/ai/git-workflow.md](docs/ai/git-workflow.md)
- Task storage: [docs/ai/task-storage-workflow.md](docs/ai/task-storage-workflow.md)
- Agent roles: [docs/ai/agents/manager.md](docs/ai/agents/manager.md), [docs/ai/agents/coder.md](docs/ai/agents/coder.md), [docs/ai/agents/qa.md](docs/ai/agents/qa.md)
