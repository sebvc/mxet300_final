#  L3 script to log closest obstacle measurements for display.
import time
import L1_lidar as li
import L2_vector as v
import L1_log as log
import numpy as np 

fileName1 = "x-axis_log.txt"
fileName2 = "y-axis_log.txt"
fileName3 = "heading_log.txt"
fileName4 = "distance_log.txt"


if __name__ == "__main__":
    while(True):
        # get Data
        (r,alpha) = v.getNearest()
        (x, y) = v.polar2cart(r,alpha)
        # print
        log.uniqueFile(x,       fileName1)
        log.uniqueFile(y,       fileName2)
        log.uniqueFile(alpha,   fileName3)
        log.uniqueFile(r,       fileName4)
        print("files Updated")
        time.sleep(.2)
