#!/bin/bash
# usage: stills.sh "1 2 3" times
cd /home/claude/murree
for n in $1; do BSEG=1 FPS=30 blender -b --python film_by.py -- $n 40 8 still $2 2>&1 | grep -E "Error|Traceback|line [0-9]+|STILL" | grep -v EGL | sed "s/^/[$n] /"; done
