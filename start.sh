#!/bin/bash

# Cleanup, if restarting a container
rm -f /tmp/.X1-lock /tmp/.X11-unix/X1

# Start virtual screen
sudo /sbin/start-stop-daemon --start --pidfile /tmp/custom_xvfb_1.pid --make-pidfile --background --exec /usr/bin/Xvfb -- :1 -ac -screen 0 1280x1024x16;
sleep 5;

export EAGLE_DIR=/opt/eagle-9.6.2;
export DISPLAY=:1;
export EAGLE_USER="rhernandez@valiot.io"
export EAGLE_PSW="DeltaEcho9"

# Eagle Auto Login.
sudo ${EAGLE_DIR}/eagle & sleep 40;
sudo xdotool key Left;
sleep 5;
sudo xdotool key Return;
sleep 5;
sudo xdotool type ${EAGLE_USER};
sleep 5;
sudo xdotool key Return;
sleep 5;
sudo xdotool type ${EAGLE_PSW};
sleep 5;
sudo xdotool key Return;
sleep 10;
sudo kill $(pidof ${EAGLE_DIR}/eagle);
sleep 2;

# Execute CAM Jobs
sudo ${EAGLE_DIR}/eagle -X -c+ -N -dCAMJOB -j/home/user/ELECROW_gerber_v9.cam -o/home/user/bin /home/user/optoSensor.brd
sleep 3

# Verify outputs
sudo ls -ls /home/user/bin/
echo *************************************
sudo ls -ls /home/user/bin/Assembly/
echo *************************************
sudo ls -ls /home/user/bin/Gerbers/
