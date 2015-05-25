import RPi.GPIO as GPIO
import time



class SSRController:


  SSR_PIN = 14  # Pin for the 30A SSR used to drive high-power
  OUTLET_PIN_1 = 15  # Pin for the 10A SSR used to drive outlet
  OUTLET_PIN_2 = 18  # Pin for the 10A SSR used to drive second outlet


  def __init__(self):
    # set up GPIO using BCM numbering

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.SSR_PIN, GPIO.OUT)
    GPIO.setup(self.OUTLET_PIN_1, GPIO.OUT)
    GPIO.setup(self.OUTLET_PIN_2, GPIO.OUT)
    self.PumpOff()
    self.SSROff()

  def PumpOn(self):
    GPIO.output(self.OUTLET_PIN_1, GPIO.LOW)
    GPIO.output(self.OUTLET_PIN_2, GPIO.LOW)


  def SSROn(self):
    GPIO.output(self.SSR_PIN, GPIO.HIGH)


  def SSROff(self):

    GPIO.output(self.SSR_PIN, GPIO.LOW)

  def PumpOff(self):
    GPIO.output(self.OUTLET_PIN_1, GPIO.HIGH)



