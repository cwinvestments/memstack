## When to notify

There are two notification triggers:

### 1. Before any approval prompt

When you are about to run a command that will trigger an approval prompt (file writes, compound commands, potentially dangerous operations), **split it into two separate steps**:

**Step 1 — Voice notification (standalone Bash call):**

Run the TTS command as its own isolated tool call. Do not combine it with any other tool call in the same response.

- **Windows:** `powershell -c "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('Claude needs your attention')"`
- **macOS:** `say "Claude needs your attention"`
- **Linux:** `spd-say "Claude needs your attention" || espeak "Claude needs your attention" || echo -e '\a'`

**Step 2 — Actual command:**

Only after the TTS call completes, run the actual command that requires approval in the next response.

Never combine the TTS and the tool call in the same step. The voice must complete before the approval prompt appears.

### 2. After completing work

After completing any task, run the appropriate notification as a standalone Bash call.

## Message selection

Pick the message based on what just happened:
- **Task complete** (work finished, no input needed): `"Task complete"`
- **Needs attention** (about to ask a question, need approval, waiting for input): `"Claude needs your attention"`
- **Error occurred** (something failed, build broke, command errored): `"Something went wrong"`

## Rules

- Do not skip notifications. Run them every time.
- TTS and approval-triggering tool calls must NEVER be in the same response. Two separate steps, two separate responses.
- For task completion: notification runs AFTER the final output.
