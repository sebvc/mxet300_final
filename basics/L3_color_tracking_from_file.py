# L3_color_tracking.py
# This program was designed to have SCUTTLE following a target using a USB camera input

import cv2              # For image capture and processing
import numpy as np      
import L2_speed_control as sc
import L2_inverse_kinematics as ik
import L2_kinematics as kin
import netifaces as ni
from time import sleep
from math import radians, pi
import csv


# Gets IP to grab MJPG stream
def getIp():
    for interface in ni.interfaces()[1:]:   #For interfaces eth0 and wlan0
    
        try:
            ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            return ip
            
        except KeyError:                    #We get a KeyError if the interface does not have the info
            continue                        #Try the next interface since this one has no IPv4
        
    return 0


def set_up_cam():
    global fov
    global camera
    #    Camera
    stream_ip = getIp()
    if not stream_ip: 
        print("Failed to get IP for camera stream")
        exit()

    camera_input = 'http://' + stream_ip + ':8090/?action=stream'   # Address for stream

    size_w  = 240   # Resized image width. This is the image width in pixels.
    size_h = 160	# Resized image height. This is the image height in pixels.

    fov = 1         # Camera field of view in rad (estimate)
    
    # Try opening camera with default method
    try:
        camera = cv2.VideoCapture(0)    
    except: pass

    # Try opening camera stream if default method failed
    if not camera.isOpened():
        camera = cv2.VideoCapture(camera_input)    

    camera.set(3, size_w)                       # Set width of images that will be retrived from camera
    camera.set(4, size_h)                       # Set height of images that will be retrived from camera

def seeTarget():
    global v1_min, v2_min, v3_min, v1_max, v2_max, v3_max 
    global image 
    global height
    global width
    global channels
    global thresh
    global kernel
    global mask
    global cnts
    global camera
    ret, image = camera.read()  # Get image from camera

    # Make sure image was grabbed
    if not ret:
        print("Failed to retrieve image!")
        return

    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)              # Convert image to HSV

    height, width, channels = image.shape                       # Get shape of image

    thresh = cv2.inRange(image, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))   # Find all pixels in color range

    kernel = np.ones((5,5),np.uint8)                            # Set kernel size
    mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)     # Open morph: removes noise w/ erode followed by dilate
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)      # Close morph: fills openings w/ dilate followed by erode
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)[-2]                        # Find closed shapes in image
            
    return (len(cnts) and len(cnts) < 3) #boolean of if target found  # If more than 0 and less than 3 closed shapes exist

def goToBall(): 
    global cnts
    global width
    global angle_margin
    global target_width
    global width_margin
    global fov

    c = max(cnts, key=cv2.contourArea)                      # return the largest target area
    x,y,w,h = cv2.boundingRect(c)                           # Get bounding rectangle (x,y,w,h) of the largest contour
    center = (int(x+0.5*w), int(y+0.5*h))                   # defines center of rectangle around the largest target area
    angle = round(((center[0]/width)-0.5)*fov, 3)           # angle of vector towards target center from camera, where 0 deg is centered

    wheel_measured = kin.getPdCurrent()                     # Wheel speed measurements

    # If robot is facing target
    if abs(angle) < angle_margin:                                 
        e_width = target_width - w                          # Find error in target width and measured width

                    # If error width is within acceptable margin
        if abs(e_width) < width_margin:
            sc.driveOpenLoop(np.array([0.,0.]))             # Stop when centered and aligned
            print("Aligned! ",w)
            sleep(0.15)
            return

        fwd_effort = e_width/target_width                   
                
        wheel_speed = ik.getPdTargets(np.array([0.8*fwd_effort, -0.5*angle]))   # Find wheel speeds for approach and heading correction
        sc.driveClosedLoop(wheel_speed, wheel_measured, 0)  # Drive closed loop
        print("Angle: ", angle, " | Target L/R: ", *wheel_speed, " | Measured L\R: ", *wheel_measured)
        return

    wheel_speed = ik.getPdTargets(np.array([0, -1.1*angle]))    # Find wheel speeds for only turning

    sc.driveClosedLoop(wheel_speed, wheel_measured, 0)          # Drive robot
    print("Angle: ", angle, " | Target L/R: ", *wheel_speed, " | Measured L\R: ", *wheel_measured)
        
def getHSVfromCSV(object_name_key):
    global v1_min
    global v2_min
    global v3_min
    global v1_max
    global v2_max
    global v3_max
    global target_width
    global angle_margin
    global width_margin
    # added/moved file to pull color image data
    csvReader = csv.DictReader(open("ball_tracking.csv",'r'))


    for row in csvReader:
        if(row["key"] == object_name_key): # specify which data HSV vlaues to use from csv e.g. key == dogball
            #    Color Range, described in HSV
            v1_min = int(row["minH"])      # Minimum H value
            v2_min = int(row["minS"])     # Minimum S value
            v3_min = int(row["minV"])      # Minimum V value

            v1_max = int(row["maxH"])     # Maximum H value
            v2_max = int(row["maxS"])    # Maximum S value
            v3_max = int(row["maxV"])    # Maximum V value

            target_width = int(row["target_width"])      # Target pixel width of tracked object
            angle_margin = float(row["angle_margin"])      # Radians object can be from image center to be considered "centered"
            width_margin = int(row["width_margin"])      # Minimum width error to drive forward/back
            break
        else: continue
    # test HSV values with print();
    # print(v1_min,v2_min,v3_min,v1_max,v2_max,v3_max,target_width,angle_margin,width_margin,"%%%%%%%%%%%%%%%%",sep='\n')

#    Camera
stream_ip = getIp()
if not stream_ip: 
    print("Failed to get IP for camera stream")
    exit()

camera_input = 'http://' + stream_ip + ':8090/?action=stream'   # Address for stream

size_w  = 240   # Resized image width. This is the image width in pixels.
size_h = 160	# Resized image height. This is the image height in pixels.

fov = 1         # Camera field of view in rad (estimate)

def main():
    # Try opening camera with default method
    try:
        camera = cv2.VideoCapture(0)    
    except: pass

    # Try opening camera stream if default method failed
    if not camera.isOpened():
        camera = cv2.VideoCapture(camera_input)    

    camera.set(3, size_w)  # Set width of images that will be retrived from camera
    camera.set(4, size_h)  # Set height of images that will be retrived from camera

    getHSVfromCSV("dogball")
    
    try:
        while True:
            sleep(.05)                                          

            ret, image = camera.read()  # Get image from camera

            # Make sure image was grabbed
            if not ret:
                print("Failed to retrieve image!")
                break

            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)              # Convert image to HSV

            height, width, channels = image.shape                       # Get shape of image

            thresh = cv2.inRange(image, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))   # Find all pixels in color range

            kernel = np.ones((5,5),np.uint8)                            # Set kernel size
            mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)     # Open morph: removes noise w/ erode followed by dilate
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)      # Close morph: fills openings w/ dilate followed by erode
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)[-2]                        # Find closed shapes in image
            
            if len(cnts) and len(cnts) < 3:                             # If more than 0 and less than 3 closed shapes exist

                c = max(cnts, key=cv2.contourArea)                      # return the largest target area
                x,y,w,h = cv2.boundingRect(c)                           # Get bounding rectangle (x,y,w,h) of the largest contour
                center = (int(x+0.5*w), int(y+0.5*h))                   # defines center of rectangle around the largest target area
                angle = round(((center[0]/width)-0.5)*fov, 3)           # angle of vector towards target center from camera, where 0 deg is centered

                wheel_measured = kin.getPdCurrent()                     # Wheel speed measurements

                # If robot is facing target
                if abs(angle) < angle_margin:                                 
                    e_width = target_width - w                          # Find error in target width and measured width

                    # If error width is within acceptable margin
                    if abs(e_width) < width_margin:
                        sc.driveOpenLoop(np.array([0.,0.]))             # Stop when centered and aligned
                        print("Aligned! ",w)
                        continue

                    fwd_effort = e_width/target_width                   
                    
                    wheel_speed = ik.getPdTargets(np.array([0.8*fwd_effort, -0.5*angle]))   # Find wheel speeds for approach and heading correction
                    sc.driveClosedLoop(wheel_speed, wheel_measured, 0)  # Drive closed loop
                    print("Angle: ", angle, " | Target L/R: ", *wheel_speed, " | Measured L\R: ", *wheel_measured)
                    continue

                wheel_speed = ik.getPdTargets(np.array([0, -1.1*angle]))    # Find wheel speeds for only turning

                sc.driveClosedLoop(wheel_speed, wheel_measured, 0)          # Drive robot
                print("Angle: ", angle, " | Target L/R: ", *wheel_speed, " | Measured L\R: ", *wheel_measured)

            else:
                print("No targets")
                sc.driveOpenLoop(np.array([0.,0.]))         # stop if no targets detected

                
    except KeyboardInterrupt: # condition added to catch a "Ctrl-C" event and exit cleanly
        pass

    finally:
    	print("Exiting Color Tracking.")



if __name__ == '__main__':
    main()
