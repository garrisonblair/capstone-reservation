import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

def light_led(pin, duration):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    GPIO.output(pin, True)
    time.sleep(duration)
    GPIO.output(pin, False)

    GPIO.cleanup()
