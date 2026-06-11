# ADR 0001: Python SDK Connection Strategy for Jetski Hub Sync

* **Status**: Accepted
* **Date**: 2026-06-10

## Context

When automating agent tasks using the Google Antigravity/Jetski Python SDK, developers often want to monitor the agent's progress visually. 

By default, the SDK's `LocalAgentConfig` and `LocalConnectionStrategy` spawn a standalone background harness binary. While this works for headless/CI execution, it runs in a separate process from the user's active Jetski Language Server (which powers the Jetski Hub Web UI). 

Because they are separate processes:
1. They only share state via the filesystem database.
2. The already-open Jetski Hub UI in the browser does not receive real-time events (WebSockets) from the standalone SDK process.
3. The UI does not refresh automatically; it requires a manual page reload (F5) to see updates.

We need a way to programmatically drive the agent via Python scripts while maintaining real-time, interactive visibility in the Jetski Hub UI.

## Decision

We will use the **`GrpcConnectionStrategy`** (or equivalent remote connection strategy) in our Python automation scripts to connect directly to the **already running local Language Server process** instead of spawning a new standalone harness.

The script will:
1. Parse the active gRPC port and CSRF token from the local server's lockfile (`~/.gemini/jetski/daemon_port` or `~/.config/antigravity/daemon_port`).
2. Establish a gRPC connection to the running server.
3. Stream steps and prompts through this connection.

```python
from google.antigravity.connections.grpc import GrpcConnectionStrategy
from google.antigravity.conversation import Conversation

# Connect to the active local Language Server port
strategy = GrpcConnectionStrategy(
    address="localhost:<ACTIVE_PORT>",
    csrf_token="<CSRF_TOKEN>"
)
async with Conversation.create(strategy) as conversation:
    await conversation.chat("Perform task...")
```

## Consequences

### Consequences

*   **Real-time UI Mirroring (Pro)**: Any prompt sent by the Python script, along with the agent's internal thoughts, tool execution steps, and file diffs, will render live in the open Jetski Hub browser tab in real-time.
*   **Shared Session Context (Pro)**: The script and the UI operate on the exact same session state, allowing a developer to start a task via script and immediately take over manually in the Hub if the agent gets stuck.
*   **Server Dependency (Con)**: The script cannot run completely headless/standalone; it requires the Jetski Language Server to be actively running on the workstation/Cloudtop.
*   **Port Management (Con)**: The script must dynamically resolve the port from the lockfile since the Language Server port is dynamically assigned on startup.
