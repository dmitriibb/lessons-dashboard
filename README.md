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

More detail: [docs/business/plan.v1.md](/c:/projects/lessons-dashboard/docs/business/plan.v1.md)

## Agentic Workflow

The project is also intended to be developed with AI agents running in GitHub-based automation:

- `Manager` reviews tasks, validates scope, resolves ambiguity, and communicates with the human user when needed.
- `Coder` implements tasks on feature branches with a strong focus on code quality, security, readability, and performance.
- `QA` reviews the implementation, checks business logic, validates edge cases, and confirms the task is actually solved.

Planned flow:

1. The user adds tasks to the repository.
2. A cloud worker starts the agent workflow.
3. `Manager` reviews tasks and forwards ready tasks to `Coder`.
4. `Coder` implements the task on `feature/*` from `dev` and opens a PR to `dev`.
5. `QA` reviews and validates the PR.
6. If approved, the task returns to `Manager` and the PR is merged to `dev` with squash merge.
7. If no work is available, or user input is required, agents notify the user and wait.
8. If all agents are idle for a defined period, the worker can stop to save resources.

More detail:

- [docs/ai/workflow.md](/c:/projects/lessons-dashboard/docs/ai/workflow.md)
- [docs/ai/git-workflow.md](/c:/projects/lessons-dashboard/docs/ai/git-workflow.md)
- [docs/ai/agents/manager.md](/c:/projects/lessons-dashboard/docs/ai/agents/manager.md)
- [docs/ai/agents/coder.md](/c:/projects/lessons-dashboard/docs/ai/agents/coder.md)
- [docs/ai/agents/qa.md](/c:/projects/lessons-dashboard/docs/ai/agents/qa.md)
