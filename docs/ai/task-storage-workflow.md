# Task Storage Workflow

## Purpose

This document defines how work items are stored in the repository and how the current GitHub agent workflow moves them through the lifecycle.

The current workflow keeps task state visible inside the repository through task folders, PRs, and summary files. It does not rely on a machine-written task journal.

## Directory Structure

The repository uses two root-level directories for task lifecycle management:

- `tasks/`
- `tasks_done/`

### tasks

`tasks/` contains active or not-yet-completed work items.

Each task must have its own folder inside `tasks/`.

Minimal example:

```text
tasks/
  task-1-init-backed-service/
    description.md
```

### tasks_done

`tasks_done/` contains completed tasks.

When a PR to `dev` is merged successfully, the `Complete Task On Merge` workflow moves the whole task folder from `tasks/` into `tasks_done/`.

## Per-Task Files

### Required before dispatch

Each new task folder must contain:

- `description.md`

### Generated during implementation and review

The workflow expects the agents to add these files on the feature branch before merge:

- `code.summary.md`
- `qa.summary.md`

### Legacy optional files

Older task folders may also contain:

- `agents-journal.json`

The current workflow ignores this file. It can stay in the repository for historical context, but it is no longer required and should not be updated by `Manager`, `Coder`, or `QA`.

## description.md

`description.md` is the business and implementation request for one task.

It should follow a consistent structure so `Coder` and `QA` can read the same intent.

The current template sections are:

- `Main Goal`
- `Details`
- `Definition of Done`
- `Restrictions`

Template:

- [templates/description.template.md](templates/description.template.md)

## code.summary.md

`code.summary.md` is written by `Coder` in the task folder on the feature branch.

It should explain:

- what changed
- what was validated
- any remaining follow-up or known risk

Template:

- [templates/code.summary.template.md](templates/code.summary.template.md)

## qa.summary.md

`qa.summary.md` is written by `QA` in the task folder on the same PR branch before final merge.

It should record:

- what was reviewed
- whether the PR is acceptable
- which checks or risks remain relevant

Template:

- [templates/qa.summary.template.md](templates/qa.summary.template.md)

## Agent Responsibilities

### Manager

`Manager` is responsible for:

- scanning task folders in `tasks/`
- requiring `description.md`
- selecting the next task or a requested task
- assigning that task to `Coder`

`Manager` does not update task journals or move task folders.

### Coder

`Coder` is responsible for:

- reading the task description
- implementing the task on a feature branch from `dev`
- writing `code.summary.md`
- opening a PR to `dev`

### QA

`QA` is responsible for:

- reviewing the Coder PR against the task description
- writing `qa.summary.md`
- either requesting fixes or merging the PR

## Expected Flow

### 1. User creates a task

The user creates a new folder under `tasks/` and adds:

- `description.md`

### 2. Manager dispatches the task

The `Manager Dispatch` workflow selects the task and assigns it to Copilot with the `coder` custom agent.

### 3. Coder starts implementation

`Coder` writes `code.summary.md` in the task folder and opens a PR to `dev`.

The PR description must include:

`Task-Folder: tasks/<task-name>`

### 4. QA reviews

`QA` writes `qa.summary.md` on the PR branch.

If changes are needed:

- `QA` leaves concrete PR comments
- the task stays in `tasks/`
- `Coder` updates the same PR

If the task is accepted:

- `QA` merges the PR to `dev` when the environment permits it

### 5. Post-merge completion

After the PR is merged:

- the `Complete Task On Merge` workflow moves the full task folder from `tasks/` to `tasks_done/`
- the matching Coder dispatch issue is closed

## Naming Guidance

Recommended task folder naming style:

- `task-<number>-<short-kebab-case-name>`

Example:

- `task-1-init-backed-service`

This keeps tasks human-readable and stable.

## Notes

- If the task description format evolves later, the template should be updated together with this document.
- `agents-journal-example.json` can remain as a legacy reference, but it is not part of the current automation flow.
