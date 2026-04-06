#!/bin/bash
# Pre-tool TTS notification — reads config from .claude/tts-config.json

# TTS notifications are opt-in. Set MEMSTACK_ENABLE_TTS=true to enable.
if [ "$MEMSTACK_ENABLE_TTS" != "true" ]; then
  exit 0
fi

CONFIG_FILE="${BASH_SOURCE%/*}/../tts-config.json"

# Default message
MSG="Claude needs your attention"

if [ -f "$CONFIG_FILE" ]; then
  # Check if enabled (default: true)
  ENABLED=$(python -c "import json; print(json.load(open('$CONFIG_FILE')).get('enabled', True))" 2>/dev/null)
  if [ "$ENABLED" = "False" ]; then
    exit 0
  fi

  # Read approval_prompt message
  CUSTOM=$(python -c "import json; print(json.load(open('$CONFIG_FILE')).get('messages', {}).get('approval_prompt', ''))" 2>/dev/null)
  if [ -n "$CUSTOM" ]; then
    MSG="$CUSTOM"
  fi
fi

if command -v powershell.exe &>/dev/null; then
    powershell.exe -c "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('$MSG')"
elif command -v say &>/dev/null; then
    say "$MSG"
elif command -v espeak &>/dev/null; then
    espeak "$MSG"
else
    echo -e '\a'
fi
