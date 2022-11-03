# this code is intended to be used to create a path utilising inverse kinematics
# use this code as a template to create pre-determined paths using known chassis forward velocity (x dot) in m/s, 
# chassis angular velocity (theta dot) in rad/s, and motion duration in sec for each motion to create the path

import L1_log as log
import L2_inverse_kinematics as ik
import L2_speed_control as sc
import numpy as np
from time import sleep

# define some variables that can be used to create the path
# make use of these definitions in the motions list
pi = np.pi                  # utilize the numpy library to define pi
d1 = 0.5                      # distance in meters of segment 1 in the path
d2 = 0.25                      # distance in meters of segment 2 in the path
forward_velocity = 0.0      # forward velocity (x dot) in m/s of SCUTTLE. NOTE that the max forward velocity of SCUTTLE is 0.4 m/s

# below is a list setup to run through each motion segment to create the path.
# the list elements within each list are in order as follows: chassis forward velocity (m/s), chassis angular velocity (rad/s), and motion duration (sec)
# enter the chassis forward velocity (x dot) in m/s, chassis angular velocity (theta dot) in rad/s, and motion duration in sec for each motion to create the path
motions = [		     # These motions have been fine tuned from their initial values.
    [0.4, 0.0,      1.25],   # Motion 1	: move forward at .4m/s for 1.25s to move d1 (tuned)
    [0.0, pi/2.0,   1.25],   # Motion 2	: rotate in place CCW 90 degrees (tuned)
    [0.4, 0.0,      0.625],  # Motion 3	: move forward at .4m/s for .625s to move d2 (tuned)
    [0.0, pi/2.0,   1.25],   # Motion 4 : rotate CCW 90deg (motion 2)
    [0.4, 0.0,      1.25],   # Motion 5	: move forward d1 (motion 1)
    [0.0, -pi/2.0,  1.25],   # Motion 6	: rotate CW 90deg (tuned)
    [0.4, 0.0,      0.625],  # Motion 7	: move forward d2 (motion 3)
    [0.0, -pi/2.0,  1.25],   # Motion 8	: rotate CW 90deg (motion 6)
    [0.4, 0.0,      1.25],   # Motion 9	: move forward d1 (motion 1)
    [0.0, pi/2.0,   5.0],    # Motion 10: Do a victory spin (CCW 360deg)
]

# iterate through and perform each open loop motion and then wait the specified duration.
for  count, motion in enumerate(motions):
    print("Motion: ", count+1, "\t Chassis Forward Velocity (m/s): {:.2f} \t Chassis Angular Velocity (rad/s): {:.2f} \t Duration (sec): {:.2f}".format(motion[0], motion[1], motion[2]))
    wheel_speeds = ik.getPdTargets(motion[:2])                  # take the forward speed(m/s) and turning speed(rad/s) and use inverse kinematics to deterimine wheel speeds
    sc.driveOpenLoop(wheel_speeds)                              # take the calculated wheel speeds and use them to run the motors
    sleep(motion[2])                                            # wait the motion duration
