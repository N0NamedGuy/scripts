#!/bin/bash

MAIN_MONITOR=LVDS1
SECOND_MONITOR=(HDMI1 VGA1)

# Checks if a monitor is connected
# $1 - Source to check
# returns 0 if connected, other values otherwise
function check_connected() {
    xrandr -q | grep "$1 connected" > /dev/null
    echo $?
}

for mon in $SECOND_MONITOR; do
    if [ `check_connected $mon` -eq 0 ]; then
        xrandr --output $mon --auto --right-of $MAIN_MONITOR --output $MAIN_MONITOR --primary --auto
        exit
    fi
done

# Turn off every and any external monitor (since they're all unplugged anyway)
for mon in $SECOND_MONITOR; do
    xrandr --output $mon --off
    exit
done

# Leave the main screen on
xrandr --output $MAIN_MONITOR --primary --auto
