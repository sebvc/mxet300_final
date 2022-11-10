import ObstacleAvoidanceTest1 as avoid
import L3_color_tracking_from_file as track
import L2_inverse_kinematics as ik
import L2_kinematics as kin
import L2_speed_control as sc


lidar_points = 500

if __name__ == "__main__":
    track.getHSVfromCSV("dogball")
    track.set_up_cam()


    try:

        while True:

            if (avoid.LIDAR_obstacle_seen(lidar_points)):
                # AVOID with lidar
                print("LIDAR",end='')
                avoid.avoid_Obstacle()

            elif(track.seeTarget()):
                track.goToBall()
                #run ball tracking
                print("WEBCAM",end='')
            
            else: # default free path
                print("Default Path")
                wheel_speeds = ik.getPdTargets( [0.15, 0.0])  # default parameters
                wheel_measured = kin.getPdCurrent()
                sc.driveClosedLoop(wheel_speeds,wheel_measured,0)
                
    except KeyboardInterrupt: # condition added to catch a "Ctrl-C" event and exit cleanly
        pass

    finally:
    	print("Exiting!.")