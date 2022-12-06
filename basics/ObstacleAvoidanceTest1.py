import L2_vector as vec
import L2_speed_control as sc
import numpy as np
import L2_kinematics as kin
import L2_inverse_kinematics as ik
from time import sleep


lidar_points = 500

def LIDAR_obstacle_seen(lidar_points):
    global angle
    nearestArray = vec.getNearest(lidar_points)
    distance = nearestArray[0]
    angle = nearestArray[1]
    thetaDot = 0.0
    return inBound_rth(distance,angle)
def avoid_Obstacle():
    global angle
    if (angle >= 0): # if object on left (positive angle)
        thetaDot = -6 #turn right (CW)
        print("\t\t\tturning right (CW)")
    else: # if object on right (negative angle)
        thetaDot = 6 #turn left (CCW)
        print("\t\t\tturning left (CCW)")
    wheel_speeds = ik.getPdTargets(np.array([0,thetaDot]))
    wheel_measured = kin.getPdCurrent()
    sc.driveClosedLoop(wheel_speeds,wheel_measured,0)  

# Bounding Box Function
def inBound_rth(r,th):
    maxAngle= 75
    minAngle= -75
    #@ bounding angles distance is 0.28
    # returns bool: True if point is closer than defined boundary
    if ((minAngle<th) and (th<maxAngle)):
        # check boundary_distance(th)
        boundary_distance = np.sqrt((np.cos(th))**2+(.7*np.sin(th))**2)
        return  r < boundary_distance 
        '''
                   (.5, 0deg)
        (0.4, 40deg) .__W__. (0.4, -40deg)
                     |     |
        (.28 75deg) O|__L__|O (.28 -75deg)

        graph polar r = sqrt((.9cos(th))^2+(.6sin(th))^2)
        
        KEY
        O : motor/powered wheel
        . : caster wheel
        L : lidar
        W : webcam
        '''      
    else: # outside of angles
        return False

if __name__ == "__main__":
    while(1):
        nearestArray = vec.getNearest(lidar_points)
        distance = nearestArray[0]
        angle = nearestArray[1]
        thetaDot = 0.0
                                        
        if inBound_rth(distance,angle):
            #avoidingTurn = [0,90-angle,]
            if (angle >= 0): # if object on left (positive angle)
                thetaDot = -6 #turn right (CW)
                print("\t\t\tturning right (CW)")
            else: # if object on right (negative angle)
                thetaDot = 6 #turn left (CCW)
                print("\t\t\tturning left (CCW)")
            wheel_speeds = ik.getPdTargets(np.array([0,thetaDot]))
            wheel_measured = kin.getPdCurrent()
            sc.driveClosedLoop(wheel_speeds,wheel_measured,0)  

        else: 
            wheel_speeds = ik.getPdTargets( [0.25, 0.0])  
            wheel_measured = kin.getPdCurrent()
            sc.driveClosedLoop(wheel_speeds,wheel_measured,0)  
        
        print("(",distance,"," , angle,"deg )")
        sleep(0.25)



