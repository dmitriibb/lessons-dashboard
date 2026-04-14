# AI Workflow

## Goal

This document describes the current GitHub-based agentic delivery workflow for the project.

The user defines tasks in the repository. GitHub Actions orchestrates the queue, GitHub Copilot cloud agent implements tasks as `Coder`, and an AI-driven QA step reviews the resulting PR before merge. The process should work without relying on the user's local machine.

## Runtime Roles

The current runtime uses:

- `GitHub Actions Orchestrator`
- `Coder`
- `QA`

Role references:

- [agents/manager.md](/c:/projects/lessons-dashboard/docs/ai/agents/manager.md)
- [agents/coder.md](/c:/projects/lessons-dashboard/docs/ai/agents/coder.md)
- [agents/qa.md](/c:/projects/lessons-dashboard/docs/ai/agents/qa.md)
- [task-storage-workflow.md](/c:/projects/lessons-dashboard/docs/ai/task-storage-workflow.md)

## High-Level Flow

### 1. User Creates Tasks

The user prepares tasks under `tasks/`, one folder per task.

Each task folder must contain:

- `description.md`
- `agents-journal.json`

Each completed implementation cycle should also produce:

- `coder.summary.md`
- `qa.summary.md`

### 2. Orchestrator Starts

The user starts the process with a GitHub workflow trigger.

The current runtime entry point is `workflow_dispatch`. Future triggers may include `push` to `tasks/**` or scheduled runs.

### 3. Orchestrator Selects a Task

The GitHub Actions orchestrator:

- picks a task folder
- records the handoff in `agents-journal.json`
- creates a GitHub issue for implementation
- assigns the issue to the GitHub Copilot cloud agent configured as `Coder`

The orchestrator is responsible for queue handling and state transitions. It does not make product decisions.

### 4. Coder Implements the Task

`Coder` receives the task through GitHub Copilot cloud agent and must:

- create a `feature/<feature-name>` branch from `dev`
- implement the task
- update the task journal
- create `coder.summary.md`
- open a PR from the feature branch to `dev`

### 5. QA Reviews the PR

When a PR targeting `dev` is opened for a managed task, the QA workflow runs.

The QA step uses the `QA` role instructions together with:

- the original `description.md`
- the PR diff
- the coder summary

The QA step must:

- create or update `qa.summary.md`
- append a QA journal entry
- produce a binary decision for the workflow: `approved` or `changes_requested`

### 6. Merge Decision

If QA returns `approved`:

- the workflow squash-merges the PR into `dev`

If QA returns `changes_requested`:

- the workflow does not merge the PR
- the workflow output must clearly state that the PR was not merged

## Workflow Rules

The current rules are:

- Task queue orchestration is handled by GitHub Actions.
- `Coder` must follow [agents/coder.md](/c:/projects/lessons-dashboard/docs/ai/agents/coder.md).
- `QA` must follow [agents/qa.md](/c:/projects/lessons-dashboard/docs/ai/agents/qa.md).
- Both `Coder` and `QA` must update `agents-journal.json`.
- Merge to `main` is outside the scope of agent work.
- Merge to `dev` must use squash merge.

## Implementation Notes

The workflow is intentionally event-driven:

- one run dispatches work to `Coder`
- another run reacts to the resulting PR and performs QA

This avoids long-running idle jobs while still keeping the full flow in GitHub.

## Expected Benefits

If implemented well, this workflow should provide:

- GitHub-native task dispatch
- AI-driven implementation
- AI-driven review before merge
- visible task state in the repository
- low idle cost because workflows run only on demand
