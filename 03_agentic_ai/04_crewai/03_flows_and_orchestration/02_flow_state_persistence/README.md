# Module 02 - Flow State Persistence

> **MLCourse - Flows and Orchestration - Flow State Persistence**

Long-running flows need to survive crashes and restarts. This module covers
@persist for automatic state checkpointing, SQLite-based storage, and how to
resume or fork flows from saved states.

## What you'll learn

- Use @persist to automatically save flow state
- Configure SQLite checkpointing for local persistence
- Resume flows from their last checkpoint
- Fork a flow from a saved state to explore alternatives
- Manage checkpoint lifecycle and cleanup

## Key concepts

- **@persist decorator**: marks state fields for automatic checkpointing
- **SQLite checkpointing**: local file-based state storage
- **Resume**: restart a flow from its last saved state
- **Fork**: branch from a checkpoint into an alternative execution path
- **Checkpoint lifecycle**: creation, reading, and cleanup of saved states

## Contents

1. `01_persist_decorator.ipynb` - @persist basics, which fields to persist
2. `02_sqlite_checkpointing.ipynb` - SQLite storage, configuration, inspection
3. `03_resume_and_fork.ipynb` - resuming flows, forking from checkpoints

After this module, continue to `03_human_in_the_loop` for approval gates.
