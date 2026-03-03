#!/bin/bash
if command -v say &>/dev/null; then
    say "Claude needs your attention"
elif command -v espeak &>/dev/null; then
    espeak "Claude needs your attention"
else
    echo -e '\a'
fi
