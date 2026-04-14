# AI Git Workflow

## Branch Model

The repository uses three branch categories:

- `main` for the stable version
- `dev` for active integration and ongoing development
- `feature/<feature-name>` for task-specific implementation branches

## Rules

### main

- `main` is the stable branch.
- Agents do not commit directly to `main`.
- Agents do not merge directly to `main`.

### dev

- `dev` is the integration branch.
- It may temporarily contain work in progress or breaking changes.
- Feature work is merged into `dev` after review.

### feature branches

- Each new implementation task starts from `dev`.
- Branch naming should follow `feature/<feature-name>`.
- A feature branch should be scoped to one task or one tightly related unit of work.

## Standard Flow

### 1. Start Work

When `Coder` starts a new ready task dispatched by the orchestrator:

- Create a new branch from `dev`
- Use the `feature/<feature-name>` naming convention

### 2. Implement

`Coder` performs the implementation on the feature branch, updates the task artifacts, and pushes the branch to the remote repository.

### 3. Open PR

`Coder` opens a pull request:

- Source: `feature/<feature-name>`
- Target: `dev`
- The PR should clearly identify the originating task folder

### 4. QA Review

`QA` reviews the PR and validates the implementation.

Possible outcomes:

- `changes_requested`
- `approved`

### 5. Fixes if Needed

If changes are required:

- `Coder` updates the same feature branch
- `QA` reviews again

### 6. Merge

If the PR is approved by the QA workflow:

- Merge from feature branch to `dev`
- Use squash merge

Squash merge is preferred so that `dev` reflects one clean commit per completed feature rather than a long sequence of small implementation commits.

## Merge Constraints

- Agents never merge to `main`
- Agents should not bypass QA review
- Feature branches should not be reused for unrelated work
- If a task changes meaning substantially, a new branch should be considered

## Why This Flow

This git model supports the intended workflow:

- the orchestrator can reason about task boundaries
- `Coder` gets isolated implementation branches
- `QA` reviews self-contained PRs
- `dev` remains readable because of squash merges
- `main` stays protected as the stable branch

## Open Git Questions

The following points still need future decisions:

- Whether QA approval should eventually require automated tests in addition to AI review
- Whether protected branch rules will be enforced on `dev`
- Whether additional branch prefixes will be needed later, such as `fix/` or `chore/`
- How release promotion from `dev` to `main` will be handled
