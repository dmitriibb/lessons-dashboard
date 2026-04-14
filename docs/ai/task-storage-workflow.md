# Task Storage Workflow

## Purpose

This document defines how work items are stored in the repository and how automation and AI roles move tasks through the workflow.

The goal is to keep task state visible inside the repository itself, without requiring an external task tracker in the first version.

## Directory Structure

The repository uses two root-level directories for task lifecycle management:

- `tasks/`
- `tasks_done/`

### tasks

`tasks/` contains active or not-yet-completed work items.

Each task must have its own folder inside `tasks/`.

Example:

```text
tasks/
  task-1-init-backed-service/
    description.md
    agents-journal.json
    coder.summary.md
    qa.summary.md
```

### tasks_done

`tasks_done/` contains completed tasks.

Moving a fully completed task from `tasks/` to `tasks_done/` is not automated in the current workflow. That step can be added later once the merge flow is stable.

## Per-Task Files

Each task folder contains two required files:

- `description.md`
- `agents-journal.json`

As the workflow progresses, the task folder should also gain:

- `coder.summary.md`
- `qa.summary.md`

## description.md

`description.md` is the business and implementation request for one task.

It should follow a consistent structure so the orchestrator, `Coder`, and `QA` can all read the same intent.

The current template sections are:

- `Main Goal`
- `Details`
- `Definition of Done`
- `Restrictions`

Template:

- [templates/description.template.md](/c:/projects/lessons-dashboard/docs/ai/templates/description.template.md)

## agents-journal.json

`agents-journal.json` is the execution log for that task.

It is used to keep a machine-readable history of what each workflow stage did and when.

Each journal entry records:

- `timestamp`
- `agent`
- `entry`
- `details`

Template:

- [templates/agents-journal.template.json](/c:/projects/lessons-dashboard/docs/ai/templates/agents-journal.template.json)

## Summary Files

### coder.summary.md

This file is created by `Coder` and should summarize:

- what was implemented
- major technical notes or assumptions

Template:

- [templates/coder.summary.template.md](/c:/projects/lessons-dashboard/docs/ai/templates/coder.summary.template.md)

### qa.summary.md

This file is created by `QA` and should summarize:

- the review decision
- the main review findings
- the next expected action

Template:

- [templates/qa.summary.template.md](/c:/projects/lessons-dashboard/docs/ai/templates/qa.summary.template.md)

## Role Responsibilities

### GitHub Actions Orchestrator

The orchestrator is responsible for:

- scanning task folders in `tasks/`
- selecting a task for dispatch
- adding a journal entry when the task is picked up
- forwarding the task to `Coder`

### Coder

`Coder` is responsible for:

- reading the task description
- adding journal entries when implementation starts
- creating `coder.summary.md`
- adding journal entries when implementation is handed to `QA`

### QA

`QA` is responsible for:

- adding journal entries when review starts
- creating `qa.summary.md`
- adding journal entries when the review is approved or when changes are requested

## Expected Flow

### 1. User creates a task

The user creates a new folder under `tasks/` and adds:

- `description.md`
- `agents-journal.json`

### 2. Orchestrator picks up the task

The orchestrator writes a journal event that the task was picked up and dispatched to `Coder`.

### 3. Coder starts implementation

`Coder` writes a journal event that implementation has started.

`Coder` also writes `coder.summary.md` before opening the PR.

When implementation is complete, `Coder` writes a journal event that the task is being passed to `QA`.

### 4. QA reviews

`QA` writes a journal event that review has started.

If changes are needed:

- `QA` adds a journal entry describing the result
- `QA` updates `qa.summary.md`
- the task returns to `Coder`

If the task is approved:

- `QA` adds a journal entry that the task passed QA
- `QA` updates `qa.summary.md`
- the workflow merges the PR into `dev`

## Journal Entry Style

Journal entries should be:

- short enough to scan quickly
- specific enough to understand what happened
- chronological
- written as factual event records rather than long discussion threads

## Naming Guidance

Recommended task folder naming style:

- `task-<number>-<short-kebab-case-name>`

Example:

- `task-1-init-backed-service`

This keeps tasks human-readable and stable.

## Notes

- `agents-journal-example.json` can be kept as an example during early setup, but the actual workflow file for each task is `agents-journal.json`
- if the task description format evolves later, the template should be updated together with this document
