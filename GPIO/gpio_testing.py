import RPi.GPIO as GPIO
import time

# set up GPIO using BCM numbering

GPIO.setmode(GPIO.BCM)

SSR_PIN = 14  # Pin for the 30A SSR used to drive high-power


GPIO.setup(SSR_PIN, GPIO.OUT)
GPIO.setup(OUTLET_PIN_1, GPIO.OUT)
GPIO.setup(OUTLET_PIN_2, GPIO.OUT)

ssr_on = False
GPIO.output(SSR_PIN, GPIO.LOW)

while True:
  time.sleep(1)
  if ssr_on:
    print("Off")
    ssr_on = False
    GPIO.output(SSR_PIN, GPIO.LOW)
  else:
    print("On")
    ssr_on = True
    GPIO.output(SSR_PIN, GPIO.HIGH)


GPIO.cleanup()
