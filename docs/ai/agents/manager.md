# Manager Role

## Current Status

The historical `Manager` agent role is currently replaced at runtime by GitHub Actions orchestration.

This file is kept to preserve the product intent behind the original workflow, but the active implementation does not start a separate AI manager session.

## Runtime Replacement

GitHub Actions now performs the manager-side operational work:

- scan `tasks/`
- select a task for processing
- append an orchestration entry to `agents-journal.json`
- create the implementation issue
- dispatch the task to `Coder`
- react to QA outcome through workflow logic

## What Is Not Automated Here

The current orchestrator is a state coordinator, not a product-thinking agent.

It should not:

- invent missing business requirements
- rewrite task scope on its own
- make architectural decisions that belong to `Coder` or the user

If task quality gates are needed later, they should be added explicitly as a separate AI review step instead of being hidden inside the orchestration logic.
