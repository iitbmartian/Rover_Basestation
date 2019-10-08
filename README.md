Rover_Basestation
===============================================================
The following Repo contains Base Station code for MSI 2016.

# Instructions for pre-run checks and setting up the basestation

## How to charge batteries:
1. Get a multimeter, check the charges and compare it with rating
2. If charge is less connect the battery to the chargee () using THINNER WIRED SIDE
3. Keep checking the charge state regularly, diconnect one rating value is reached

## How to create a ROS workspace:
1. Create a new directory
2. Create a "src" folder, put your code files here
3. Navigate back to workspace folder and run "catkin_make"
4. source devel/setup.bash

## How to initialize a ROS terminal
1. source /opt/ros/kinetic/setup.bash (usually in bashrc file)
2. export ROS_IP i.e. current system's IP
3. export ROS_MATER_URI i.e. master's IP
4. Navigate into the workspace and run "source devel/setup.bash"
5. roslaunch <launch_file_of_respective_code>

## How to SSH into a computer
1. ssh computer_name@IP
2. Enter password
-- to shutdown --
3. sudo shutdown now

## How to setup wifi settings from a tenminal
1. sudo nano /etc/wpa_supplicant/
2. wpa_supplicant.conf

OR

1. sudo nano /etc/network/interfaces

## Run a sftp client to get file structure. For this:
1. Go to Files -> Connect to server
2. In server address, type sftp://rover-nuc@ip.ip.ip.ip/ to start sftp session

## Interface settings
1. `ls /dev` gives the list of devices connected to the computer
2. Look out for `ttyACMx`, it denotes USB port x+1, using `ls /dev | grep ttyACMx`  
3. Rules of interfacing are present in `/etc/udev` folder
4. Edit `72-roboclaw.rules` as per requirement
5. Use `udevadm info -a -n /dev/ttyACM0 | grep '{product}'`and `udevadm info -a -n /dev/ttyACM0 | grep '{product}'` to find `ATTRS{product}` and `ATTRS{devpath}` respectively of the port ttyACM0
6. To grant necessary permissions to the interface ports use `sudo chmod 666 /dev/ttyACM*`
