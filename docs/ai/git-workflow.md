# AI Git Workflow

## Branch Model

The repository uses three branch categories:

- `main` for the stable version
- `dev` for active integration and task execution
- `feature/<task-name>` for task-specific implementation branches

Task folders that are ready to run through the agent workflow must already exist on `dev` before `Manager` dispatches them.

## Rules

### main

- `main` is the stable branch.
- Agents do not commit directly to `main`.
- Agents do not merge directly to `main`.

### dev

- `dev` is the integration branch.
- `Manager` dispatches Coder work against `dev`.
- `Coder` PRs always target `dev`.
- Completed task folders are moved from `tasks/` to `tasks_done/` on `dev` after the PR is merged.

### feature branches

- Each implementation task starts from `dev`.
- Branch naming should follow `feature/<task-name>` or another narrow name derived from one task folder.
- A feature branch is scoped to one task.

## Standard Flow

### 1. Dispatch

`Manager` assigns one task to Copilot and forces the run to start from `dev`.

### 2. Implement

`Coder` creates a feature branch from `dev`, implements the task, and writes `tasks/<task-name>/code.summary.md` on that branch.

### 3. Open PR

`Coder` opens a pull request:

- Source: `feature/<task-name>`
- Target: `dev`

The PR description must contain the exact marker:

`Task-Folder: tasks/<task-name>`

That marker is required by the post-merge task completion workflow.

### 4. QA Review

`QA` reviews the same PR, writes `tasks/<task-name>/qa.summary.md`, and then either:

- requests changes on the PR
- or merges the PR to `dev`

### 5. Merge

When the PR is acceptable, the merge strategy is squash merge into `dev`.

Squash merge keeps `dev` readable by representing one completed task as one integration commit.

### 6. Post-Merge Completion

After the PR to `dev` is merged, a GitHub Actions workflow moves `tasks/<task-name>` to `tasks_done/<task-name>`.

## Merge Constraints

- Agents never merge to `main`
- `Coder` does not merge its own PR
- `QA` must not merge before `qa.summary.md` is committed on the PR branch
- Feature branches are not reused for unrelated work
- `agents-journal.json` is not part of the current merge contract

## Why This Flow

This git model supports the current GitHub-based agent flow:

- `Manager` stays deterministic and lightweight
- `Coder` gets an isolated branch from `dev`
- `QA` works against one self-contained PR
- `dev` remains the single integration branch for active tasks
- `main` stays protected as the stable branch
