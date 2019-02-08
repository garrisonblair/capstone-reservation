import RPi.GPIO as GPIO
import time

def light_led(pin, duration):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    GPIO.ouput(pin, True)
    time.sleep(duration)
    GPIO.output(pin, False)

    GPIO.cleanup()
