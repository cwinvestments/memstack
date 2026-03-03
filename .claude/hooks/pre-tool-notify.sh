#!/bin/bash
if command -v powershell.exe &>/dev/null; then
    powershell.exe -c "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('Claude needs your attention')"
elif command -v say &>/dev/null; then
    say "Claude needs your attention"
elif command -v espeak &>/dev/null; then
    espeak "Claude needs your attention"
else
    echo -e '\a'
fi
