## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.

import sys
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()

update_thread = repeating_timer(2, update_sim)


## STUDENT CODE BEGINS
## ----------------------------------------------------------------------------------------------------------
## Example to rotate the base: arm.rotateBase(90)


arm.home()
time.sleep(2)

#while loop will continuously run within the for loop
while True:

    #defined a function open_autoclave(container) that opens the autoclave bin for each of the large containers
    def open_autoclave(container):
        if container == 4:  #Large Red
            open_drawer = arm.open_red_autoclave(True)
        elif container == 5:  #Large Green
            open_drawer = arm.open_green_autoclave(True)
        elif container == 6:  #Large Blue
            open_drawer = arm.open_blue_autoclave(True)
        else:
            return False
   
    #defined a function get_dropoff(container) that returns the dropoff location for the specified container
    def get_dropoff(container):
        if container == 1: #Small Red
            dropoff = [-0.5775, 0.2392, 0.4214]
        elif container == 2: #Small Green
            dropoff = [0.0, -0.6251, 0.4214]
        elif container == 3: #Small Blue
            dropoff = [0.0, 0.6251, 0.4214]
        elif container == 4: #Large Red
            dropoff = [-0.3888, 0.161, 0.3100]
        elif container == 5: #Large Green
            dropoff = [0.0, -0.4208, 0.3100]
        elif container == 6: #Large Blue
            dropoff = [0.0, 0.4208, 0.3100]
        else:
            dropoff = [0.4064, 0.0, 0.4826]
        return dropoff

    #defined a function close_autoclave(container) that closes the autoclave bin for each of the large containers
    def close_autoclave(container):
        if container == 4:  #Large Red
            close_drawer = arm.open_red_autoclave(False)
        elif container == 5:  #Large Green
            close_drawer = arm.open_green_autoclave(False)
        elif container == 6:  #Large Blue
            close_drawer = arm.open_blue_autoclave(False)
        else:
            return False

    #turns container ID input into an integer
    x = input("Provide a container ID between 1-6, or enter 7 to exit:")
    x = int(x)

    #range given for designated containers between 1 to 6
    if 1 <= x <= 6:
        pass
    #program terminates when input is 7
    elif x == 7:
        quit()
    #else prints invalid container ID and returns to home position
    else:
        print("Invalid Container ID, returning to home position.")

    #threshold of muscle emulator defined to be 0.5
    th = 0.5
    #home location of q-arm defined
    home = [0.4064, 0.0, 0.4826]
    #pickup location of containers defined
    pickup = [0.5193, 0.003, 0.04700]

    arm.spawn_cage(x)
    
    print("Pickup location of your container is:", pickup)

    #when L and R is above and equal to th; q-arm moves to pickup location
    while True:
        if arm.emg_left() > th and arm.emg_right() > th and arm.emg_left() == arm.emg_right():
            arm.move_arm(0.5200, 0.0, 0.04700)
            break
    time.sleep(2)

    #when L is above th and R is equal to 0; q-arm closes gripper to pick up container 
    while True: 
        if arm.emg_left() > th and arm.emg_right() == 0:
            arm.control_gripper(35)
            break
    time.sleep(2)

    #when L and R is above and equal to th; q-arm moves container to home location
    while True: 
        if arm.emg_left() and arm.emg_right() > th and arm.emg_left() == arm.emg_right():
            arm.move_arm(home[0], home[1], home[2])
            break
    time.sleep(2)

    #when R is above th and L is equal to 0; autoclave drawer for specified large container opens
    while True: 
        if arm.emg_left() == 0 and arm.emg_right() > th:
            open_drawer = open_autoclave(x)
            break
    time.sleep(2)

    #get_dropoff(x) is defined to be dropoff
    dropoff = get_dropoff(x)
    print("Dropoff location of your container is:", dropoff)

    #when L and R is above and equal to th; q-arm moves container to dropoff location
    while True:
        if arm.emg_left() and arm.emg_right() > th and arm.emg_left() == arm.emg_right():
            arm.move_arm(dropoff[0], dropoff[1], dropoff[2])
            break
    time.sleep(2)

    #when L is above th and R is equal to 0; q-arm opens gripper to dropoff container 
    while True:
        if arm.emg_left() > th and arm.emg_right() == 0:
            arm.control_gripper(-35)
            break
    time.sleep(2)

    #when R is above th and L is equal to 0; autoclave drawer for specified large container closes
    while True:
        if arm.emg_left() == 0 and arm.emg_right() > th:
            close_drawer = close_autoclave(x)
            break
    time.sleep(2)

    ##when L and R is above and equal to th; q-arm moves to home location
    while True:
        if arm.emg_left() and arm.emg_right() > th and arm.emg_left() == arm.emg_right():
            arm.move_arm(home[0], home[1], home[2])
            break
