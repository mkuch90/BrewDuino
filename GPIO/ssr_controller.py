import RPi.GPIO as GPIO
import time



class SSRController:


  SSR_PIN = 14  # Pin for the 30A SSR used to drive high-power


  def __init__(self):
    # set up GPIO using BCM numbering

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.SSR_PIN, GPIO.OUT)
    self.SSROff()

  def SSROn(self):
    GPIO.output(self.SSR_PIN, GPIO.HIGH)

  def SSROff(self):
    GPIO.output(self.SSR_PIN, GPIO.LOW)



