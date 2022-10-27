import L2_vector
import L2_speed_control as sc
import numpy as np
import L2_kinematics as kin
import L2_inverse_kinematics as ik
from time import sleep
wheel_speeds = ik.getPdTargets( [0.5, 0.0])   
while(1):
    nearestArray = L2_vector.getNearest()
    distance = nearestArray[0]
    angle = nearestArray[1]
    x = distance * np.cos(angle)
    y = distance * np.sin(angle)
    print("distance"+str(distance)+"\n")
    print("angle"+str(angle))
    print("X"+str(x))
    print("Y"+str(y))
    #if distance:
    #    sc.driveOpenLoop(wheel_speeds)                              # take the calculated wheel speeds and use them to run the motors
   # if np.abs(y)<0.1:
  #      sc.driveOpenLoop(np.array([0.,0.]))
    sleep(0.5)
    
    