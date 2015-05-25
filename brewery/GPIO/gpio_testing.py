import RPi.GPIO as GPIO
import time

#set up GPIO using BCM numbering

GPIO.setmode(GPIO.BCM)

SSR_PIN = 14 # Pin for the 30A SSR used to drive high-power
OUTLET_PIN_1 = 15 # Pin for the 10A SSR used to drive outlet
OUTLET_PIN_2 = 18 # Pin for the 10A SSR used to drive second outlet


GPIO.setup(SSR_PIN, GPIO.OUT)
GPIO.setup(OUTLET_PIN_1, GPIO.OUT)
GPIO.setup(OUTLET_PIN_2, GPIO.OUT)

ssr_on = False
GPIO.output(SSR_PIN, GPIO.LOW)
GPIO.output(OUTLET_PIN_1, GPIO.HIGH)
GPIO.output(OUTLET_PIN_2, GPIO.HIGH)

while True:
  time.sleep(1)
  if ssr_on:
    print("Off")
    ssr_on = False
    GPIO.output(SSR_PIN, GPIO.LOW)
    GPIO.output(OUTLET_PIN_1, GPIO.HIGH)
    GPIO.output(OUTLET_PIN_2, GPIO.HIGH)
  else:
    print("On")
    ssr_on = True
    GPIO.output(SSR_PIN, GPIO.HIGH)
    GPIO.output(OUTLET_PIN_1, GPIO.LOW)
    GPIO.output(OUTLET_PIN_2, GPIO.LOW)


GPIO.cleanup()
