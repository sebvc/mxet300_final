
def grabBall():
    wheel_speeds = ik.getPdTargets( [0.0, 0.0])  # default parameters
    wheel_measured = kin.getPdCurrent()
    sc.driveClosedLoop(wheel_speeds,wheel_measured,0)
    time.sleep()
    servo.ChangeDutyCycle(1)