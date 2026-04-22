# Lessons Dashboard

Lessons Dashboard is a web application for online teachers. It is intended to help teachers plan lessons, manage students, share lesson content, and keep schedules organized in one place.

## Business Plan

The product is centered around a teacher workflow:

- Create, update, and copy lesson plans.
- Connect lesson plans to one or many students.
- Attach lesson materials such as images, audio, and other files.
- Create lessons that can be shared with students online.
- Track students, their progress, teacher notes, and related lessons.
- Manage a calendar-based schedule with lesson statuses.
- Support teacher registration and authorization.
- Let students work as registered users or join a lesson through a teacher-generated link tied to a specific student.
- Store all application data in a database.
- Build the frontend in React and the backend in Go.

More detail: [docs/business/plan.v1.md](docs/business/plan.v1.md)

## Agentic Workflow

The project is also intended to be developed with AI agents running in GitHub-based automation:

- `Manager` is a lightweight GitHub Actions workflow that selects the next task and dispatches it to Copilot.
- `Coder` is a GitHub Copilot cloud agent using the repository custom agent profile `coder`.
- `QA` is a GitHub Copilot cloud agent using the repository custom agent profile `qa`.

Current flow:

1. The user adds a task folder under `tasks/` on `dev` with `description.md`.
2. The `Manager Dispatch` workflow chooses the task and assigns a GitHub issue to Copilot with the `coder` custom agent and the selected Coder model.
3. `Coder` implements the task on `feature/*` from `dev`, writes `code.summary.md`, and opens a PR to `dev`.
4. `QA` reviews the PR with the `qa` custom agent, writes `qa.summary.md`, and either requests fixes or merges the PR.
5. After merge, the `Complete Task On Merge` workflow moves the task folder to `tasks_done/`.

Repository prerequisites:

- GitHub Copilot cloud agent must be enabled for this repository.
- The repository must have a `COPILOT_ASSIGNMENT_TOKEN` secret that can assign issues to Copilot.
- The `dev` branch must exist and GitHub Actions must be allowed to push the post-merge task move commit.

More detail:

- [docs/ai/workflow.md](docs/ai/workflow.md)
- [docs/ai/git-workflow.md](docs/ai/git-workflow.md)
- [docs/ai/task-storage-workflow.md](docs/ai/task-storage-workflow.md)
- [docs/ai/agents/manager.md](docs/ai/agents/manager.md)
- [docs/ai/agents/coder.md](docs/ai/agents/coder.md)
- [docs/ai/agents/qa.md](docs/ai/agents/qa.md)
