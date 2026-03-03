# Template v3 Project Spec

## Purpose

This repository is a template for building Python services with:

- API runtime mode
- Worker runtime mode (one-shot or loop)

The specification is the source of truth. Code implements specs.

## Terminology

- `API mode`: long-running HTTP process exposing endpoints.
- `Worker mode`: process that executes background jobs.
- `One-shot worker`: starts, runs one unit of work, exits.
- `Loop worker`: starts, repeats work, stops on signal.

## Normative Rules

- Behavior requirements in domain specs SHALL be implemented as written.
- If behavior is not specified, it MUST be clarified before implementation.
- Public API contracts SHALL be documented in corresponding domain specs.
- Security, privacy, and logging constraints SHOULD be defined in domain specs.

## Runtime Model

- `APP_TYPE=api` SHALL start the HTTP service.
- `APP_TYPE=worker` SHALL start the worker runtime.
- `WORKER_MODE=oneshot` SHALL execute one work cycle and exit.
- `WORKER_MODE=loop` SHALL execute repeated cycles and support graceful stop.

## Data/Integration Conventions

Each project created from this template should define:

- timestamp format and timezone policy
- identifiers and validation rules
- error format and error code strategy
- external integration contracts

These conventions belong in domain specs under `openspec/specs/`.
