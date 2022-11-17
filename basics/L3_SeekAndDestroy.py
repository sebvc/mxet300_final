
import ObstacleAvoidanceTest1 as avoid
import L3_color_tracking_from_file as track
import L2_inverse_kinematics as ik
import L2_kinematics as kin
import L2_speed_control as sc
#import ServoGPIO as servo
import RPi.GPIO as GPIO
import time

servoPin = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin,GPIO.OUT)
servo = GPIO.PWM(servoPin,50)
servo.start(10)

lidar_points = 500
state = 0 
align_count =0
'''
state meaning:
    0: No ball
    1: See ball
    2: Aligned
    3: Got ball
'''

if __name__ == "__main__":
    track.getHSVfromCSV("tennisball")
    track.set_up_cam()
    #servo.setup()
    #servo.open()

    try:

        while True:
            print("State: ",state)
            target_seen, state = track.seeTarget(state)
            # if (avoid.LIDAR_obstacle_seen(lidar_points)):
            if (False):
                # AVOID with lidar
                print("LIDAR",end=' ')
                avoid.avoid_Obstacle()
            elif(target_seen):
                print("WEBCAM",end=' ')
                state, align_count = track.goToBall(state,align_count)
                #run ball tracking
                
            
            else: # default free path
                print("Default Path")
                # wheel_speeds = ik.getPdTargets( [0.15, 0.0])  # default parameters
                wheel_speeds = ik.getPdTargets( [0.0, 0.0])  # default parameters
                wheel_measured = kin.getPdCurrent()
                sc.driveClosedLoop(wheel_speeds,wheel_measured,0)
            # if(state==3):
            #     servo.ChangeDutyCycle(1)
            if(align_count>=10):
                print("\n\nball found!!!!\n")
                time.sleep(2)
                wheel_speeds = ik.getPdTargets([0.16, 0.0])  # default parameters
                wheel_measured = kin.getPdCurrent()
                sc.driveClosedLoop(wheel_speeds,wheel_measured,0)                
                print("\nstop.")
                time.sleep(.8)
                wheel_speeds = ik.getPdTargets([0.0, 0.0])  # default parameters
                wheel_measured = kin.getPdCurrent()
                sc.driveClosedLoop(wheel_speeds,wheel_measured,0)
                servo.ChangeDutyCycle(1)
                break
            while True: # has ball.
                print("do new thing")

    except KeyboardInterrupt: # condition added to catch a "Ctrl-C" event and exit cleanly
        pass

    finally:
        #servo.cleanup()
        servo.stop()
        GPIO.cleanup()
        print("Exiting!.")
