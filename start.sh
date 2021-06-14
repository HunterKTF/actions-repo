#!/bin/bash

# Cleanup, if restarting a container
rm -f /tmp/.X1-lock /tmp/.X11-unix/X1

# Start virtual screen
/sbin/start-stop-daemon --start --pidfile /tmp/custom_xvfb_1.pid --make-pidfile --background --exec /usr/bin/Xvfb -- :1 -ac -screen 0 1280x1024x16;
sleep 5;

export EAGLE_DIR=eagle-9.6.2;
export DISPLAY=:1;
export EAGLE_USER="rhernandez@valiot.io"
export EAGLE_PSW="DeltaEcho9"

# Eagle Auto Login.
${EAGLE_DIR}/eagle & sleep 59;
xdotool key Left;
sleep 8;
xdotool key Return;
sleep 8;
xdotool type ${EAGLE_USER};
sleep 8;
xdotool key Return;
sleep 8;
xdotool type ${EAGLE_PSW};
sleep 8;
xdotool key Return;
sleep 10;
kill $(pidof ${EAGLE_DIR}/eagle);
sleep 4;

# Execute CAM Jobs
sudo ${EAGLE_DIR}/eagle -X -c+ -N -dCAMJOB -j/home/user/ELECROW_gerber_v9.cam -o/home/user/ /home/user/optoSensor.brd

# Verify outputs
ls /home/user;
