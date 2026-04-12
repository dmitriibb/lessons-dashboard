# Cloud Deployment

## Purpose

This document records the currently agreed cloud deployment direction for the project.

The goal is to keep the infrastructure simple, cheap, and easy to operate in the early stage, while still being good enough for real development and limited real usage.

## Selected Provider and VM

The currently selected infrastructure option is:

- provider: `Google Cloud`
- service: `Compute Engine`
- machine type: `e2-medium`
- memory: `4 GiB RAM`

Why this option was selected:

- cheaper than the comparable small AWS EC2 options we reviewed
- supports stop-and-start usage well
- enough RAM for the initial stack without operating too close to the limit
- simple for a single-VM early-stage deployment

## Selected Stack

The currently agreed application deployment stack is:

- reverse proxy
- `Go` backend
- `MariaDB` database
- `React` frontend application

### Frontend decision

The frontend will be:

- a normal `React` application
- without server-side rendering
- deployed as its own application container or service
- not treated as a server-side rendered app

This means the frontend remains a client-side app, but it is not being documented here as a pure static-file-only hosting model.

## Database Decision

The current database choice is:

- `MariaDB`

Reason:

- lighter than `MySQL` for the small self-hosted setup
- sufficient for the current project scope
- helps keep memory usage more comfortable on a `4 GiB` machine

## Deployment Shape

Early-stage deployment will use one VM with Docker Compose.

The VM is expected to host:

- reverse proxy
- backend service
- frontend service
- database service

This keeps the initial setup simple and cheap.

## Environment Strategy

The current strategy is to avoid paying for multiple always-on environments.

### Main environment

There will be a normal deployment for the main branch.

### Dev environment

Sometimes we will also need a `dev` environment or a temporary feature-related environment.

To control cost, we accept small downtime and do not require both environments to stay up all the time.

## Docker Compose Strategy

The current plan is to maintain two Docker Compose configurations.

### Compose file 1

A compose configuration for the main deployment only.

Expected contents:

- proxy
- frontend for main
- backend for main
- database

### Compose file 2

A compose configuration intended for switching deployment mode when development access is needed.

This second configuration is meant to cover the cases where development deployment is needed on the same VM.

### Operating rule

To save money and keep the server small:

- we accept a small downtime window
- when `dev` is needed, we can stop the running main deployment and start the development-oriented deployment mode instead

The exact file naming is still open, but the intended model is:

- one compose setup optimized for main
- one compose setup used when we need the development environment on the same machine

## Proxy Direction

A reverse proxy will be used in front of the application services.

The proxy is needed to:

- expose the frontend and backend cleanly
- support host-based or path-based routing
- make future environment switching easier
- avoid exposing raw internal ports directly

The exact proxy technology is not fixed yet, but likely candidates are:

- `Caddy`
- `Nginx`
- `Traefik`

## Memory Expectation

The `e2-medium` choice is based on the rough memory expectations for:

- Linux + Docker
- reverse proxy
- Go backend
- React frontend app
- MariaDB

Why `4 GiB` was selected instead of `2 GiB`:

- `2 GiB` would be too tight once database, frontend, backend, and proxy all run together
- `4 GiB` gives safer headroom
- `MariaDB` helps reduce pressure compared with `MySQL`

## Cost Control Principles

Current cost-saving principles:

- prefer a single VM
- avoid a managed database in the first version
- stop environments when they are not needed
- accept limited downtime for environment switching
- keep the design simple until real usage justifies more complexity

## Open Decisions

The following details still need to be finalized later:

- exact reverse proxy choice
- exact Docker Compose file names and structure
- domain and subdomain plan
- TLS certificate strategy
- persistent volume and backup strategy for `MariaDB`
- whether main and dev should share one DB service with separate databases, or use separate DB containers
- exact process for switching between main and dev deployments on the VM

## Related Documents

- Cloud comparison note: [notes/cloud.providers.comparison.md](/c:/projects/lessons-dashboard/notes/cloud.providers.comparison.md)
- Business plan: [docs/business/plan.v1.md](/c:/projects/lessons-dashboard/docs/business/plan.v1.md)
