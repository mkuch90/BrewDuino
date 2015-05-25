
from datetime import datetime

def Log(message):
  print("{0} - {1}".format(datetime.now().time(), message))

class SSRController:

  def __init__(self):
    Log("Using Fake SSR")

  def PumpOn(self):
    Log("Pump On")


  def SSROn(self):
    Log("SSR On")


  def SSROff(self):
    Log("SSR Off")

  def PumpOff(self):
    Log("Pump off")



