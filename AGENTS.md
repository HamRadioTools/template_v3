# AGENTS instructions

This code repository is designed to be used with AI coding agents (ChatGPT, Claude and others).

These instructions apply **globally** to all agents unless explicitly overridden.

The main developer documentation lives in the `docs` directory.

---

## General principles

- Prefer **clarity over cleverness**.
- Prefer **explicitness over magic**.
- Follow **existing project structure and conventions**.
- Avoid introducing new abstractions unless clearly justified.
- Do not refactor unrelated code.
- Prioritize alwasy functional programming over object-orinted programming without breaking other herein defined principles.

> IMPORTANT NOTE:  
> Agents should behave as **senior architects, software architects, software engineers, coders and/or maintainers**, not code generators.

---

## Documentation

### Sructure

- All formal documentation lives under the `docs/` directory.
- Any new document **must follow a consecutive numeric prefix** with the exception of ADRs (Architectural Decission Records) that will folow its own format rules:

  ```txt
  docs/
  001-architecture-overview.md
  002-authentication-model.md
  003-telemetry-pipeline.md
  ```

- Numbers are **monotonic** and never reused.
- Filenames should be:
  - lowercase.
  - dash-separated.
  - descriptive but concise.

- For ADRs: any new document **must follow a consecutive numeric format following `adr` prefix** in lowercase :

 ```txt
  docs/
  adr01-cache-usage.md
  adr02-mqtt-topic-structure.md
  ```

### Authoring rules

- Prefer **inline explanations in tests** when tightly coupled to behaviour
- Use `docs/` for:
  - architecture decisions.
  - non-obvious design trade-offs.
  - cross-module behaviour.
  - long-form explanations.
- Inline comments should reference documentation when applicable, e.g.:

    ```python
    # See docs/0004-token-lifecycle.md
    ```

- Hyperlinks to docs/ files are encouraged when it improves traceability

### Building documentation

- Documentation does not need to be built by default.
- Local builds are recommended only when:
  - diagrams are involved.
  - rendering affects correctness.
  - the change is documentation-heavy.
- Agents should not introduce documentation tooling unless explicitly requested.

---

## Environment setup

- Use existing tooling defined in:
  - pyproject.toml
  - Cargo.toml
  - .env.example (if present)
- Do not assume global tools are installed.
- Do not modify environment setup files unless required by the task.

---

## Running tests

### Language: Python

- Use `pytest` to run tests.
- Use `mypy` to analyze complexity and accuracy.
- Use `black` for opinionated code format.

Rules:

- Tests must be deterministic.
- New features require tests.
- Bug fixes require regression tests.
- Prefer small, focused tests.

### Language: Rust

- Use `cargo test`
- Use `cargo fmt`
- Use `cargo clippy --all-targets --all-features -- -D warnings`

Rules:

- Do not suppress warnings without justification.
- Avoid unsafe code unless unavoidable.
- Prefer explicit lifetimes when clarity improves.

---

## Pull request workflow

Agents should follow this workflow:

- Understand the intent:
  - Do not guess requirements.
  - Ask for clarification if behaviour is ambiguous.
- Make minimal changes:
  - No drive-by refactors.
  - No unrelated formatting changes.
- Update tests and docs:
  - Tests for behaviour.
  - Docs for architecture or contracts.
- Keep commits logical:
  - One concern per commit when possible.
  - Clear, descriptive commit messages.
- Leave the codebase cleaner:
  - Remove dead code if directly related.
  - Improve naming only when necessary.

---

## What agents must NOT do

- Introduce new dependencies without approval.
- Change public APIs silently.
- Reformat large files unnecessarily.
- Replace existing patterns with personal preferences.
- Assume production configuration details.
- Tamper with unneeded files, folders, programs and, in general, anything not directly related to project never, but specially, never silently.

---

## Final note

If these instructions conflict with...

- AGENT.md (OpenAI ChatGPT)
- CLAUDE.md (Antrhopic)
- explicit user instructions

... the most specific instruction always wins. When in doubt, ask first.
