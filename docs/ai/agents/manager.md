# Manager Agent

## Purpose

`Manager` is not a cloud AI agent in this repository.

`Manager` is a small GitHub Actions dispatch step that selects one task and hands it to `Coder`.

## Responsibilities

- Read active task folders under `tasks/`
- Honor an optional requested `task_name`
- Require `description.md`
- Skip tasks that already have an open `Coder task:` dispatch issue
- Create and assign a GitHub issue to `copilot-swe-agent[bot]`
- Pass `custom_agent: coder`
- Pass the selected `coder_model`
- Record the selected `qa_model` for the later QA handoff
- Force the cloud-agent task to branch from `dev`

## Explicit Non-Responsibilities

`Manager` does not:

- run an LLM to decide whether a task is ready
- write or update `agents-journal.json`
- change code
- review pull requests
- move task folders to `tasks_done/`

## Dispatch Contract

The issue created by `Manager` must tell `Coder` to:

1. branch from `dev`
2. implement only the selected task
3. create `tasks/<task-name>/code.summary.md`
4. open a PR to `dev`
5. include `Task-Folder: tasks/<task-name>` in the PR description

## Guardrails

`Manager` should not:

- invent product decisions
- interpret vague requirements with an LLM
- assign more than one active task when one is enough
- update legacy journals just to track state

## Success Criteria

`Manager` is successful when:

- exactly one valid task is selected
- Coder receives deterministic inputs
- the chosen base branch is `dev`
- the selected models are captured for the execution flow
