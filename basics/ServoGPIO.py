import RPi.GPIO as GPIO
import time

global servo

def setup(GPIOpin=24):
    #GPIO24 is pin18
    global servo

    servoPin = GPIOpin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPin,GPIO.OUT)
    servo = GPIO.PWM(servoPin,50)
    servo.start(10)

def close():#servo, dcyc=1):
    servo.ChangeDutyCycle(1) # close

def open():#servo, dcyc=10):
    servo.ChangeDutyCycle(10) # open
if __name__ == "__main__":
    setup()
    while(1):
        open()
        time.sleep(5)
        close()
        time.sleep(5)
def cleanup():
    global servo
    servo.stop()
    GPIO.cleanup()