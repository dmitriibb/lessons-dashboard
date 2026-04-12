# Task Storage Workflow

## Purpose

This document defines how work items are stored in the repository and how agents should move tasks through the workflow.

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
```

### tasks_done

`tasks_done/` contains completed tasks.

When a task is fully finished, the `Manager` agent is responsible for moving the whole task folder from `tasks/` into `tasks_done/`.

## Per-Task Files

Each task folder contains two main files:

- `description.md`
- `agents-journal.json`

## description.md

`description.md` is the business and implementation request for one task.

It should follow a consistent structure so `Manager`, `Coder`, and `QA` can all read the same intent.

The current template sections are:

- `Main Goal`
- `Details`
- `Definition of Done`
- `Restrictions`

Template:

- [templates/description.template.md](/c:/projects/lessons-dashboard/docs/ai/templates/description.template.md)

## agents-journal.json

`agents-journal.json` is the execution log for that task.

It is used to keep a machine-readable history of what each agent did and when.

Each journal entry records:

- `timestamp`
- `agent`
- `entry`
- `details`

Template:

- [templates/agents-journal.template.json](/c:/projects/lessons-dashboard/docs/ai/templates/agents-journal.template.json)

## Agent Responsibilities

### Manager

`Manager` is responsible for:

- scanning task folders in `tasks/`
- reading `description.md`
- deciding whether a task is clear enough
- adding journal entries when the task is picked up
- forwarding ready work to `Coder`
- moving the task folder to `tasks_done/` after the task is fully completed

### Coder

`Coder` is responsible for:

- reading the task description
- adding journal entries when implementation starts
- adding journal entries when implementation is handed to `QA`

### QA

`QA` is responsible for:

- adding journal entries when review starts
- adding journal entries when the review is approved or when changes are requested

## Expected Flow

### 1. User creates a task

The user creates a new folder under `tasks/` and adds:

- `description.md`
- `agents-journal.json`

### 2. Manager picks up the task

`Manager` reads the task and writes a journal event that the task was picked up.

If the task is clear and ready, `Manager` writes a journal entry that it is being passed to `Coder`.

If the task is not clear, `Manager` writes that it is blocked and communicates with the user.

### 3. Coder starts implementation

`Coder` writes a journal event that implementation has started.

When implementation is complete, `Coder` writes a journal event that the task is being passed to `QA`.

### 4. QA reviews

`QA` writes a journal event that review has started.

If changes are needed:

- `QA` adds a journal entry describing the result
- the task returns to `Coder`

If the task is approved:

- `QA` adds a journal entry that the task passed QA
- the task returns to `Manager` for completion handling

### 5. Manager closes the task

After QA approval and workflow completion:

- `Manager` adds the final journal entry
- `Manager` moves the full task folder from `tasks/` to `tasks_done/`

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
