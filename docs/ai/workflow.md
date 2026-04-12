# AI Workflow

## Goal

This document describes the intended agentic delivery workflow for the project.

The main idea is that the human user defines tasks, while AI agents process those tasks in a controlled flow inside GitHub-based automation. The user should be able to manage work with minimal dependence on a local laptop and should eventually be able to control the process from a phone or tablet.

## Agents

The workflow uses three agents:

- `Manager`
- `Coder`
- `QA`

Detailed role definitions live in:

- [agents/manager.md](/c:/projects/lessons-dashboard/docs/ai/agents/manager.md)
- [agents/coder.md](/c:/projects/lessons-dashboard/docs/ai/agents/coder.md)
- [agents/qa.md](/c:/projects/lessons-dashboard/docs/ai/agents/qa.md)
- [task-storage-workflow.md](/c:/projects/lessons-dashboard/docs/ai/task-storage-workflow.md)

## High-Level Flow

### 1. User Creates Tasks

The user prepares a list of tasks and pushes them into the GitHub repository.

Tasks are stored in the repository under the `tasks/` directory, one folder per task.

The exact repository task flow is documented in:

- [task-storage-workflow.md](/c:/projects/lessons-dashboard/docs/ai/task-storage-workflow.md)

### 2. Cloud Worker Starts

The user triggers a GitHub-based worker or automation run.

The exact execution platform is still to be finalized, but the intended direction is GitHub-hosted automation rather than relying on the user's personal device.

### 3. Manager Reviews Tasks

`Manager` checks each new task and decides whether it is ready for implementation.

The review includes:

- Is the task description clear enough?
- Does the task contradict current behavior or existing architecture?
- Does the task need user clarification?
- Is the task small and specific enough for implementation?

If anything is unclear, `Manager` is responsible for communicating with the user.

The exact communication channel is not decided yet.

### 4. Manager Dispatches Ready Tasks

If a task is ready, `Manager` forwards it to `Coder`.

Tasks should normally be handled one by one unless a future workflow explicitly supports safe parallel implementation.

### 5. Coder Implements the Task

`Coder` performs the implementation work:

- Creates a feature branch from `dev`
- Writes the code
- Adds or updates tests where appropriate
- Opens a PR from the feature branch to `dev`

`Coder` should optimize for:

- Readability
- Maintainability
- Robustness
- Security
- Performance

### 6. QA Reviews the PR

`QA` validates the implementation before merge.

The review includes:

- PR review of the code changes
- Validation of business logic
- Checking major edge cases
- Confirming the task was actually solved

The exact environment for preview deployment or branch testing is not finalized yet.

### 7. QA Outcome

If `QA` finds issues:

- `QA` reports them directly to `Coder`
- `Coder` fixes the issues
- `QA` reviews again

If `QA` approves:

- `QA` signals successful validation
- The task returns to `Manager` for workflow completion

### 8. Merge and Handover

After successful QA:

- `Manager` confirms the workflow state
- `Coder` merges the PR according to the Git workflow rules
- `Manager` marks the task as complete
- `Manager` moves the task folder from `tasks/` to `tasks_done/`
- `Manager` assigns the next ready task

### 9. Waiting State

If no tasks are available, or if remaining tasks require human input:

- Agents notify the user
- Agents wait for a response

### 10. Idle Shutdown

If all agents remain idle for a defined period, such as 10 to 15 minutes:

- The worker should stop
- Resource usage should be minimized

This is an explicit design goal to avoid paying for unnecessary always-on automation.

## Workflow Rules

The current intended rules are:

- `Manager` is the gatekeeper for task readiness.
- `Coder` should not invent product decisions that require user input.
- `QA` should validate both correctness and task completion, not only code style.
- Unclear requirements should go back to the user through `Manager`.
- Merge to `main` is outside the scope of agent work.

## Open Workflow Questions

These points still need design decisions:

- How the `Manager` communicates with the user
- How PR previews or feature-branch deployments are exposed to `QA`
- Whether agents run as separate jobs, separate services, or coordinated steps in one pipeline
- How agent state is persisted between workflow runs
- How idle detection is implemented in GitHub-based automation

## Expected Benefits

If implemented well, this workflow should provide:

- Clear separation of responsibility
- Better task quality before coding starts
- Stronger code quality control
- Reduced need for the user to sit at a laptop
- A path toward mobile-first task management for the human user
