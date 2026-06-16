---
description: Programmatically play back conversation flows in Jetski Hub chats using text fixtures.
---

# Conversation Playback Automation Workflow

This workflow guide describes how to use the lightweight conversation playback script to programmatically run through chat playbacks, eliminating the need to manually type prompts during testing.

---

## How it Works

The playback script (`tests/playback_conversation.py`) parses a text file containing a list of prompts separated by a `=== PROMPT ===` delimiter line. It then plays them back sequentially into a Jetski Hub conversation by calling the `agentapi` CLI tool.

Because `agentapi` blocks until the agent completes its turn, the playback is automatically throttled and paced to the agent's actual execution speed.

---

## How to Run the Playback

### Scenario A: Playback into a New Chat (Recommended)
If you want to start a fresh chat and run the playback automatically:
1. Open your terminal and change directory to your active target project folder (e.g. `~/projects/sdd-harness-test`):
   ```bash
   cd ~/projects/sdd-harness-test
   ```
2. Run the playback script pointing to your prompts file (without passing `--conv_id`):
   ```bash
   ~/projects/ag-setup/tests/playback_conversation.py --file ~/projects/ag-setup/tests/fixtures/blueprint_prompts.txt
   ```
3. The script will:
   * Spawn a new conversation in Jetski Hub.
   * Print the new **Conversation ID** and clickable **Hub URL**.
   * Play back all prompts sequentially.

### Scenario B: Playback into an Existing Chat
If you have an active conversation open in Jetski Hub and want to automate the remaining prompts:
1. Copy the **Conversation ID** from the Hub browser URL (the UUID part at the end of the URL).
2. Run the script passing the `--conv_id` flag:
   ```bash
   ~/projects/ag-setup/tests/playback_conversation.py --file /path/to/prompts.txt --conv_id <your_conversation_id>
   ```

---

## Playback File Format
Prompts inside the text file must be separated by `=== PROMPT ===` on a line by itself. Multi-line prompts are fully supported.

Example:
```text
First prompt text here
=== PROMPT ===
Second prompt text
Can span multiple lines
=== PROMPT ===
Third prompt text
```
