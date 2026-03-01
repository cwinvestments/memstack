## When to notify

There are two notification triggers:

### 1. Before any approval prompt or question

**Before** presenting any question, approval prompt, choice, or request for user input, run the "needs attention" notification FIRST, then present the prompt. This alerts the user to return to the terminal.

### 2. After completing work

After completing any task and before presenting your final response, run the appropriate notification.

## Message selection

Pick the message based on what just happened:
- **Task complete** (work finished, no input needed): `"Task complete"`
- **Needs attention** (about to ask a question, need approval, waiting for input): `"Claude needs your attention"`
- **Error occurred** (something failed, build broke, command errored): `"Something went wrong"`

## Command

Run this command with `MESSAGE` set to the appropriate text:
```bash
MESSAGE="Task complete"; if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then powershell -c "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('$MESSAGE')"; elif [[ "$OSTYPE" == "darwin"* ]]; then say "$MESSAGE"; elif command -v spd-say &>/dev/null; then spd-say "$MESSAGE"; elif command -v espeak &>/dev/null; then espeak "$MESSAGE"; else echo -e '\a'; fi
```

## Rules

- Do not skip notifications. Run them every time.
- For approval prompts: notification runs BEFORE the prompt text, not after.
- For task completion: notification runs AFTER the final output.
