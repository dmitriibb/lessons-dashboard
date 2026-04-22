# AI Workflow

## Goal

This document defines the current GitHub-based agent workflow used in this repository.

The workflow is intentionally narrow:

- `Manager` is simple automation.
- `Coder` and `QA` are GitHub Copilot cloud agents with repository custom agent profiles.
- Task state is carried by task folders, PRs, and summary files, not by task journals.

## Agents

The workflow uses three roles:

- `Manager`
- `Coder`
- `QA`

Role definitions live in:

- [agents/manager.md](agents/manager.md)
- [agents/coder.md](agents/coder.md)
- [agents/qa.md](agents/qa.md)
- [task-storage-workflow.md](task-storage-workflow.md)

The cloud-agent profiles that GitHub actually runs live in:

- [../../.github/agents/coder.agent.md](../../.github/agents/coder.agent.md)
- [../../.github/agents/qa.agent.md](../../.github/agents/qa.agent.md)

## Supported Model Choices

The workflow dispatch input currently supports the GitHub cloud-agent model values documented by GitHub for Copilot cloud agent model selection:

- `Auto`
- `Claude Sonnet 4.5`
- `Claude Opus 4.7`
- `GPT-5.2-Codex`

`Manager` passes the selected `coder_model` directly when it assigns the Coder issue to Copilot. The selected `qa_model` is recorded for the QA handoff.

## GitHub Prerequisites

The repository setup must satisfy all of the following before the workflow can run end to end:

- GitHub Copilot cloud agent must be enabled for the repository.
- The `dev` branch must already exist.
- The repository must have a secret named `COPILOT_ASSIGNMENT_TOKEN`.
- That token must be a user token or GitHub App user token that can assign issues to Copilot.
- For a fine-grained personal access token, GitHub documents these minimum permissions for Copilot issue assignment:
	- read access to metadata
	- read and write access to actions
	- read and write access to contents
	- read and write access to issues
	- read and write access to pull requests
- GitHub Actions must be allowed to push to `dev` for the post-merge task move commit.
- Optional repository variables `BOT_GIT_NAME` and `BOT_GIT_EMAIL` can be set to control the identity used by the post-merge workflow commit.

## End-to-End Flow

### 1. User prepares a task

The user adds a folder under `tasks/` on `dev`.

Each active task folder must contain:

- `description.md`

Optional legacy files such as `agents-journal.json` can stay in the repository, but they are not part of the current automation contract.

### 2. Manager dispatches Coder

The `Manager Dispatch` GitHub Actions workflow is started manually from the Actions tab.

It can:

- dispatch a specific `task_name`
- or pick the next task folder in `tasks/` that has a `description.md` and no open Coder dispatch issue

When the workflow selects a task it:

- creates a GitHub issue titled `Coder task: <task-name>`
- assigns that issue to `copilot-swe-agent[bot]`
- passes `custom_agent: coder`
- passes the selected `coder_model`
- forces the task to start from `dev`
- includes task-specific instructions that require `code.summary.md` and a PR to `dev`

`Manager` does not call an LLM, review scope, or update task journals.

### 3. Coder implements the task

GitHub Copilot cloud agent runs with the repository custom agent profile `coder`.

`Coder` must:

- create a feature branch from `dev`
- implement the requested change
- add or update validation as needed
- create `tasks/<task-name>/code.summary.md`
- open a PR to `dev`
- include the exact line `Task-Folder: tasks/<task-name>` in the PR description

That PR description marker is required by the post-merge automation.

### 4. QA reviews the PR

`QA` is a separate GitHub Copilot cloud agent persona backed by the repository custom agent profile `qa`.

`QA` works against the existing Coder PR and must:

- review the task description, diff, and validation evidence
- create `tasks/<task-name>/qa.summary.md` on the PR branch
- request fixes when the PR is not acceptable
- merge the PR to `dev` with squash merge when the PR is acceptable and the environment permits it

## Current GitHub Limitation

GitHub documents full API support for assigning issues to Copilot with a chosen custom agent and model.

GitHub does not currently document an equivalent API for switching an already-open pull request to a different custom agent with a chosen model. Because of that:

- Coder dispatch is automated in GitHub Actions
- QA model selection is recorded by the Manager workflow for the handoff
- the actual QA launch is expected to happen from a GitHub-supported cloud-agent entrypoint such as GitHub.com, Copilot Chat, or another supported client

The repository still defines the `qa` custom agent so the QA behavior is standardized even when the launch is manual.

### 5. Merge completion moves the task

When the PR to `dev` is merged, the `Complete Task On Merge` workflow:

- reads the `Task-Folder:` marker from the merged PR body
- moves that task folder from `tasks/` to `tasks_done/`
- closes the matching `Coder task: <task-name>` issue

## Non-Goals

The current workflow intentionally does not:

- maintain `agents-journal.json`
- ask `Manager` to interpret or approve requirements with an LLM
- merge anything to `main`
- let `Coder` merge its own PR

## Expected Outcome

If the workflow is followed correctly:

- task selection stays simple and deterministic
- Coder work is branch-isolated and reviewable
- QA produces a committed summary before merge
- completed tasks are archived automatically in `tasks_done/`
