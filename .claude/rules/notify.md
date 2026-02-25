After completing any task and before presenting your final response to the user, run this command:
```bash
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then powershell -c "(New-Object Media.SoundPlayer 'C:\Windows\Media\chimes.wav').PlaySync()"; elif [[ "$OSTYPE" == "darwin"* ]]; then afplay /System/Library/Sounds/Glass.aiff; elif command -v paplay &>/dev/null; then paplay /usr/share/sounds/freedesktop/stereo/complete.oga; else echo -e '\a'; fi
```

This alerts the user that you are finished and waiting for input. Do this every time you complete work — after commits, after file edits, after answering questions. Do not skip this step.
