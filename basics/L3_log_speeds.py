#  L3 script to log velocity measurements for display.
import time
import L2_kinematics as ki
import L1_log as log




fileName1 = "xdot_log.txt"
fileName2 = "thetadot_log.txt"
fileName3 = "pdl_log.txt"
fileName4 = "pdr_log.txt"


if __name__ == "__main__":
    while(True):
        # get speeds
        (xDot, thetaDot) = ki.getMotion()
        (pdl, pdr) = ki.getPdCurrent()
        # print
        log.uniqueFile(xDot,       fileName1)
        log.uniqueFile(thetaDot,   fileName2)
        log.uniqueFile(pdl,        fileName3)
        log.uniqueFile(pdr,        fileName4)
        print("files Updated")
        time.sleep(.2)
