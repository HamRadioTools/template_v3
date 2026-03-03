# Spec: Example Module

## Scope

Defines minimal behavior for a sample API endpoint and worker task.

## Requirements

### Requirement: Health Endpoint

The service SHALL expose a health endpoint.

#### Scenario: Return liveness status

- Given the service is running
- When a client sends `GET /health`
- Then response status is `200`
- And response JSON includes `"status": "ok"`

### Requirement: Worker One-Shot Execution

Worker one-shot mode SHALL execute exactly one work cycle and exit.

#### Scenario: One-shot run

- Given `APP_TYPE=worker`
- And `WORKER_MODE=oneshot`
- When the process starts
- Then one work cycle is executed
- And cleanup runs
- And the process exits successfully

### Requirement: Worker Loop Execution

Worker loop mode SHALL execute work repeatedly until termination signal.

#### Scenario: Loop run and graceful stop

- Given `APP_TYPE=worker`
- And `WORKER_MODE=loop`
- When the process starts
- Then work cycles repeat with configured poll interval
- When SIGTERM is received
- Then the worker finishes cleanup and exits
